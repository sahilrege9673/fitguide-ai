import * as React from 'react';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', isLoading = false, disabled, children, ...props }, ref) => {
    const baseStyles = 'inline-flex items-center justify-center font-display font-semibold transition-colors duration-fast focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-lime disabled:pointer-events-none disabled:opacity-50 select-none uppercase tracking-wider';

    const variants = {
      primary: 'bg-lime text-carbon hover:bg-lime-hover active:bg-lime-muted shadow-sm',
      secondary: 'bg-forest text-chalk hover:bg-forest-light border border-carbon-border',
      outline: 'bg-transparent text-chalk border border-forest hover:bg-forest/50 hover:border-sand/40',
      ghost: 'bg-transparent text-sand hover:text-chalk hover:bg-forest/40',
      danger: 'bg-burnt text-chalk hover:bg-burnt/90 border border-burnt',
    };

    const sizes = {
      sm: 'h-8 px-3 text-xs rounded-sm',
      md: 'h-11 px-5 text-sm rounded-sm',
      lg: 'h-13 px-7 text-base rounded-md',
    };

    return (
      <button
        ref={ref}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin text-current" />}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
