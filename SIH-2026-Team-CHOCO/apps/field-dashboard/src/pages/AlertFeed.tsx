import { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button, Badge, useAppSelector } from '@sih/ui-kit';
import { MapPin, Navigation, UserCheck, Clock, AlertTriangle, CheckCircle } from 'lucide-react';

export function AlertFeed() {
  const activeAlerts = useAppSelector(state => state.alerts.activeAlerts);
  
  // Local state to simulate button interactions
  const [interceptedIds, setInterceptedIds] = useState<Set<string>>(new Set());
  const [navigatingId, setNavigatingId] = useState<string | null>(null);

  // Fallback to mock data if no live WebSocket alerts are present (for demo purposes)
  const displayAlerts = activeAlerts.length > 0 ? activeAlerts : [
    { alert_id: '1', atm_id: 'Indiranagar ATM #452', risk_score: 95, message: 'High probability of cash-out in progress.', timestamp: 'Just now', isRead: false },
    { alert_id: '2', atm_id: 'Koramangala ATM #112', risk_score: 88, message: 'Suspicious transaction velocity detected.', timestamp: '15 mins ago', isRead: false },
    { alert_id: '4', atm_id: 'Domlur ATM #22', risk_score: 92, message: 'Linked to recent cyber complaint.', timestamp: '5 mins ago', isRead: false },
    { alert_id: '3', atm_id: 'MG Road ATM #05', risk_score: 45, message: 'Routine flag.', timestamp: '1 hour ago', isRead: true },
  ];

  const handleNavigate = (id: string) => {
    setNavigatingId(id);
    setTimeout(() => {
      window.open('https://www.google.com/maps/search/ATM', '_blank');
      setNavigatingId(null);
    }, 800);
  };

  const handleIntercept = (id: string) => {
    setInterceptedIds(prev => new Set(prev).add(id));
  };

  return (
    <div className="max-w-[1600px] mx-auto space-y-8">
      {/* Page Header */}
      <div className="flex justify-between items-center mb-8 bg-surface/95 backdrop-blur-md p-6 rounded-lg border border-line shadow-sm">
        <div>
          <h1 className="text-3xl font-bold text-ink tracking-tight">Active Patrol Assignments</h1>
          <p className="text-muted font-medium mt-2">Sector: Indiranagar South • Unit 4</p>
        </div>
        <div className="flex flex-col items-end">
          <div className="flex items-center bg-surface-2 border border-line px-5 py-3 rounded-md">
            <span className="w-3 h-3 bg-good rounded-full animate-pulse mr-3 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></span>
            <span className="text-sm font-bold text-ink tracking-wide">GPS Tracking Active</span>
          </div>
          {activeAlerts.length > 0 && (
            <span className="text-xs text-accent font-bold mt-2 flex items-center">
              <AlertTriangle className="w-3 h-3 mr-1" /> Live WebSockets Connected
            </span>
          )}
        </div>
      </div>

      {/* Desktop Grid Layout */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        {displayAlerts.map(alert => {
          const isIntercepted = interceptedIds.has(alert.alert_id);
          const isNavigating = navigatingId === alert.alert_id;
          const isActive = !alert.isRead && alert.risk_score > 50 && !isIntercepted;
          
          return (
            <Card key={alert.alert_id} className={`overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1 ${isActive ? 'border-crit shadow-md bg-surface ring-1 ring-crit/20' : 'opacity-70 bg-surface-2 border-line'}`}>
              <div className={`h-1.5 w-full ${isActive ? 'bg-crit' : isIntercepted ? 'bg-good' : 'bg-line-2'}`}></div>
              
              <CardHeader className="pb-3 pt-5 px-6">
                <div className="flex justify-between items-start">
                  <CardTitle className="text-lg flex items-start space-x-2 text-ink leading-tight">
                    <MapPin className={`w-5 h-5 mt-0.5 shrink-0 ${isActive ? 'text-crit' : isIntercepted ? 'text-good' : 'text-muted'}`} />
                    <span>{alert.atm_id}</span>
                  </CardTitle>
                  <Badge variant={isIntercepted ? 'good' : alert.risk_score > 90 ? 'crit' : alert.risk_score > 80 ? 'warn' : 'default'} className="ml-2 shrink-0 shadow-sm font-bold">
                    {isIntercepted ? 'En Route' : `${alert.risk_score}% Risk`}
                  </Badge>
                </div>
              </CardHeader>
              
              <CardContent className="px-6 pb-6 space-y-6">
                <div className="text-sm text-body line-clamp-2 min-h-[40px]">
                  {alert.message}
                </div>
                
                <div className="flex justify-between items-center text-sm bg-surface-2 p-3 rounded-md border border-line">
                  <span className="font-mono text-ink font-bold">{alert.risk_score > 90 ? '1.2 km' : '3.4 km'} away</span>
                  <span className="flex items-center text-muted font-medium">
                    <Clock className="w-4 h-4 mr-1.5" />
                    {alert.timestamp}
                  </span>
                </div>
                
                {isActive ? (
                  <div className="grid grid-cols-2 gap-3 pt-2">
                    <Button 
                      variant="outline" 
                      className="w-full h-11 border-accent text-accent hover:bg-accent hover:text-white transition-all"
                      onClick={() => handleNavigate(alert.alert_id)}
                      disabled={isNavigating}
                    >
                      <Navigation className={`w-4 h-4 mr-2 ${isNavigating ? 'animate-pulse' : ''}`} /> 
                      {isNavigating ? 'Routing...' : 'Navigate'}
                    </Button>
                    <Button 
                      variant="destructive" 
                      className="w-full h-11 transition-all"
                      onClick={() => handleIntercept(alert.alert_id)}
                    >
                      <UserCheck className="w-4 h-4 mr-2" /> Intercept
                    </Button>
                  </div>
                ) : (
                  <div className="pt-2">
                    <Button variant="outline" className={`w-full h-11 ${isIntercepted ? 'text-good border-good bg-good-soft' : 'text-muted'}`} disabled>
                      {isIntercepted ? (
                        <><CheckCircle className="w-4 h-4 mr-2" /> Units Dispatched</>
                      ) : (
                        'Resolved'
                      )}
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
