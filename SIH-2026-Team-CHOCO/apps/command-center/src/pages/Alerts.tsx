import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Badge, Button } from '@sih/ui-kit';
import { ShieldAlert, Filter, CheckCircle2, Lock } from 'lucide-react';

export function Alerts() {
  const [filtersActive, setFiltersActive] = useState(false);
  const [dispatchState, setDispatchState] = useState<'idle' | 'dispatching' | 'dispatched'>('idle');
  const [freezeState, setFreezeState] = useState<'idle' | 'freezing' | 'frozen'>('idle');

  const handleDispatch = () => {
    setDispatchState('dispatching');
    setTimeout(() => setDispatchState('dispatched'), 1200);
  };

  const handleFreeze = () => {
    setFreezeState('freezing');
    setTimeout(() => setFreezeState('frozen'), 1200);
  };

  return (
    <div className="space-y-6 max-w-[1600px] mx-auto">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-ink tracking-tight">Active Intel Alerts</h1>
        <Button 
          variant={filtersActive ? 'default' : 'outline'} 
          className={filtersActive ? 'bg-accent text-white' : ''}
          onClick={() => setFiltersActive(!filtersActive)}
        >
          <Filter className="w-4 h-4 mr-2" />
          {filtersActive ? 'Filters Active (High Risk Only)' : 'Filter Alerts'}
        </Button>
      </div>
      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle className="flex items-center">
            <ShieldAlert className="w-5 h-5 mr-2 text-crit" />
            High Priority Threats
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="rounded-md border border-line">
            <table className="w-full text-sm text-left">
              <thead className="text-xs text-muted uppercase bg-surface-2 border-b border-line">
                <tr>
                  <th className="px-6 py-4">Threat Level</th>
                  <th className="px-6 py-4">Target Entity</th>
                  <th className="px-6 py-4">Details</th>
                  <th className="px-6 py-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-line bg-surface">
                {/* Alert 1 */}
                <tr className="hover:bg-surface-2 transition-colors">
                  <td className="px-6 py-4"><Badge variant="crit">95% Risk</Badge></td>
                  <td className="px-6 py-4 font-medium text-ink">Indiranagar ATM #452</td>
                  <td className="px-6 py-4 text-muted">Synchronized rapid cash-out detected (4 cards)</td>
                  <td className="px-6 py-4 text-right">
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={handleDispatch}
                      disabled={dispatchState !== 'idle'}
                      className={`transition-all min-w-[130px] ${dispatchState === 'dispatched' ? 'bg-good-soft text-good border-good' : ''}`}
                    >
                      {dispatchState === 'idle' && 'Dispatch Unit'}
                      {dispatchState === 'dispatching' && 'Dispatching...'}
                      {dispatchState === 'dispatched' && <><CheckCircle2 className="w-4 h-4 mr-2" /> Dispatched</>}
                    </Button>
                  </td>
                </tr>
                {/* Alert 2 */}
                <tr className="hover:bg-surface-2 transition-colors">
                  <td className="px-6 py-4"><Badge variant="warn">82% Risk</Badge></td>
                  <td className="px-6 py-4 font-medium text-ink">Account: M. Kumar</td>
                  <td className="px-6 py-4 text-muted">Layer 2 Mule: High velocity passthrough</td>
                  <td className="px-6 py-4 text-right">
                    <Button 
                      variant={freezeState === 'frozen' ? 'destructive' : 'outline'} 
                      size="sm"
                      onClick={handleFreeze}
                      disabled={freezeState !== 'idle'}
                      className={`transition-all min-w-[130px] ${freezeState === 'frozen' ? 'bg-crit text-white' : ''}`}
                    >
                      {freezeState === 'idle' && 'Freeze Account'}
                      {freezeState === 'freezing' && 'Freezing...'}
                      {freezeState === 'frozen' && <><Lock className="w-4 h-4 mr-2" /> Frozen</>}
                    </Button>
                  </td>
                </tr>
                {/* Optional filtered alert */}
                {!filtersActive && (
                  <tr className="hover:bg-surface-2 transition-colors opacity-70">
                    <td className="px-6 py-4"><Badge variant="default">45% Risk</Badge></td>
                    <td className="px-6 py-4 font-medium text-ink">MG Road ATM #05</td>
                    <td className="px-6 py-4 text-muted">Routine flag (Pattern matched minor deviance)</td>
                    <td className="px-6 py-4 text-right">
                      <Button variant="outline" size="sm" disabled>Resolved</Button>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
