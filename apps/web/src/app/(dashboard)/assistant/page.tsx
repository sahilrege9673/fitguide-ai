'use client';

import * as React from 'react';
import Link from 'next/link';
import { createClient } from '@/lib/supabase/client';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { 
  MessageSquare, 
  Send, 
  Plus, 
  Sparkles, 
  ShieldAlert, 
  ShieldCheck, 
  Dumbbell, 
  Square, 
  ArrowRight,
  Clock,
  Flame,
  Info,
  CheckCircle2,
  RefreshCw,
  ExternalLink
} from 'lucide-react';

interface Conversation {
  id: string;
  user_id: string;
  title: string;
  created_at: string;
  updated_at: string;
  message_count: number;
}

interface ChatMessage {
  id: string;
  sender_role: 'user' | 'assistant' | 'system';
  content: string;
  isStreaming?: boolean;
  isSafetyStop?: boolean;
  created_at: string;
}

const QUICK_PROMPTS = [
  {
    label: "30-Min Upper Hypertrophy",
    prompt: "Suggest a focused 30-minute upper body hypertrophy workout based on my available equipment."
  },
  {
    label: "Knee-Friendly Squat Alternative",
    prompt: "What is an effective knee-friendly quad alternative to barbell back squats?"
  },
  {
    label: "Active Recovery Protocol",
    prompt: "How should I structure my active recovery routine on my upcoming rest day?"
  },
  {
    label: "Core & Hip Mobility",
    prompt: "Recommend a 15-minute athletic core and hip mobility routine to improve lifting stability."
  }
];

export default function AssistantPage() {
  const [conversations, setConversations] = React.useState<Conversation[]>([]);
  const [activeConvId, setActiveConvId] = React.useState<string | null>(null);
  const [messages, setMessages] = React.useState<ChatMessage[]>([]);
  const [inputPrompt, setInputPrompt] = React.useState('');
  const [isLoadingThreads, setIsLoadingThreads] = React.useState(true);
  const [isLoadingMessages, setIsLoadingMessages] = React.useState(false);
  const [isStreaming, setIsStreaming] = React.useState(false);
  const [errorMsg, setErrorMsg] = React.useState<string | null>(null);

  const messagesEndRef = React.useRef<HTMLDivElement>(null);
  const abortControllerRef = React.useRef<AbortController | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages, isStreaming]);

  // Load conversations on mount
  React.useEffect(() => {
    loadConversations();
  }, []);

  const getAuthToken = async () => {
    const supabase = createClient();
    const { data: { session } } = await supabase.auth.getSession();
    return session?.access_token || null;
  };

  const loadConversations = async () => {
    setIsLoadingThreads(true);
    setErrorMsg(null);
    try {
      const token = await getAuthToken();
      if (!token) return;

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/chat/conversations`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const data: Conversation[] = await res.json();
        setConversations(data);
        if (data.length > 0 && !activeConvId) {
          selectConversation(data[0].id);
        } else if (data.length === 0) {
          // Auto create a starting conversation
          createNewConversation();
        }
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to load conversation history.');
    } finally {
      setIsLoadingThreads(false);
    }
  };

  const createNewConversation = async () => {
    setErrorMsg(null);
    try {
      const token = await getAuthToken();
      if (!token) return;

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/chat/conversations`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ title: 'New Consultation' })
      });

      if (res.ok) {
        const newConv: Conversation = await res.json();
        setConversations(prev => [newConv, ...prev]);
        setActiveConvId(newConv.id);
        setMessages([]);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to initiate conversation.');
    }
  };

  const selectConversation = async (convId: string) => {
    setActiveConvId(convId);
    setIsLoadingMessages(true);
    setErrorMsg(null);
    try {
      const token = await getAuthToken();
      if (!token) return;

      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/chat/conversations/${convId}/messages`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const msgs: any[] = await res.json();
        setMessages(msgs.map(m => ({
          id: m.id,
          sender_role: m.sender_role,
          content: m.content,
          isSafetyStop: m.content.includes('SAFETY INTERVENTION'),
          created_at: m.created_at
        })));
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to retrieve messages.');
    } finally {
      setIsLoadingMessages(false);
    }
  };

  const handleSendMessage = async (textToSend?: string) => {
    const prompt = (textToSend || inputPrompt).trim();
    if (!prompt || isStreaming || !activeConvId) return;

    setInputPrompt('');
    setErrorMsg(null);

    // Append user message immediately
    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      sender_role: 'user',
      content: prompt,
      created_at: new Date().toISOString()
    };

    // Placeholder assistant message for streaming
    const assistantMessageId = `asst-${Date.now()}`;
    const assistantMessage: ChatMessage = {
      id: assistantMessageId,
      sender_role: 'assistant',
      content: '',
      isStreaming: true,
      created_at: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage, assistantMessage]);
    setIsStreaming(true);

    const abortController = new AbortController();
    abortControllerRef.current = abortController;

    try {
      const token = await getAuthToken();
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1'}/chat/conversations/${activeConvId}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token || ''}`
        },
        body: JSON.stringify({ content: prompt }),
        signal: abortController.signal
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => null);
        throw new Error(errData?.detail || `Server responded with ${res.status}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error('Readable stream not supported.');

      const decoder = new TextDecoder();
      let streamedContent = '';
      let isSafety = false;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data:')) {
            const dataStr = line.replace('data:', '').trim();
            if (!dataStr) continue;
            try {
              const parsed = JSON.parse(dataStr);
              if (parsed.status === 'safety_stop') {
                isSafety = true;
              }
              if (parsed.token) {
                streamedContent += parsed.token;
                setMessages(prev => prev.map(m => 
                  m.id === assistantMessageId 
                    ? { ...m, content: streamedContent, isSafetyStop: isSafety } 
                    : m
                ));
              }
            } catch {
              // Ignore partial JSON lines
            }
          }
        }
      }

      // Finalize message
      setMessages(prev => prev.map(m => 
        m.id === assistantMessageId 
          ? { ...m, isStreaming: false, isSafetyStop: isSafety } 
          : m
      ));

      // Refresh conversations list to update title and message count
      loadConversations();

    } catch (err: any) {
      if (err.name === 'AbortError') {
        setMessages(prev => prev.map(m => 
          m.id === assistantMessageId 
            ? { ...m, content: m.content + ' [Generation stopped]', isStreaming: false } 
            : m
        ));
      } else {
        setErrorMsg(err.message || 'Stream processing failed.');
        setMessages(prev => prev.filter(m => m.id !== assistantMessageId));
      }
    } finally {
      setIsStreaming(false);
      abortControllerRef.current = null;
    }
  };

  const handleStopGeneration = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const activeConv = conversations.find(c => c.id === activeConvId);

  // Simple Markdown renderer for headers, bold text, and lists
  const renderFormattedContent = (content: string) => {
    const lines = content.split('\n');
    return lines.map((line, idx) => {
      // Header 3
      if (line.startsWith('### ')) {
        return (
          <h4 key={idx} className="font-heading font-bold text-chalk text-base tracking-tight mt-3 mb-1">
            {line.replace('### ', '')}
          </h4>
        );
      }
      // Bullet items
      if (line.startsWith('- ') || line.startsWith('* ')) {
        const text = line.substring(2);
        return (
          <div key={idx} className="flex items-start gap-2 text-chalk/90 text-sm leading-relaxed my-0.5">
            <span className="text-lime mt-1.5 w-1.5 h-1.5 rounded-full bg-lime shrink-0" />
            <span>{formatInlineMarkdown(text)}</span>
          </div>
        );
      }
      // Numbered lists
      const numMatch = line.match(/^(\d+)\.\s+(.*)/);
      if (numMatch) {
        return (
          <div key={idx} className="flex items-start gap-2 text-chalk/90 text-sm leading-relaxed my-0.5">
            <span className="font-mono text-lime font-bold text-xs shrink-0 mt-0.5">{numMatch[1]}.</span>
            <span>{formatInlineMarkdown(numMatch[2])}</span>
          </div>
        );
      }
      // Empty line
      if (!line.trim()) {
        return <div key={idx} className="h-2" />;
      }
      // Standard prose
      return (
        <p key={idx} className="text-chalk/90 text-sm leading-relaxed my-1">
          {formatInlineMarkdown(line)}
        </p>
      );
    });
  };

  // Inline bold and code formatting
  const formatInlineMarkdown = (text: string) => {
    const parts = text.split(/(\*\*.*?\*\*|\*.*?\*|`.*?`)/g);
    return parts.map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i} className="font-semibold text-lime">{part.slice(2, -2)}</strong>;
      }
      if (part.startsWith('*') && part.endsWith('*')) {
        return <em key={i} className="italic text-sand">{part.slice(1, -1)}</em>;
      }
      if (part.startsWith('`') && part.endsWith('`')) {
        return <code key={i} className="px-1 py-0.5 font-mono text-xs bg-forest rounded text-lime">{part.slice(1, -1)}</code>;
      }
      return part;
    });
  };

  return (
    <div className="flex flex-col lg:flex-row h-[calc(100vh-4rem)] lg:h-screen bg-carbon overflow-hidden">
      
      {/* Sidebar: Conversation Threads */}
      <aside className="w-full lg:w-72 bg-carbon border-b lg:border-b-0 lg:border-r border-forest/60 flex flex-col shrink-0">
        <div className="p-4 border-b border-forest/60 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-lime" />
            <h2 className="font-heading font-bold text-chalk text-sm uppercase tracking-wider">
              Consultations
            </h2>
          </div>
          <Button 
            variant="outline" 
            size="sm" 
            onClick={createNewConversation}
            className="border-lime text-lime hover:bg-lime/10 h-8 px-2"
          >
            <Plus className="w-3.5 h-3.5 mr-1" />
            New
          </Button>
        </div>

        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {isLoadingThreads ? (
            <div className="space-y-2 p-2">
              <Skeleton className="h-10 w-full bg-forest/40" />
              <Skeleton className="h-10 w-full bg-forest/40" />
              <Skeleton className="h-10 w-full bg-forest/40" />
            </div>
          ) : conversations.length === 0 ? (
            <div className="p-4 text-center text-sand text-xs font-mono">
              No previous threads found.
            </div>
          ) : (
            conversations.map(conv => {
              const isActive = conv.id === activeConvId;
              return (
                <button
                  key={conv.id}
                  onClick={() => selectConversation(conv.id)}
                  className={`w-full text-left p-3 rounded transition-colors text-xs flex flex-col gap-1 ${
                    isActive 
                      ? 'bg-forest/80 border-l-2 border-lime text-chalk' 
                      : 'hover:bg-forest/40 text-sand hover:text-chalk'
                  }`}
                >
                  <span className="font-medium truncate text-chalk">
                    {conv.title}
                  </span>
                  <div className="flex items-center justify-between text-[10px] text-sand/80 font-mono">
                    <span>{new Date(conv.updated_at).toLocaleDateString()}</span>
                    <span>{conv.message_count} msgs</span>
                  </div>
                </button>
              );
            })
          )}
        </div>

        <div className="p-3 border-t border-forest/60 bg-forest/20 text-[11px] text-sand flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-lime shrink-0" />
          <span>Grounded in active profile &amp; weekly schedule</span>
        </div>
      </aside>

      {/* Main Chat Pane */}
      <main className="flex-1 flex flex-col min-w-0 bg-carbon">
        
        {/* Top Header & Safety Banner */}
        <header className="border-b border-forest/60 p-4 bg-carbon shrink-0">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <h1 className="font-heading font-bold text-chalk text-base tracking-tight truncate">
                {activeConv?.title || 'FeedGuide Athletic Assistant'}
              </h1>
              <Badge variant="outline" className="border-forest text-sand text-[10px]">
                Gemini 3.5 Flash
              </Badge>
            </div>
            <Link 
              href="/exercises" 
              className="text-xs font-mono text-lime hover:underline flex items-center gap-1"
            >
              <Dumbbell className="w-3.5 h-3.5" />
              Exercise Library
            </Link>
          </div>

          {/* Fitness Disclaimer */}
          <div className="bg-forest/30 border border-forest/80 rounded px-3 py-2 flex items-start gap-2 text-[11px] text-sand leading-relaxed">
            <Info className="w-4 h-4 text-lime shrink-0 mt-0.5" />
            <div>
              <strong className="text-chalk font-semibold">Athletic Guidance Disclaimer:</strong> FeedGuide AI provides evidence-based athletic and movement guidance, not medical diagnosis or clinical treatment. If experiencing chest pain, dizziness, or acute joint pain, stop physical activity immediately and consult emergency healthcare.
            </div>
          </div>
        </header>

        {/* Messages Feed */}
        <div className="flex-1 overflow-y-auto p-4 lg:p-6 space-y-4">
          {errorMsg && (
            <Alert variant="error">
              {errorMsg}
            </Alert>
          )}

          {isLoadingMessages ? (
            <div className="space-y-4 max-w-3xl mx-auto">
              <Skeleton className="h-16 w-3/4 bg-forest/40 rounded" />
              <Skeleton className="h-24 w-5/6 bg-forest/30 rounded" />
              <Skeleton className="h-16 w-2/3 bg-forest/40 rounded" />
            </div>
          ) : messages.length === 0 ? (
            <div className="max-w-2xl mx-auto py-8 text-center space-y-6">
              <div className="w-12 h-12 rounded-full bg-forest border border-lime/40 flex items-center justify-center mx-auto text-lime">
                <Dumbbell className="w-6 h-6" />
              </div>
              <div className="space-y-2">
                <h3 className="font-heading font-bold text-chalk text-xl tracking-tight">
                  FeedGuide AI Training Assistant
                </h3>
                <p className="text-sand text-sm max-w-md mx-auto">
                  Ask questions about movement mechanics, exercise substitutions, recovery pacing, or request structured session recommendations.
                </p>
              </div>

              {/* Quick Prompt Chips */}
              <div className="pt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 text-left">
                {QUICK_PROMPTS.map((qp, i) => (
                  <button
                    key={i}
                    onClick={() => handleSendMessage(qp.prompt)}
                    className="p-3 bg-forest/30 hover:bg-forest/60 border border-forest/80 hover:border-lime rounded text-xs text-chalk transition-colors group flex items-start justify-between"
                  >
                    <div>
                      <div className="font-semibold text-lime group-hover:underline mb-1">
                        {qp.label}
                      </div>
                      <div className="text-[11px] text-sand/90 line-clamp-2">
                        {qp.prompt}
                      </div>
                    </div>
                    <ArrowRight className="w-3.5 h-3.5 text-sand group-hover:text-lime shrink-0 ml-2 mt-1" />
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="max-w-3xl mx-auto space-y-4">
              {messages.map(msg => {
                const isUser = msg.sender_role === 'user';
                const isSafety = msg.isSafetyStop;

                return (
                  <div 
                    key={msg.id}
                    className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
                  >
                    <div className="flex items-center gap-2 mb-1 text-[11px] font-mono text-sand">
                      <span>{isUser ? 'You' : 'FeedGuide AI'}</span>
                      <span>•</span>
                      <span>{new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>

                    <div
                      className={`max-w-2xl p-4 rounded-md text-sm ${
                        isUser
                          ? 'bg-forest text-chalk border border-lime/30'
                          : isSafety
                          ? 'bg-orange/10 text-chalk border-2 border-orange'
                          : 'bg-forest/20 text-chalk border border-forest/80'
                      }`}
                    >
                      {isSafety && (
                        <div className="flex items-center gap-2 text-orange font-bold font-mono text-xs uppercase mb-2">
                          <ShieldAlert className="w-4 h-4" />
                          Safety Intervention Triggered
                        </div>
                      )}

                      <div>
                        {renderFormattedContent(msg.content)}
                        {msg.isStreaming && (
                          <span className="inline-block w-2 h-4 bg-lime ml-1 animate-pulse align-middle" />
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Bar */}
        <footer className="border-t border-forest/60 p-4 bg-carbon shrink-0">
          <div className="max-w-3xl mx-auto">
            <div className="relative flex items-end gap-2 bg-forest/20 border border-forest rounded-md p-2 focus-within:border-lime">
              <textarea
                value={inputPrompt}
                onChange={(e) => setInputPrompt(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about workout substitutions, recovery, or programming... (Enter to send)"
                rows={2}
                disabled={isStreaming}
                className="w-full bg-transparent text-chalk placeholder:text-sand/60 text-sm focus:outline-none resize-none font-sans px-2"
              />

              <div className="flex items-center gap-2 shrink-0 pb-1">
                {isStreaming ? (
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={handleStopGeneration}
                    className="border-orange text-orange hover:bg-orange/10 h-8 px-2"
                  >
                    <Square className="w-3.5 h-3.5 mr-1" />
                    Stop
                  </Button>
                ) : (
                  <Button
                    type="button"
                    variant="primary"
                    size="sm"
                    onClick={() => handleSendMessage()}
                    disabled={!inputPrompt.trim()}
                    className="h-8 px-3"
                  >
                    <Send className="w-3.5 h-3.5 mr-1" />
                    Send
                  </Button>
                )}
              </div>
            </div>

            <div className="mt-2 flex items-center justify-between text-[11px] text-sand/80 font-mono">
              <span>Shift + Enter for new line</span>
              <span>15 requests / min limit</span>
            </div>
          </div>
        </footer>

      </main>
    </div>
  );
}
