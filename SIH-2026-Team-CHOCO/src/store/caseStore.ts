import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { CaseIntelligence } from '@/lib/api'

interface CaseState {
  intelligence: CaseIntelligence | null
  setIntelligence: (intelligence: CaseIntelligence) => void
  clearIntelligence: () => void
}

// Keep the latest backend snapshot available when a user switches dashboards.
export const useCaseStore = create<CaseState>()(
  persist(
    (set) => ({
      intelligence: null,
      setIntelligence: (intelligence) => set({ intelligence }),
      clearIntelligence: () => set({ intelligence: null }),
    }),
    { name: 'cybercell-active-case' },
  ),
)
