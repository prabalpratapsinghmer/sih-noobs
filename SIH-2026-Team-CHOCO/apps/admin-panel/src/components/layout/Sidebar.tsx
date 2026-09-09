import { Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Building2, BrainCircuit, Settings } from 'lucide-react';

const NAV_ITEMS = [
  { name: 'Dashboard', path: '/', icon: LayoutDashboard },
  { name: 'User Management', path: '/users', icon: Users },
  { name: 'Station Assignments', path: '/stations', icon: Building2 },
  { name: 'Model Deployments', path: '/models', icon: BrainCircuit },
  { name: 'Settings', path: '/settings', icon: Settings },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <aside className="w-64 h-screen border-r border-line bg-surface-2/95 backdrop-blur-md flex flex-col shrink-0">
      <div className="h-16 flex items-center px-6 border-b border-line">
        <h1 className="font-bold text-xl text-ink tracking-tight">
          Admin Panel
        </h1>
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
          <span>Admin Privilege</span>
          <span className="text-accent font-semibold flex items-center">
            Superuser
          </span>
        </div>
      </div>
    </aside>
  );
}
