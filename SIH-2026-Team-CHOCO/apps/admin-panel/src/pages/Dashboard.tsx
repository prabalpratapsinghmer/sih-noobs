import { Card, CardContent } from '@sih/ui-kit';
import { Users, Building2, BrainCircuit, Activity } from 'lucide-react';

export function Dashboard() {
  const stats = [
    { label: 'Active Personnel', value: '1,248', icon: Users, trend: '+12 this week' },
    { label: 'Registered Stations', value: '84', icon: Building2, trend: 'Fully Online' },
    { label: 'ML Models Active', value: '2', icon: BrainCircuit, trend: 'v2.4 & v1.8' },
    { label: 'System Uptime', value: '99.99%', icon: Activity, trend: 'All systems operational' },
  ];

  return (
    <div className="max-w-[1400px] mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-ink tracking-tight">Admin Overview</h1>
        <p className="text-muted mt-2">Manage the CHOCO platform infrastructure and personnel.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <Card key={i} className="shadow-sm border border-line">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted mb-1">{stat.label}</p>
                    <h3 className="text-3xl font-bold text-ink tracking-tight">{stat.value}</h3>
                  </div>
                  <div className="w-12 h-12 rounded-full bg-accent-soft flex items-center justify-center text-accent">
                    <Icon className="w-6 h-6" />
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-line-2">
                  <p className="text-xs text-muted font-medium">{stat.trend}</p>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
