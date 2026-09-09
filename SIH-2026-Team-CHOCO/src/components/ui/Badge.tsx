import React from 'react'
import { cn } from '@/lib/utils'

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'nominal' | 'warning' | 'critical' | 'info' | 'live' | 'neutral'
  pulse?: boolean
}

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = 'neutral', pulse = false, children, ...props }, ref) => {
    const variantStyles = {
      nominal: 'border-[#2b5945] text-[#a0d1b8] bg-[#2b5945]/20',
      warning: 'border-[#8c7847] text-[#fae0a6] bg-[#8c7847]/20',
      critical: 'border-[#994500] text-[#ff7066] bg-[#994500]/20',
      info: 'border-[#4e8af7] text-[#9bc0f7] bg-[#4e8af7]/20',
      live: 'border-white text-[#121417] bg-white font-bold',
      neutral: 'border-[#636363] text-[#c0c9c2] bg-[#121417]',
    }

    return (
      <span
        ref={ref}
        className={cn(
          'inline-flex items-center gap-1.5 px-2 py-0.5 rounded-badge text-xs font-mono tracking-wider uppercase border select-none',
          variantStyles[variant],
          className
        )}
        {...props}
      >
        {(variant === 'live' || pulse) && (
          <span className="w-1.5 h-1.5 rounded-full bg-current opacity-90 inline-block" />
        )}
        {children}
      </span>
    )
  }
)

Badge.displayName = 'Badge'
