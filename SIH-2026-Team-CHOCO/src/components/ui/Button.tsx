import React from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive' | 'accent' | 'palantir'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', isLoading = false, children, disabled, ...props }, ref) => {
    const baseStyles =
      'inline-flex items-center justify-center font-sans font-medium rounded-btn transition-colors duration-150 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#2b5945] active:translate-y-[1px] disabled:opacity-40 disabled:pointer-events-none select-none tracking-normal'

    const variantStyles = {
      // Palantir High-contrast Invert Button
      primary:
        'bg-white text-[#121417] hover:bg-black/30 backdrop-blur-md hover:text-white border border-white hover:border-white',
      // Palantir Deep Green Accent
      accent:
        'bg-[#2b5945] text-white hover:bg-[#356e56] border border-[#2b5945] hover:border-[#356e56]',
      palantir:
        'bg-[#2b5945] text-white hover:bg-[#356e56] border border-[#2b5945] hover:border-[#356e56]',
      // Palantir Invert Dark Card Button
      secondary:
        'bg-black/30 backdrop-blur-md text-white border border-[#636363] hover:bg-white hover:text-[#121417] hover:border-white',
      // Subtle Bordered Ghost
      ghost:
        'bg-transparent text-[#c0c9c2] hover:text-white hover:bg-[#2f3234] border border-transparent hover:border-[#636363]',
      // Danger Action
      destructive:
        'bg-transparent text-[#ff4136] border border-[#994500] hover:bg-[#994500] hover:text-white',
    }

    const sizeStyles = {
      sm: 'text-xs px-3 py-1.5 min-h-[32px] gap-1.5',
      md: 'text-sm px-4 py-2 min-h-[38px] gap-2',
      lg: 'text-base px-6 py-2.5 min-h-[44px] gap-2.5',
    }

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(baseStyles, variantStyles[variant], sizeStyles[size], className)}
        {...props}
      >
        {isLoading && (
          <svg
            className="animate-spin -ml-1 mr-2 h-3.5 w-3.5 text-current"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
