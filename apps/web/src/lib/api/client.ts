import { createClient } from '@/lib/supabase/client';

export function getApiBaseUrl(): string {
  // If explicitly configured in environment variables
  const configured = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL;
  if (configured && configured.trim()) {
    const trimmed = configured.trim().replace(/\/+$/, '');
    return trimmed.endsWith('/api/v1') ? trimmed : `${trimmed}/api/v1`;
  }

  // Browser-side fallback for production domains (e.g. Vercel)
  if (typeof window !== 'undefined') {
    const host = window.location.hostname;
    if (host !== 'localhost' && host !== '127.0.0.1') {
      return 'https://fitguide-ai.onrender.com/api/v1';
    }
  }

  // Server-side fallback for production builds
  if (process.env.NODE_ENV === 'production') {
    return 'https://fitguide-ai.onrender.com/api/v1';
  }

  // Local development fallback
  return 'http://localhost:8000/api/v1';
}

export const API_BASE_URL = getApiBaseUrl();

let _cachedToken: string | null = null;
let _tokenExpiry: number = 0;

export async function getAuthToken(): Promise<string | null> {
  const now = Date.now();
  if (_cachedToken && now < _tokenExpiry) {
    return _cachedToken;
  }
  try {
    const supabase = createClient();
    const { data: { session } } = await supabase.auth.getSession();
    if (session?.access_token) {
      _cachedToken = session.access_token;
      _tokenExpiry = now + 30000; // 30-second in-memory cache
      return _cachedToken;
    }
  } catch {
    // fallback
  }
  _cachedToken = null;
  return null;
}

export function invalidateAuthCache(): void {
  _cachedToken = null;
  _tokenExpiry = 0;
}

export class ApiError extends Error {
  code: string;
  details: Array<{ field?: string; issue: string }>;

  constructor(message: string, code: string = 'API_ERROR', details: Array<{ field?: string; issue: string }> = []) {
    super(message);
    this.name = 'ApiError';
    this.code = code;
    this.details = details;
  }
}

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAuthToken();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const baseUrl = getApiBaseUrl();
  const url = `${baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

  try {
    const res = await fetch(url, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const errorJson = await res.json().catch(() => null);
      if (errorJson && errorJson.error) {
        throw new ApiError(
          errorJson.error.message || 'An error occurred',
          errorJson.error.code || 'API_ERROR',
          errorJson.error.details || []
        );
      }
      throw new ApiError(
        errorJson?.detail || `Request failed with status ${res.status}`,
        res.status === 401 ? 'UNAUTHORIZED' : 'HTTP_ERROR'
      );
    }

    if (res.status === 204) {
      return {} as T;
    }

    return await res.json() as T;
  } catch (err: unknown) {
    if (err instanceof ApiError) {
      throw err;
    }
    const message = err instanceof Error ? err.message : 'Network request failed';
    throw new ApiError(message, 'NETWORK_ERROR');
  }
}
