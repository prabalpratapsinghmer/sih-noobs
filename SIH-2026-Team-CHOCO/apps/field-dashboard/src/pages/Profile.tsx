import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@sih/ui-kit';
import { ShieldAlert } from 'lucide-react';

export function Profile() {
  const [backupRequested, setBackupRequested] = useState(false);

  return (
    <div className="max-w-[1200px] mx-auto space-y-6">
      <h1 className="text-2xl font-bold text-ink tracking-tight">Officer Profile & Unit Settings</h1>
      
      <Card className="shadow-sm border border-line">
        <CardHeader className="pb-3 border-b border-line bg-surface-2/95 backdrop-blur-md">
          <CardTitle>Unit 4 - Indiranagar South</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 pt-6">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-muted uppercase font-bold tracking-wider">Officer ID</label>
              <div className="mt-1 font-medium text-ink">BGL-4491-C</div>
            </div>
            <div>
              <label className="text-xs text-muted uppercase font-bold tracking-wider">Assigned Vehicle</label>
              <div className="mt-1 font-medium text-ink">KA-01-G-9982 (Interceptor)</div>
            </div>
            <div>
              <label className="text-xs text-muted uppercase font-bold tracking-wider">Shift Schedule</label>
              <div className="mt-1 font-medium text-ink">Night Shift (20:00 - 08:00)</div>
            </div>
            <div>
              <label className="text-xs text-muted uppercase font-bold tracking-wider">GPS Tracking</label>
              <div className="mt-1 font-medium text-good">Active (High Precision)</div>
            </div>
          </div>
          
          <div className="h-px bg-line my-4"></div>
          
          <Button 
            variant="destructive" 
            className={`w-full h-12 text-base transition-all ${backupRequested ? 'bg-crit text-white animate-pulse' : ''}`}
            onClick={() => setBackupRequested(true)}
            disabled={backupRequested}
          >
            <ShieldAlert className="w-5 h-5 mr-2" />
            {backupRequested ? 'HQ Notified! Backup is en route.' : 'Request Backup / Emergency'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
