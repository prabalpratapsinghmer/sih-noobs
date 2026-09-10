import React, { useMemo, useState, useEffect } from 'react'
import {
  ReactFlow,
  Background,
  Controls,
  Handle,
  Position,
  type Node,
  type Edge,
  type NodeProps,
} from '@xyflow/react'
import '@xyflow/react/dist/style.css'
import { User, Landmark, MapPin, Lock, Users, ShieldAlert, Zap, AlertCircle } from 'lucide-react'
import { formatINR, cn } from '@/lib/utils'
import { Badge } from '@/components/ui/Badge'
import { useDemoStore } from '@/store/demoStore'
import { useCaseStore } from '@/store/caseStore'

// Custom Victim Node
const VictimNode: React.FC<NodeProps> = ({ data }) => {
  const isSelected = data.isSelected as boolean
  return (
    <div
      className={cn(
        'w-[195px] bg-black/30 backdrop-blur-md border rounded-card shadow-xl transition-all duration-300',
        isSelected ? 'border-[#a0d1b8] ring-2 ring-[#a0d1b8]/40' : 'border-[#636363] hover:border-[#fae0a6]'
      )}
    >
      <Handle type="source" position={Position.Right} className="!bg-[#a0d1b8] !w-2.5 !h-2.5 !border-none" />
      <div className="p-2.5 border-b border-[#636363]/50 flex items-center justify-between bg-[#121417]">
        <div className="flex items-center gap-1.5">
          <div className="p-1 bg-[#1a1c1e] border border-[#2b5945] rounded-sm">
            <User className="w-3 h-3 text-[#a0d1b8]" />
          </div>
          <span className="text-[10px] font-mono text-[#a0d1b8] font-bold tracking-wider">
            VICTIM {(data.index as number) || 1}
          </span>
        </div>
        <span className="text-[9px] font-mono text-[#9b9b9b] px-1.5 py-0.5 rounded bg-black/40 backdrop-blur-sm">
          {data.caseId as string}
        </span>
      </div>
      <div className="p-2.5">
        <div className="text-xs font-sans font-semibold text-white leading-tight">
          {data.name as string}
        </div>
        <div className="text-[11px] font-mono text-[#9b9b9b] pt-0.5 flex items-center justify-between">
          <span>{data.account as string}</span>
          <span className="text-[9px] text-[#fae0a6]">{data.timeAgo as string}</span>
        </div>
        <div className="mt-2 bg-black/40 backdrop-blur-sm rounded-sm p-1.5 flex items-center justify-between border border-[#636363]/30">
          <span className="text-[9px] font-mono text-[#9b9b9b]">DEFRAUDED</span>
          <span className="text-xs font-bold font-mono text-[#ff4136]">
            {formatINR(data.amount as number)}
          </span>
        </div>
      </div>
    </div>
  )
}

// Custom Mule Node
const MuleNode: React.FC<NodeProps> = ({ data }) => {
  const isFrozen = data.frozen as boolean
  const risk = data.risk as number

  return (
    <div
      className={cn(
        'w-[205px] bg-black/30 backdrop-blur-md border rounded-card shadow-xl transition-colors duration-500',
        isFrozen ? 'border-[#a0d1b8] shadow-[0_0_15px_rgba(43,89,69,0.2)]' : 'border-[#636363]'
      )}
    >
      <Handle type="target" position={Position.Left} className="!bg-[#636363] !w-2.5 !h-2.5 !border-none" />
      <Handle type="source" position={Position.Right} className="!bg-[#636363] !w-2.5 !h-2.5 !border-none" />

      <div
        className={cn(
          'p-2.5 border-b flex items-center justify-between',
          isFrozen ? 'border-[#a0d1b8]/30 bg-[#a0d1b8]/10' : 'border-[#636363]/50 bg-[#121417]'
        )}
      >
        <div className="flex items-center gap-1.5">
          <div className="p-1 bg-[#1a1c1e] rounded-sm relative">
            <Landmark className={cn('w-3 h-3', isFrozen ? 'text-[#a0d1b8]' : 'text-[#c0c9c2]')} />
            {isFrozen && <Lock className="w-2.5 h-2.5 text-[#a0d1b8] absolute -bottom-1 -right-1" />}
          </div>
          <span className="text-[10px] font-mono text-[#9b9b9b] font-bold tracking-wider">
            LAYER {data.tier as number} MULE
          </span>
        </div>
        {!isFrozen ? (
          <span className={cn('text-[10px] font-mono font-bold', risk > 0.9 ? 'text-[#ff4136]' : 'text-[#ff7066]')}>
            {(risk * 100).toFixed(1)}% RISK
          </span>
        ) : (
          <span className="text-[10px] font-mono font-bold text-[#a0d1b8]">FROZEN</span>
        )}
      </div>
      <div className="p-2.5">
        <div className="text-xs font-sans font-semibold text-white leading-tight">
          {data.bank as string}
        </div>
        <div className="text-[11px] font-mono text-[#9b9b9b] pt-0.5">
          {data.account as string}
        </div>
        <div className="mt-2 bg-black/40 backdrop-blur-sm rounded-sm p-1.5 flex items-center justify-between border border-[#636363]/30">
          <span className="text-[9px] font-mono text-[#9b9b9b]">THROUGHPUT</span>
          <span className="text-xs font-bold font-mono text-[#fae0a6]">
            {formatINR(data.amount as number)}
          </span>
        </div>
      </div>
    </div>
  )
}

// Custom ATM Target Node
const AtmNode: React.FC<NodeProps> = ({ data }) => {
  return (
    <div className="w-[190px] bg-black/30 backdrop-blur-md border border-[#ff4136] rounded-card shadow-[0_0_15px_rgba(255,65,54,0.2)]">
      <Handle type="target" position={Position.Left} className="!bg-[#ff4136] !w-2.5 !h-2.5 !border-none" />
      <div className="p-2.5 border-b border-[#ff4136]/30 bg-[#ff4136]/10 flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <div className="p-1 bg-[#ff4136]/20 rounded-sm">
            <MapPin className="w-3 h-3 text-[#ff4136]" />
          </div>
          <span className="text-[10px] font-mono text-[#ff4136] font-bold tracking-wider">CASHOUT</span>
        </div>
        <Badge variant="critical" className="scale-75 origin-right">LIVE</Badge>
      </div>
      <div className="p-2.5">
        <div className="text-xs font-sans font-semibold text-white leading-tight">
          {data.name as string}
        </div>
        <div className="flex items-center justify-between text-[11px] font-mono pt-1">
          <span className="text-[#9b9b9b]">DISPATCH ETA</span>
          <span className="text-[#ff7066] font-bold">{data.eta as string}</span>
        </div>
        <div className="text-[11px] font-mono text-[#fae0a6] pt-0.5 font-medium">
          {data.patrol as string}
        </div>
      </div>
    </div>
  )
}

const nodeTypes = {
  victim: VictimNode,
  mule: MuleNode,
  atm: AtmNode,
}

const DEFAULT_VICTIMS_POOL = [
  {
    id: 'v1',
    caseId: 'CC-2026-F819',
    name: 'Rohan Sharma',
    account: 'HDFC •••• 4912',
    amount: 500000,
    timeAgo: '4m ago',
    fraudType: 'Fake IPO Allotment Scam',
  },
  {
    id: 'v2',
    caseId: 'CC-2026-F820',
    name: 'Priya Patel',
    account: 'ICICI •••• 8192',
    amount: 350000,
    timeAgo: '11m ago',
    fraudType: 'Telegram Task Scam',
  },
  {
    id: 'v3',
    caseId: 'CC-2026-F821',
    name: 'Vikram Malhotra',
    account: 'SBI •••• 3341',
    amount: 240000,
    timeAgo: '18m ago',
    fraudType: 'Digital Arrest Threat',
  },
  {
    id: 'v4',
    caseId: 'CC-2026-F822',
    name: 'Ananya Rao',
    account: 'AXIS •••• 7729',
    amount: 420000,
    timeAgo: '26m ago',
    fraudType: 'FedEx Customs Fraud',
  },
  {
    id: 'v5',
    caseId: 'CC-2026-F823',
    name: 'Rajesh Verma',
    account: 'KOTAK •••• 6501',
    amount: 190000,
    timeAgo: '35m ago',
    fraudType: 'Electricity Bill APK Scam',
  },
]

export const MoneyTrailGraph: React.FC = () => {
  const { allNodesFrozen, currentStage, victimName: demoVictimName, amount: demoAmount, caseId: demoCaseId } = useDemoStore()
  const intelligence = useCaseStore((state) => state.intelligence)
  const liveMules = intelligence?.mule_nodes
  const liveAtm = intelligence?.atms[0]

  const [victimCount, setVictimCount] = useState<number>(3)
  const [selectedVictimId, setSelectedVictimId] = useState<string | null>(null)
  const [backendComplaints, setBackendComplaints] = useState<any[]>([])

  useEffect(() => {
    fetch('/api/v1/police/complaints')
      .then((res) => res.json())
      .then((data) => {
        if (data?.items && Array.isArray(data.items)) {
          setBackendComplaints(data.items)
        }
      })
      .catch(() => {})
  }, [])

  // Build active victims list
  const activeVictims = useMemo(() => {
    const list = [...DEFAULT_VICTIMS_POOL]
    const effectiveName = intelligence?.victim_name || demoVictimName
    const effectiveAmount = intelligence?.amount || demoAmount
    const effectiveCaseId = intelligence?.complaint_id || demoCaseId

    if (effectiveName) {
      list[0] = {
        ...list[0],
        name: effectiveName,
        amount: effectiveAmount || list[0].amount,
        caseId: effectiveCaseId || list[0].caseId,
      }
    }
    // Blend with backend complaints if available
    if (backendComplaints.length > 0) {
      backendComplaints.forEach((c, idx) => {
        if (idx < list.length && idx > 0) {
          list[idx] = {
            id: `v${idx + 1}`,
            caseId: c.complaint_id || `CC-2026-${1000 + idx}`,
            name: c.name || list[idx].name,
            account: `UPI •••• ${c.fraudster_upi ? c.fraudster_upi.slice(-4) : 4000 + idx}`,
            amount: c.amount || list[idx].amount,
            timeAgo: `${(idx + 1) * 7}m ago`,
            fraudType: c.fraud_type || 'Syndicate Transfer',
          }
        }
      })
    }
    return list.slice(0, victimCount)
  }, [backendComplaints, demoAmount, demoCaseId, demoVictimName, intelligence, victimCount])

  const totalDefrauded = useMemo(() => {
    return activeVictims.reduce((acc, v) => acc + v.amount, 0)
  }, [activeVictims])

  const nodes: Node[] = useMemo(() => {
    const frozen = allNodesFrozen || currentStage >= 4
    const baseNodes: Node[] = []

    // Calculate vertical spacing dynamically for multiple victims
    const spacing = 110
    const startY = Math.max(20, 220 - ((activeVictims.length - 1) * spacing) / 2)

    activeVictims.forEach((v, i) => {
      baseNodes.push({
        id: `victim-${v.id}`,
        type: 'victim',
        position: { x: 30, y: startY + i * spacing },
        data: {
          index: i + 1,
          name: v.name,
          caseId: v.caseId,
          account: v.account,
          amount: v.amount,
          timeAgo: v.timeAgo,
          isSelected: selectedVictimId === v.id,
        },
      })
    })

    // Layer 1 Mule Accounts (Receives diversified inflow from multiple victims)
    const layer1Amount = Math.round(totalDefrauded / 2)
    const layer2Amount = Math.round(totalDefrauded / 4)

    return [
      ...baseNodes,
      // Layer 1 Mule Accounts
      {
        id: 'mule-1a',
        type: 'mule',
        position: { x: 340, y: 110 },
        data: {
          bank: liveMules?.[0]?.bank || 'Axis Bank Primary Shell',
          tier: 1,
          risk: liveMules?.[0]?.risk_score || 0.94,
          account: 'UTIB •••• 8291',
          amount: layer1Amount,
          frozen,
        },
      },
      {
        id: 'mule-1b',
        type: 'mule',
        position: { x: 340, y: 340 },
        data: {
          bank: liveMules?.[1]?.bank || 'Canara Bank Dormant VPA',
          tier: 1,
          risk: liveMules?.[1]?.risk_score || 0.91,
          account: 'CNRB •••• 5519',
          amount: layer1Amount,
          frozen,
        },
      },
      // Layer 2 Mule Accounts (Dispersed 4-node sub-tier)
      {
        id: 'mule-2a',
        type: 'mule',
        position: { x: 650, y: 20 },
        data: {
          bank: liveMules?.[2]?.bank || 'Kotak Micro-Corporate',
          tier: 2,
          risk: liveMules?.[2]?.risk_score || 0.88,
          account: 'KKBK •••• 1042',
          amount: layer2Amount,
          frozen,
        },
      },
      {
        id: 'mule-2b',
        type: 'mule',
        position: { x: 650, y: 155 },
        data: {
          bank: liveMules?.[3]?.bank || 'ICICI Fast-Collect Node',
          tier: 2,
          risk: liveMules?.[3]?.risk_score || 0.96,
          account: 'ICIC •••• 3381',
          amount: layer2Amount,
          frozen,
        },
      },
      {
        id: 'mule-2c',
        type: 'mule',
        position: { x: 650, y: 290 },
        data: {
          bank: 'PNB Synthetic Current',
          tier: 2,
          risk: 0.85,
          account: 'PUNB •••• 7123',
          amount: layer2Amount,
          frozen,
        },
      },
      {
        id: 'mule-2d',
        type: 'mule',
        position: { x: 650, y: 425 },
        data: {
          bank: 'SBI Digital Virtual Node',
          tier: 2,
          risk: 0.89,
          account: 'SBIN •••• 9921',
          amount: layer2Amount,
          frozen,
        },
      },
      // ATM Cashout Node
      {
        id: 'atm-1',
        type: 'atm',
        position: { x: 1040, y: 175 },
        data: {
          name: liveAtm?.name || 'ATM #04 Indiranagar 100ft',
          eta: `${liveAtm?.eta_min || 6} MIN`,
          patrol: `${liveAtm?.assigned_patrol || 'Delta-4'} Dispatched`,
        },
      },
    ]
  }, [activeVictims, allNodesFrozen, currentStage, intelligence, liveAtm, liveMules, selectedVictimId, totalDefrauded])

  const edges: Edge[] = useMemo(() => {
    const isFrozen = allNodesFrozen || currentStage >= 4
    const victimEdges: Edge[] = []

    activeVictims.forEach((v, idx) => {
      const vid = `victim-${v.id}`
      const isSelected = selectedVictimId === v.id || selectedVictimId === null
      const strokeColor = isFrozen ? '#2b5945' : isSelected ? '#ff7066' : '#636363'

      // Feed victim funds alternately/together into mule 1a & mule 1b
      victimEdges.push({
        id: `e-${vid}-1a`,
        source: vid,
        target: 'mule-1a',
        type: 'bezier',
        animated: !isFrozen,
        style: { stroke: strokeColor, strokeWidth: isSelected ? 2 : 1 },
        ...(idx === 0
          ? {
              label: formatINR(Math.round(v.amount / 2)),
              labelStyle: { fill: '#ffffff', fontFamily: 'monospace', fontSize: 10, fontWeight: 600 },
              labelBgStyle: { fill: '#000000', stroke: '#636363', rx: 4, ry: 4 },
            }
          : {}),
      })

      victimEdges.push({
        id: `e-${vid}-1b`,
        source: vid,
        target: 'mule-1b',
        type: 'bezier',
        animated: !isFrozen,
        style: { stroke: strokeColor, strokeWidth: isSelected ? 2 : 1 },
      })
    })

    return [
      ...victimEdges,
      // Layer 1a to Layer 2
      {
        id: 'e-1a-2a',
        source: 'mule-1a',
        target: 'mule-2a',
        animated: !isFrozen,
        style: { stroke: isFrozen ? '#2b5945' : '#ff4136', strokeWidth: 1.5 },
        label: formatINR(Math.round(totalDefrauded / 4)),
        labelStyle: { fill: '#c0c9c2', fontFamily: 'monospace', fontSize: 10 },
        labelBgStyle: { fill: '#000000', stroke: '#636363', rx: 4, ry: 4 },
      },
      {
        id: 'e-1a-2b',
        source: 'mule-1a',
        target: 'mule-2b',
        animated: !isFrozen,
        style: { stroke: isFrozen ? '#2b5945' : '#ff4136', strokeWidth: 1.5 },
      },
      // Layer 1b to Layer 2
      {
        id: 'e-1b-2c',
        source: 'mule-1b',
        target: 'mule-2c',
        animated: !isFrozen,
        style: { stroke: isFrozen ? '#2b5945' : '#ff4136', strokeWidth: 1.5 },
        label: formatINR(Math.round(totalDefrauded / 4)),
        labelStyle: { fill: '#c0c9c2', fontFamily: 'monospace', fontSize: 10 },
        labelBgStyle: { fill: '#000000', stroke: '#636363', rx: 4, ry: 4 },
      },
      {
        id: 'e-1b-2d',
        source: 'mule-1b',
        target: 'mule-2d',
        animated: !isFrozen,
        style: { stroke: isFrozen ? '#2b5945' : '#ff4136', strokeWidth: 1.5 },
      },
      // Layer 2b to ATM
      {
        id: 'e-2b-atm',
        source: 'mule-2b',
        target: 'atm-1',
        animated: true,
        style: { stroke: '#fae0a6', strokeWidth: 2, strokeDasharray: '4 4' },
        label: 'CASHOUT PIPELINE',
        labelStyle: { fill: '#fae0a6', fontFamily: 'monospace', fontSize: 10, fontWeight: 700 },
        labelBgStyle: { fill: '#000000', stroke: '#8c7847', rx: 4, ry: 4 },
      },
    ]
  }, [activeVictims, allNodesFrozen, currentStage, selectedVictimId, totalDefrauded])

  return (
    <div className="w-full h-full min-h-[460px] bg-black/30 backdrop-blur-md border border-[#636363] rounded-sm relative flex flex-col overflow-hidden select-none text-white">
      {/* Top Header Controls Bar */}
      <div className="p-3 border-b border-[#636363]/40 flex items-center justify-between flex-wrap gap-2 z-10 bg-black/30 backdrop-blur-md">
        <div className="flex items-center gap-2 flex-wrap">
          <div className="flex items-center gap-2 bg-[#121417] px-3 py-1 rounded-btn border border-[#636363]/60">
            <Users className="w-3.5 h-3.5 text-[#a0d1b8]" />
            <span className="font-mono text-xs font-bold text-white tracking-wider">
              MULTI-VICTIM GNN ONSET
            </span>
          </div>

          <Badge variant="live">{activeVictims.length} VICTIMS DEFRAUDED</Badge>
          <span className="text-xs font-mono text-[#fae0a6] font-bold">
            TOTAL SIPHONED: {formatINR(totalDefrauded)}
          </span>
        </div>

        {/* Multi-Victim Selector Pill Switcher */}
        <div className="flex items-center gap-1.5 font-mono text-xs">
          <span className="text-[11px] text-[#9b9b9b] uppercase tracking-wider hidden sm:inline">
            Cluster Mode:
          </span>
          {[1, 3, 5].map((cnt) => (
            <button
              key={cnt}
              onClick={() => {
                setVictimCount(cnt)
                setSelectedVictimId(null)
              }}
              className={cn(
                'px-2.5 py-1 rounded-btn text-xs font-mono transition-all border',
                victimCount === cnt
                  ? 'bg-white text-black font-bold border-white shadow-sm'
                  : 'bg-[#121417] text-[#c0c9c2] border-[#636363] hover:text-white hover:border-white'
              )}
            >
              {cnt === 1 ? 'Single Victim' : `${cnt} Victims Ring`}
            </button>
          ))}
        </div>
      </div>

      {/* Victims Sub-Tab Filter for Detailed Inspection */}
      {activeVictims.length > 1 && (
        <div className="py-1.5 px-3 bg-[#0a0c0e] border-b border-[#636363]/30 flex items-center gap-2 overflow-x-auto no-scrollbar z-10">
          <span className="text-[10px] font-mono text-[#9b9b9b] uppercase tracking-wider shrink-0">
            ISOLATE VICTIM TRAIL:
          </span>
          <button
            onClick={() => setSelectedVictimId(null)}
            className={cn(
              'px-2 py-0.5 rounded text-[10px] font-mono shrink-0 transition-all',
              selectedVictimId === null
                ? 'bg-[#2b5945] text-white font-bold'
                : 'bg-[#16191d] text-[#c0c9c2] hover:text-white'
            )}
          >
            Show All Inflows
          </button>
          {activeVictims.map((v) => (
            <button
              key={v.id}
              onClick={() => setSelectedVictimId(v.id === selectedVictimId ? null : v.id)}
              className={cn(
                'px-2 py-0.5 rounded text-[10px] font-mono shrink-0 transition-all border',
                selectedVictimId === v.id
                  ? 'bg-white text-black font-bold border-white'
                  : 'bg-[#16191d] text-[#c0c9c2] border-[#636363]/40 hover:border-white'
              )}
            >
              {v.name} ({formatINR(v.amount)})
            </button>
          ))}
        </div>
      )}

      {/* Main XYFlow Canvas Area */}
      <div className="relative flex-1 w-full min-h-[360px]">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          nodeTypes={nodeTypes}
          fitView
          minZoom={0.2}
          maxZoom={1.5}
          proOptions={{ hideAttribution: true }}
        >
          <Background color="#2f3234" gap={20} />
          <Controls
            className="!bg-black/30 backdrop-blur-md !border !border-[#636363] !rounded-sm !shadow-none overflow-hidden"
            showInteractive={false}
          />
        </ReactFlow>
      </div>

      {/* Bottom Summary Bar */}
      <div className="p-2 px-3 bg-[#0c0e11] border-t border-[#636363]/40 flex items-center justify-between flex-wrap gap-2 text-xs font-mono text-[#9b9b9b] z-10">
        <div className="flex items-center gap-3">
          <span className="text-[#a0d1b8]">LAYER-1 CONVERGENCE: 2 SHELL ACCOUNTS</span>
          <span className="text-[#636363]">/</span>
          <span>LAYER-2 DISPERSION: 4 VIRTUAL VPAs</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-1.5 h-1.5 rounded-full bg-[#ff4136] animate-ping" />
          <span className="text-white font-medium">REAL-TIME MULTI-SOURCE GRAPH RECONSTRUCTION ACTIVE</span>
        </div>
      </div>
    </div>
  )
}
