import React, { useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { useAuthStore } from '@/store/authStore'
import { AccessDenied } from '@/components/auth/AccessDenied'
import { Shield, KeyRound, ArrowRight } from 'lucide-react'

interface ProtectedRouteProps {
  children: React.ReactNode
  allowedRoles: string[]
  moduleName?: string
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  allowedRoles,
  moduleName = 'Tactical Console',
}) => {
  const location = useLocation()
  const { isAuthenticated, hasClearance, openAuthModalWithPrompt } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated) {
      openAuthModalWithPrompt(
        `Authentication Required: Please sign in with authorized credentials to access ${moduleName}.`,
        location.pathname
      )
    }
  }, [isAuthenticated, location.pathname, moduleName, openAuthModalWithPrompt])

  // 1. Unauthenticated barrier
  if (!isAuthenticated) {
    return (
      <div className="min-h-[80vh] flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-[#0e1014] border border-[#636363]/60 rounded-card p-6 md:p-8 shadow-2xl text-center space-y-5 animate-in fade-in">
          <div className="w-12 h-12 rounded-btn bg-[#181b20] border border-[#38d39f]/40 text-[#38d39f] flex items-center justify-center mx-auto">
            <KeyRound className="w-6 h-6" />
          </div>

          <div className="space-y-1">
            <span className="font-mono text-[11px] text-[#38d39f] uppercase tracking-widest font-semibold">
              SECURE ACCESS GATEWAY
            </span>
            <h2 className="font-sans text-xl font-bold text-white">
              Authentication Required
            </h2>
            <p className="text-body-sm text-[#9b9b9b] mt-2">
              Access to <strong className="text-white">{moduleName}</strong> requires an active authenticated session.
              Please sign in to proceed.
            </p>
          </div>

          <div className="pt-2">
            <button
              onClick={() =>
                openAuthModalWithPrompt(
                  `Sign in with authorized officer credentials to access ${moduleName}.`,
                  location.pathname
                )
              }
              className="w-full py-3 px-4 rounded-btn bg-[#2b5945] hover:bg-[#346b53] border border-[#38d39f]/50 text-white font-sans font-semibold text-xs tracking-wider flex items-center justify-center gap-2 transition-all duration-200 active:scale-[0.98]"
            >
              <span>SIGN IN TO ACCESS CONSOLE ↳</span>
            </button>
          </div>
        </div>
      </div>
    )
  }

  // 2. Role Clearance check
  if (!hasClearance(allowedRoles)) {
    return <AccessDenied allowedRoles={allowedRoles} moduleName={moduleName} />
  }

  // 3. Authorized
  return <>{children}</>
}
