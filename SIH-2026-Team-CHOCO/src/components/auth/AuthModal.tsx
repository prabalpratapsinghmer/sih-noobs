import React, { useState } from 'react'
import {
  X,
  Shield,
  Lock,
  Mail,
  User,
  Eye,
  EyeOff,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Building,
  KeyRound,
  Sparkles,
} from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { cn } from '@/lib/utils'
import { useNavigate } from 'react-router-dom'
import { GoogleLogin } from '@/components/auth/GoogleLogin'

export const AuthModal: React.FC = () => {
  const navigate = useNavigate()
  const {
    isAuthModalOpen,
    authModalMode,
    authMessage,
    redirectPath,
    setRedirectPath,
    openAuthModal,
    closeAuthModal,
    login,
    signup,
    loginWithGoogle,
    isLoading,
    error,
  } = useAuthStore()

  const [showPassword, setShowPassword] = useState(false)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Sign In state
  const [loginIdentifier, setLoginIdentifier] = useState('')
  const [loginPassword, setLoginPassword] = useState('')

  // Sign Up state
  const [signupFullName, setSignupFullName] = useState('')
  const [signupUsername, setSignupUsername] = useState('')
  const [signupEmail, setSignupEmail] = useState('')
  const [signupPassword, setSignupPassword] = useState('')
  const [signupRole, setSignupRole] = useState('INSPECTOR')
  const [signupStation, setSignupStation] = useState('Bengaluru Central Command')

  if (!isAuthModalOpen) return null

  const handleSuccessRedirect = () => {
    if (redirectPath) {
      navigate(redirectPath)
      setRedirectPath(null)
    }
  }

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSuccessMessage(null)
    const res = await login(loginIdentifier, loginPassword)
    if (res.success) {
      setSuccessMessage('Authentication verified. Welcome back to GAURDIAN Command.')
      setTimeout(() => {
        closeAuthModal()
        setSuccessMessage(null)
        handleSuccessRedirect()
      }, 900)
    }
  }


  const handleSignupSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSuccessMessage(null)
    const res = await signup({
      username: signupUsername,
      email: signupEmail,
      password: signupPassword,
      full_name: signupFullName,
      role: signupRole,
      station: signupStation,
    })
    if (res.success) {
      setSuccessMessage('Sovereign account provisioned and synchronized with Supabase.')
      setTimeout(() => {
        closeAuthModal()
        setSuccessMessage(null)
      }, 1200)
    }
  }



  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-black/80 backdrop-blur-md animate-in fade-in duration-200">
      <div
        className="relative w-full max-w-lg bg-[#0e1013] border border-[#636363]/60 rounded-card shadow-2xl overflow-hidden"
        role="dialog"
        aria-modal="true"
      >
        {/* Top Header Bar */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-[#636363]/40 bg-[#14171b]">
          <div className="flex items-center gap-3">
            <div className="w-7 h-7 rounded-sm bg-white text-black font-bold flex items-center justify-center text-xs">
              GD
            </div>
            <div>
              <h2 className="font-sans font-bold text-sm text-white tracking-wider">
                SOVEREIGN IDENTITY ACCESS
              </h2>
              <p className="font-mono text-[10px] text-[#9b9b9b] uppercase tracking-wider">
                PostgreSQL · Redis Cache · Supabase GoTrue
              </p>
            </div>
          </div>
          <button
            onClick={closeAuthModal}
            className="w-8 h-8 rounded-btn bg-[#1e2124] border border-[#636363]/40 text-[#c0c9c2] hover:text-white hover:border-white flex items-center justify-center transition-colors"
            aria-label="Close dialog"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Tab Selector */}
        <div className="grid grid-cols-2 border-b border-[#636363]/40 bg-[#121417]">
          <button
            onClick={() => openAuthModal('signin')}
            className={cn(
              'py-3 text-xs font-mono tracking-wider uppercase transition-all duration-150 border-b-2 font-semibold',
              authModalMode === 'signin'
                ? 'text-white border-[#38d39f] bg-[#1a1e22]'
                : 'text-[#9b9b9b] border-transparent hover:text-white hover:bg-[#16181b]'
            )}
          >
            Sign In
          </button>
          <button
            onClick={() => openAuthModal('signup')}
            className={cn(
              'py-3 text-xs font-mono tracking-wider uppercase transition-all duration-150 border-b-2 font-semibold',
              authModalMode === 'signup'
                ? 'text-white border-[#38d39f] bg-[#1a1e22]'
                : 'text-[#9b9b9b] border-transparent hover:text-white hover:bg-[#16181b]'
            )}
          >
            Create Account
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-5 max-h-[80vh] overflow-y-auto">
          {/* Target Clearance Context Message */}
          {authMessage && (
            <div className="flex items-center gap-2.5 p-3 rounded-card bg-[#2b5945]/25 border border-[#38d39f]/50 text-[#a0d1b8] text-xs animate-in fade-in">
              <KeyRound className="w-4 h-4 text-[#38d39f] shrink-0" />
              <span>{authMessage}</span>
            </div>
          )}

          {/* Direct Google Sign-In Button */}
          <div>
            <GoogleLogin onSuccess={() => setSuccessMessage('Google ID Verified. Session active.')} />

            <div className="relative my-4">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-[#636363]/40" />
              </div>
              <div className="relative flex justify-center text-[10px] uppercase font-mono">
                <span className="bg-[#0e1013] px-3 text-[#9b9b9b] tracking-widest">
                  or authenticate with credentials
                </span>
              </div>
            </div>
          </div>

          {/* Feedback Alerts */}
          {error && (
            <div className="flex items-center gap-2.5 p-3 rounded-card bg-red-950/40 border border-red-800/60 text-red-300 text-xs animate-in fade-in">
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {successMessage && (
            <div className="flex items-center gap-2.5 p-3 rounded-card bg-emerald-950/40 border border-emerald-800/60 text-emerald-300 text-xs animate-in fade-in">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              <span>{successMessage}</span>
            </div>
          )}

          {/* Forms */}
          {authModalMode === 'signin' ? (
            /* SIGN IN FORM */
            <form onSubmit={handleLoginSubmit} className="space-y-4">
              <div className="space-y-1.5">
                <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                  Username or Official Email
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#9b9b9b]">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    required
                    value={loginIdentifier}
                    onChange={(e) => setLoginIdentifier(e.target.value)}
                    placeholder="e.g. vikramaditya or officer@cybercell.gov.in"
                    className="w-full pl-9 pr-3 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs placeholder-[#636363] focus:outline-none focus:border-[#38d39f] font-mono transition-colors"
                  />
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#9b9b9b]">
                    <Lock className="w-4 h-4" />
                  </div>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={loginPassword}
                    onChange={(e) => setLoginPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full pl-9 pr-10 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs placeholder-[#636363] focus:outline-none focus:border-[#38d39f] font-mono transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-[#9b9b9b] hover:text-white"
                  >
                    {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-2 py-2.5 px-4 rounded-btn bg-[#2b5945] hover:bg-[#346b53] border border-[#38d39f]/50 text-white font-sans font-semibold text-xs tracking-wider flex items-center justify-center gap-2 transition-all duration-200 active:scale-[0.99] disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>VERIFYING CREDENTIALS...</span>
                  </>
                ) : (
                  <>
                    <KeyRound className="w-4 h-4" />
                    <span>AUTHENTICATE SESSION ↳</span>
                  </>
                )}
              </button>
            </form>
          ) : (

            /* SIGN UP FORM */
            <form onSubmit={handleSignupSubmit} className="space-y-3.5">
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1">
                  <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                    Full Name
                  </label>
                  <input
                    type="text"
                    required
                    value={signupFullName}
                    onChange={(e) => setSignupFullName(e.target.value)}
                    placeholder="Insp. Arjun Mehta"
                    className="w-full px-3 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs placeholder-[#636363] focus:outline-none focus:border-[#38d39f] font-sans transition-colors"
                  />
                </div>

                <div className="space-y-1">
                  <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                    Username
                  </label>
                  <input
                    type="text"
                    required
                    value={signupUsername}
                    onChange={(e) => setSignupUsername(e.target.value)}
                    placeholder="arjun_mehta"
                    className="w-full px-3 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs placeholder-[#636363] focus:outline-none focus:border-[#38d39f] font-mono transition-colors"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                  Official Email Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#9b9b9b]">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="email"
                    required
                    value={signupEmail}
                    onChange={(e) => setSignupEmail(e.target.value)}
                    placeholder="arjun@police.gov.in"
                    className="w-full pl-9 pr-3 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs placeholder-[#636363] focus:outline-none focus:border-[#38d39f] font-mono transition-colors"
                  />
                </div>
              </div>

              <div className="space-y-1">
                <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                  Password (min 6 characters)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-[#9b9b9b]">
                    <Lock className="w-4 h-4" />
                  </div>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    minLength={6}
                    value={signupPassword}
                    onChange={(e) => setSignupPassword(e.target.value)}
                    placeholder="••••••••••••"
                    className="w-full pl-9 pr-10 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs placeholder-[#636363] focus:outline-none focus:border-[#38d39f] font-mono transition-colors"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center text-[#9b9b9b] hover:text-white"
                  >
                    {showPassword ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3 pt-1">
                <div className="space-y-1">
                  <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                    Assigned Role
                  </label>
                  <select
                    value={signupRole}
                    onChange={(e) => setSignupRole(e.target.value)}
                    className="w-full px-3 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs focus:outline-none focus:border-[#38d39f] font-mono cursor-pointer"
                  >
                    <option value="INSPECTOR">INSPECTOR (Tactical)</option>
                    <option value="CONSTABLE">CONSTABLE (Field Squad)</option>
                    <option value="CITIZEN">CITIZEN (Public Reporting)</option>
                    <option value="ADMIN">ADMIN (Central HQ)</option>
                  </select>
                </div>

                <div className="space-y-1">
                  <label className="block text-[11px] font-mono uppercase text-[#c0c9c2] tracking-wider">
                    Station / Division
                  </label>
                  <input
                    type="text"
                    value={signupStation}
                    onChange={(e) => setSignupStation(e.target.value)}
                    placeholder="e.g. Koramangala Squad"
                    className="w-full px-3 py-2 bg-[#171a1e] border border-[#636363]/60 rounded-btn text-white text-xs placeholder-[#636363] focus:outline-none focus:border-[#38d39f] font-sans transition-colors"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full mt-3 py-2.5 px-4 rounded-btn bg-[#2b5945] hover:bg-[#346b53] border border-[#38d39f]/50 text-white font-sans font-semibold text-xs tracking-wider flex items-center justify-center gap-2 transition-all duration-200 active:scale-[0.99] disabled:opacity-50"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>CREATING SOVEREIGN ACCOUNT...</span>
                  </>
                ) : (
                  <>
                    <Shield className="w-4 h-4" />
                    <span>INITIALIZE SOVEREIGN ACCOUNT ↳</span>
                  </>
                )}
              </button>
            </form>
          )}

          {/* Bottom Security Assurance */}
          <div className="pt-2 border-t border-[#636363]/30 flex items-center justify-between text-[11px] text-[#9b9b9b] font-mono">
            <span className="flex items-center gap-1.5">
              <Shield className="w-3 h-3 text-[#38d39f]" />
              256-bit AES · Supabase PII Encrypted
            </span>
            <button
              onClick={() => openAuthModal(authModalMode === 'signin' ? 'signup' : 'signin')}
              className="text-[#38d39f] hover:underline"
            >
              {authModalMode === 'signin' ? 'Need an account? Register' : 'Already registered? Sign In'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
