import React, { useState } from 'react'
import { ComplaintWizard } from '@/components/wizard/ComplaintWizard'
import { CaseTracker } from '@/components/wizard/CaseTracker'
import { FilePlus, Search, ShieldCheck } from 'lucide-react'
import { useDemoStore } from '@/store/demoStore'
import { useCaseStore } from '@/store/caseStore'
import { cn } from '@/lib/utils'

export const Report: React.FC = () => {
  const { currentStage, caseId } = useDemoStore()
  const intelligence = useCaseStore((state) => state.intelligence)
  const setIntelligence = useCaseStore((state) => state.setIntelligence)
  const [activeTab, setActiveTab] = useState<'wizard' | 'tracker'>(
    currentStage >= 2 ? 'tracker' : 'wizard'
  )
  const [activeCaseId, setActiveCaseId] = useState(caseId || 'CC-2026-F819')
  const [caseData, setCaseData] = useState({
    name: intelligence?.victim_name || 'Rohan Sharma',
    phone: '9876543210',
    amount: intelligence?.amount || 500000,
    fraudType: 'INVESTMENT_SCAM',
    suspectUpi: intelligence?.target_vpa || 'nexus.invest@ybl',
  })

  const handleSuccess = (newId: string, formData: any, response: any) => {
    if (response.intelligence) {
      setIntelligence(response.intelligence)
    }
    useDemoStore.setState({
      caseId: newId,
      victimName: formData.name,
      amount: formData.amount,
      currentStage: 2,
    })
    setActiveCaseId(newId)
    setCaseData({
      name: formData.name,
      phone: formData.phone,
      amount: formData.amount,
      fraudType: formData.fraudType,
      suspectUpi: formData.suspectUpi,
    })
    setActiveTab('tracker')
  }

  return (
    <div className="min-h-screen bg-[#1e2124] text-white pt-24 pb-16 px-4 md:px-8">
      <div className="w-full max-w-5xl mx-auto space-y-8">
        {/* Top Header & Segmented Switcher */}
        <div className="flex items-center justify-between flex-wrap gap-4 pb-6 border-b border-[#636363]/40">
          <div className="flex items-center gap-3.5">
            <div className="w-10 h-10 rounded-card bg-[#000000] border border-[#2b5945] flex items-center justify-center text-[#a0d1b8] shadow-sm">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs text-[#a0d1b8] font-semibold tracking-wider uppercase">
                  CITIZEN PROTOCOL 1930
                </span>
                <span className="text-[#636363]">/</span>
                <span className="font-mono text-[11px] text-[#9b9b9b]">GOLDEN WINDOW ACTIVE</span>
              </div>
              <h1 className="text-xl sm:text-2xl font-sans font-bold text-white tracking-tight">
                Incident Intake & Real-Time Case Tracker
              </h1>
            </div>
          </div>

          {/* Palantir Pill Segmented Switcher */}
          <div className="flex items-center p-1 rounded-btn bg-[#121417] border border-[#636363]">
            <button
              onClick={() => setActiveTab('wizard')}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-btn text-xs font-sans font-medium transition-all duration-200',
                activeTab === 'wizard'
                  ? 'bg-white text-[#121417] font-semibold shadow-sm'
                  : 'text-[#c0c9c2] hover:text-white'
              )}
            >
              <FilePlus className="w-3.5 h-3.5" />
              <span>File New Incident</span>
            </button>

            <button
              onClick={() => setActiveTab('tracker')}
              className={cn(
                'flex items-center gap-2 px-4 py-2 rounded-btn text-xs font-sans font-medium transition-all duration-200',
                activeTab === 'tracker'
                  ? 'bg-white text-[#121417] font-semibold shadow-sm'
                  : 'text-[#c0c9c2] hover:text-white'
              )}
            >
              <Search className="w-3.5 h-3.5" />
              <span>Track ({activeCaseId})</span>
            </button>
          </div>
        </div>

        {/* Main View Area */}
        {activeTab === 'wizard' ? (
          <ComplaintWizard onSuccess={handleSuccess} />
        ) : (
          <CaseTracker caseId={activeCaseId} initialData={caseData} />
        )}
      </div>
    </div>
  )
}
