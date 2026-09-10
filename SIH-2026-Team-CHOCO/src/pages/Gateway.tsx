import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import {
  Shield,
  Zap,
  Target,
  TrendingUp,
  Clock,
  CheckCircle2,
  ExternalLink,
  ArrowRight,
  Radio,
  FileText,
  Activity,
  Layers,
  ChevronRight,
  Lock,
  Globe,
  Database,
  Search,
  UserCheck,
  KeyRound,
} from 'lucide-react'
import { formatCompactINR, cn } from '@/lib/utils'
import { useAuthStore } from '@/store/authStore'
import { StatutoryModal } from '@/components/ui/StatutoryModal'


// Category Pills per Palantir cardSelector
const categories = [
  { id: 'all', label: 'All Capabilities' },
  { id: 'ontology', label: 'Mule Ring Ontology' },
  { id: 'intercept', label: 'ATM Cash-Out Radar' },
  { id: 'freeze', label: 'Universal NPCI Freeze' },
  { id: 'copilot', label: 'Section 91 Copilot' },
  { id: 'citizen', label: 'Citizen Incident Intake' },
]

// Feature Showcase Cards
const featureCards = [
  {
    id: 'c1',
    category: 'citizen',
    index: '/0.1',
    title: 'Citizen Rapid Incident Intake & Evidence Vault',
    subtitle: '1930 & National Portal Instant Synchronization',
    description:
      '4-step verified reporting wizard for fraud victims. Captures transaction UTR numbers, account chains, and digital screenshots in under 90 seconds. Instantly generates tamper-proof case manifest CC-2026-XXXX.',
    path: '/report',
    badge: 'PUBLIC SECTOR',
    ctaText: '↳ File Incident Report',
    meta: 'LATENCY < 90 SECONDS · AUTO-OTP · WHATSAPP DISPATCH',
  },
  {
    id: 'c2',
    category: 'ontology',
    index: '/0.2',
    title: 'Mule Ring Ontology & Dynamic Graph Neural Network',
    subtitle: 'Deep Multi-Hop Transaction Graph Decomposition',
    description:
      'Traces compromised funds across 3+ mule tiers in real-time. High-dimensional graph models isolate shell accounts, dormant current accounts, and synthetic UPI handles before cash withdrawal.',
    path: '/command',
    badge: 'TACTICAL INTELLIGENCE',
    ctaText: '↳ Launch Investigation Room',
    meta: 'MULTI-HOP RECONSTRUCTION · 94.2% ACCURACY · XYFLOW ENGINE',
  },
  {
    id: 'c3',
    category: 'intercept',
    index: '/0.3',
    title: 'ATM Cash-Out Radar & Spatio-Temporal Prediction',
    subtitle: 'Nearest ATM Cluster geofencing & dispatch route',
    description:
      'Predicts physical withdrawal coordinates with sub-350m radius based on past mule syndication patterns. Dispatches nearest mobile field patrol squad with automated turn-by-turn routing.',
    path: '/field',
    badge: 'FIELD OPERATIONS',
    ctaText: '↳ Open Field Patrol Console',
    meta: 'GEOLOCATION ERROR < 350M · TURN-BY-TURN · AUDIO CHIME',
  },
  {
    id: 'c4',
    category: 'freeze',
    index: '/0.4',
    title: 'Universal NPCI Instant Multi-Hop Freeze Directive',
    subtitle: 'One-Click Autonomous Settlement Freezing',
    description:
      'Synchronous API trigger broadcast to 42 schedule commercial banks and payment intermediaries. Freezes downstream mule balances before funds reach crypto off-ramps or hawala brokers.',
    path: '/command',
    badge: 'STATUTORY AUTOMATION',
    ctaText: '↳ Trigger Mock Freeze Protocol',
    meta: '12 CONCURRENT HOPS · NPCI ADAPTER · 6-MINUTE WINDOW',
  },
  {
    id: 'c5',
    category: 'copilot',
    index: '/0.5',
    title: 'AI Investigator Copilot & Section 91 CrPC Drafter',
    subtitle: 'Legal Notice Generation & UPI Reverse Discovery',
    description:
      'Domain-adapted legal reasoning agent drafting high-fidelity Section 91 CrPC notice templates for bank nodal officers and ISP IP disclosure requests in strictly under 10 seconds.',
    path: '/command',
    badge: 'GOVERNANCE AI',
    ctaText: '↳ Consult Tactical Copilot',
    meta: 'INDIAN PENAL CODE & BNS COMPLIANT · DIGITAL SIGNATURE READY',
  },
  {
    id: 'c6',
    category: 'ontology',
    index: '/0.6',
    title: 'Station Telemetry, STM Drift & Model Governance',
    subtitle: 'Institutional Audit Logs & Cross-Jurisdiction Metrics',
    description:
      'Real-time supervisory telemetry tracking station response times, algorithm precision drift, nodal officer SLA compliance, and cross-state cybercrime syndication heatmaps.',
    path: '/admin',
    badge: 'SUPERVISORY',
    ctaText: '↳ Access Telemetry Console',
    meta: 'END-TO-END AUDIT TRAIL · STM MONITORING · STATE HEATMAPS',
  },
]

export function Gateway() {
  const [activeCategory, setActiveCategory] = useState('all')
  const [selectedPolicyDoc, setSelectedPolicyDoc] = useState<string | null>(null)
  const navigate = useNavigate()
  const { isAuthenticated, hasClearance, openAuthModalWithPrompt } = useAuthStore()

  const handleProtectedClick = (
    e: React.MouseEvent,
    path: string,
    allowedRoles: string[],
    title: string
  ) => {
    e.preventDefault()
    if (!isAuthenticated) {
      openAuthModalWithPrompt(
        `Authentication Required: Please sign in with authorized credentials to access ${title}.`,
        path
      )
      return
    }
    navigate(path)
  }

  const getCardRoles = (path: string) => {
    if (path === '/command') return ['COMMAND_HQ']
    if (path === '/field') return ['POLICE', 'CONSTABLE', 'COMMAND_HQ']
    if (path === '/admin') return ['COMMAND_HQ']
    return ['COMMAND_HQ', 'POLICE', 'CONSTABLE', 'CITIZEN']
  }

  const filteredCards =
    activeCategory === 'all'
      ? featureCards
      : featureCards.filter((c) => c.category === activeCategory)


  return (
    <div className="min-h-screen bg-[#1e2124] text-white">
      {/* Top Technical Metadata Ticker Bar */}
      <div className="pt-20 pb-4 px-4 md:px-12 border-b border-[#636363]/30 bg-[#121417]/80">
        <div className="mx-auto max-w-[1440px] flex flex-wrap items-center justify-between gap-4 text-xs font-mono text-[#9b9b9b]">
          <div className="flex items-center gap-3">
            <span className="inline-flex items-center gap-1.5 text-white font-semibold">
              <span className="w-1.5 h-1.5 rounded-full bg-[#a0d1b8]" />
              SOVEREIGN DEFENSE GRID 2026
            </span>
            <span className="text-[#636363]">/</span>
            <span>BUILT ON: → GAURDIAN ONTOLOGY → MULE GRAPH → REAL-TIME NPCI INTERCEPT</span>
          </div>
          <div className="flex items-center gap-6">
            <span className="hidden sm:inline">STATE OF OPERATIONAL READINESS: 100%</span>
            <span className="text-[#a0d1b8] bg-[#2b5945]/25 border border-[#2b5945] px-2 py-0.5 rounded-btn font-medium">
              NATIONAL PROTOCOL ACTIVE
            </span>
          </div>
        </div>
      </div>

      {/* Hero Section - Palantir Cinematic Dark Style */}
      <section className="relative pt-16 pb-20 lg:pt-28 lg:pb-32 px-4 md:px-12 overflow-hidden">
        {/* Subtle grid pattern background */}
        <div
          className="absolute inset-0 opacity-[0.03] pointer-events-none"
          style={{
            backgroundImage: `radial-gradient(#ffffff 1px, transparent 1px)`,
            backgroundSize: '32px 32px',
          }}
        />

        <div className="relative mx-auto max-w-[1440px]">
          <div className="max-w-4xl">
            {/* Tagline */}
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-[#121417] border border-[#636363]/60 rounded-btn mb-8">
              <Shield className="w-3.5 h-3.5 text-[#2b5945]" />
              <span className="font-mono text-xs tracking-wide text-[#c0c9c2]">
                National Cybercrime Intercept & Asset Preservation Grid
              </span>
            </div>

            {/* Display Headline */}
            <h1 className="text-display-2xl font-bold font-sans text-white tracking-tight leading-[1.4] mb-8">
              Sovereign Cyber Defense
              <br />
              <span className="text-[#a0a0a0]">For Every Threat Vector.</span>
            </h1>

            {/* Subtitle */}
            <p className="text-body-lg md:text-xl text-[#c0c9c2] font-normal leading-relaxed max-w-2xl mb-10">
              When financial cybercrime strikes, the first six minutes determine asset recovery.
              GAURDIAN integrates citizen intake, mule graph decomposition, and physical ATM intercept into a single, unified operational loop.
            </p>

            {/* Action Buttons - Palantir High Contrast Invert Style with Clearance Gateways */}
            <div className="flex flex-wrap items-center gap-4 pt-2">
              <button
                onClick={(e) =>
                  handleProtectedClick(
                    e,
                    '/report',
                    ['COMMAND_HQ', 'POLICE', 'CONSTABLE', 'CITIZEN'],
                    'Incident Reporting Portal'
                  )
                }
                className="inline-flex items-center justify-center bg-white text-[#121417] hover:bg-[#000000] hover:text-white border border-white font-sans font-semibold text-sm px-6 py-3 rounded-btn transition-all duration-200 active:scale-[0.98]"
              >
                File Emergency Report
                <ArrowRight className="w-4 h-4 ml-2" />
              </button>
              <button
                onClick={(e) =>
                  handleProtectedClick(
                    e,
                    '/command',
                    ['COMMAND_HQ'],
                    'Tactical Command HQ & Mule Graph'
                  )
                }
                className="inline-flex items-center justify-center bg-[#000000] text-white border border-[#636363] hover:border-white font-sans font-medium text-sm px-6 py-3 rounded-btn transition-all duration-200 active:scale-[0.98]"
              >
                Launch Tactical Command
              </button>
              <button
                onClick={(e) =>
                  handleProtectedClick(
                    e,
                    '/field',
                    ['POLICE', 'CONSTABLE', 'COMMAND_HQ'],
                    'Field Patrol Console & ATM Radar'
                  )
                }
                className="inline-flex items-center justify-center bg-transparent text-[#9b9b9b] hover:text-white font-sans font-medium text-sm px-4 py-3 transition-colors"
              >
                Field Patrol Console ↳
              </button>
            </div>
          </div>
        </div>
      </section>



      {/* Numerical Telemetry Metrics Strip */}
      <section className="border-y border-[#636363]/40 bg-[#000000] py-8 px-4 md:px-12">
        <div className="mx-auto max-w-[1440px]">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 lg:gap-8">
            <div className="border-l border-[#636363]/40 pl-4 sm:pl-6">
              <div className="font-mono text-xs text-[#9b9b9b] tracking-wider mb-1">
                /0.1 Total Funds Preserved
              </div>
              <div className="font-mono text-2xl sm:text-3xl font-bold text-white tabular-nums" style={{ lineHeight: 1.4 }}>
                {formatCompactINR(82490000)}
              </div>
              <p className="text-xs text-[#a0d1b8] font-mono mt-1">↑ 14.8% over previous cycle</p>
            </div>

            <div className="border-l border-[#636363]/40 pl-4 sm:pl-6">
              <div className="font-mono text-xs text-[#9b9b9b] tracking-wider mb-1">
                /0.2 Active Mule Intercepts
              </div>
              <div className="font-mono text-2xl sm:text-3xl font-bold text-[#fae0a6] tabular-nums" style={{ lineHeight: 1.4 }}>
                47 SYNDICATES
              </div>
              <p className="text-xs text-[#9b9b9b] font-mono mt-1">12 concurrent bank pipelines</p>
            </div>

            <div className="border-l border-[#636363]/40 pl-4 sm:pl-6">
              <div className="font-mono text-xs text-[#9b9b9b] tracking-wider mb-1">
                /0.3 Golden-Window Latency
              </div>
              <div className="font-mono text-2xl sm:text-3xl font-bold text-white tabular-nums" style={{ lineHeight: 1.4 }}>
                3m 42s
              </div>
              <p className="text-xs text-[#a0d1b8] font-mono mt-1">Benchmark target: &lt; 6m 00s</p>
            </div>

            <div className="border-l border-[#636363]/40 pl-4 sm:pl-6">
              <div className="font-mono text-xs text-[#9b9b9b] tracking-wider mb-1">
                /0.4 Prediction Precision
              </div>
              <div className="font-mono text-2xl sm:text-3xl font-bold text-white tabular-nums" style={{ lineHeight: 1.4 }}>
                94.2%
              </div>
              <p className="text-xs text-[#9b9b9b] font-mono mt-1">Spatio-Temporal Model v4.2</p>
            </div>
          </div>
        </div>
      </section>

      {/* Statement Highlight Section - Direct Palantir Typography Motif */}
      <section className="py-20 lg:py-32 px-4 md:px-12 bg-[#121417]/50 border-b border-[#636363]/30">
        <div className="mx-auto max-w-[1440px]">
          <div className="max-w-4xl">
            <div className="font-mono text-xs tracking-wider uppercase text-[#9b9b9b] mb-6">
              OPERATIONAL THESIS
            </div>
            <blockquote className="text-2xl sm:text-3xl md:text-4xl font-sans font-medium text-white leading-relaxed">
              "Our software powers real-time,{' '}
              <span className="text-[#a0a0a0] font-normal">AI-driven asset preservation</span> across
              India's financial infrastructure, connecting citizen complaints with law enforcement
              field dispatch within the critical{' '}
              <span className="text-[#a0d1b8] font-semibold underline decoration-[#a0d1b8]/40 underline-offset-8">
                six-minute golden window
              </span>
              ."
            </blockquote>
            <div className="mt-8 flex items-center gap-4 text-xs font-mono text-[#9b9b9b]">
              <span className="text-white font-semibold">DIRECTORATE OF CYBER INTELLIGENCE</span>
              <span>—</span>
              <span>NATIONAL I4C ALLIANCE SPECIFICATION</span>
            </div>
          </div>
        </div>
      </section>

      {/* Category Pills Bar & Interactive Feature Grid (Palantir cardSelector pattern) */}
      <section className="py-20 lg:py-28 px-4 md:px-12">
        <div className="mx-auto max-w-[1440px]">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-6">
            <div>
              <h2 className="text-display-lg font-bold font-sans text-white">
                Architected for High-Stakes Operations
              </h2>
            </div>
            <p className="text-xs font-mono text-[#9b9b9b] max-w-sm">
              Explore interconnected nodes across reporting, intelligence decomposition, legal sanction, and tactical patrol dispatch.
            </p>
          </div>

          {/* Category Selector Pills Bar */}
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pb-4 mb-8">
            {categories.map((cat) => (
              <button
                key={cat.id}
                onClick={() => setActiveCategory(cat.id)}
                className={cn(
                  'px-4 py-2 text-xs md:text-sm font-sans rounded-btn border transition-all duration-200 whitespace-nowrap active:scale-[0.98]',
                  activeCategory === cat.id
                    ? 'bg-white text-[#121417] border-white font-semibold shadow-sm'
                    : 'bg-[#121417] text-[#c0c9c2] border-[#636363] hover:text-white hover:border-white'
                )}
              >
                {cat.label}
              </button>
            ))}
          </div>

          {/* Feature Showcase Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredCards.map((card) => (
              <a
                key={card.id}
                href={card.path}
                onClick={(e) =>
                  handleProtectedClick(e, card.path, getCardRoles(card.path), card.title)
                }
                className="group p-6 bg-[#000000] border border-[#636363] rounded-card hover:border-white transition-all duration-200 flex flex-col justify-between cursor-pointer"
              >
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <span className="font-mono text-xs text-[#9b9b9b] tracking-wider">{card.index}</span>
                    <span className="text-xs font-mono px-2 py-0.5 rounded-pill bg-[#2b5945]/20 text-[#a0d1b8] border border-[#2b5945]">
                      {card.badge}
                    </span>
                  </div>

                  <h3 className="text-lg font-sans font-semibold text-white group-hover:text-white transition-colors mb-1">
                    {card.title}
                  </h3>
                  <p className="text-xs text-[#fae0a6] font-mono mb-3">{card.subtitle}</p>
                  <p className="text-xs text-[#c0c9c2] leading-relaxed mb-6">
                    {card.description}
                  </p>
                </div>

                <div className="pt-4 border-t border-[#636363]/40">
                  <div className="text-xs font-mono text-[#9b9b9b] mb-2 truncate">
                    {card.meta}
                  </div>
                  <span className="text-xs font-mono font-medium text-white group-hover:text-[#a0d1b8] flex items-center justify-between">
                    <span>{card.ctaText}</span>
                    <ChevronRight className="w-3.5 h-3.5 text-[#9b9b9b] group-hover:translate-x-1 transition-transform" />
                  </span>
                </div>
              </a>
            ))}
          </div>

        </div>
      </section>

      {/* Partner Quotes & Testimonials with Palantir Editorial Motif */}
      <section className="py-20 px-4 md:px-12 bg-[#1e2124]">
        <div className="mx-auto max-w-[1440px]">
          <div className="text-left mb-12">
            <h2 className="text-display-md font-bold font-sans text-white">
              Tactical Testimonials
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-[#636363]/40 border-y border-[#636363]/40">
            <div className="p-6 md:p-8 text-white">
              <p className="text-xs font-mono text-[#a0d1b8] mb-4">/ CASE STUDY — INDIRANAGAR PS</p>
              <p className="text-sm text-[#c0c9c2] leading-relaxed italic mb-6">
                "GAURDIAN eliminated our 45-minute jurisdictional delay. The automated Section 91 CrPC notice was generated instantly, enabling NPCI to freeze ₹4.8 Lakhs before the mule could reach the ATM."
              </p>
              <div className="pt-4 border-t border-[#636363]/40">
                <p className="text-xs font-semibold text-white">Insp. K. Ramanathan</p>
                <p className="text-xs font-mono text-[#9b9b9b]">Station House Officer, Bengaluru Cyber Unit</p>
              </div>
            </div>

            <div className="p-6 md:p-8 text-white">
              <p className="text-xs font-mono text-[#a0d1b8] mb-4">/ CASE STUDY — NPCI RISK CELL</p>
              <p className="text-sm text-[#c0c9c2] leading-relaxed italic mb-6">
                "Multi-hop graph decomposition identified 14 accounts originating from a single device fingerprint. We halted downstream settlement in under 180 seconds across 4 separate private banks."
              </p>
              <div className="pt-4 border-t border-[#636363]/40">
                <p className="text-xs font-semibold text-white">Dr. Shreya Sengupta</p>
                <p className="text-xs font-mono text-[#9b9b9b]">Principal Analyst, Financial Intelligence Unit</p>
              </div>
            </div>

            <div className="p-6 md:p-8 text-white">
              <p className="text-xs font-mono text-[#a0d1b8] mb-4">/ CASE STUDY — FIELD PATROL 04</p>
              <p className="text-sm text-[#c0c9c2] leading-relaxed italic mb-6">
                "The turn-by-turn routing geofenced the exact ATM kiosk 4 minutes before withdrawal. We apprehended the runner in possession of 18 fraudulent debit cards."
              </p>
              <div className="pt-4 border-t border-[#636363]/40">
                <p className="text-xs font-semibold text-white">Sub-Insp. Vinod G.</p>
                <p className="text-xs font-mono text-[#9b9b9b]">Command Intercept Unit, Zone 3</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Split 50/50 Dual CTA Banner - Signature Palantir Section */}
      <section className="grid grid-cols-1 md:grid-cols-2 border-y border-[#636363]/40">
        {/* Left Side: Matte Light High-Contrast CTA */}
        <div className="bg-[#e0e0e0] text-[#121417] p-12 lg:p-20 flex flex-col justify-between">
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold font-sans tracking-tight leading-snug mb-4">
              Are you currently experiencing fraud or extortion?
            </h2>
            <p className="text-sm text-[#494a4b] max-w-md leading-relaxed mb-8">
              No account creation required. Immediate OTP phone verification logs your complaint directly to the 1930 National Cybercrime Portal and triggers instant downstream freezes.
            </p>
          </div>
          <div>
            <button
              onClick={(e) =>
                handleProtectedClick(
                  e,
                  '/report',
                  ['COMMAND_HQ', 'POLICE', 'CONSTABLE', 'CITIZEN'],
                  'Citizen Incident Intake'
                )
              }
              className="inline-flex items-center gap-2 bg-[#121417] text-white hover:bg-black font-sans font-semibold text-xs px-6 py-3 rounded-btn transition-all"
            >
              Report Incident Immediately
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Right Side: Matte Dark Sovereign CTA */}
        <div className="bg-[#121417] text-white p-12 lg:p-20 flex flex-col justify-between border-t md:border-t-0 md:border-l border-[#636363]/40">
          <div>
            <h2 className="text-2xl sm:text-3xl font-bold font-sans tracking-tight leading-snug mb-4">
              Access the Police HQ Command Center
            </h2>
            <p className="text-sm text-[#c0c9c2] max-w-md leading-relaxed mb-8">
              Analyze multi-tier mule graphs, execute NPCI Universal Freezes, simulate spatio-temporal ATM clustering, and draft Section 91 CrPC legal notices with AI Copilot.
            </p>
          </div>
          <div>
            <button
              onClick={(e) =>
                handleProtectedClick(
                  e,
                  '/command',
                  ['COMMAND_HQ'],
                  'Tactical Command HQ'
                )
              }
              className="inline-flex items-center gap-2 bg-white text-black hover:bg-[#2b5945] hover:text-white border border-white font-sans font-semibold text-xs px-6 py-3 rounded-btn transition-all"
            >
              Launch Tactical HQ
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>

        </div>
      </section>

      {/* Comprehensive Palantir Multi-Column Footer */}
      <footer className="bg-[#000000] py-16 px-4 md:px-12 border-t border-[#636363]/40 text-white">
        <div className="mx-auto max-w-[1440px]">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
            {/* Col 1: Brand & Status */}
            <div className="col-span-2">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-7 h-7 rounded-sm bg-white flex items-center justify-center text-black font-bold text-xs">
                  CC
                </div>
                <span className="font-sans font-bold text-sm tracking-wider">GAURDIAN DEFENSE</span>
              </div>
              <p className="text-xs text-[#9b9b9b] max-w-sm leading-relaxed mb-6">
                GAURDIAN sovereign financial cybercrime defense architecture. Built for law enforcement, citizen preservation, and financial intelligence interdiction.
              </p>
              <div className="flex items-center gap-2 text-xs font-mono text-[#c0c9c2]">
                <span className="w-2 h-2 rounded-full bg-[#a0d1b8]" />
                <span>ALL STATE NODES ONLINE</span>
              </div>
            </div>

            {/* Col 2: Capabilities */}
            <div>
              <div className="text-xs font-mono tracking-wider text-[#9b9b9b] uppercase mb-4">
                Capabilities
              </div>
              <ul className="space-y-2.5 text-xs text-[#c0c9c2]">
                <li><Link to="/report" className="hover:text-white transition-colors">Incident Intake</Link></li>
                <li><Link to="/command" className="hover:text-white transition-colors">Mule Ontology</Link></li>
                <li><Link to="/command" className="hover:text-white transition-colors">Universal Freeze</Link></li>
                <li><Link to="/field" className="hover:text-white transition-colors">ATM Intercept</Link></li>
                <li><Link to="/admin" className="hover:text-white transition-colors">Telemetry & STM</Link></li>
              </ul>
            </div>

            {/* Col 3: Statutory */}
            <div>
              <div className="text-xs font-mono tracking-wider text-[#9b9b9b] uppercase mb-4">
                Statutory Directives
              </div>
              <ul className="space-y-2.5 text-xs text-[#c0c9c2]">
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('crpc-91')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    Section 91 CrPC Directive
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('it-act-69b')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    IT Act Section 69B
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('npci-1930')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    NPCI Standard 1930 SOP
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('rbi-kyc')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    RBI KYC & Mule Directives
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('bns-alignment')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    BNS 2023 Alignments
                  </button>
                </li>
              </ul>
            </div>

            {/* Col 4: Operations */}
            <div>
              <div className="text-xs font-mono tracking-wider text-[#9b9b9b] uppercase mb-4">
                Operations & Grid
              </div>
              <ul className="space-y-2.5 text-xs text-[#c0c9c2]">
                <li><a href="tel:1930" className="hover:text-white transition-colors flex items-center gap-1.5"><span className="text-[#a0d1b8]">↳</span> Helpline: 1930 (National)</a></li>
                <li><a href="tel:112" className="hover:text-white transition-colors flex items-center gap-1.5"><span className="text-[#a0d1b8]">↳</span> Emergency: 112 (Dispatch)</a></li>
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('indiranagar-hq')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    Indiranagar Cyber HQ
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('karnataka-cid')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    Karnataka CID Cyber Division
                  </button>
                </li>
                <li>
                  <button
                    onClick={() => setSelectedPolicyDoc('national-i4c')}
                    className="hover:text-white hover:underline transition-colors text-left font-sans"
                  >
                    National I4C Grid Alliance
                  </button>
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar with Social Pills and Copyright */}
          <div className="pt-8 border-t border-[#636363]/30 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="font-mono text-xs text-[#9b9b9b]">
              © 2026 GAURDIAN PLATFORM. ALL RIGHTS RESERVED. PALANTIR DESIGN FIDELITY.
            </div>

            <div className="flex flex-wrap items-center gap-2">
              <button
                onClick={() => setSelectedPolicyDoc('national-i4c')}
                className="px-3 py-1 rounded-pill bg-[#121417] border border-[#636363] hover:border-[#a0d1b8] text-xs font-mono text-[#c0c9c2] hover:text-white transition-colors cursor-pointer"
                title="View I4C Certification & Framework"
              >
                I4C SECURE
              </button>
              <button
                onClick={() => setSelectedPolicyDoc('npci-1930')}
                className="px-3 py-1 rounded-pill bg-[#121417] border border-[#636363] hover:border-[#a0d1b8] text-xs font-mono text-[#c0c9c2] hover:text-white transition-colors cursor-pointer"
                title="View NPCI API Protocol Specification"
              >
                NPCI API v2
              </button>
              <button
                onClick={() => setSelectedPolicyDoc('security-encryption')}
                className="px-3 py-1 rounded-pill bg-[#121417] border border-[#636363] hover:border-[#a0d1b8] text-xs font-mono text-[#c0c9c2] hover:text-white transition-colors cursor-pointer"
                title="View AES-256-GCM Cryptographic Specs"
              >
                ENCRYPTION: AES-256-GCM
              </button>
              <button
                onClick={() => setSelectedPolicyDoc('privacy-policy')}
                className="px-3 py-1 rounded-pill bg-[#121417] border border-[#636363] hover:border-[#a0d1b8] text-xs font-mono text-[#c0c9c2] hover:text-white transition-colors cursor-pointer"
                title="View Citizen Privacy Policy (DPDP Act 2023)"
              >
                DPDP PRIVACY
              </button>
            </div>
          </div>
        </div>
      </footer>

      {/* Interactive Statutory & Legal Directives Modal */}
      <StatutoryModal
        documentId={selectedPolicyDoc}
        onClose={() => setSelectedPolicyDoc(null)}
      />
    </div>
  )
}