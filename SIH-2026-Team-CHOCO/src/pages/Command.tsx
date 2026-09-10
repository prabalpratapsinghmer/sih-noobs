import React, { useEffect, useState } from 'react'
import { ThreatMap } from '@/components/command/ThreatMap'
import { MoneyTrailGraph } from '@/components/command/MoneyTrailGraph'
import { UniversalFreezeButton } from '@/components/command/UniversalFreezeButton'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { Terminal, Shield, FileText } from 'lucide-react'
import { useAppStore } from '@/store/appStore'
import { useDemoStore } from '@/store/demoStore'
import { useCaseStore } from '@/store/caseStore'
import { formatINR } from '@/lib/utils'

export const Command: React.FC = () => {
  const { setCopilotOpen } = useAppStore()
  const { caseId, amount, victimName, allNodesFrozen, currentStage } = useDemoStore()
  const intelligence = useCaseStore((state) => state.intelligence)
  const setIntelligence = useCaseStore((state) => state.setIntelligence)
  const activeCaseId = intelligence?.complaint_id || caseId
  const activeAmount = intelligence?.amount || amount
  const activeVictimName = intelligence?.victim_name || victimName || 'Rohan Sharma'

  const [complaints, setComplaints] = useState<any[]>([])

  useEffect(() => {
    fetch('/api/v1/police/complaints')
      .then(res => res.json())
      .then(data => {
        if (data?.items) {
          setComplaints(data.items)
        }
      })
      .catch(console.error)
  }, [])

  const handleSelectCase = async (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedId = e.target.value
    try {
      const res = await fetch(`/api/v1/victim/intelligence/${selectedId}`)
      const data = await res.json()
      if (data && data.complaint_id) {
        setIntelligence(data)
      }
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="min-h-screen bg-[#1e2124] text-white pt-20 pb-16 px-4 md:px-6">
      <div className="w-full max-w-[1740px] mx-auto space-y-4">
        {/* Top Telemetry Mission Strip - Palantir Dark Surface */}
        <div className="p-4 bg-[#000000] border border-[#636363] rounded-card flex items-center justify-between flex-wrap gap-4 select-none">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#ff4136]" />
              <span className="font-mono text-xs font-bold text-white tracking-wider">
                TACTICAL ROOM
              </span>
              <select
                value={activeCaseId}
                onChange={handleSelectCase}
                className="bg-[#1e2124] border border-[#636363] text-white text-xs font-mono px-2 py-1 ml-2 rounded"
              >
                <option value={activeCaseId}>{activeCaseId}</option>
                {complaints.filter(c => c.complaint_id !== activeCaseId).map(c => (
                  <option key={c.complaint_id} value={c.complaint_id}>
                    {c.complaint_id} ({c.fraud_type})
                  </option>
                ))}
              </select>
            </div>

            <Badge variant="critical">GNN THREAT ELEVATED</Badge>
            <span className="text-xs font-mono text-[#9b9b9b] hidden sm:inline">
              TOPOLOGY: 3-HOP SYNTHETIC MULE RING
            </span>
          </div>

          <div className="flex items-center gap-6 font-mono text-xs">
            <div>
              <span className="text-[#9b9b9b]">VICTIM: </span>
              <span className="text-[#a0d1b8] font-bold">{activeVictimName}</span>
            </div>
            <div>
              <span className="text-[#9b9b9b]">SIPHONED: </span>
              <span className="text-[#fae0a6] font-bold">{formatINR(activeAmount)}</span>
            </div>
            <div>
              <span className="text-[#9b9b9b]">PRESERVED: </span>
              <span className={allNodesFrozen || currentStage >= 4 ? 'text-[#a0d1b8] font-bold' : 'text-[#9b9b9b] font-bold'}>
                {allNodesFrozen || currentStage >= 4 ? formatINR(amount) : '₹0'}
              </span>
            </div>
            <div>
              <span className="text-[#9b9b9b]">TARGET VPA: </span>
              <span className="text-white font-semibold">{intelligence?.target_vpa || 'nexus.invest@ybl'}</span>
            </div>
          </div>
        </div>

        {/* Main Split Cockpit Grid: Left = Threat Map, Right = Money Trail Graph */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
          {/* Left: Tactical Threat Map */}
          <div className="h-[560px]">
            <ThreatMap />
          </div>

          {/* Right: GNN Money Trail Graph */}
          <div className="h-[560px]">
            <MoneyTrailGraph />
          </div>
        </div>

        {/* Bottom Mission Control Bar */}
        <div className="p-4 bg-[#000000] border border-[#636363] rounded-card flex items-center justify-between flex-wrap gap-4 select-none">
          <div className="flex items-center gap-3">
            <UniversalFreezeButton />

            <Button
              variant="secondary"
              size="md"
              onClick={() => setCopilotOpen(true)}
              className="font-mono text-xs"
            >
              <Terminal className="w-3.5 h-3.5 mr-1.5 text-[#a0d1b8]" />
              AI FORENSIC COPILOT
            </Button>
          </div>

          <div className="flex items-center gap-2 font-mono text-xs">
            <Button
              variant="ghost"
              size="sm"
              className="text-xs"
              onClick={() => alert('Section 91 CrPC notice auto-dispatched to Nodal Officer NPCI.')}
            >
              <FileText className="w-3.5 h-3.5 mr-1 text-[#fae0a6]" />
              AUTO-GENERATE CRPC NOTICE
            </Button>

            <Button
              variant="ghost"
              size="sm"
              className="text-xs"
              onClick={() => alert('FIR draft FIR-2026-BLR-0419 transmitted to State Cyber Police Registry.')}
            >
              <Shield className="w-3.5 h-3.5 mr-1 text-[#4e8af7]" />
              DISPATCH STATE FIR
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
