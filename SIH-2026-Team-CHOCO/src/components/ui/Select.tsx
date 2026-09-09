import React from 'react'
import { ChevronDown } from 'lucide-react'
import { cn } from '@/lib/utils'

export interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  options: SelectOption[]
  error?: string
  helperText?: string
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, options, error, helperText, id, ...props }, ref) => {
    const selectId = id || (label ? label.toLowerCase().replace(/\s+/g, '-') : undefined)

    return (
      <div className="w-full flex flex-col space-y-1.5">
        {label && (
          <label htmlFor={selectId} className="text-xs font-sans font-medium text-[#9b9b9b]">
            {label}
          </label>
        )}
        <div className="relative">
          <select
            id={selectId}
            ref={ref}
            className={cn(
              'w-full min-h-[42px] px-4 py-2.5 bg-[#1e2124] text-white rounded-input text-sm appearance-none',
              'border border-[#636363] hover:border-[#c0c9c2]',
              'focus:outline-none focus:border-[#2b5945] focus:ring-2 focus:ring-[#2b5945]/30',
              'transition-all duration-200 disabled:opacity-40 disabled:cursor-not-allowed pr-10',
              error && 'border-[#ff4136] focus:border-[#ff4136]',
              className
            )}
            {...props}
          >
            {options.map((opt) => (
              <option key={opt.value} value={opt.value} disabled={opt.disabled} className="bg-[#121417] text-white">
                {opt.label}
              </option>
            ))}
          </select>
          <ChevronDown className="w-4 h-4 text-[#9b9b9b] absolute right-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
        </div>
        {error && <span className="text-xs font-sans text-[#ff4136]">{error}</span>}
        {!error && helperText && <span className="text-xs font-sans text-[#9b9b9b]">{helperText}</span>}
      </div>
    )
  }
)

Select.displayName = 'Select'
