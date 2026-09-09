import { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, Button, Badge } from '@sih/ui-kit';
import { LiveMap } from '../components/map/LiveMap';
import { MoneyTrailGraph } from '../components/graph/MoneyTrailGraph';
import { Download, AlertOctagon, CheckCircle2, ShieldAlert, X } from 'lucide-react';

export function Dashboard() {
  const [exportStatus, setExportStatus] = useState<'idle' | 'exporting' | 'done'>('idle');
  const [freezeStatus, setFreezeStatus] = useState<'idle' | 'confirming' | 'frozen'>('idle');
  
  const [complaints, setComplaints] = useState<any[]>([]);
  const [selectedComplaintId, setSelectedComplaintId] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/v1/police/complaints')
      .then(res => res.json())
      .then(data => {
        if (data && data.items) {
          setComplaints(data.items);
          if (data.items.length > 0) {
            setSelectedComplaintId(data.items[0].complaint_id);
          }
        }
      })
      .catch(err => console.error("Failed to load complaints:", err));
  }, []);

  const handleExport = () => {
    setExportStatus('exporting');
    setTimeout(() => {
      setExportStatus('done');
      setTimeout(() => setExportStatus('idle'), 3000);
    }, 1500);
  };

  const handleFreezeConfirm = () => {
    setFreezeStatus('frozen');
    setTimeout(() => setFreezeStatus('idle'), 4000); // Reset for demo purposes after 4s
  };

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-ink tracking-tight flex items-center space-x-4">
          <span>Command Center</span>
          {complaints.length > 0 && (
            <select 
              className="ml-4 p-2 text-sm border border-line bg-surface rounded-md focus:outline-none focus:ring-1 focus:ring-primary"
              value={selectedComplaintId || ''}
              onChange={(e) => setSelectedComplaintId(e.target.value)}
            >
              {complaints.map(c => (
                <option key={c.complaint_id} value={c.complaint_id}>
                  {c.complaint_id} - ₹{c.amount} ({c.fraud_type})
                </option>
              ))}
            </select>
          )}
        </h1>
        <div className="space-x-3 flex">
          <Button 
            variant="outline" 
            onClick={handleExport}
            disabled={exportStatus !== 'idle'}
            className={`transition-all ${exportStatus === 'done' ? 'bg-good-soft text-good border-good' : ''}`}
          >
            {exportStatus === 'idle' && <><Download className="w-4 h-4 mr-2" /> Export Report</>}
            {exportStatus === 'exporting' && <><Download className="w-4 h-4 mr-2 animate-bounce" /> Generating...</>}
            {exportStatus === 'done' && <><CheckCircle2 className="w-4 h-4 mr-2" /> Report Downloaded!</>}
          </Button>
          
          <Button 
            variant={freezeStatus === 'frozen' ? 'default' : 'destructive'}
            onClick={() => setFreezeStatus('confirming')}
            disabled={freezeStatus === 'frozen'}
            className={freezeStatus === 'frozen' ? 'bg-crit border-crit' : ''}
          >
            {freezeStatus === 'frozen' ? (
              <><ShieldAlert className="w-4 h-4 mr-2 animate-pulse text-white" /> Network Frozen</>
            ) : (
              <><AlertOctagon className="w-4 h-4 mr-2" /> Trigger Universal Freeze</>
            )}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map Mount Point */}
        <Card className="lg:col-span-2 h-[600px] flex flex-col shadow-sm">
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <CardTitle>Live Threat Heatmap</CardTitle>
              <Badge variant="crit">3 High Risk ATMs</Badge>
            </div>
          </CardHeader>
          <CardContent className="flex-1 p-0 m-6 mt-0 rounded-md border border-line overflow-hidden">
            <LiveMap />
          </CardContent>
        </Card>

        {/* Side Panel (Graph / Alerts) */}
        <Card className="h-[600px] flex flex-col shadow-sm">
          <CardHeader className="pb-4">
            <CardTitle>Money Trail Analysis</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 p-0 m-6 mt-0 rounded-md border border-line overflow-hidden">
            {selectedComplaintId ? (
              <MoneyTrailGraph complaintId={selectedComplaintId} />
            ) : (
              <div className="flex h-full items-center justify-center text-muted">No case selected</div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Freeze Confirmation Modal */}
      {freezeStatus === 'confirming' && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-in fade-in duration-200">
          <Card className="w-full max-w-md shadow-2xl border-crit">
            <CardHeader className="flex flex-row justify-between items-center border-b border-crit/20 bg-crit-soft/30">
              <CardTitle className="text-crit flex items-center">
                <AlertOctagon className="w-5 h-5 mr-2" /> CRITICAL ACTION
              </CardTitle>
              <button onClick={() => setFreezeStatus('idle')} className="text-muted hover:text-ink transition-colors">
                <X className="w-5 h-5" />
              </button>
            </CardHeader>
            <CardContent className="pt-6">
              <p className="text-ink font-medium mb-2">Are you absolutely sure you want to trigger a Universal Freeze?</p>
              <p className="text-sm text-muted mb-6">This will immediately block all flagged accounts and send freeze mandates to partner banks via the API. This action cannot be easily undone.</p>
              <div className="flex space-x-3">
                <Button variant="outline" className="flex-1" onClick={() => setFreezeStatus('idle')}>Cancel</Button>
                <Button variant="destructive" className="flex-1" onClick={handleFreezeConfirm}>Confirm Freeze</Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
