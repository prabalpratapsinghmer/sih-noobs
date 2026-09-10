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
import GhostFibers from '@/components/ui/GhostFibers'

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
    <div className="min-h-[100dvh] bg-transparent text-white flex flex-col antialiased selection:bg-[#2b5945] selection:text-white transition-colors duration-200 relative overflow-x-hidden">
      {/* GhostFibers WebGL dynamic ambient background */}
      <div className="fixed inset-0 z-0 pointer-events-none">
        <GhostFibers
          lineColor="#140E35"
          glowColor="#3437A0"
          speed={0.2}
          scale={2}
          rotation={0}
          rotationSpeed={0.25}
          layers={4}
          waveAmplitude={0.015}
          waveFrequency={3}
          waveSpeed={0.15}
          layerSpeed={0.08}
          twist={0.1}
          twistFrequency={5}
          twistSpeed={1.2}
          lineFrequency={5}
          lineSpacing={2}
          lineSharpness={16}
          glowFalloff={10}
          glowIntensity={1.6}
          brightness={2}
          blueBoost={1.25}
          vignette={0.8}
          grain={0.05}
          dpr={1}
          lightMode={false}
          fps={60}
          paused={false}
        />
      </div>

      {/* Acrylic backdrop for high contrast text readability */}
      <div className="fixed inset-0 bg-black/20 backdrop-blur-[8px] pointer-events-none z-0" />

      <div className="relative z-10 flex flex-col min-h-screen">
        <GlobalShortcuts />
        <Topbar />

        <main className="flex-1 pb-16 lg:pb-6">
        <Routes>
          <Route path="/" element={<Gateway />} />

          {/* Citizen Incident Intake - Accessible to Citizens, Constables, Police, Command HQ */}
          <Route
            path="/report"
            element={
              <ProtectedRoute
                allowedRoles={['COMMAND_HQ', 'POLICE', 'CONSTABLE', 'CITIZEN']}
                moduleName="Incident Reporting Portal"
              >
                <Report />
              </ProtectedRoute>
            }
          />

          {/* Tactical Command HQ & Mule Graph - Command HQ Only (Police & Citizens cannot access) */}
          <Route
            path="/command"
            element={
              <ProtectedRoute
                allowedRoles={['COMMAND_HQ']}
                moduleName="Tactical Command HQ & Mule Ontology"
              >
                <Command />
              </ProtectedRoute>
            }
          />

          {/* Field Patrol Radar & Cashout Maps - Police Dashboard (Police, Constable & Command HQ) */}
          <Route
            path="/field"
            element={
              <ProtectedRoute
                allowedRoles={['POLICE', 'CONSTABLE', 'COMMAND_HQ']}
                moduleName="Police Field Patrol & ATM Radar"
              >
                <Field />
              </ProtectedRoute>
            }
          />

          {/* Supervisory Governance & STM Telemetry - Command HQ Only */}
          <Route
            path="/admin"
            element={
              <ProtectedRoute
                allowedRoles={['COMMAND_HQ']}
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
    </div>
  )
}

export default App