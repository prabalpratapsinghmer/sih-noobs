import { Outlet, Link, useLocation } from 'react-router-dom';
import { ShieldAlert, User } from 'lucide-react';
import { useWebSocket } from '@sih/ui-kit';

export function WebLayout() {
  const location = useLocation();
  const unreadAlerts = 2; // In a real app, this comes from Redux state
  
  // Initialize WebSocket connection for the app lifecycle
  useWebSocket();

  return (
    <div className="flex h-screen w-full bg-bg font-sans overflow-hidden">
      {/* Sidebar Navigation */}
      <aside className="w-64 h-full bg-surface border-r border-line flex flex-col shrink-0 z-10 shadow-sm">
        <div className="h-16 flex items-center px-6 border-b border-line">
          <h1 className="font-bold text-xl text-ink tracking-tight">
            Field Dashboard
          </h1>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <Link to="/alerts" className={`flex items-center px-4 py-3 rounded-md transition-colors ${location.pathname === '/alerts' ? 'bg-accent-soft text-accent' : 'text-muted hover:bg-surface-2 hover:text-ink'}`}>
            <ShieldAlert className="w-5 h-5 mr-3" />
            <span className="font-medium">Active Patrol</span>
            {unreadAlerts > 0 && (
              <span className="ml-auto bg-crit text-white text-[10px] font-bold px-2 py-0.5 rounded-full">{unreadAlerts}</span>
            )}
          </Link>
          <Link to="/profile" className={`flex items-center px-4 py-3 rounded-md transition-colors ${location.pathname === '/profile' ? 'bg-accent-soft text-accent' : 'text-muted hover:bg-surface-2 hover:text-ink'}`}>
            <User className="w-5 h-5 mr-3" />
            <span className="font-medium">Profile & Settings</span>
          </Link>
        </nav>
        <div className="p-4 border-t border-line bg-surface-2/50">
           <div className="flex items-center text-sm text-ink font-medium">
             <div className="w-8 h-8 rounded-full bg-accent-soft text-accent flex items-center justify-center mr-3">
               S
             </div>
             <div>
               <p className="leading-none">Constable Sharma</p>
               <p className="text-xs text-muted mt-1 leading-none">Indiranagar Unit</p>
             </div>
           </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 h-full overflow-y-auto bg-surface-2 p-8">
        <Outlet />
      </main>
    </div>
  );
}
