import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@sih/ui-kit';
import { CheckCircle2, RotateCcw } from 'lucide-react';

export function Settings() {
  const [testState, setTestState] = useState<'idle' | 'testing' | 'success'>('idle');
  const [rollbackState, setRollbackState] = useState<{stm: boolean, gnn: boolean}>({ stm: false, gnn: false });

  const handleTestConnection = () => {
    setTestState('testing');
    setTimeout(() => {
      setTestState('success');
      setTimeout(() => setTestState('idle'), 3000);
    }, 1500);
  };

  const handleRollback = (model: 'stm' | 'gnn') => {
    setRollbackState(prev => ({ ...prev, [model]: true }));
    setTimeout(() => {
      setRollbackState(prev => ({ ...prev, [model]: false }));
    }, 2000);
  };

  return (
    <div className="space-y-6 max-w-[1000px] mx-auto">
      <h1 className="text-2xl font-bold text-ink tracking-tight">System Settings</h1>
      
      <Card className="shadow-sm border border-line">
        <CardHeader className="pb-3 border-b border-line bg-surface-2/95 backdrop-blur-md">
          <CardTitle>Model Deployments</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6 pt-6">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-medium text-ink">ATM Spatio-Temporal Prediction Model</h3>
              <p className="text-sm text-muted">Version: v2.4 (Production)</p>
            </div>
            <Button 
              variant="outline" 
              onClick={() => handleRollback('stm')}
              disabled={rollbackState.stm}
              className={rollbackState.stm ? 'bg-good-soft text-good border-good' : ''}
            >
              {rollbackState.stm ? <><CheckCircle2 className="w-4 h-4 mr-2" /> Rolled back to v2.3</> : 'Rollback'}
            </Button>
          </div>
          <div className="h-px bg-line"></div>
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-medium text-ink">Mule Graph Neural Network</h3>
              <p className="text-sm text-muted">Version: v1.8 (Production)</p>
            </div>
            <Button 
              variant="outline"
              onClick={() => handleRollback('gnn')}
              disabled={rollbackState.gnn}
              className={rollbackState.gnn ? 'bg-good-soft text-good border-good' : ''}
            >
              {rollbackState.gnn ? <><CheckCircle2 className="w-4 h-4 mr-2" /> Rolled back to v1.7</> : 'Rollback'}
            </Button>
          </div>
        </CardContent>
      </Card>
      
      <Card className="shadow-sm border border-line">
        <CardHeader className="pb-3 border-b border-line bg-surface-2/95 backdrop-blur-md">
          <CardTitle>Global Integrations</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 pt-6">
          <div className="flex justify-between items-center">
            <div>
              <h3 className="font-medium text-ink">Core Banking API (Mock)</h3>
              <p className="text-sm text-good">Status: Connected</p>
            </div>
            <Button 
              variant="outline"
              onClick={handleTestConnection}
              disabled={testState !== 'idle'}
              className={`min-w-[160px] transition-all ${testState === 'success' ? 'bg-good-soft text-good border-good' : ''}`}
            >
              {testState === 'idle' && 'Test Connection'}
              {testState === 'testing' && <><RotateCcw className="w-4 h-4 mr-2 animate-spin" /> Pinging...</>}
              {testState === 'success' && <><CheckCircle2 className="w-4 h-4 mr-2" /> Perfect Ping (12ms)</>}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
