import * as React from 'react';
import { cn } from '@/lib/utils';
import { AlertTriangle, Info, CheckCircle2 } from 'lucide-react';

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'error' | 'warning' | 'info' | 'success';
  title?: string;
}

export function Alert({ className, variant = 'info', title, children, ...props }: AlertProps) {
  const styles = {
    error: 'border-burnt/60 bg-burnt/10 text-chalk',
    warning: 'border-burnt/40 bg-carbon-surface text-chalk',
    info: 'border-forest bg-carbon-surface text-sand',
    success: 'border-lime/40 bg-forest/30 text-chalk',
  };

  const icons = {
    error: <AlertTriangle className="h-5 w-5 text-burnt shrink-0 mt-0.5" />,
    warning: <AlertTriangle className="h-5 w-5 text-burnt shrink-0 mt-0.5" />,
    info: <Info className="h-5 w-5 text-sand shrink-0 mt-0.5" />,
    success: <CheckCircle2 className="h-5 w-5 text-lime shrink-0 mt-0.5" />,
  };

  return (
    <div
      role="alert"
      className={cn('flex gap-3 p-4 rounded-sm border', styles[variant], className)}
      {...props}
    >
      {icons[variant]}
      <div className="flex-1 text-sm leading-relaxed">
        {title && <h5 className="font-display font-semibold tracking-tight uppercase mb-1 text-chalk">{title}</h5>}
        <div>{children}</div>
      </div>
    </div>
  );
}
