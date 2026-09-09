import React, { useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import { Topbar } from '@/components/layout/Topbar'
import { MobileBottomDock } from '@/components/layout/MobileBottomDock'
import { Gateway } from '@/pages/Gateway'
import { Report } from '@/pages/Report'
import { Command } from '@/pages/Command'
import { Field } from '@/pages/Field'
import { Admin } from '@/pages/Admin'
import { useAppStore } from '@/store/appStore'

function GlobalShortcuts() {
  const { toggleCopilot } = useAppStore()

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+Space or Alt+C toggles forensic copilot
      if (((e.ctrlKey || e.metaKey) && e.code === 'Space') || (e.altKey && e.key === 'c')) {
        e.preventDefault()
        toggleCopilot()
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [toggleCopilot])

  return null
}

import { ProtectedRoute } from '@/components/auth/ProtectedRoute'
import { UniversalChatbot } from '@/components/chat/UniversalChatbot'

export const App: React.FC = () => {
  const { theme } = useAppStore()

  useEffect(() => {
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
  }, [theme])

  return (
    <div className="min-h-[100dvh] bg-[#1e2124] text-white flex flex-col antialiased selection:bg-[#2b5945] selection:text-white transition-colors duration-200">
      <GlobalShortcuts />
      <Topbar />

      <main className="flex-1 pb-16 lg:pb-6">
        <Routes>
          <Route path="/" element={<Gateway />} />

          {/* Citizen Incident Intake - Accessible to Citizens, Constables, Inspectors, Admins */}
          <Route
            path="/report"
            element={
              <ProtectedRoute
                allowedRoles={['ADMIN', 'INSPECTOR', 'CONSTABLE', 'CITIZEN']}
                moduleName="Incident Reporting Portal"
              >
                <Report />
              </ProtectedRoute>
            }
          />

          {/* Tactical Command HQ & Mule Graph - Level 2 (Inspector) & Level 3 (Admin) Only */}
          <Route
            path="/command"
            element={
              <ProtectedRoute
                allowedRoles={['ADMIN', 'INSPECTOR']}
                moduleName="Tactical Command HQ & Mule Ontology"
              >
                <Command />
              </ProtectedRoute>
            }
          />

          {/* Field Patrol Radar & Cashout Maps - Level 1 (Constable), Level 2 (Inspector), Level 3 (Admin) */}
          <Route
            path="/field"
            element={
              <ProtectedRoute
                allowedRoles={['ADMIN', 'INSPECTOR', 'CONSTABLE']}
                moduleName="Field Patrol & ATM Radar"
              >
                <Field />
              </ProtectedRoute>
            }
          />

          {/* Supervisory Governance & STM Telemetry - Level 3 (Admin / Director Moksh) Only */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute
                allowedRoles={['ADMIN']}
                moduleName="Central Governance & Supervisory Telemetry"
              >
                <Admin />
              </ProtectedRoute>
            }
          />

          <Route path="*" element={<Gateway />} />
        </Routes>
      </main>

      <MobileBottomDock />
      <UniversalChatbot />
    </div>
  )
}

export default App