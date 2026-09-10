import { Shield, Wifi, Zap, User, Search, Bell, ChevronDown, Menu, X, ArrowUpRight, Radio, FileText, Lock, Globe, LogIn, LogOut } from 'lucide-react'
import { useState, useEffect } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { cn } from '@/lib/utils'
import { api } from '@/lib/api'
import { useAuthStore } from '@/store/authStore'
import { AuthModal } from '@/components/auth/AuthModal'
import { ThemeToggle } from '@/components/layout/ThemeToggle'


const navItems = [
  { path: '/', label: 'Overview' },
  { path: '/report', label: 'Report Incident' },
  { path: '/command', label: 'Command HQ' },
  { path: '/field', label: 'Field Patrol' },
  { path: '/admin', label: 'Telemetry & STM' },
]

export function Topbar() {
  const location = useLocation()
  const navigate = useNavigate()
  const [isSearchOpen, setIsSearchOpen] = useState(false)
  const [isNavModalOpen, setIsNavModalOpen] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [backendStatus, setBackendStatus] = useState<{ connected: boolean; latency: number }>({
    connected: false,
    latency: 12,
  })

  const { user, isAuthenticated, openAuthModal, logout, checkSession } = useAuthStore()

  useEffect(() => {
    checkSession()
  }, [checkSession])


  useEffect(() => {
    let mounted = true
    const check = async () => {
      const h = await api.checkHealth()
      if (mounted) {
        setBackendStatus({ connected: h.is_connected, latency: h.latency_ms })
      }
    }
    check()
    const interval = setInterval(check, 8000)
    return () => {
      mounted = false
      clearInterval(interval)
    }
  }, [])

  // Close nav modal on route change
  useEffect(() => {
    setIsNavModalOpen(false)
    setIsSearchOpen(false)
  }, [location.pathname])

  // Lock body scroll when modal or palette is open
  useEffect(() => {
    if (isNavModalOpen || isSearchOpen) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => {
      document.body.style.overflow = ''
    }
  }, [isNavModalOpen, isSearchOpen])

  // Keyboard shortcut ⌘K
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault()
        setIsSearchOpen((prev) => !prev)
      }
      if (e.key === 'Escape') {
        setIsSearchOpen(false)
        setIsNavModalOpen(false)
        setIsProfileOpen(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-[1600] bg-black/30 backdrop-blur-md border-b border-[#636363]/40">
        <div className="mx-auto max-w-[1440px] px-4 md:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Brand Logo - Palantir Style */}
            <Link to="/" className="flex items-center gap-3 group" aria-label="GAURDIAN Home">
              <div className="w-8 h-8 rounded-sm bg-white flex items-center justify-center text-black font-bold text-xs tracking-tighter group-hover:bg-[#2b5945] group-hover:text-white transition-colors duration-200">
                GD
              </div>
              <div className="flex flex-col">
                <span className="font-sans font-bold text-sm text-white tracking-widest leading-snug">
                  GAURDIAN
                </span>
                <span className="text-[11px] font-mono text-[#9b9b9b] tracking-wider leading-snug">
                  SOVEREIGN DEFENSE
                </span>
              </div>
            </Link>

            {/* Desktop Navigation Links */}
            <nav className="hidden lg:flex items-center gap-6" role="navigation" aria-label="Main navigation">
              {navItems.map(({ path, label }) => {
                const isActive = location.pathname === path
                return (
                  <Link
                    key={path}
                    to={path}
                    className={cn(
                      'text-xs font-sans tracking-wide uppercase transition-colors duration-200 py-1 border-b-2',
                      isActive
                        ? 'text-white border-[#2b5945] font-semibold'
                        : 'text-[#9b9b9b] border-transparent hover:text-white'
                    )}
                  >
                    {label}
                  </Link>
                )
              })}
            </nav>

            {/* Right Side Actions */}
            <div className="flex items-center gap-2.5">
              {/* Live Status Pill */}
              <div className="hidden sm:flex items-center gap-2 px-3 py-1 bg-[#121417] border border-[#636363]/50 rounded-btn text-mono-xs text-[#c0c9c2]">
                <span className={cn('w-1.5 h-1.5 rounded-full', backendStatus.connected ? 'bg-[#38d39f] shadow-[0_0_8px_#38d39f]' : 'bg-[#fae0a6]')} />
                <span className="font-mono text-[11px]">
                  {backendStatus.connected ? `API: LIVE (${backendStatus.latency}ms)` : `GRID: SIM (${backendStatus.latency}ms)`}
                </span>
              </div>

              {/* Primary "File Report" CTA button */}
              <Link
                to="/report"
                className="hidden md:inline-flex items-center justify-center bg-white text-[#121417] hover:bg-black/30 backdrop-blur-md hover:text-white border border-white font-sans font-semibold text-xs px-4 py-2 rounded-btn transition-all duration-200 active:scale-[0.98]"
              >
                File Report
              </Link>

              {/* Search Button (Square Palantir Box) */}
              <button
                onClick={() => setIsSearchOpen(true)}
                className="w-9 h-9 flex items-center justify-center rounded-btn bg-[#121417] border border-[#636363] text-[#c0c9c2] hover:text-white hover:border-white transition-colors"
                aria-label="Open Command Palette (⌘K)"
                title="Search / Command Palette (⌘K)"
              >
                <Search className="w-4 h-4" />
              </button>

              {/* Theme Toggle Button (Dark / Light Mode) */}
              <ThemeToggle />

              {/* Profile or Sign In Button */}
              {isAuthenticated ? (
                <div className="relative">
                  <button
                    onClick={() => setIsProfileOpen(!isProfileOpen)}
                    className="flex items-center gap-2 h-9 px-2.5 rounded-btn bg-[#121417] border border-[#38d39f]/60 text-white hover:border-white transition-colors"
                    aria-label="User Profile"
                  >
                    <span className="w-2 h-2 rounded-full bg-[#38d39f] shadow-[0_0_6px_#38d39f]" />
                    <span className="font-mono text-xs max-w-[100px] truncate hidden sm:inline">
                      {user?.username || 'Officer'}
                    </span>
                    <User className="w-4 h-4 text-[#c0c9c2]" />
                  </button>

                  {isProfileOpen && (
                    <div className="absolute right-0 top-full mt-2 w-72 bg-black/30 backdrop-blur-md border border-[#636363] rounded-card p-4 shadow-floating z-50 animate-in fade-in zoom-in-95 duration-150">
                      <div className="border-b border-[#636363]/40 pb-3 mb-3">
                        <div className="flex items-center justify-between">
                          <p className="font-sans text-sm font-semibold text-white">
                            {user?.username || 'Tactical Officer'}
                          </p>
                          <span className="px-1.5 py-0.5 rounded text-[10px] font-mono bg-[#2b5945] text-[#38d39f]">
                            {user?.role || 'INSPECTOR'}
                          </span>
                        </div>
                        <p className="font-mono text-xs text-[#9b9b9b] truncate">{user?.email}</p>
                        <p className="font-mono text-[11px] text-[#38d39f] font-medium mt-1">
                          ID: {user?.badge_number || 'CC-ACTIVE'} · {user?.station || 'Command HQ'}
                        </p>
                      </div>
                      <div className="space-y-1 text-xs font-sans">
                        <Link
                          to="/command"
                          onClick={() => setIsProfileOpen(false)}
                          className="flex items-center gap-2.5 px-3 py-2 text-[#c0c9c2] hover:text-white hover:bg-[#2f3234] rounded-btn transition-colors"
                        >
                          <Zap className="w-3.5 h-3.5 text-[#2b5945]" />
                          Active Investigation Room
                        </Link>
                        <Link
                          to="/field"
                          onClick={() => setIsProfileOpen(false)}
                          className="flex items-center gap-2.5 px-3 py-2 text-[#c0c9c2] hover:text-white hover:bg-[#2f3234] rounded-btn transition-colors"
                        >
                          <Wifi className="w-3.5 h-3.5 text-[#8c7847]" />
                          Field Intercept Roster
                        </Link>
                        <Link
                          to="/admin"
                          onClick={() => setIsProfileOpen(false)}
                          className="flex items-center gap-2.5 px-3 py-2 text-[#c0c9c2] hover:text-white hover:bg-[#2f3234] rounded-btn transition-colors"
                        >
                          <Shield className="w-3.5 h-3.5 text-blue-400" />
                          Station Audit Logs
                        </Link>
                        <hr className="border-[#636363]/40 my-1" />
                        <button
                          onClick={() => {
                            setIsProfileOpen(false)
                            logout()
                          }}
                          className="w-full flex items-center gap-2.5 px-3 py-2 text-red-400 hover:text-red-300 hover:bg-red-950/30 rounded-btn transition-colors text-left"
                        >
                          <LogOut className="w-3.5 h-3.5" />
                          Sign Out Session
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                <div className="flex items-center gap-1.5">
                  <button
                    onClick={() => openAuthModal('signin')}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-btn bg-[#171a1e] hover:bg-[#2b5945] text-[#c0c9c2] hover:text-white border border-[#636363]/60 hover:border-[#38d39f] font-sans font-semibold text-xs transition-all duration-200"
                  >
                    <LogIn className="w-3.5 h-3.5" />
                    <span>Sign In</span>
                  </button>
                  <button
                    onClick={() => openAuthModal('signup')}
                    className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-btn bg-[#2b5945] hover:bg-[#38d39f] text-white hover:text-black font-sans font-semibold text-xs transition-all duration-200"
                  >
                    <span>Register</span>
                  </button>
                </div>
              )}


              {/* Hamburger / Navigation Launchpad Trigger (Palantir Square Box) */}
              <button
                onClick={() => setIsNavModalOpen(!isNavModalOpen)}
                className="w-9 h-9 flex items-center justify-center rounded-btn bg-[#121417] border border-[#636363] text-white hover:border-white transition-colors"
                aria-label={isNavModalOpen ? 'Close Navigation' : 'Open Navigation'}
              >
                {isNavModalOpen ? <X className="w-4 h-4" /> : <Menu className="w-4 h-4" />}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Full-Screen Navigation Launchpad Modal - Exact Palantir Pattern */}
      {isNavModalOpen && (
        <div className="fixed inset-0 z-[1500] bg-black/30 backdrop-blur-md pt-20 px-4 md:px-12 pb-12 overflow-y-auto animate-in fade-in duration-200">
          <div className="mx-auto max-w-[1400px] h-full flex flex-col justify-between">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 py-8">
              {/* Column 1: Sovereign Navigation with ↳ right-angle arrows */}
              <div className="lg:col-span-4 border-b lg:border-b-0 lg:border-r border-[#636363]/30 pb-8 lg:pb-0 lg:pr-8">
                <p className="text-[11px] font-mono tracking-widest text-[#9b9b9b] uppercase mb-6">
                  Sovereign Platforms
                </p>
                <div className="space-y-4">
                  <div>
                    <Link
                      to="/"
                      className="text-2xl font-bold font-sans text-white hover:text-[#2b5945] transition-colors flex items-center justify-between"
                    >
                      GAURDIAN Gateway
                      <ArrowUpRight className="w-5 h-5 text-[#9b9b9b]" />
                    </Link>
                    <p className="text-xs text-[#9b9b9b] mt-1">National financial cyber defense grid</p>
                  </div>

                  <div className="pl-3 border-l border-[#636363]/40 space-y-3 pt-2">
                    <Link
                      to="/report"
                      className="group flex items-center gap-2 text-base font-medium text-[#c0c9c2] hover:text-white transition-colors"
                    >
                      <span className="text-[#38d39f] group-hover:translate-x-1 transition-transform">↳</span>
                      Citizen Reporting Portal (1930 Sync)
                    </Link>

                    <Link
                      to="/command"
                      className="group flex items-center gap-2 text-base font-medium text-[#c0c9c2] hover:text-white transition-colors"
                    >
                      <span className="text-[#38d39f] group-hover:translate-x-1 transition-transform">↳</span>
                      Tactical Command HQ & Mule Ontology
                    </Link>

                    <Link
                      to="/field"
                      className="group flex items-center gap-2 text-base font-medium text-[#c0c9c2] hover:text-white transition-colors"
                    >
                      <span className="text-[#38d39f] group-hover:translate-x-1 transition-transform">↳</span>
                      Field Patrol & ATM Intercept PWA
                    </Link>

                    <Link
                      to="/admin"
                      className="group flex items-center gap-2 text-base font-medium text-[#c0c9c2] hover:text-white transition-colors"
                    >
                      <span className="text-[#38d39f] group-hover:translate-x-1 transition-transform">↳</span>
                      Telemetry, STM & AI Roster
                    </Link>
                  </div>
                </div>

                <div className="mt-8 pt-6 border-t border-[#636363]/30">
                  <p className="text-[11px] font-mono tracking-widest text-[#9b9b9b] uppercase mb-3">
                    Statutory Protocols
                  </p>
                  <ul className="space-y-2 text-xs font-mono text-[#c0c9c2]">
                    <li>→ Section 91 CrPC Automated Notice Engine</li>
                    <li>→ NPCI Immediate Payment Reverse Freeze</li>
                    <li>→ Telecom KYC IMEI/IMSI Blacklist API</li>
                  </ul>
                </div>
              </div>

              {/* Column 2: Intelligence Briefs Cards */}
              <div className="lg:col-span-5 border-b lg:border-b-0 lg:border-r border-[#636363]/30 pb-8 lg:pb-0 lg:pr-8">
                <p className="text-[11px] font-mono tracking-widest text-[#9b9b9b] uppercase mb-6">
                  Real-time Intelligence
                </p>
                <div className="space-y-4">
                  <div className="p-4 bg-[#121417] border border-[#636363] rounded-card hover:border-white transition-colors">
                    <div className="flex items-center justify-between text-[11px] font-mono text-[#9b9b9b] mb-2">
                      <span className="text-[#fae0a6]">INTELLIGENCE REPORT / 2026.09</span>
                      <span>INDIRANAGAR SECTOR 4</span>
                    </div>
                    <h4 className="text-sm font-semibold text-white mb-2">
                      3-Layer Mule Ring Intercepted: ₹4.8 Lakhs Preserved at HAL 2nd Stage ATM
                    </h4>
                    <p className="text-xs text-[#9b9b9b] line-clamp-2">
                      Tactical patrol squad dispatched within 210 seconds of OTP-less cyber reporting. Mule runner apprehended prior to cash withdrawal.
                    </p>
                    <div className="mt-3 flex items-center justify-between">
                      <Link to="/command" className="text-xs font-mono text-[#38d39f] hover:text-white">
                        ↳ Open Investigation Graph
                      </Link>
                      <span className="text-[11px] font-mono px-2 py-0.5 rounded-pill bg-[#2b5945]/20 text-[#a0d1b8] border border-[#2b5945]">
                        FROZEN
                      </span>
                    </div>
                  </div>

                  <div className="p-4 bg-[#121417] border border-[#636363] rounded-card hover:border-white transition-colors">
                    <div className="flex items-center justify-between text-[11px] font-mono text-[#9b9b9b] mb-2">
                      <span className="text-[#a0d1b8]">ALGORITHM METRIC</span>
                      <span>STM V4.2 ACTIVE</span>
                    </div>
                    <h4 className="text-sm font-semibold text-white mb-2">
                      Spatio-Temporal Model Accuracy: 94.2% on First-Hop Destination Prediction
                    </h4>
                    <p className="text-xs text-[#9b9b9b] line-clamp-2">
                      Autonomous graph neural network predicts withdrawal cluster radius with average geolocation error under 350 meters.
                    </p>
                    <div className="mt-3 flex items-center justify-between">
                      <Link to="/admin" className="text-xs font-mono text-[#38d39f] hover:text-white">
                        ↳ Review Telemetry
                      </Link>
                      <span className="text-[11px] font-mono text-[#9b9b9b]">UPDATED 2M AGO</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Column 3: Capabilities & Quick Protocols */}
              <div className="lg:col-span-3 flex flex-col justify-between">
                <div>
                  <p className="text-[11px] font-mono tracking-widest text-[#9b9b9b] uppercase mb-6">
                    Quick Directives
                  </p>
                  <div className="space-y-3">
                    <Link
                      to="/report"
                      className="block p-3 bg-[#121417] border border-[#636363]/50 rounded-card hover:border-[#2b5945] transition-colors"
                    >
                      <span className="text-xs font-semibold text-white block">Emergency Incident Intake</span>
                      <span className="text-[11px] text-[#9b9b9b]">Generate citizen case ID in &lt; 90s</span>
                    </Link>

                    <Link
                      to="/command"
                      className="block p-3 bg-[#121417] border border-[#636363]/50 rounded-card hover:border-[#2b5945] transition-colors"
                    >
                      <span className="text-xs font-semibold text-white block">Universal NPCI Freeze Protocol</span>
                      <span className="text-[11px] text-[#9b9b9b]">Broadcast stop-payment to all 12 hops</span>
                    </Link>

                    <Link
                      to="/field"
                      className="block p-3 bg-[#121417] border border-[#636363]/50 rounded-card hover:border-[#2b5945] transition-colors"
                    >
                      <span className="text-xs font-semibold text-white block">Dispatch Nearest Patrol Unit</span>
                      <span className="text-[11px] text-[#9b9b9b]">Haptic confirmation with GPS telemetry</span>
                    </Link>
                  </div>
                </div>

                <div className="pt-8 border-t border-[#636363]/30 flex items-center justify-between">
                  <div className="text-[11px] font-mono text-[#9b9b9b] space-y-1">
                    <p>© 2026 GAURDIAN / CHOCO DEFENSE</p>
                    <p>Designed on Palantir Architectural Principles</p>
                  </div>
                  <ThemeToggle showLabel />
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Command Palette Overlay */}
      {isSearchOpen && (
        <div
          className="fixed inset-0 z-[1700] bg-black/30 backdrop-blur-md/80 backdrop-blur-sm flex items-start justify-center pt-24 px-4 animate-in fade-in duration-150"
          onClick={() => setIsSearchOpen(false)}
        >
          <div
            className="w-full max-w-2xl bg-black/30 backdrop-blur-md border border-[#636363] rounded-card p-4 shadow-floating animate-in slide-in-from-top-4 duration-200 text-white"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-[#9b9b9b]" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search commands, navigate routes, trigger protocols... (Esc to exit)"
                className="w-full bg-[#121417] border border-[#636363] rounded-btn pl-11 pr-14 py-2.5 text-sm text-white placeholder:text-[#9b9b9b] focus:outline-none focus:border-[#2b5945]"
                autoFocus
              />
              <kbd className="absolute right-3.5 top-1/2 -translate-y-1/2 px-2 py-0.5 bg-black/40 backdrop-blur-sm border border-[#636363] rounded text-mono-xs text-[#9b9b9b] font-mono">
                ESC
              </kbd>
            </div>

            <div className="mt-4 space-y-1">
              <p className="text-[11px] font-mono tracking-wider text-[#9b9b9b] uppercase px-3 py-1">
                Navigation Targets
              </p>
              {navItems.map(({ path, label }) => (
                <button
                  key={path}
                  onClick={() => {
                    navigate(path)
                    setIsSearchOpen(false)
                  }}
                  className="w-full flex items-center justify-between px-3 py-2 rounded-btn text-xs font-sans text-[#c0c9c2] hover:text-white hover:bg-[#2f3234] transition-colors text-left"
                >
                  <span className="font-medium">{label}</span>
                  <span className="font-mono text-[11px] text-[#9b9b9b]">{path}</span>
                </button>
              ))}

              <hr className="border-[#636363]/40 my-2" />

              <p className="text-[11px] font-mono tracking-wider text-[#9b9b9b] uppercase px-3 py-1">
                Emergency Directives
              </p>
              <button
                onClick={() => {
                  navigate('/command')
                  setIsSearchOpen(false)
                }}
                className="w-full flex items-center justify-between px-3 py-2 rounded-btn text-xs font-sans text-[#ff7066] hover:bg-[#994500]/20 transition-colors text-left"
              >
                <span className="font-medium">Trigger Universal Freeze Directive (NPCI)</span>
                <span className="font-mono text-[11px] px-1.5 py-0.5 rounded bg-[#994500]/40 text-white">EMERGENCY</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Global Sovereign Auth Modal */}
      <AuthModal />
    </>
  )
}