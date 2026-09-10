import React, { useState } from 'react'
import { PatrolCard, type PatrolAlertItem } from '@/components/field/PatrolCard'
import { Radio } from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { useDemoStore } from '@/store/demoStore'
import { useCaseStore } from '@/store/caseStore'
import { formatINR } from '@/lib/utils'

const initialAlerts: PatrolAlertItem[] = [
  {
    id: 'ALT-BLR-01',
    atmId: 'ATM-04 INDIRANAGAR',
    atmName: 'HDFC Bank 100ft Road Branch e-Lobby',
    coordinates: '12.9784° N, 77.6408° E',
    distanceKm: 0.8,
    etaMin: 4,
    riskScore: 0.942,
    amount: '₹2,50,000',
    status: 'PENDING',
  },
  {
    id: 'ALT-BLR-02',
    atmId: 'ATM-07 KORAMANGALA',
    atmName: 'Axis Bank 5th Block 80ft Road',
    coordinates: '12.9352° N, 77.6245° E',
    distanceKm: 2.4,
    etaMin: 9,
    riskScore: 0.887,
    amount: '₹1,50,000',
    status: 'PENDING',
  },
  {
    id: 'ALT-BLR-03',
    atmId: 'ATM-01 MG ROAD',
    atmName: 'State Bank of India Metro Station Concourse',
    coordinates: '12.9756° N, 77.6066° E',
    distanceKm: 4.1,
    etaMin: 14,
    riskScore: 0.814,
    amount: '₹1,00,000',
    status: 'PENDING',
  },
]

export const Field: React.FC = () => {
  const [alerts, setAlerts] = useState<PatrolAlertItem[]>(initialAlerts)
  const { patrolDispatched, caseResolved, dispatchedPatrols, isDemoRunning } = useDemoStore()
  const intelligence = useCaseStore((state) => state.intelligence)
  
  const dashboardAlerts = intelligence?.atms?.map((atm) => {
    const id = `${intelligence.complaint_id}-${atm.atm_id}`
    const isDispatched = dispatchedPatrols[id] || (isDemoRunning && patrolDispatched)
    return {
      id,
      atmId: atm.atm_id,
      atmName: atm.name,
      coordinates: `${atm.latitude.toFixed(4)}° N, ${atm.longitude.toFixed(4)}° E`,
      distanceKm: 0.8,
      etaMin: atm.eta_min,
      riskScore: atm.risk_score,
      amount: formatINR(atm.amount),
      status: (isDispatched ? 'DISPATCHED' : 'PENDING') as PatrolAlertItem['status'],
    }
  })

  const visibleAlerts = dashboardAlerts?.length
    ? dashboardAlerts.map((alert) => {
        const saved = alerts.find((s) => s.id === alert.id)
        if (saved) {
          if (alert.status === 'DISPATCHED' && saved.status === 'PENDING') {
            return alert
          }
          return saved
        }
        return alert
      })
    : alerts

  const handleStatusChange = (id: string, newStatus: PatrolAlertItem['status']) => {
    setAlerts((prev) => {
      const visible = dashboardAlerts?.find((alert) => alert.id === id)
      return prev.some((alert) => alert.id === id)
        ? prev.map((alert) => (alert.id === id ? { ...alert, status: newStatus } : alert))
        : visible
        ? [...prev, { ...visible, status: newStatus }]
        : prev
    })
  }

  return (
    <div className="min-h-screen bg-transparent text-white pt-20 pb-24 px-3 sm:px-4 select-none">
      <div className="w-full max-w-2xl mx-auto space-y-4">
        {/* Officer Tactical Identity Header */}
        <div className="p-4 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-btn bg-[#121417] border border-[#2b5945] flex items-center justify-center text-[#a0d1b8] font-mono font-bold text-xs">
              Δ4
            </div>
            <div>
              <div className="text-sm font-sans font-semibold text-white">
                Const. Raghavendra K.
              </div>
              <div className="text-xs font-mono text-[#9b9b9b]">
                BEAT PATROL UNIT DELTA-4 · INDIRANAGAR SECTOR
              </div>
            </div>
          </div>

          <Badge variant={caseResolved ? 'nominal' : patrolDispatched ? 'critical' : 'live'}>
            {caseResolved ? 'RESOLVED' : patrolDispatched ? 'DISPATCHED' : 'PATROLLING'}
          </Badge>
        </div>

        {/* GPS & Tactical Link Banner */}
        <div className="p-3.5 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card flex items-center justify-between font-mono text-xs text-[#c0c9c2]">
          <div className="flex items-center gap-2">
            <Radio className="w-3.5 h-3.5 text-[#a0d1b8]" />
            <span>POLICE RADIO: SECURE MESH 154.25 MHz</span>
          </div>
          <span className="text-[#a0d1b8] font-semibold">GPS LOCK · 12.9716, 77.5946</span>
        </div>

        {/* Priority Alert Section */}
        <div className="space-y-3">
          <div className="flex items-center justify-between px-1">
            <span className="font-mono text-xs font-semibold text-[#9b9b9b] tracking-wide">
              Incoming Priority Dispatch Alerts ({visibleAlerts.length})
            </span>
            <span className="font-mono text-xs text-[#fae0a6] font-medium">REAL-TIME GNN DISPATCH</span>
          </div>

          <div className="space-y-3">
            {visibleAlerts.map((alert) => (
              <PatrolCard key={alert.id} alert={alert} onStatusChange={handleStatusChange} />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
