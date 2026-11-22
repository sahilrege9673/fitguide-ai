import { createClient } from '@/lib/supabase/client';

const rawBase = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
const API_BASE_URL = rawBase.endsWith('/api/v1') ? rawBase : `${rawBase.replace(/\/$/, '')}/api/v1`;

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
  const supabase = createClient();
  const { data: { session } } = await supabase.auth.getSession();

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };

  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`;
  }

  const url = `${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`;

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
