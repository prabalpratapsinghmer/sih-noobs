import React from 'react'
import { cn } from '@/lib/utils'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
  isMono?: boolean
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = 'text', label, error, helperText, isMono = false, id, ...props }, ref) => {
    const inputId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)

    return (
      <div className="w-full flex flex-col space-y-1.5">
        {label && (
          <label htmlFor={inputId} className="text-xs font-sans font-medium text-[#9b9b9b]">
            {label}
          </label>
        )}
        <input
          id={inputId}
          type={type}
          ref={ref}
          className={cn(
            'w-full min-h-[42px] px-4 py-2.5 bg-black/40 backdrop-blur-sm text-white rounded-input text-sm',
            'border border-[#636363] hover:border-[#c0c9c2]',
            'focus:outline-none focus:border-[#2b5945] focus:ring-2 focus:ring-[#2b5945]/30',
            'placeholder:text-[#9b9b9b] transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed',
            isMono && 'font-mono tracking-tight',
            error && 'border-[#ff4136] focus:border-[#ff4136] focus:ring-[#ff4136]/30',
            className
          )}
          {...props}
        />
        {error && <span className="text-xs font-sans text-[#ff4136] tracking-tight">{error}</span>}
        {!error && helperText && <span className="text-xs font-sans text-[#9b9b9b]">{helperText}</span>}
      </div>
    )
  }
)

Input.displayName = 'Input'
