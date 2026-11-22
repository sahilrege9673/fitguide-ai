import os
import re
from uuid import uuid5, NAMESPACE_DNS
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from app.rag.embeddings import embedding_service

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "corpus")

class DocumentMetadata(BaseModel):
    document_id: str
    title: str
    source_name: str
    source_url: str
    license_type: str
    category: str
    target_age_groups: List[str] = Field(default_factory=list)

class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    filename: str
    source_name: str
    source_url: str
    category: str
    target_age_groups: List[str]
    chunk_index: int
    content: str
    token_count: int
    embedding: Optional[List[float]] = None

class TextChunker:
    """
    Token-aware recursive text chunker.
    Splits text targeting ~350-450 tokens (approx 1400-1800 chars)
    with 50-token (approx 200 chars) sliding overlap.
    """
    def __init__(self, target_tokens: int = 400, overlap_tokens: int = 50):
        self.target_chars = target_tokens * 4
        self.overlap_chars = overlap_tokens * 4

    def chunk_text(self, text: str) -> List[str]:
        # Clean text
        text = text.strip()
        if not text:
            return []

        # Split into semantic paragraphs
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        chunks: List[str] = []
        current_chunk = ""

        for p in paragraphs:
            if not current_chunk:
                current_chunk = p
            elif len(current_chunk) + len(p) + 2 <= self.target_chars:
                current_chunk += "\n\n" + p
            else:
                chunks.append(current_chunk)
                # Apply sliding overlap
                words = current_chunk.split()
                overlap_words = words[-self.overlap_chars // 5:] if len(words) > 10 else []
                overlap_text = " ".join(overlap_words)
                current_chunk = (overlap_text + "\n\n" + p).strip() if overlap_text else p

        if current_chunk:
            chunks.append(current_chunk)

        return chunks


class IngestionPipeline:
    """
    Orchestrates parsing of knowledge corpus, chunking, metadata extraction,
    and vector embedding generation.
    """
    @classmethod
    def parse_metadata_header(cls, file_content: str, filename: str) -> tuple[DocumentMetadata, str]:
        lines = file_content.splitlines()
        meta_dict: Dict[str, Any] = {
            "document_id": str(uuid5(NAMESPACE_DNS, f"fitguide.doc.{filename}")),
            "title": filename.replace(".md", "").replace("_", " ").title(),
            "source_name": "Health Guidelines",
            "source_url": "https://fitguide.ai/sources",
            "license_type": "Public Guidance",
            "category": "general_fitness",
            "target_age_groups": ["adult_18_64"]
        }

        body_lines = []
        in_header = True

        for line in lines:
            if in_header and line.startswith("# "):
                parts = line[2:].split(":", 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower().replace(" ", "_")
                    val = parts[1].strip()
                    if key == "title":
                        meta_dict["title"] = val
                    elif key == "source":
                        meta_dict["source_name"] = val
                    elif key == "url":
                        meta_dict["source_url"] = val
                    elif key == "license":
                        meta_dict["license_type"] = val
                    elif key == "category":
                        meta_dict["category"] = val
                    elif key in ["target_age_groups", "target_age_group"]:
                        meta_dict["target_age_groups"] = [g.strip() for g in val.split(",") if g.strip()]
                    continue
            in_header = False
            body_lines.append(line)

        meta = DocumentMetadata(**meta_dict)
        clean_body = "\n".join(body_lines).strip()
        return meta, clean_body

    @classmethod
    async def load_and_chunk_corpus(cls, corpus_path: str = CORPUS_DIR) -> List[DocumentChunk]:
        chunker = TextChunker()
        chunks: List[DocumentChunk] = []

        if not os.path.exists(corpus_path):
            return chunks

        filenames = sorted(os.listdir(corpus_path))
        for filename in filenames:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(corpus_path, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            meta, body = cls.parse_metadata_header(content, filename)
            text_chunks = chunker.chunk_text(body)

            for idx, text in enumerate(text_chunks):
                chunk_id = str(uuid5(NAMESPACE_DNS, f"fitguide.chunk.{filename}.{idx}"))
                token_count = max(1, len(text.split()) * 4 // 3)

                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=meta.document_id,
                    document_title=meta.title,
                    filename=filename,
                    source_name=meta.source_name,
                    source_url=meta.source_url,
                    category=meta.category,
                    target_age_groups=meta.target_age_groups,
                    chunk_index=idx,
                    content=text,
                    token_count=token_count
                )
                chunks.append(chunk)

        # Batch embed all chunks
        texts_to_embed = [c.content for c in chunks]
        embeddings = await embedding_service.embed_batch(texts_to_embed)
        for chunk, emb in zip(chunks, embeddings):
            chunk.embedding = emb

        return chunks
