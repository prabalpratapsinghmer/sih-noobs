import { LayoutDashboard, Bot, ShieldAlert, Settings } from 'lucide-react';
import { Link, useLocation } from 'react-router-dom';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'AI Analyst', path: '/llm', icon: Bot },
  { name: 'Active Alerts', path: '/alerts', icon: ShieldAlert },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 h-screen border-r border-line bg-surface-2/95 backdrop-blur-md flex flex-col hidden md:flex shrink-0">
      <div className="h-14 flex items-center px-6 border-b border-line font-bold text-lg text-ink tracking-tight">
        Command Center
      </div>
      <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.path;
          const Icon = item.icon;
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-3 py-2 rounded-md transition-colors ${
                isActive 
                  ? 'bg-accent-soft text-accent font-medium' 
                  : 'text-muted hover:bg-surface hover:text-ink'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>
      <div className="p-4 border-t border-line">
        <div className="text-xs text-muted font-mono flex items-center justify-between">
          <span>System Status</span>
          <span className="text-good font-semibold flex items-center">
            <span className="w-2 h-2 rounded-full bg-good mr-1.5 animate-pulse"></span>
            Online
          </span>
        </div>
      </div>
    </aside>
  );
}
