'use client';

import * as React from 'react';
import { getApiBaseUrl } from '@/lib/api/client';

/**
 * ServerWarmup Component
 * Non-blocking background health check fired on initial application mount.
 * Proactively wakes up Render free-tier containers from inactivity spin-down
 * so that subsequent button clicks and navigation feel immediate.
 */
export function ServerWarmup() {
  React.useEffect(() => {
    try {
      const warmup = () => {
        const url = `${getApiBaseUrl()}/health`;
        fetch(url, {
          method: 'GET',
          cache: 'no-store',
          headers: { 'Accept': 'application/json' }
        }).catch(() => {
          // Silent catch: non-blocking background wake-up
        });
      };

      if (typeof window !== 'undefined') {
        if ('requestIdleCallback' in window) {
          (window as any).requestIdleCallback(warmup, { timeout: 1500 });
        } else {
          setTimeout(warmup, 300);
        }
      }
    } catch {
      // Ignore background warmup exceptions
    }
  }, []);

  return null;
}
