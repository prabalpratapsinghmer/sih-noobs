import React from 'react'
import { Link } from 'react-router-dom'
import { CheckCircle2, Clock, ArrowUpRight, Lock, Activity, ShieldCheck } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardDescription } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { formatINR, cn } from '@/lib/utils'
import { useDemoStore } from '@/store/demoStore'

interface CaseTrackerProps {
  caseId?: string
  initialData?: {
    name: string
    phone: string
    amount: number
    fraudType: string
    suspectUpi: string
  }
}

export const CaseTracker: React.FC<CaseTrackerProps> = ({
  caseId = 'CC-2026-F819',
  initialData = {
    name: 'Rohan Sharma',
    phone: '9876543210',
    amount: 500000,
    fraudType: 'INVESTMENT_SCAM',
    suspectUpi: 'nexus.invest@ybl',
  },
}) => {
  const { currentStage, allNodesFrozen, patrolDispatched, caseResolved } = useDemoStore()

  // Compute status step index (0: SUBMITTED, 1: AI_ANALYZING, 2: ACTION_TAKEN, 3: RESOLVED)
  let statusStep = 0
  if (currentStage >= 2) statusStep = 1
  if (currentStage >= 4) statusStep = 2
  if (currentStage >= 6 || caseResolved) statusStep = 3

  const stages = [
    { label: 'SUBMITTED', subtitle: 'Portal Lodged', icon: Clock },
    { label: 'AI ANALYZING', subtitle: 'GNN Mule Trace', icon: Activity },
    { label: 'ACTION TAKEN', subtitle: 'NPCI Accounts Frozen', icon: Lock },
    { label: 'RESOLVED', subtitle: 'Funds Secured', icon: CheckCircle2 },
  ]

  const auditEvents = [
    {
      time: '02:24:10 IST',
      stage: 'SUBMISSION',
      text: `Citizen complaint logged for ${formatINR(initialData.amount)} against VPA ${initialData.suspectUpi}.`,
      status: 'nominal',
    },
    ...(currentStage >= 2
      ? [
          {
            time: '02:24:13 IST',
            stage: 'GRAPH INTELLIGENCE',
            text: 'GNN 3-Hop Traversal identified 8 mule accounts across Axis, HDFC & Canara banks.',
            status: 'warning',
          },
        ]
      : []),
    ...(currentStage >= 3
      ? [
          {
            time: '02:24:16 IST',
            stage: 'STM FORECAST',
            text: 'Spatial-Temporal Model predicts 94.2% likelihood of cashout at ATM #04 Indiranagar in 6 min.',
            status: 'warning',
          },
        ]
      : []),
    ...(currentStage >= 4 || allNodesFrozen
      ? [
          {
            time: '02:24:19 IST',
            stage: 'FREEZE DIRECTIVE',
            text: 'Universal Freeze executed via NPCI API. 8/8 accounts locked. ₹5,00,000 contained.',
            status: 'critical',
          },
        ]
      : []),
    ...(currentStage >= 5 || patrolDispatched
      ? [
          {
            time: '02:24:22 IST',
            stage: 'FIELD INTERCEPT',
            text: 'Patrol Unit Delta-4 dispatched to Indiranagar ATM cluster. Geo-fence engaged.',
            status: 'warning',
          },
        ]
      : []),
    ...(currentStage >= 6 || caseResolved
      ? [
          {
            time: '02:24:25 IST',
            stage: 'CASE RESOLVED',
            text: 'Suspect detained. Section 91 CrPC notice served. 100% of siphoned balance recovered.',
            status: 'nominal',
          },
        ]
      : []),
  ]

  return (
    <div className="w-full max-w-5xl mx-auto space-y-6 text-white">
      {/* Top Banner Card */}
      <Card className="bg-[#000000] border border-[#636363] rounded-card p-6">
        <CardHeader>
          <div className="flex items-center justify-between flex-wrap gap-2 mb-3">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs text-[#9b9b9b] font-medium uppercase">
                National Cyber Crime Incident Registry
              </span>
              <Badge variant="live">LIVE INCIDENT TRACKING</Badge>
            </div>
            <span className="font-mono text-xs text-[#fae0a6] font-semibold">
              CASE REFERENCE: {caseId}
            </span>
          </div>

          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pt-2">
            <div>
              <CardTitle className="text-3xl font-mono text-white font-bold">{caseId}</CardTitle>
              <CardDescription className="font-mono text-xs text-[#c0c9c2] mt-1.5">
                Complainant: {initialData.name} · Siphoned: {formatINR(initialData.amount)} · Target VPA: {initialData.suspectUpi}
              </CardDescription>
            </div>

            <div className="flex items-center gap-2">
              <Link to="/command">
                <Button variant="secondary" size="sm" className="font-mono text-xs">
                  COMMAND HQ GRAPH
                  <ArrowUpRight className="w-3.5 h-3.5 ml-1" />
                </Button>
              </Link>
            </div>
          </div>

          {/* 4-Stage Horizontal Status Bar */}
          <div className="pt-6 pb-2">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {stages.map((stg, idx) => {
                const Icon = stg.icon
                const isPassed = idx < statusStep
                const isCurrent = idx === statusStep
                return (
                  <div
                    key={stg.label}
                    className={cn(
                      'pt-3 border-t-2 transition-all duration-200',
                      isCurrent
                        ? 'border-white text-white'
                        : isPassed
                        ? 'border-[#a0d1b8] text-white'
                        : 'border-[#636363]/40 text-[#9b9b9b]'
                    )}
                  >
                    <div className="flex items-center justify-between mb-1.5">
                      <Icon
                        className={cn(
                          'w-4 h-4',
                          isCurrent
                            ? 'text-white'
                            : isPassed
                            ? 'text-[#a0d1b8]'
                            : 'text-[#9b9b9b]'
                        )}
                      />
                      <span className={cn('font-mono text-xs font-bold', isCurrent ? 'text-white' : 'text-[#9b9b9b]')}>
                        0{idx + 1}
                      </span>
                    </div>
                    <div className="font-sans text-xs font-bold tracking-tight">{stg.label}</div>
                    <div className="text-xs font-sans mt-0.5 text-[#9b9b9b]">
                      {stg.subtitle}
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* Grid: Financial Recovery Status & Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-5 bg-[#000000] border border-[#636363] rounded-card">
          <span className="text-xs font-mono text-[#9b9b9b] uppercase tracking-wider block font-medium">
            RECOVERED / PRESERVED BALANCE
          </span>
          <div className="text-2xl font-mono font-bold text-[#a0d1b8] mt-1.5 tabular-nums">
            {allNodesFrozen || currentStage >= 4 ? formatINR(initialData.amount) : '₹0'}
          </div>
          <p className="text-xs font-sans text-[#c0c9c2] mt-1.5">
            {allNodesFrozen || currentStage >= 4
              ? '100% of siphoned balance secured via NPCI API'
              : 'Tracer active across banking settlement rails'}
          </p>
        </Card>

        <Card className="p-5 bg-[#000000] border border-[#636363] rounded-card">
          <span className="text-xs font-mono text-[#9b9b9b] uppercase tracking-wider block font-medium">
            SUSPECT MULE NODES
          </span>
          <div className="text-2xl font-mono font-bold text-white mt-1.5 tabular-nums">
            {currentStage >= 2 ? '8 IDENTIFIED' : 'PENDING GNN'}
          </div>
          <p className="text-xs font-sans text-[#c0c9c2] mt-1.5">
            {currentStage >= 2 ? '3-Hop mule accounts isolated across 3 banks' : 'Multi-hop expansion initialized'}
          </p>
        </Card>

        <Card className="p-5 bg-[#000000] border border-[#636363] rounded-card">
          <span className="text-xs font-mono text-[#9b9b9b] uppercase tracking-wider block font-medium">
            POLICE FIR STATUS
          </span>
          <div className="text-2xl font-mono font-bold text-[#fae0a6] mt-1.5">
            {caseResolved ? 'FIR REGISTERED' : 'PROVISIONAL'}
          </div>
          <p className="text-xs font-sans text-[#c0c9c2] mt-1.5">
            {caseResolved ? 'CR-0928/2026 lodged at Indiranagar PS' : 'Pre-FIR Forensic Intake'}
          </p>
        </Card>
      </div>

      {/* Incident Audit Trail */}
      <Card className="bg-[#000000] border border-[#636363] rounded-card p-6">
        <div className="flex items-center justify-between pb-3.5 border-b border-[#636363]/40 mb-2">
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-sans font-semibold text-white">
              Chronological Incident Audit Trail
            </h2>
            <span className="px-2 py-0.5 rounded-pill text-xs font-mono bg-[#121417] text-[#c0c9c2] border border-[#636363]">
              REAL-TIME
            </span>
          </div>
          <span className="text-xs font-mono text-[#9b9b9b]">
            CRYPTOGRAPHICALLY AUDITABLE
          </span>
        </div>

        <div className="divide-y divide-[#636363]/30">
          {auditEvents.map((evt, i) => (
            <div
              key={i}
              className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs"
            >
              <div className="flex items-center gap-3">
                <span className="font-mono text-xs font-semibold text-[#9b9b9b] shrink-0">
                  {evt.time}
                </span>
                <span className="font-sans font-semibold text-white">
                  {evt.stage}
                </span>
                <span className="text-[#c0c9c2] font-sans hidden md:inline">
                  — {evt.text}
                </span>
              </div>
              <Badge variant={evt.status as any}>{evt.status.toUpperCase()}</Badge>
            </div>
          ))}
        </div>

        <div className="mt-5 pt-3.5 border-t border-[#636363]/40 flex flex-col sm:flex-row items-center justify-between text-xs font-mono text-[#9b9b9b] gap-2">
          <span className="flex items-center gap-2 text-[#a0d1b8] font-medium">
            <ShieldCheck className="w-4 h-4" /> BLOCKCHAIN ANCHOR: 0x81b7...4e92 (BLOCK #18,924,103)
          </span>
          <span>CHOCO TAMPER-PROOF EVIDENCE LEDGER</span>
        </div>
      </Card>
    </div>
  )
}
