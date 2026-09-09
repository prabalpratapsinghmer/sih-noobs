import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@sih/ui-kit';
import { ShieldAlert, Database, HardDrive, RefreshCw } from 'lucide-react';

export function Settings() {
  const [cacheCleared, setCacheCleared] = useState(false);
  
  // Initialize from localStorage so it persists across navigations
  const [maintMode, setMaintMode] = useState(() => {
    return localStorage.getItem('maintMode') === 'true';
  });

  // Save to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('maintMode', maintMode.toString());
  }, [maintMode]);

  const handleClearCache = () => {
    setCacheCleared(true);
    setTimeout(() => setCacheCleared(false), 2000);
  };

  return (
    <div className="max-w-[1000px] mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold text-ink tracking-tight">System Settings</h1>
        <p className="text-muted mt-2">Global configuration for the CHOCO enforcement platform.</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {/* Database & Storage */}
        <Card className="shadow-sm border border-line">
          <CardHeader className="pb-3 border-b border-line bg-surface-2/95 backdrop-blur-md">
            <CardTitle className="flex items-center text-ink">
              <Database className="w-5 h-5 mr-2 text-accent" />
              Database & Storage
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6 space-y-4">
            <div className="flex justify-between items-center p-4 border border-line rounded-lg bg-surface">
              <div>
                <h3 className="font-semibold text-ink">Neo4j Graph Database</h3>
                <p className="text-sm text-muted">Currently using 4.2 GB of 10 GB limit.</p>
              </div>
              <Button variant="outline">Optimize Index</Button>
            </div>
            <div className="flex justify-between items-center p-4 border border-line rounded-lg bg-surface">
              <div>
                <h3 className="font-semibold text-ink">System Cache (Redis)</h3>
                <p className="text-sm text-muted">Temporary prediction results and session tokens.</p>
              </div>
              <Button 
                variant="outline" 
                onClick={handleClearCache}
                className={cacheCleared ? 'text-good border-good bg-good-soft' : ''}
              >
                <HardDrive className="w-4 h-4 mr-2" />
                {cacheCleared ? 'Cache Purged!' : 'Clear Cache'}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Security & Maintenance */}
        <Card className={`shadow-sm transition-all ${maintMode ? 'border-crit bg-crit-soft/10' : 'border-crit/20'}`}>
          <CardHeader className={`pb-3 border-b transition-all ${maintMode ? 'bg-crit-soft border-crit/30' : 'border-line bg-crit-soft/50'}`}>
            <CardTitle className="flex items-center text-crit">
              <ShieldAlert className="w-5 h-5 mr-2" />
              Security & Maintenance
            </CardTitle>
          </CardHeader>
          <CardContent className="pt-6 space-y-4">
            <div className="flex justify-between items-center p-4 border border-line rounded-lg bg-surface">
              <div>
                <h3 className="font-semibold text-ink">Maintenance Mode</h3>
                <p className="text-sm text-muted">Suspends all non-admin access to the Command Center.</p>
                {maintMode && <p className="text-xs text-crit font-bold mt-1">System is currently locked down.</p>}
              </div>
              <Button 
                variant={maintMode ? 'default' : 'destructive'}
                onClick={() => setMaintMode(!maintMode)}
              >
                <RefreshCw className={`w-4 h-4 mr-2 ${maintMode ? 'animate-spin' : ''}`} />
                {maintMode ? 'Disable Maintenance' : 'Enable Maintenance'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
