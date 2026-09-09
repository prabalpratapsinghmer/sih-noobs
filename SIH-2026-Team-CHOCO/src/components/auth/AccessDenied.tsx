import React from 'react'
import { Link } from 'react-router-dom'
import { ShieldAlert, Lock, ArrowRight, UserCheck, KeyRound, ArrowLeft } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'

interface AccessDeniedProps {
  allowedRoles: string[]
  moduleName?: string
}

export const AccessDenied: React.FC<AccessDeniedProps> = ({ allowedRoles, moduleName = 'Tactical Dashboard' }) => {
  const { user, openAuthModalWithPrompt } = useAuthStore()

  return (
    <div className="min-h-[80vh] flex items-center justify-center p-4">
      <div className="max-w-xl w-full bg-[#0c0e12] border border-red-900/60 rounded-card p-6 md:p-8 shadow-2xl relative overflow-hidden">
        {/* Subtle red warning grid overlay */}
        <div
          className="absolute inset-0 opacity-[0.05] pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(#ef4444 1px, transparent 1px)`,
            backgroundSize: '24px 24px',
          }}
        />

        <div className="relative space-y-6">
          {/* Header */}
          <div className="flex items-center gap-3 border-b border-red-900/40 pb-4">
            <div className="w-10 h-10 rounded-btn bg-red-950/80 border border-red-800 text-red-400 flex items-center justify-center shrink-0">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs text-red-400 uppercase font-bold tracking-wider">
                  SECURITY PROTOCOL BNS-403
                </span>
                <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-red-950 text-red-400 border border-red-800/60">
                  RESTRICTED ACCESS
                </span>
              </div>
              <h1 className="font-sans text-lg font-bold text-white tracking-wide">
                Insufficient Clearance for {moduleName}
              </h1>
            </div>
          </div>

          {/* Description */}
          <p className="text-body-sm text-[#c0c9c2] leading-relaxed">
            This operational module contains sensitive sovereign intelligence, including real-time dynamic graph
            decompositions, live ATM surveillance coordinates, and NPCI statutory freeze directives. Your current
            credentials do not meet the minimum authorization threshold for this operational layer.
          </p>

          {/* Access Matrix Card */}
          <div className="grid grid-cols-2 gap-3 p-3.5 bg-[#14171d] border border-[#636363]/40 rounded-card font-mono text-xs">
            <div>
              <span className="text-[#9b9b9b] block text-[10px] uppercase">Active Identity</span>
              <span className="text-white font-semibold">{user?.username || 'Anonymous'}</span>
              <span className="text-yellow-400 block text-[11px] mt-0.5">Role: {user?.role || 'UNAUTHENTICATED'}</span>
            </div>
            <div>
              <span className="text-[#9b9b9b] block text-[10px] uppercase">Clearance Required</span>
              <span className="text-[#38d39f] font-semibold">{allowedRoles.join(' or ')}</span>
              <span className="text-[#9b9b9b] block text-[11px] mt-0.5">Hierarchy: Level 2 / Level 3</span>
            </div>
          </div>

          {/* Hierarchy Explanation Note */}
          <div className="p-3 bg-[#171a20] border-l-2 border-yellow-500/80 rounded-r-btn text-xs text-[#9b9b9b] space-y-1">
            <p className="font-sans font-semibold text-white">Hierarchical Clearance Breakdown:</p>
            <p>• <strong className="text-white">ADMIN (Director Moksh)</strong>: Level 3 — Universal access to all systems.</p>
            <p>• <strong className="text-white">INSPECTOR (Vikram)</strong>: Level 2 — Tactical Command & Mule Graph.</p>
            <p>• <strong className="text-white">CONSTABLE (Chetan)</strong>: Level 1 — Field Intercept & Public Reports.</p>
            <p>• <strong className="text-white">CITIZEN (Rahul)</strong>: Level 0 — Public Incident Reporting only.</p>
          </div>

          {/* Action CTAs */}
          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              onClick={() =>
                openAuthModalWithPrompt(
                  `Sign in with Director or Inspector credentials to access ${moduleName}.`
                )
              }
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-btn bg-[#2b5945] hover:bg-[#346b53] border border-[#38d39f]/50 text-white font-sans font-semibold text-xs transition-all duration-150 active:scale-[0.98]"
            >
              <KeyRound className="w-3.5 h-3.5 text-[#38d39f]" />
              <span>Switch to Authorized Account ↳</span>
            </button>

            <Link
              to="/report"
              className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-btn bg-[#1a1d22] hover:bg-[#252930] text-[#c0c9c2] hover:text-white border border-[#636363]/40 font-sans font-medium text-xs transition-colors"
            >
              <span>Incident Portal</span>
            </Link>

            <Link
              to="/"
              className="inline-flex items-center gap-1.5 px-3 py-2 text-[#9b9b9b] hover:text-white font-sans text-xs transition-colors ml-auto"
            >
              <ArrowLeft className="w-3 h-3" />
              <span>Overview</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
