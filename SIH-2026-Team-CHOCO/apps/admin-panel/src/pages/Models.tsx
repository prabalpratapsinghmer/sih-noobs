import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button, Badge } from '@sih/ui-kit';
import { BrainCircuit, Play, Square, RotateCcw } from 'lucide-react';

export function Models() {
  const [models, setModels] = useState(() => {
    const saved = localStorage.getItem('adminModels');
    if (saved) return JSON.parse(saved);
    return {
      stm: { isTraining: false, isSuspended: false, progress: 0 },
      gnn: { isTraining: false, isSuspended: false, progress: 0 }
    };
  });

  useEffect(() => {
    localStorage.setItem('adminModels', JSON.stringify(models));
  }, [models]);

  const handleRetrain = (modelKey: 'stm' | 'gnn') => {
    setModels((prev: any) => ({ ...prev, [modelKey]: { ...prev[modelKey], isTraining: true, progress: 0 } }));
    
    // Simulate training progress
    const interval = setInterval(() => {
      setModels((prev: any) => {
        const currentProgress = prev[modelKey].progress;
        if (currentProgress >= 100) {
          clearInterval(interval);
          return { ...prev, [modelKey]: { ...prev[modelKey], isTraining: false, progress: 0 } };
        }
        return { ...prev, [modelKey]: { ...prev[modelKey], progress: currentProgress + 10 } };
      });
    }, 400);
  };

  const handleSuspend = (modelKey: 'stm' | 'gnn') => {
    setModels((prev: any) => ({ ...prev, [modelKey]: { ...prev[modelKey], isSuspended: !prev[modelKey].isSuspended } }));
  };

  return (
    <div className="max-w-[1400px] mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-ink tracking-tight">Model Deployments</h1>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Model 1: STM */}
        <Card className={`shadow-sm border transition-all ${models.stm.isSuspended ? 'border-crit/50 bg-crit-soft/10' : 'border-line'}`}>
          <CardHeader className="pb-3 border-b border-line bg-surface-2/95 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center text-ink">
                <BrainCircuit className={`w-5 h-5 mr-2 ${models.stm.isSuspended ? 'text-crit' : 'text-accent'}`} />
                Spatio-Temporal Transformer
              </CardTitle>
              {models.stm.isSuspended ? (
                <Badge variant="crit">Suspended</Badge>
              ) : models.stm.isTraining ? (
                <Badge variant="warn" className="animate-pulse">Training... {models.stm.progress}%</Badge>
              ) : (
                <Badge variant="good" className="animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.4)]">Production</Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="pt-6 space-y-6">
            <div className="grid grid-cols-3 gap-4 border-b border-line pb-6">
              <div>
                <p className="text-xs text-muted font-bold uppercase tracking-wider mb-1">Version</p>
                <p className="text-ink font-medium">v2.4</p>
              </div>
              <div>
                <p className="text-xs text-muted font-bold uppercase tracking-wider mb-1">Latency</p>
                <p className="text-ink font-medium">{models.stm.isTraining ? '---' : '120ms'}</p>
              </div>
              <div>
                <p className="text-xs text-muted font-bold uppercase tracking-wider mb-1">Last Trained</p>
                <p className="text-ink font-medium">{models.stm.progress === 100 ? 'Just now' : '2 days ago'}</p>
              </div>
            </div>
            
            {models.stm.isTraining && (
              <div className="w-full bg-line-2 rounded-full h-1.5 mb-2">
                <div className="bg-warn h-1.5 rounded-full transition-all duration-300" style={{ width: `${models.stm.progress}%` }}></div>
              </div>
            )}
            
            <div className="flex space-x-3">
              <Button 
                className="bg-accent hover:bg-accent-2 text-white flex-1 transition-all"
                onClick={() => handleRetrain('stm')}
                disabled={models.stm.isTraining || models.stm.isSuspended}
              >
                <RotateCcw className={`w-4 h-4 mr-2 ${models.stm.isTraining ? 'animate-spin' : ''}`} /> 
                {models.stm.isTraining ? 'Training in progress...' : 'Retrain'}
              </Button>
              <Button 
                variant={models.stm.isSuspended ? "default" : "destructive"} 
                className="flex-1 transition-all"
                onClick={() => handleSuspend('stm')}
                disabled={models.stm.isTraining}
              >
                {models.stm.isSuspended ? <Play className="w-4 h-4 mr-2" /> : <Square className="w-4 h-4 mr-2" />}
                {models.stm.isSuspended ? 'Resume Model' : 'Suspend'}
              </Button>
            </div>
          </CardContent>
        </Card>
        
        {/* Model 2: GNN */}
        <Card className={`shadow-sm border transition-all ${models.gnn.isSuspended ? 'border-crit/50 bg-crit-soft/10' : 'border-line'}`}>
          <CardHeader className="pb-3 border-b border-line bg-surface-2/95 backdrop-blur-md">
            <div className="flex items-center justify-between">
              <CardTitle className="flex items-center text-ink">
                <BrainCircuit className={`w-5 h-5 mr-2 ${models.gnn.isSuspended ? 'text-crit' : 'text-accent'}`} />
                Graph Neural Network (Mule)
              </CardTitle>
              {models.gnn.isSuspended ? (
                <Badge variant="crit">Suspended</Badge>
              ) : models.gnn.isTraining ? (
                <Badge variant="warn" className="animate-pulse">Training... {models.gnn.progress}%</Badge>
              ) : (
                <Badge variant="good" className="animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.4)]">Production</Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="pt-6 space-y-6">
            <div className="grid grid-cols-3 gap-4 border-b border-line pb-6">
              <div>
                <p className="text-xs text-muted font-bold uppercase tracking-wider mb-1">Version</p>
                <p className="text-ink font-medium">v1.8</p>
              </div>
              <div>
                <p className="text-xs text-muted font-bold uppercase tracking-wider mb-1">Latency</p>
                <p className="text-ink font-medium">{models.gnn.isTraining ? '---' : '215ms'}</p>
              </div>
              <div>
                <p className="text-xs text-muted font-bold uppercase tracking-wider mb-1">Last Trained</p>
                <p className="text-ink font-medium">{models.gnn.progress === 100 ? 'Just now' : '5 days ago'}</p>
              </div>
            </div>
            
            {models.gnn.isTraining && (
              <div className="w-full bg-line-2 rounded-full h-1.5 mb-2">
                <div className="bg-warn h-1.5 rounded-full transition-all duration-300" style={{ width: `${models.gnn.progress}%` }}></div>
              </div>
            )}
            
            <div className="flex space-x-3">
              <Button 
                className="bg-accent hover:bg-accent-2 text-white flex-1 transition-all"
                onClick={() => handleRetrain('gnn')}
                disabled={models.gnn.isTraining || models.gnn.isSuspended}
              >
                <RotateCcw className={`w-4 h-4 mr-2 ${models.gnn.isTraining ? 'animate-spin' : ''}`} /> 
                {models.gnn.isTraining ? 'Training in progress...' : 'Retrain'}
              </Button>
              <Button 
                variant={models.gnn.isSuspended ? "default" : "destructive"} 
                className="flex-1 transition-all"
                onClick={() => handleSuspend('gnn')}
                disabled={models.gnn.isTraining}
              >
                {models.gnn.isSuspended ? <Play className="w-4 h-4 mr-2" /> : <Square className="w-4 h-4 mr-2" />}
                {models.gnn.isSuspended ? 'Resume Model' : 'Suspend'}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
