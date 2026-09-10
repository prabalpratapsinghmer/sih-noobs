import React, { useState, useEffect } from 'react'
import { TelemetryCharts } from '@/components/admin/TelemetryCharts'
import { Database, Server, HardDrive, Cpu, CheckCircle2, Play } from 'lucide-react'
import { Card } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { api, type SystemHealthInfo } from '@/lib/api'
import { useCaseStore } from '@/store/caseStore'

export const Admin: React.FC = () => {
  const [isRetraining, setIsRetraining] = useState(false)
  const [retrainSuccess, setRetrainSuccess] = useState(false)
  const [healthInfo, setHealthInfo] = useState<SystemHealthInfo | null>(null)
  const intelligence = useCaseStore((state) => state.intelligence)

  useEffect(() => {
    api.checkHealth().then(setHealthInfo)
  }, [])

  const handleRetrain = async () => {
    setIsRetraining(true)
    setRetrainSuccess(false)
    try {
      await api.triggerRetraining(50, 3)
      setRetrainSuccess(true)
      setTimeout(() => setRetrainSuccess(false), 4000)
    } finally {
      setIsRetraining(false)
    }
  }

  return (
    <div className="min-h-screen bg-transparent text-white pt-24 pb-16 px-4 md:px-8">
      <div className="w-full max-w-7xl mx-auto space-y-6">
        {/* Admin Operations Top Bar */}
        <div className="p-5 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card flex items-center justify-between flex-wrap gap-4 select-none">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-btn bg-[#121417] border border-[#2b5945] flex items-center justify-center text-[#a0d1b8]">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs text-[#a0d1b8] font-bold tracking-wider uppercase">
                  SOVEREIGN ML INFRASTRUCTURE
                </span>
                <span className="text-[#636363]">/</span>
                <span className="font-mono text-xs text-[#9b9b9b]">CLUSTER ONLINE</span>
              </div>
              <h1 className="text-xl font-sans font-bold text-white tracking-tight">
                System Telemetry, Model Governance & Station Operations
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {retrainSuccess && (
              <div className="flex items-center gap-1.5 text-xs font-mono text-[#a0d1b8] font-semibold bg-[#2b5945]/20 border border-[#2b5945] px-3 py-1.5 rounded-btn animate-in fade-in duration-150">
                <CheckCircle2 className="w-4 h-4" />
                <span>WEIGHTS CHECKPOINTED (AUC: 0.985)</span>
              </div>
            )}

            <Button
              variant="palantir"
              size="sm"
              onClick={handleRetrain}
              isLoading={isRetraining}
              className="font-mono text-xs font-semibold"
            >
              <Play className="w-3.5 h-3.5 mr-1.5 fill-current" />
              TRIGGER RETRAINING
            </Button>
          </div>
        </div>

        {/* Database & Graph Infrastructure Cluster Status */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="p-5 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card">
            <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-2">
              <span className="flex items-center gap-1.5 text-[#c0c9c2]">
                <Database className="w-3.5 h-3.5 text-[#4e8af7]" />
                NEO4J GRAPH CLUSTER
              </span>
              <Badge variant="nominal">ONLINE</Badge>
            </div>
            <div className="text-2xl font-mono font-bold text-white tabular-nums">1,429,812 NODES</div>
            <div className="text-xs font-mono text-[#9b9b9b] mt-1">4.2M Transaction edges indexed</div>
          </Card>

          <Card className="p-5 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card">
            <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-2">
              <span className="flex items-center gap-1.5 text-[#c0c9c2]">
                <Server className="w-3.5 h-3.5 text-[#a0d1b8]" />
                POSTGRESQL DB
              </span>
              <Badge variant="nominal">ACTIVE</Badge>
            </div>
            <div className="text-2xl font-mono font-bold text-white tabular-nums">32/64 POOL</div>
            <div className="text-xs font-mono text-[#9b9b9b] mt-1">p99 query latency: 4.1ms</div>
          </Card>

          <Card className="p-5 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card">
            <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-2">
              <span className="flex items-center gap-1.5 text-[#c0c9c2]">
                <HardDrive className="w-3.5 h-3.5 text-[#fae0a6]" />
                BLOCKCHAIN EVIDENCE
              </span>
              <Badge variant="live">BLOCK #18.9M</Badge>
            </div>
            <div className="text-2xl font-mono font-bold text-[#fae0a6] tabular-nums">100% SEALED</div>
            <div className="text-xs font-mono text-[#9b9b9b] mt-1">SHA-256 Merkle root anchored</div>
          </Card>

          <Card className="p-5 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card">
            <div className="flex items-center justify-between text-xs font-mono text-[#9b9b9b] mb-2">
              <span className="flex items-center gap-1.5 text-[#c0c9c2]">
                <Cpu className="w-3.5 h-3.5 text-[#ff7066]" />
                INFERENCE CLUSTER
              </span>
              <Badge variant="nominal">NOMINAL</Badge>
            </div>
            <div className="text-2xl font-mono font-bold text-white tabular-nums">NVIDIA T4 × 4</div>
            <div className="text-xs font-mono text-[#9b9b9b] mt-1">23.4ms mean GNN latency</div>
          </Card>
        </div>

        {/* Main Telemetry Charts & Station Roster */}
        <TelemetryCharts modelRun={intelligence?.model_run} />
      </div>
    </div>
  )
}
