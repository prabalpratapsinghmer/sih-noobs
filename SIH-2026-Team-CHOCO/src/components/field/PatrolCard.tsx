import React, { useState, useEffect } from 'react'
import { Navigation, MapPin, CheckCircle2, Radio, Shield, Clock } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { useDemoStore } from '@/store/demoStore'

export interface PatrolAlertItem {
  id: string
  atmId: string
  atmName: string
  coordinates: string
  distanceKm: number
  etaMin: number
  riskScore: number
  amount: string
  status: 'PENDING' | 'DISPATCHED' | 'ACKNOWLEDGED' | 'ON_SITE' | 'SECURED'
}

interface PatrolCardProps {
  alert: PatrolAlertItem
  onStatusChange?: (id: string, newStatus: PatrolAlertItem['status']) => void
}

export const PatrolCard: React.FC<PatrolCardProps> = ({ alert, onStatusChange }) => {
  const [status, setStatus] = useState<PatrolAlertItem['status']>(alert.status)
  const { resolveCase } = useDemoStore()

  useEffect(() => {
    setStatus(alert.status)
  }, [alert.status])

  const handleAdvance = () => {
    let next: PatrolAlertItem['status'] = 'ACKNOWLEDGED'
    if (status === 'PENDING' || status === 'DISPATCHED') next = 'ACKNOWLEDGED'
    else if (status === 'ACKNOWLEDGED') next = 'ON_SITE'
    else if (status === 'ON_SITE') {
      next = 'SECURED'
      resolveCase()
    }
    setStatus(next)
    onStatusChange?.(alert.id, next)
  }

  const isCritical = alert.riskScore > 0.9

  return (
    <Card
      density="compact"
      className={`border rounded-card transition-all text-white ${
        status === 'SECURED'
          ? 'border-[#2b5945] bg-black/30 backdrop-blur-md'
          : isCritical
          ? 'border-[#ff4136]/60 bg-black/30 backdrop-blur-md'
          : 'border-[#636363] bg-black/30 backdrop-blur-md'
      }`}
    >
      <div className="flex items-center justify-between pb-2.5 border-b border-[#636363]/40 mb-2.5">
        <div className="flex items-center gap-2">
          <span className="font-mono text-xs font-bold text-white">{alert.atmId}</span>
          <Badge variant={status === 'SECURED' ? 'nominal' : isCritical ? 'critical' : 'warning'} pulse={isCritical && status !== 'SECURED'}>
            {status}
          </Badge>
        </div>

        <div className="flex items-center gap-1.5 font-mono text-xs text-[#9b9b9b]">
          <Clock className="w-3 h-3 text-[#fae0a6]" />
          <span>ETA: {alert.etaMin} MIN</span>
        </div>
      </div>

      <div className="space-y-3">
        <div>
          <div className="text-sm font-sans font-semibold text-white flex items-center gap-1.5">
            <MapPin className="w-3.5 h-3.5 text-[#a0d1b8] shrink-0" />
            <span>{alert.atmName}</span>
          </div>
          <div className="text-xs font-mono text-[#9b9b9b] mt-0.5">{alert.coordinates}</div>
        </div>

        <div className="grid grid-cols-3 gap-2 py-2 px-1 border-t border-b border-[#636363]/40 font-mono text-xs">
          <div>
            <span className="text-xs text-[#9b9b9b] block font-medium">DISTANCE</span>
            <span className="font-bold text-white">{alert.distanceKm} KM</span>
          </div>
          <div>
            <span className="text-xs text-[#9b9b9b] block font-medium">PREDICTED RISK</span>
            <span className="font-bold text-[#ff7066]">{(alert.riskScore * 100).toFixed(1)}%</span>
          </div>
          <div>
            <span className="text-xs text-[#9b9b9b] block font-medium">VOLUME</span>
            <span className="font-bold text-[#fae0a6]">{alert.amount}</span>
          </div>
        </div>

        {/* Action button */}
        <div className="pt-1">
          {status === 'PENDING' && (
            <Button size="sm" variant="secondary" className="w-full text-xs font-mono font-semibold opacity-50 cursor-not-allowed pointer-events-none">
              <Radio className="w-3.5 h-3.5 mr-1.5" />
              AWAITING HQ DISPATCH
            </Button>
          )}

          {status === 'DISPATCHED' && (
            <Button size="sm" variant="palantir" className="w-full text-xs font-mono font-semibold" onClick={handleAdvance}>
              <Radio className="w-3.5 h-3.5 mr-1.5" />
              ACKNOWLEDGE DISPATCH
            </Button>
          )}

          {status === 'ACKNOWLEDGED' && (
            <Button size="sm" variant="primary" className="w-full text-xs font-mono font-semibold" onClick={handleAdvance}>
              <Navigation className="w-3.5 h-3.5 mr-1.5" />
              CONFIRM ARRIVAL AT ATM
            </Button>
          )}

          {status === 'ON_SITE' && (
            <button
              onClick={handleAdvance}
              className="w-full inline-flex items-center justify-center gap-2 py-2 px-4 rounded-btn text-xs font-mono bg-[#994500] text-white hover:bg-[#b85300] font-bold border border-[#994500] transition-colors"
            >
              <Shield className="w-3.5 h-3.5" />
              CONFIRM SUSPECT INTERCEPT & SECURE
            </button>
          )}

          {status === 'SECURED' && (
            <div className="p-2.5 rounded-btn bg-[#2b5945]/20 border border-[#2b5945] flex items-center justify-between text-xs font-mono text-[#a0d1b8] font-semibold">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-[#a0d1b8]" /> SUSPECT SECURED
              </span>
              <span>RECOVERY LOGGED</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  )
}
