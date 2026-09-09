import React, { useState } from 'react'
import { CheckCircle2, X, Zap } from 'lucide-react'
import { Button } from '@/components/ui/Button'
import { useDemoStore } from '@/store/demoStore'
import { api } from '@/lib/api'

export const UniversalFreezeButton: React.FC = () => {
  const { allNodesFrozen, triggerUniversalFreeze } = useDemoStore()
  const [state, setState] = useState<'idle' | 'confirming' | 'freezing' | 'frozen'>(
    allNodesFrozen ? 'frozen' : 'idle'
  )

  const handleStartConfirm = () => {
    if (allNodesFrozen) return
    setState('confirming')
  }

  const handleExecuteFreeze = async () => {
    setState('freezing')
    try {
      await api.triggerUniversalFreeze('CC-2026-F819', ['mule-1a', 'mule-1b', 'mule-2a', 'mule-2b', 'mule-2c', 'mule-2d'])
    } catch (err) {
      console.warn('Freeze execution simulated', err)
    }
    setTimeout(() => {
      triggerUniversalFreeze()
      setState('frozen')
    }, 1200)
  }

  if (allNodesFrozen || state === 'frozen') {
    return (
      <div className="flex items-center gap-2 px-4 py-2.5 rounded-btn bg-[#2b5945]/20 border border-[#2b5945] text-[#a0d1b8] font-mono text-xs font-semibold select-none">
        <CheckCircle2 className="w-4 h-4 text-[#a0d1b8]" />
        <span>8/8 NODES FROZEN · NPCI DIRECTIVE COMPLETE</span>
      </div>
    )
  }

  if (state === 'confirming') {
    return (
      <div className="flex items-center gap-2 bg-[#000000] p-1.5 rounded-btn border-2 border-[#ff4136] animate-pulse">
        <span className="font-mono text-xs text-[#ff7066] font-bold px-2">
          LOCK ALL 8 NODES & ₹5,00,000?
        </span>
        <Button
          size="sm"
          variant="destructive"
          onClick={handleExecuteFreeze}
          className="text-xs bg-[#994500] text-white hover:bg-[#b85300] font-mono font-bold border-[#994500]"
        >
          CONFIRM
        </Button>
        <Button
          size="sm"
          variant="ghost"
          onClick={() => setState('idle')}
          className="text-xs text-[#9b9b9b] hover:text-white px-2"
        >
          <X className="w-3.5 h-3.5" />
        </Button>
      </div>
    )
  }

  if (state === 'freezing') {
    return (
      <Button variant="secondary" size="md" isLoading className="font-mono text-xs text-[#fae0a6] border-[#8c7847] bg-[#121417]">
        BROADCASTING NPCI DIRECTIVES...
      </Button>
    )
  }

  return (
    <button
      onClick={handleStartConfirm}
      className="inline-flex items-center gap-2 font-mono text-xs uppercase tracking-wider bg-[#994500] text-white hover:bg-[#b85300] px-4 py-2.5 rounded-btn font-semibold transition-all duration-200 active:scale-[0.98]"
    >
      <Zap className="w-3.5 h-3.5 fill-current" />
      <span>UNIVERSAL FREEZE (8 NODES)</span>
    </button>
  )
}
