import { Bell, Search, ShieldCheck } from 'lucide-react';

export function Topbar() {
  return (
    <header className="h-16 border-b border-line bg-surface/95 backdrop-blur-md flex items-center justify-between px-6 shrink-0 shadow-sm z-10">
      <div className="flex items-center text-muted bg-surface-2 px-3 py-2 rounded-md border border-line-2 text-sm w-80 cursor-text hover:border-accent/50 transition-colors">
        <Search className="w-4 h-4 mr-2" />
        <span>Global Search (⌘K)</span>
      </div>

      <div className="flex items-center space-x-4">
        <button className="relative p-2 text-muted hover:text-ink transition-colors">
          <Bell className="w-5 h-5" />
        </button>
        <div className="h-6 w-px bg-line mx-1"></div>
        <div className="flex items-center space-x-3 cursor-pointer p-1 pr-2 rounded-full hover:bg-surface-2 transition-colors">
          <div className="w-8 h-8 rounded-full bg-accent text-white flex items-center justify-center font-bold text-sm shadow-sm">
            <ShieldCheck className="w-4 h-4" />
          </div>
          <div className="hidden sm:block text-sm text-left">
            <p className="font-medium text-ink leading-none mb-0.5">System Admin</p>
            <p className="text-[11px] text-muted leading-none">Headquarters</p>
          </div>
        </div>
      </div>
    </header>
  );
}
