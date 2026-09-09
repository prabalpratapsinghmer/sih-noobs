import { create } from 'zustand'

export interface OfficerProfile {
  name: string
  rank: string
  division: string
  badgeId: string
  station: string
}

export interface SystemAlert {
  id: string
  timestamp: string
  level: 'CRITICAL' | 'WARNING' | 'NOMINAL' | 'INFO'
  message: string
  read: boolean
  targetRoute?: string
}

interface AppState {
  systemStatus: 'NOMINAL' | 'ELEVATED' | 'CRITICAL'
  wsLatency: number
  isLiveApi: boolean
  copilotOpen: boolean
  officer: OfficerProfile
  alerts: SystemAlert[]
  commandPaletteOpen: boolean
  theme: 'dark' | 'light'
  setSystemStatus: (status: 'NOMINAL' | 'ELEVATED' | 'CRITICAL') => void
  setWsLatency: (latency: number) => void
  setIsLiveApi: (live: boolean) => void
  setCopilotOpen: (open: boolean) => void
  toggleCopilot: () => void
  setCommandPaletteOpen: (open: boolean) => void
  markAlertRead: (id: string) => void
  markAllAlertsRead: () => void
  addAlert: (alert: Omit<SystemAlert, 'id' | 'timestamp' | 'read'>) => void
  setTheme: (theme: 'dark' | 'light') => void
  toggleTheme: () => void
}

const applyThemeToDocument = (theme: 'dark' | 'light') => {
  if (typeof document !== 'undefined') {
    const root = document.documentElement
    if (theme === 'light') {
      root.classList.remove('dark')
      root.classList.add('light')
      root.style.colorScheme = 'light'
    } else {
      root.classList.remove('light')
      root.classList.add('dark')
      root.style.colorScheme = 'dark'
    }
  }
}

const getInitialTheme = (): 'dark' | 'light' => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('cybercell_theme') as 'dark' | 'light' | null
    if (saved === 'light' || saved === 'dark') {
      applyThemeToDocument(saved)
      return saved
    }
  }
  applyThemeToDocument('dark')
  return 'dark'
}

export const useAppStore = create<AppState>((set, get) => ({
  theme: getInitialTheme(),
  systemStatus: 'NOMINAL',
  wsLatency: 18,
  isLiveApi: false,
  copilotOpen: false,
  commandPaletteOpen: false,
  officer: {
    name: 'Insp. Vikramaditya Singh',
    rank: 'Inspector of Police',
    division: 'Cyber Crime Investigation Cell (CHOCO)',
    badgeId: 'CC-9042',
    station: 'Bengaluru Central Command',
  },
  alerts: [
    {
      id: 'alt-01',
      timestamp: '02:24:10',
      level: 'CRITICAL',
      message: 'Rapid fund dispersal detected across 4 UPI handles under Layer-2.',
      read: false,
      targetRoute: '/command',
    },
    {
      id: 'alt-02',
      timestamp: '02:21:45',
      level: 'WARNING',
      message: 'ATM #04 Indiranagar risk index elevated to 0.942. High cashout probability.',
      read: false,
      targetRoute: '/field',
    },
    {
      id: 'alt-03',
      timestamp: '02:15:30',
      level: 'NOMINAL',
      message: 'NPCI API Gateway sync confirmed. Latency: 18ms. Zero packet loss.',
      read: true,
      targetRoute: '/admin',
    },
  ],
  setSystemStatus: (systemStatus) => set({ systemStatus }),
  setWsLatency: (wsLatency) => set({ wsLatency }),
  setIsLiveApi: (isLiveApi) => set({ isLiveApi }),
  setCopilotOpen: (copilotOpen) => set({ copilotOpen }),
  toggleCopilot: () => set((state) => ({ copilotOpen: !state.copilotOpen })),
  setCommandPaletteOpen: (commandPaletteOpen) => set({ commandPaletteOpen }),
  markAlertRead: (id) =>
    set((state) => ({
      alerts: state.alerts.map((a) => (a.id === id ? { ...a, read: true } : a)),
    })),
  markAllAlertsRead: () =>
    set((state) => ({
      alerts: state.alerts.map((a) => ({ ...a, read: true })),
    })),
  addAlert: (alert) =>
    set((state) => ({
      alerts: [
        {
          id: `alt-${Date.now()}`,
          timestamp: new Date().toTimeString().slice(0, 8),
          read: false,
          ...alert,
        },
        ...state.alerts,
      ],
    })),
  setTheme: (theme) => {
    localStorage.setItem('cybercell_theme', theme)
    applyThemeToDocument(theme)
    set({ theme })
  },
  toggleTheme: () => {
    const nextTheme = get().theme === 'dark' ? 'light' : 'dark'
    localStorage.setItem('cybercell_theme', nextTheme)
    applyThemeToDocument(nextTheme)
    set({ theme: nextTheme })
  },
}))
