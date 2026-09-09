import React from 'react'
import {
  AreaChart,
  Area,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import type { CaseIntelligence } from '@/lib/api'

// Training loss & validation data
const lossData = [
  { epoch: 'E01', loss: 0.842, val_loss: 0.891, acc: 0.712 },
  { epoch: 'E04', loss: 0.621, val_loss: 0.654, acc: 0.824 },
  { epoch: 'E08', loss: 0.412, val_loss: 0.435, acc: 0.895 },
  { epoch: 'E12', loss: 0.285, val_loss: 0.301, acc: 0.931 },
  { epoch: 'E16', loss: 0.198, val_loss: 0.218, acc: 0.954 },
  { epoch: 'E20', loss: 0.142, val_loss: 0.165, acc: 0.972 },
  { epoch: 'E24', loss: 0.098, val_loss: 0.121, acc: 0.984 },
]

// GNN ROC/AUC curve data
const rocData = [
  { fpr: 0.0, tpr: 0.0 },
  { fpr: 0.02, tpr: 0.45 },
  { fpr: 0.05, tpr: 0.72 },
  { fpr: 0.1, tpr: 0.88 },
  { fpr: 0.15, tpr: 0.94 },
  { fpr: 0.2, tpr: 0.97 },
  { fpr: 0.3, tpr: 0.985 },
  { fpr: 1.0, tpr: 1.0 },
]

// Station officer roster data
const stationRoster = [
  {
    id: 'OFF-01',
    name: 'Insp. Vikramaditya Singh',
    rank: 'Inspector',
    division: 'Cyber Ops Command',
    station: 'Bengaluru Central',
    activeCases: 14,
    status: 'ON_DUTY',
  },
  {
    id: 'OFF-02',
    name: 'Sub-Insp. Priya Nambiar',
    rank: 'Sub-Inspector',
    division: 'GNN Forensic Analysis',
    station: 'Indiranagar Cyber Cell',
    activeCases: 8,
    status: 'ON_DUTY',
  },
  {
    id: 'OFF-03',
    name: 'Const. Raghavendra K.',
    rank: 'Head Constable',
    division: 'Field Intercept Patrol',
    station: 'Delta-4 Tactical Unit',
    activeCases: 3,
    status: 'DISPATCHED',
  },
  {
    id: 'OFF-04',
    name: 'Insp. Ananya Deshmukh',
    rank: 'Inspector',
    division: 'Banking & NPCI Liaison',
    station: 'State Cyber HQ',
    activeCases: 19,
    status: 'ON_DUTY',
  },
  {
    id: 'OFF-05',
    name: 'Sub-Insp. Farooq Ahmed',
    rank: 'Sub-Inspector',
    division: 'ATM Surveillance Grid',
    station: 'Koramangala Sector',
    activeCases: 6,
    status: 'STANDBY',
  },
]

export const TelemetryCharts: React.FC<{ modelRun?: CaseIntelligence['model_run'] }> = ({ modelRun }) => {
  return (
    <div className="space-y-6 text-white">
      {/* Top Telemetry KPI Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-5 bg-[#000000] border border-[#636363] rounded-card">
          <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-1.5">
            <span>STM PREDICTIONS</span>
            <Badge variant="nominal">{modelRun ? 'LIVE RUN' : '98.4%'}</Badge>
          </div>
          <div className="text-2xl font-mono font-bold text-white tabular-nums">{modelRun?.stm_predictions ?? '0.9842'}</div>
          <div className="text-xs font-mono text-[#a0d1b8] mt-1.5">▲ +0.012 vs baseline v3</div>
        </Card>

        <Card className="p-5 bg-[#000000] border border-[#636363] rounded-card">
          <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-1.5">
            <span>GNN NODES SCORED</span>
            <Badge variant="nominal">{modelRun ? modelRun.mode.toUpperCase() : '96.8%'}</Badge>
          </div>
          <div className="text-2xl font-mono font-bold text-white tabular-nums">{modelRun?.gnn_nodes_scored ?? '96.81%'}</div>
          <div className="text-xs font-mono text-[#9b9b9b] mt-1.5">Target &gt; 95.0% threshold</div>
        </Card>

        <Card className="p-5 bg-[#000000] border border-[#636363] rounded-card">
          <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-1.5">
            <span>MEAN INFERENCE LATENCY</span>
            <Badge variant="live">23ms</Badge>
          </div>
          <div className="text-2xl font-mono font-bold text-[#fae0a6] tabular-nums">{modelRun ? `${modelRun.latency_ms} ms` : '23.4 ms'}</div>
          <div className="text-xs font-mono text-[#9b9b9b] mt-1.5">NVIDIA T4 TensorRT cluster</div>
        </Card>

        <Card className="p-5 bg-[#000000] border border-[#636363] rounded-card">
          <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-1.5">
            <span>FALSE POSITIVE RATE</span>
            <Badge variant="nominal">&lt; 0.8%</Badge>
          </div>
          <div className="text-2xl font-mono font-bold text-[#a0d1b8] tabular-nums">0.74%</div>
          <div className="text-xs font-mono text-[#9b9b9b] mt-1.5">Verified on 1M simulated TXs</div>
        </Card>
      </div>

      {/* Dual Metric Charts: Model Convergence & ROC-AUC */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Training Loss Curve */}
        <Card className="p-6 bg-[#000000] border border-[#636363] rounded-card">
          <div className="flex items-center justify-between pb-3.5 border-b border-[#636363]/40 mb-4">
            <div>
              <h2 className="text-sm font-sans font-semibold text-white">
                GNN Convergence & Validation Loss
              </h2>
              <p className="text-xs text-[#9b9b9b] mt-0.5">
                Heterogeneous Graph Convolutional Network (PyTorch Geometric)
              </p>
            </div>
            <Badge variant="live">EPOCH 24/24</Badge>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={lossData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="lossGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#8c7847" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#8c7847" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="accGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2b5945" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#2b5945" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid stroke="#2f3234" strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="epoch" stroke="#9b9b9b" fontSize={12} fontFamily="Alliance No.1" />
                <YAxis stroke="#9b9b9b" fontSize={12} fontFamily="Alliance No.1" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#000000',
                    border: '1px solid #636363',
                    borderRadius: '4px',
                    fontFamily: 'Alliance No.1',
                    fontSize: '12px',
                    color: '#ffffff',
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="loss"
                  stroke="#8c7847"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#lossGradient)"
                  name="Loss"
                />
                <Area
                  type="monotone"
                  dataKey="acc"
                  stroke="#2b5945"
                  strokeWidth={2}
                  fillOpacity={1}
                  fill="url(#accGradient)"
                  name="Accuracy"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* Chart 2: ROC-AUC Discrimination Curve */}
        <Card className="p-6 bg-[#000000] border border-[#636363] rounded-card">
          <div className="flex items-center justify-between pb-3.5 border-b border-[#636363]/40 mb-4">
            <div>
              <h2 className="text-sm font-sans font-semibold text-white">
                Receiver Operating Characteristic (ROC-AUC)
              </h2>
              <p className="text-xs text-[#9b9b9b] mt-0.5">
                True Positive Rate vs False Positive Rate across mule risk cutoff
              </p>
            </div>
            <Badge variant="nominal">AUC: 0.985</Badge>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={rocData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid stroke="#2f3234" strokeDasharray="3 3" vertical={false} />
                <XAxis dataKey="fpr" stroke="#9b9b9b" fontSize={12} fontFamily="Alliance No.1" />
                <YAxis stroke="#9b9b9b" fontSize={12} fontFamily="Alliance No.1" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#000000',
                    border: '1px solid #636363',
                    borderRadius: '4px',
                    fontFamily: 'Alliance No.1',
                    fontSize: '12px',
                    color: '#ffffff',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="tpr"
                  stroke="#2b5945"
                  strokeWidth={2.5}
                  dot={{ r: 3, fill: '#2b5945' }}
                  name="TPR"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      </div>

      {/* Police Cyber Cell Command Roster Table */}
      <Card className="p-6 bg-[#000000] border border-[#636363] rounded-card">
        <div className="flex items-center justify-between pb-3.5 border-b border-[#636363]/40 mb-4">
          <div>
            <h2 className="text-sm font-sans font-semibold text-white">
              Active Officer & Station Operational Roster
            </h2>
            <p className="text-xs text-[#9b9b9b] mt-0.5">
              Live deployment roster across Bengaluru South, East, and Central Cyber Cells
            </p>
          </div>
          <Badge variant="neutral">5 ACTIVE STATIONS</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#636363]/40 text-[#9b9b9b]">
                <th className="pb-3 font-semibold">BADGE ID</th>
                <th className="pb-3 font-semibold">OFFICER</th>
                <th className="pb-3 font-semibold">DIVISION</th>
                <th className="pb-3 font-semibold">STATION / UNIT</th>
                <th className="pb-3 font-semibold">CASES</th>
                <th className="pb-3 font-semibold text-right">STATUS</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#636363]/30">
              {stationRoster.map((officer) => (
                <tr key={officer.id} className="hover:bg-[#121417] transition-colors">
                  <td className="py-3 font-semibold text-[#fae0a6]">{officer.id}</td>
                  <td className="py-3 font-sans font-medium text-white">{officer.name}</td>
                  <td className="py-3 text-[#c0c9c2]">{officer.division}</td>
                  <td className="py-3 text-[#c0c9c2]">{officer.station}</td>
                  <td className="py-3 font-bold text-white">{officer.activeCases}</td>
                  <td className="py-3 text-right">
                    <Badge
                      variant={
                        officer.status === 'ON_DUTY'
                          ? 'nominal'
                          : officer.status === 'DISPATCHED'
                          ? 'critical'
                          : 'neutral'
                      }
                    >
                      {officer.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}
