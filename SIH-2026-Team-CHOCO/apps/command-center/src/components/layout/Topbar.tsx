import { Bell, Search } from 'lucide-react';

export function Topbar() {
  // Mocking unread count (would normally come from Redux useAppSelector)
  const unreadAlerts = 3;

  return (
    <header className="h-14 border-b border-line bg-surface/95 backdrop-blur-md flex items-center justify-between px-6 shrink-0">
      {/* Left: Search / Command Palette hint */}
      <div className="flex items-center text-muted bg-surface-2 px-3 py-1.5 rounded-md border border-line-2 text-sm w-64 shadow-sm cursor-text hover:border-accent/50 transition-colors">
        <Search className="w-4 h-4 mr-2" />
        <span>Search (⌘K)</span>
      </div>

      {/* Right: Actions & Profile */}
      <div className="flex items-center space-x-4">
        <button className="relative p-2 text-muted hover:text-ink transition-colors">
          <Bell className="w-5 h-5" />
          {unreadAlerts > 0 && (
            <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 rounded-full bg-crit ring-2 ring-surface"></span>
          )}
        </button>
        <div className="h-5 w-px bg-line mx-1"></div>
        <div className="flex items-center space-x-3 cursor-pointer p-1 pr-2 rounded-full hover:bg-surface-2 transition-colors">
          <div className="w-8 h-8 rounded-full bg-accent-soft flex items-center justify-center text-accent font-bold text-sm">
            IS
          </div>
          <div className="hidden sm:block text-sm text-left">
            <p className="font-medium text-ink leading-none mb-0.5">Insp. Singh</p>
            <p className="text-[11px] text-muted leading-none">Indiranagar PS</p>
          </div>
        </div>
      </div>
    </header>
  );
}
