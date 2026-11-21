import * as React from 'react';
import { cn } from '@/lib/utils';

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'lime' | 'forest' | 'sand' | 'burnt' | 'outline';
}

export function Badge({ className, variant = 'forest', ...props }: BadgeProps) {
  const variants = {
    lime: 'bg-lime text-carbon font-semibold',
    forest: 'bg-forest text-chalk border border-carbon-border',
    sand: 'bg-forest-dark text-sand border border-sand/30',
    burnt: 'bg-burnt/20 text-burnt border border-burnt/40',
    outline: 'border border-forest text-chalk',
  };

  return (
    <div
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded-sm text-xs font-mono uppercase tracking-widest',
        variants[variant],
        className
      )}
      {...props}
    />
  );
}
