import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Home, FileText, Compass, ShieldAlert, BarChart3 } from 'lucide-react'
import { cn } from '@/lib/utils'

export const MobileBottomDock: React.FC = () => {
  const location = useLocation()

  const tabs = [
    { label: 'Gateway', path: '/', icon: Home },
    { label: 'Report', path: '/report', icon: FileText },
    { label: 'Command', path: '/command', icon: Compass },
    { label: 'Field', path: '/field', icon: ShieldAlert },
    { label: 'Telemetry', path: '/admin', icon: BarChart3 },
  ]

  return (
    <nav
      aria-label="Mobile Navigation Dock"
      className="fixed bottom-0 left-0 right-0 z-40 bg-[#000000]/95 backdrop-blur-md border-t border-[#636363]/40 lg:hidden select-none pb-[max(env(safe-area-inset-bottom,0px),8px)] pt-1"
    >
      <div className="grid grid-cols-5 h-12">
        {tabs.map((tab) => {
          const Icon = tab.icon
          const isActive = location.pathname === tab.path
          return (
            <Link
              key={tab.path}
              to={tab.path}
              className={cn(
                'flex flex-col items-center justify-center gap-1 transition-all duration-150 min-h-[44px] active:scale-95',
                isActive
                  ? 'text-white font-semibold'
                  : 'text-[#9b9b9b] hover:text-white'
              )}
            >
              <div className="relative">
                <Icon className={cn('w-4 h-4', isActive && 'text-[#38d39f]')} />
                {isActive && (
                  <span className="absolute -bottom-1.5 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-[#38d39f]" />
                )}
              </div>
              <span className="font-sans text-[10px] tracking-tight">{tab.label}</span>
            </Link>
          )
        })}
      </div>
    </nav>
  )
}
