import React from 'react'
import { Sun, Moon } from 'lucide-react'
import { useAppStore } from '@/store/appStore'
import { cn } from '@/lib/utils'

interface ThemeToggleProps {
  showLabel?: boolean
  className?: string
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ showLabel = false, className }) => {
  const { theme, toggleTheme } = useAppStore()
  const isLight = theme === 'light'

  return (
    <button
      onClick={toggleTheme}
      className={cn(
        'group relative flex items-center justify-center transition-all duration-200 active:scale-95',
        showLabel
          ? 'h-9 px-3 gap-2 rounded-btn bg-[#121417] dark:bg-[#121417] border border-[#636363]/60 hover:border-white dark:hover:border-white text-[#c0c9c2] hover:text-white'
          : 'w-9 h-9 rounded-btn bg-[#121417] dark:bg-[#121417] border border-[#636363] hover:border-white dark:hover:border-white text-[#c0c9c2] hover:text-white',
        className
      )}
      aria-label={`Switch to ${isLight ? 'Dark' : 'Light'} Mode`}
      title={`Switch to ${isLight ? 'Dark' : 'Light'} Mode`}
    >
      <div className="relative w-4 h-4 flex items-center justify-center">
        {isLight ? (
          <Sun className="w-4 h-4 text-amber-500 transition-transform duration-300 rotate-0 scale-100 group-hover:rotate-45" />
        ) : (
          <Moon className="w-4 h-4 text-[#a0d1b8] transition-transform duration-300 rotate-0 scale-100 group-hover:-rotate-12" />
        )}
      </div>

      {showLabel && (
        <span className="font-mono text-xs uppercase tracking-wider">
          {isLight ? 'Light Mode' : 'Dark Mode'}
        </span>
      )}
    </button>
  )
}
