import { create } from 'zustand'

export interface DemoStageInfo {
  stage: number
  label: string
  desc: string
  route: string
  durationSec: number
}

export const DEMO_STAGES: DemoStageInfo[] = [
  {
    stage: 1,
    label: '01 · CITIZEN FILING',
    desc: 'Citizen reports ₹5,00,000 investment fraud via VPA nexus.invest@ybl',
    route: '/report',
    durationSec: 10,
  },
  {
    stage: 2,
    label: '02 · GNN MULE DETECTION',
    desc: 'Graph Neural Network expands 3-hop mule ring across 8 bank accounts',
    route: '/command',
    durationSec: 10,
  },
  {
    stage: 3,
    label: '03 · STM ATM PREDICTION',
    desc: 'Spatial-Temporal Model forecasts ATM cashout at Indiranagar within 6 min',
    route: '/command',
    durationSec: 10,
  },
  {
    stage: 4,
    label: '04 · UNIVERSAL FREEZE',
    desc: 'One-click NPCI API broadcast locks all 8 nodes & ₹5,00,000 balance',
    route: '/command',
    durationSec: 10,
  },
  {
    stage: 5,
    label: '05 · TACTICAL INTERCEPT',
    desc: 'Field patrol dispatched with geo-coordinates to secure suspect at ATM',
    route: '/field',
    durationSec: 10,
  },
  {
    stage: 6,
    label: '06 · FORENSIC RESOLUTION',
    desc: 'Digital evidence pack hashed to blockchain; 100% fund recovery logged',
    route: '/report',
    durationSec: 10,
  },
]

export interface DemoState {
  isDemoActive: boolean
  isDemoRunning: boolean
  currentStage: number
  currentStep: number
  isPlaying: boolean
  caseId: string
  amount: number
  allNodesFrozen: boolean
  patrolDispatched: boolean
  dispatchedPatrols: Record<string, boolean>
  caseResolved: boolean

  startDemo: () => void
  stopDemo: () => void
  pauseDemo: () => void
  resumeDemo: () => void
  resetDemo: () => void
  setStage: (stage: number) => void
  triggerUniversalFreeze: () => void
  dispatchPatrol: (id?: string) => void
  resolveCase: () => void
}

export const useDemoStore = create<DemoState>((set) => ({
  isDemoActive: false,
  isDemoRunning: false,
  currentStage: 1,
  currentStep: 1,
  isPlaying: false,
  caseId: 'CC-2026-F819',
  amount: 500000,
  allNodesFrozen: false,
  patrolDispatched: false,
  dispatchedPatrols: {},
  caseResolved: false,

  startDemo: () =>
    set({
      isDemoActive: true,
      isDemoRunning: true,
      isPlaying: true,
      currentStage: 1,
      currentStep: 1,
      allNodesFrozen: false,
      patrolDispatched: false,
      dispatchedPatrols: {},
      caseResolved: false,
    }),

  stopDemo: () =>
    set({
      isDemoActive: false,
      isDemoRunning: false,
      isPlaying: false,
    }),

  pauseDemo: () => set({ isPlaying: false }),
  resumeDemo: () => set({ isPlaying: true }),

  resetDemo: () =>
    set({
      isDemoActive: false,
      isDemoRunning: false,
      isPlaying: false,
      currentStage: 1,
      currentStep: 1,
      allNodesFrozen: false,
      patrolDispatched: false,
      dispatchedPatrols: {},
      caseResolved: false,
    }),

  setStage: (stage: number) =>
    set({
      currentStage: stage,
      currentStep: stage,
      isDemoActive: true,
      isDemoRunning: true,
      allNodesFrozen: stage >= 4,
      patrolDispatched: stage >= 5,
      caseResolved: stage >= 6,
    }),

  triggerUniversalFreeze: () => set({ allNodesFrozen: true }),
  dispatchPatrol: (id?: string) =>
    set((state) => ({
      patrolDispatched: true,
      dispatchedPatrols: id ? { ...state.dispatchedPatrols, [id]: true } : state.dispatchedPatrols,
    })),
  resolveCase: () => set({ caseResolved: true }),
}))