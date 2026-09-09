import React from 'react'
import { cn } from '@/lib/utils'

export interface TabItem {
  id: string
  label: string
  badge?: string | number
  icon?: React.ComponentType<{ className?: string }>
}

export interface TabsProps {
  items: TabItem[]
  activeId: string
  onChange: (id: string) => void
  className?: string
  variant?: 'pills' | 'underline' | 'buttons'
}

export const Tabs: React.FC<TabsProps> = ({
  items,
  activeId,
  onChange,
  className,
  variant = 'pills',
}) => {
  return (
    <div
      role="tablist"
      className={cn(
        'flex items-center gap-2 overflow-x-auto no-scrollbar py-1 scroll-smooth',
        className
      )}
    >
      {items.map((tab) => {
        const isActive = activeId === tab.id
        const Icon = tab.icon

        if (variant === 'underline') {
          return (
            <button
              key={tab.id}
              role="tab"
              aria-selected={isActive}
              onClick={() => onChange(tab.id)}
              className={cn(
                'flex items-center gap-2 px-3 py-2 text-sm font-sans font-medium transition-all duration-200 border-b-2',
                isActive
                  ? 'border-[#2b5945] text-white'
                  : 'border-transparent text-[#9b9b9b] hover:text-white hover:border-[#636363]'
              )}
            >
              {Icon && <Icon className="w-4 h-4" />}
              <span>{tab.label}</span>
              {tab.badge !== undefined && (
                <span className="text-[10px] px-1.5 py-0.5 rounded-pill bg-[#2f3234] text-[#c0c9c2]">
                  {tab.badge}
                </span>
              )}
            </button>
          )
        }

        // Default: Palantir Category Pills (cardSelector pattern)
        return (
          <button
            key={tab.id}
            role="tab"
            aria-selected={isActive}
            onClick={() => onChange(tab.id)}
            className={cn(
              'flex items-center gap-2 px-4 py-2 text-xs md:text-sm font-sans font-medium rounded-btn border transition-all duration-200 whitespace-nowrap active:scale-[0.98]',
              isActive
                ? 'bg-white text-[#121417] border-white shadow-sm font-semibold'
                : 'bg-[#121417] text-[#c0c9c2] border-[#636363] hover:text-white hover:border-white hover:bg-[#2f3234]'
            )}
          >
            {Icon && <Icon className="w-3.5 h-3.5" />}
            <span>{tab.label}</span>
            {tab.badge !== undefined && (
              <span
                className={cn(
                  'text-[10px] px-1.5 py-0.5 rounded-pill',
                  isActive ? 'bg-[#121417] text-white' : 'bg-[#2f3234] text-[#9b9b9b]'
                )}
              >
                {tab.badge}
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
