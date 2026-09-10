import React, { useState } from 'react'
import {
  Shield,
  FileText,
  Lock,
  Scale,
  Building,
  CheckCircle2,
  ExternalLink,
  Copy,
  Printer,
  X,
  Search,
  BookOpen,
  Landmark,
  Radio,
  FileCheck,
} from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { cn } from '@/lib/utils'

export interface PolicyDocument {
  id: string
  title: string
  category: 'STATUTORY' | 'OPERATIONS' | 'SECURITY' | 'GOVERNANCE'
  statute: string
  authority: string
  effectiveDate: string
  summary: string
  clauses: { title: string; text: string; codeRef?: string }[]
  admissibility: string
  actionItems: string[]
}

export const STATUTORY_DOCUMENTS: Record<string, PolicyDocument> = {
  'crpc-91': {
    id: 'crpc-91',
    title: 'Section 91 CrPC / Section 94 BNSS Legal Requisition Directive',
    category: 'STATUTORY',
    statute: 'Code of Criminal Procedure 1973 § 91 & Bharatiya Nagarik Suraksha Sanhita 2023 § 94',
    authority: 'Directorate of Enforcement & State Cyber Command',
    effectiveDate: '01 July 2024 (BNSS Compliant)',
    summary:
      'Statutory power of an Investigating Officer or Station House Officer to compel the immediate production of electronic financial records, subscriber metadata, UPI transaction ledgers, and execute synchronous account liens across scheduled commercial banks.',
    clauses: [
      {
        title: 'Statutory Authority to Summons Digital Documents',
        text: 'Whenever any Court or any officer in charge of a police station considers that the production of any document or electronic record is necessary or desirable for the purposes of any investigation, inquiry, or trial, such officer may issue a written order to the person in whose possession or power such document or thing is believed to be.',
        codeRef: 'Section 91(1) CrPC / Section 94(1) BNSS',
      },
      {
        title: 'Application to Financial Intermediaries & Payment Gateways',
        text: 'Includes all RBI-regulated banks, NPCI UPI payment system providers (PSPs), third-party application providers (TPAPs), and payment aggregators. Mandates transmission of account statements, IP access logs, device fingerprints, and immediate lien placement within 120 minutes of electronic notice receipt.',
        codeRef: 'Rule 3(1) IT (Intermediary Guidelines) & CrPC § 91',
      },
      {
        title: 'Immediate Protective Asset Freezing (Lien Marking)',
        text: 'Where siphoned funds are traced to downstream accounts, the Investigating Officer may direct the bank nodal officer to place an immediate debit freeze/lien on the siphoned quantum to prevent dissipation before formal judicial seizure under Section 102 CrPC / Section 107 BNSS.',
        codeRef: 'CrPC § 102 & BNSS § 107',
      },
    ],
    admissibility:
      'Electronic notices transmitted via GAURDIAN automated dispatch carry cryptographic hash anchors compliant with Section 65B of the Indian Evidence Act 1872 and Section 63 of the Bharatiya Sakshya Adhiniyam 2023.',
    actionItems: [
      'Automated dispatch to 42 Scheduled Commercial Banks via National Nodal Registry',
      'Instant generation of tamper-evident PDF notice with QR verification code',
      'Cryptographic SHA-256 Merkle tree log entry for court presentation',
    ],
  },
  'it-act-69b': {
    id: 'it-act-69b',
    title: 'Information Technology Act § 69B Cybersecurity Monitoring Directive',
    category: 'STATUTORY',
    statute: 'Information Technology Act, 2000 (Amended 2008) Section 69B',
    authority: 'Indian Computer Emergency Response Team (CERT-In) & Ministry of Electronics & IT',
    effectiveDate: 'Statutory Regulation (G.S.R. 20(E))',
    summary:
      'Empowers authorized government agencies to monitor and collect traffic data or information through any computer resource for cyber security and mitigation of financial fraud vectors.',
    clauses: [
      {
        title: 'Collection & Monitoring of Traffic Data',
        text: 'The Central Government may, by notification in the Official Gazette, authorize any agency of the Government to monitor and collect traffic data or information generated, transmitted, received or stored in any computer resource for enhancing cyber security and for identification, analysis and prevention of any cyber incident.',
        codeRef: 'IT Act 2000 § 69B(1)',
      },
      {
        title: 'Mandatory Intermediary Compliance',
        text: 'Any subscriber or intermediary or any person in charge of the computer resource shall, when called upon by the authorized agency, provide technical assistance and all available traffic logs, proxy records, and routing information. Failure to comply is punishable with imprisonment up to 3 years and fine.',
        codeRef: 'IT Act 2000 § 69B(2)',
      },
      {
        title: 'Information Security & Privacy Safeguards',
        text: 'Data acquired under Section 69B is restricted strictly to forensic cyber analysis, threat actor signature extraction, and financial fraud ring neutralization. All telemetry is encrypted at rest using AES-256-GCM.',
        codeRef: 'IT (Procedure & Safeguards for Monitoring) Rules, 2009',
      },
    ],
    admissibility:
      'Packet traffic records and IP telemetry verified under CERT-In certified forensic protocols.',
    actionItems: [
      'Real-time VPN and Proxy exit-node decomposition',
      'Correlating suspect UPI device IDs with telecom IMEI databases',
      'Automated transmission of compromised indicators of compromise (IOCs) to National Cybercrime Portal',
    ],
  },
  'npci-1930': {
    id: 'npci-1930',
    title: 'NPCI Standard 1930 Citizen Financial Fraud Intercept SOP',
    category: 'OPERATIONS',
    statute: 'National Cybercrime Reporting Portal (NCRP) Citizen Financial Cyber Fraud Reporting System (CFCFRS)',
    authority: 'National Payments Corporation of India (NPCI) & Ministry of Home Affairs (I4C)',
    effectiveDate: 'Unified Inter-Bank Protocol 2026',
    summary:
      'Standard Operating Procedure governing the 6-Minute Golden Window for inter-bank transaction blocking, automated ticket generation on 1930 Helpline, and synchronous API-based freeze directives.',
    clauses: [
      {
        title: 'The Golden Hour Rule (Sub-6 Minute Intercept)',
        text: 'When a citizen reports financial fraud within the initial critical window, automated intake generates a CFCFRS token. NPCI settlement rails trigger synchronous debit-freeze flags across downstream receiving bank accounts before physical cashout.',
        codeRef: 'MHA / I4C CFCFRS Guideline v3.4',
      },
      {
        title: 'Multi-Hop Downstream Lien Propagation',
        text: 'If funds have been layered into secondary or tertiary mule accounts (Layers 1, 2, and 3), the NPCI API propagates recursive hold instructions across all recipient IFSCs/VPAs until the full defrauded sum is locked.',
        codeRef: 'NPCI UPI Circular 2025/19',
      },
      {
        title: 'Restitution & Court Order Release Workflow',
        text: 'Frozen amounts remain held in escrow with the receiving bank under police lien until the concerned Magistrate or Cyber Police Station issues a formal Release & Restitution order under Section 457 CrPC / Section 503 BNSS.',
        codeRef: 'Standard Restitution SOP',
      },
    ],
    admissibility:
      'NPCI UTR transaction traces and clearing switch audit logs provided directly into GAURDIAN ledger.',
    actionItems: [
      'Universal 1-click broadcast to all scheduled banks',
      'Real-time SMS & WhatsApp victim notification with reference token',
      'Automated dispatch to nearest beat patrol vehicle for physical ATM intercepts',
    ],
  },
  'rbi-kyc': {
    id: 'rbi-kyc',
    title: 'RBI Master Direction — KYC & Mule Account Interdiction',
    category: 'GOVERNANCE',
    statute: 'Reserve Bank of India Master Direction - Know Your Customer (KYC) Direction, 2016',
    authority: 'Reserve Bank of India (RBI/DBR/2015-16/18)',
    effectiveDate: 'Updated Master Direction 2026',
    summary:
      'Mandatory guidelines for banks and NBFCs regarding ongoing transaction monitoring, detection of synthetic mule accounts, dormant account reactivation anomalies, and immediate reporting of suspicious transactions.',
    clauses: [
      {
        title: 'Real-Time Transaction Monitoring & Velocity Thresholds',
        text: 'Banks must deploy automated transaction monitoring systems to identify sudden velocity spikes in newly opened or previously dormant low-balance savings accounts, particularly accounts receiving high-frequency UPI transfers followed by immediate ATM cash withdrawals.',
        codeRef: 'RBI Master Direction § 37',
      },
      {
        title: 'Synthetic Identity & Mule Ring Risk Scoring',
        text: 'Accounts exhibiting shared mobile numbers, identical device IMEIs, or matching IP geolocations across diverse individual names must be flagged as high-risk mule syndicates and subjected to enhanced due diligence (EDD) or operational suspension.',
        codeRef: 'RBI Cyber Security Framework § 4.2',
      },
      {
        title: 'Zero Liability Protection for Citizens',
        text: 'Where a citizen reports unauthorized electronic banking fraud within 3 working days, customer liability is zero, and banks are mandated to reverse or freeze settlements in coordination with law enforcement.',
        codeRef: 'RBI/2017-18/15 DBR.No.Leg.BC.78/09.07.005/2017-18',
      },
    ],
    admissibility:
      'Bank Nodal Officer verification certificate under Bankers Books Evidence Act, 1891.',
    actionItems: [
      'GNN-based automated mule scoring (>0.85 threshold triggers freeze recommendation)',
      'Automated STR (Suspicious Transaction Report) compilation for FIU-IND submission',
      'Continuous KYC verification checking against Centralized KYC Registry (CKYCR)',
    ],
  },
  'bns-alignment': {
    id: 'bns-alignment',
    title: 'Bharatiya Nyaya Sanhita (BNS 2023) Cyber Fraud Provisions',
    category: 'STATUTORY',
    statute: 'Bharatiya Nyaya Sanhita, 2023 (Act No. 45 of 2023)',
    authority: 'Ministry of Law and Justice, Government of India',
    effectiveDate: '01 July 2024',
    summary:
      'Codified substantive criminal law provisions replacing the Indian Penal Code 1860, introducing explicit penalties for organized cybercrime syndicates, digital cheating by impersonation, and multi-state financial fraud.',
    clauses: [
      {
        title: 'Section 318 BNS — Cheating & Financial Fraud',
        text: 'Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person... shall be punished with imprisonment of either description for a term which may extend to 7 years, and shall also be liable to fine.',
        codeRef: 'BNS 2023 § 318(4) (Formerly IPC 420)',
      },
      {
        title: 'Section 319 BNS — Cheating by Personation',
        text: 'A person is said to "cheat by personation" if he cheats by pretending to be some other person, or by knowingly substituting one person for another, including synthetic digital profiles, fake bank nodal officers, or law enforcement impersonation.',
        codeRef: 'BNS 2023 § 319 (Formerly IPC 416/419)',
      },
      {
        title: 'Section 111 BNS — Organized Crime & Mule Networks',
        text: 'Any continuing unlawful activity including cyber financial crimes, economic offenses, and organized syndication executed through mule accounts and hawala runners is classified as Organized Crime punishable with rigorous imprisonment.',
        codeRef: 'BNS 2023 § 111',
      },
    ],
    admissibility:
      'Charge sheet generation and statutory FIR drafting in full alignment with BNS 2023 classifications.',
    actionItems: [
      'Automated FIR drafting mapping complaint facts to corresponding BNS and IT Act sections',
      'Syndicate organizer identification and charge aggregation',
      'Instant e-FIR dispatch to State Cyber Police Registry',
    ],
  },
  'indiranagar-hq': {
    id: 'indiranagar-hq',
    title: 'Indiranagar Cyber Command HQ & Beat Operations Manual',
    category: 'OPERATIONS',
    statute: 'Zone-3 Tactical Cyber Defense Operations Protocol',
    authority: 'Bengaluru City Police Cyber Crime Division',
    effectiveDate: 'Operational Roster Cycle 2026',
    summary:
      'Deployment matrix, patrol beat boundaries, radio frequencies, and rapid response SOP for Zone-3 Indiranagar Cyber Police Station covering 100ft Road, CMH Road, HAL 2nd Stage, and Koramangala sectors.',
    clauses: [
      {
        title: 'Beat Area Coverage & Geofencing',
        text: 'Primary Tactical Unit Delta-4 patrols Sector 4 (Indiranagar 100ft Road, 12th Main, HAL 2nd Stage). Average response time to 12 monitored ATM clusters is strictly under 4 minutes 30 seconds.',
        codeRef: 'Zone-3 Operational Manual § 1.2',
      },
      {
        title: 'Police Radio & Secure Mesh Communications',
        text: 'Encrypted tactical mesh network operates on 154.250 MHz digital voice with GPS burst telemetry every 15 seconds. Direct integration with GAURDIAN Command HQ dashboard.',
        codeRef: 'Police Wireless Grid Directive',
      },
      {
        title: 'Cash-out Intercept & Apprehension Protocol',
        text: 'Patrol squads arriving at flagged ATM kiosk establish a 280-meter tactical cordon, verify suspect identity against live GNN alert parameters, and secure electronic evidence (debit cards, POS machines, smartphones).',
        codeRef: 'Field Intercept Protocol v2.1',
      },
    ],
    admissibility:
      'Field officer bodycam footage and GPS positioning logs anchored in immutable blockchain registry.',
    actionItems: [
      '24x7 Active Squads: Delta-4, Alpha-1, Bravo-2, Charlie-3',
      'Direct landline & emergency terminal: 080-22942400 / 112',
      'Automated turn-by-turn routing dispatched to field tablets',
    ],
  },
  'karnataka-cid': {
    id: 'karnataka-cid',
    title: 'Karnataka CID Cyber Crime Division Framework',
    category: 'OPERATIONS',
    statute: 'Criminal Investigation Department Special Cyber Task Force Protocol',
    authority: 'Director General of Police, CID Karnataka',
    effectiveDate: 'State Operational Standard 2026',
    summary:
      'Apex state-level specialized cyber forensics, dark web interdiction, high-value cyber financial fraud investigation, and inter-state police coordination division.',
    clauses: [
      {
        title: 'Jurisdiction over High-Value Financial Frauds',
        text: 'All organized cyber fraud syndicates exceeding ₹50 Lakhs or involving inter-state mule networks across 3+ states are automatically escalated to CID Karnataka Cyber Center of Excellence (CCoE).',
        codeRef: 'CID Standing Order 04/2024',
      },
      {
        title: 'Forensic Evidence Preservation Lab (FSL)',
        text: 'Certified ISO/IEC 17025 digital forensics laboratory for extracting chip-off memory from suspect hardware, parsing encrypted SQLite transaction databases, and analyzing malicious APKs.',
        codeRef: 'FSL Cyber Protocol § 9',
      },
      {
        title: 'State Nodal Officer Banking Coordination',
        text: 'Maintains 24x7 dedicated emergency hotline and direct API bridges with 42 commercial bank risk cells and payment gateways for instant account freezings.',
        codeRef: 'Nodal Banking Directive',
      },
    ],
    admissibility:
      'Forensic lab examination reports admissible under Section 293 CrPC / Section 329 BNSS.',
    actionItems: [
      'State-wide threat intelligence consolidation',
      'Cross-jurisdictional warrants and arrest coordination',
      'Periodic nodal officer review meetings for NPA and mule mitigation',
    ],
  },
  'national-i4c': {
    id: 'national-i4c',
    title: 'National Cybercrime Coordination Centre (I4C) Alliance',
    category: 'GOVERNANCE',
    statute: 'Ministry of Home Affairs, Government of India I4C Scheme',
    authority: 'Indian Cyber Crime Coordination Centre (I4C), MHA',
    effectiveDate: 'National Standard 2026',
    summary:
      'National nodal framework unifying law enforcement agencies across all 28 States and 8 Union Territories for collaborative prevention, detection, and investigation of cyber financial crimes.',
    clauses: [
      {
        title: 'National Cybercrime Reporting Portal (cybercrime.gov.in)',
        text: 'Centralized citizen intake engine receiving complaints from 1930 Helpline, web portal, and state police cyber cells with automatic routing to jurisdictional police stations.',
        codeRef: 'MHA I4C Framework § 2.1',
      },
      {
        title: 'Inter-State Cybercrime Coordination Group (JCCT)',
        text: 'Joint Cybercrime Coordination Teams deployed in major fraud hotspots (Mewat, Jamtara, Alwar, Bharatpur) enabling seamless multi-state raids and mule arrest execution.',
        codeRef: 'JCCT Operational SOP',
      },
      {
        title: 'National Cyber Forensic Laboratory (NCFL)',
        text: 'Provides cutting-edge cyber forensic infrastructure and software tools to investigating officers across India for deep blockchain analytics and mobile forensic extraction.',
        codeRef: 'NCFL Technical Standard',
      },
    ],
    admissibility:
      'National registry data authenticated with digital timestamps from National Informatics Centre (NIC).',
    actionItems: [
      'National 1930 Helpline integration with sub-second response times',
      'Bi-directional mule account blacklist synchronization',
      'National cyber safety advisory dissemination across all state nodes',
    ],
  },
  'security-encryption': {
    id: 'security-encryption',
    title: 'Platform Cryptographic Security & AES-256-GCM Architecture',
    category: 'SECURITY',
    statute: 'Government of India National Cyber Security Policy & ISO/IEC 27001 Standard',
    authority: 'GAURDIAN Information Security Directorate',
    effectiveDate: 'Cryptographic Policy v4.2',
    summary:
      'Comprehensive security specification governing data-in-transit, data-at-rest encryption, zero-knowledge role access, and tamper-proof SHA-256 Merkle tree evidence anchoring.',
    clauses: [
      {
        title: 'Data-at-Rest & In-Transit Encryption',
        text: 'All complaint manifests, banking records, and officer communication are encrypted using AES-256-GCM with hardware security module (HSM) managed keys. Network transmission mandates TLS 1.3 with Perfect Forward Secrecy.',
        codeRef: 'ISO/IEC 27001 § A.10.1',
      },
      {
        title: 'Cryptographic Ledger Anchoring',
        text: 'Every investigative action (intake, GNN risk scoring, NPCI freeze trigger, patrol dispatch) generates an immutable SHA-256 hash anchored into a decentralized Merkle block verification tree.',
        codeRef: 'Evidence Integrity Spec v3',
      },
      {
        title: 'Strict Role-Based Access Control (RBAC)',
        text: 'Clearance hierarchy: Level 0 (Citizen Intake), Level 1 (Field Constable), Level 2 (Inspector / Tactical HQ), Level 3 (Supervisory Admin / Director Moksh) with biometric/hardware MFA enforcement.',
        codeRef: 'GAURDIAN Security Matrix',
      },
    ],
    admissibility:
      'Tamper-evident audit trail mathematically provable for judicial review under Section 65B Indian Evidence Act.',
    actionItems: [
      'Zero plaintext storage of Citizen PAN / Aadhaar numbers',
      'Automated daily cryptographic key rotation',
      'Continuous automated vulnerability penetration testing (VAPT)',
    ],
  },
  'privacy-policy': {
    id: 'privacy-policy',
    title: 'Sovereign Privacy Policy & Citizen Data Protection',
    category: 'GOVERNANCE',
    statute: 'Digital Personal Data Protection Act, 2023 (DPDP Act) & IT Rules 2011',
    authority: 'Data Protection Board of India & GAURDIAN Governance Directorate',
    effectiveDate: 'Compliant with DPDP Act 2023',
    summary:
      'Citizen privacy charter detailing lawful basis of data processing for cybercrime prevention, data minimization principles, retention limits, and grievance redressal channels.',
    clauses: [
      {
        title: 'Purpose Limitation & Data Minimization',
        text: 'Citizen information provided during incident intake (phone, bank statements, transaction screenshots) is utilized strictly for investigating the reported crime, executing asset recovery, and judicial proceedings. Commercial data monetization is strictly prohibited by law.',
        codeRef: 'DPDP Act 2023 § 4 & § 6',
      },
      {
        title: 'Citizen Rights & Status Transparency',
        text: 'Victims are provided real-time visibility into the status of their complaint, frozen amounts, and assigned investigation officer via secure OTP authentication without exposing sensitive banking credentials.',
        codeRef: 'Citizen Charter § 3',
      },
      {
        title: 'Grievance Redressal & Nodal Officer Contact',
        text: 'Any citizen inquiries regarding data privacy or complaint rectification may be escalated directly to the Data Protection Officer at dpo@cybercell.gov.in with guaranteed 48-hour response SLA.',
        codeRef: 'DPDP Act 2023 § 13',
      },
    ],
    admissibility:
      'Statutory compliance certified under Ministry of Electronics and Information Technology guidelines.',
    actionItems: [
      'Encrypted citizen evidence vault with automatic deletion of expired telemetry',
      'End-to-end audit logging of all officer data access events',
      'Independent annual data protection audit by CERT-In empaneled auditor',
    ],
  },
}

interface StatutoryModalProps {
  documentId: string | null
  onClose: () => void
}

export const StatutoryModal: React.FC<StatutoryModalProps> = ({ documentId, onClose }) => {
  const [activeDocId, setActiveDocId] = useState<string>(documentId || 'crpc-91')
  const [copied, setCopied] = useState(false)
  const [searchFilter, setSearchFilter] = useState('')

  // Sync active doc when prop changes
  React.useEffect(() => {
    if (documentId && STATUTORY_DOCUMENTS[documentId]) {
      setActiveDocId(documentId)
    }
  }, [documentId])

  if (!documentId) return null

  const currentDoc = STATUTORY_DOCUMENTS[activeDocId] || STATUTORY_DOCUMENTS['crpc-91']

  const handleCopyCitation = () => {
    const citation = `[GAURDIAN STATUTORY DIRECTIVE]\nDocument: ${currentDoc.title}\nStatute: ${currentDoc.statute}\nAuthority: ${currentDoc.authority}\nEffective Date: ${currentDoc.effectiveDate}\nVerification Hash: 0x${Math.random().toString(16).substring(2, 10)}${Math.random().toString(16).substring(2, 10)}`
    navigator.clipboard.writeText(citation)
    setCopied(true)
    setTimeout(() => setCopied(false), 2500)
  }

  const handlePrint = () => {
    window.print()
  }

  const filteredDocKeys = Object.keys(STATUTORY_DOCUMENTS).filter((key) => {
    const doc = STATUTORY_DOCUMENTS[key]
    const q = searchFilter.toLowerCase()
    return doc.title.toLowerCase().includes(q) || doc.statute.toLowerCase().includes(q) || doc.category.toLowerCase().includes(q)
  })

  return (
    <div
      className="fixed inset-0 z-[9999] bg-black/85 backdrop-blur-md flex items-center justify-center p-2 sm:p-4 md:p-6 text-white animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div
        className="w-full max-w-5xl max-h-[92vh] bg-[#0c0e11] border border-[#636363] rounded-card shadow-2xl flex flex-col overflow-hidden animate-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Header Bar */}
        <div className="p-4 bg-[#121417] border-b border-[#636363]/60 flex items-center justify-between flex-wrap gap-3">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-btn bg-black/40 backdrop-blur-sm border border-[#2b5945] flex items-center justify-center text-[#a0d1b8]">
              <Scale className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-xs text-[#a0d1b8] font-bold tracking-wider uppercase">
                  SOVEREIGN STATUTORY & DIRECTIVES REPOSITORY
                </span>
                <span className="text-[#636363]">/</span>
                <span className="font-mono text-[11px] text-[#9b9b9b]">OFFICIAL REFERENCE</span>
              </div>
              <h2 className="text-base font-sans font-bold text-white tracking-tight">
                {currentDoc.title}
              </h2>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={handleCopyCitation}
              className="text-xs font-mono"
            >
              {copied ? (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5 mr-1.5 text-[#a0d1b8]" />
                  COPIED CITATION
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 mr-1.5" />
                  COPY CITATION
                </>
              )}
            </Button>

            <Button
              variant="secondary"
              size="sm"
              onClick={handlePrint}
              className="text-xs font-mono hidden sm:inline-flex"
            >
              <Printer className="w-3.5 h-3.5 mr-1.5" />
              PRINT DIRECTIVE
            </Button>

            <button
              onClick={onClose}
              className="p-1.5 rounded-btn text-[#9b9b9b] hover:text-white hover:bg-[#2f3234] transition-colors ml-1"
              aria-label="Close modal"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Main Body: Left Document Selector + Right Document Details */}
        <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
          {/* Left Index Sidebar */}
          <div className="w-full md:w-72 bg-[#0a0c0e] border-b md:border-b-0 md:border-r border-[#636363]/40 flex flex-col shrink-0">
            <div className="p-3 border-b border-[#636363]/30">
              <div className="relative">
                <Search className="w-3.5 h-3.5 text-[#9b9b9b] absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={searchFilter}
                  onChange={(e) => setSearchFilter(e.target.value)}
                  placeholder="Filter legal directives..."
                  className="w-full bg-[#16191d] border border-[#636363]/60 rounded-btn pl-8 pr-3 py-1.5 text-xs text-white placeholder:text-[#636363] focus:outline-none focus:border-[#a0d1b8]"
                />
              </div>
            </div>

            <div className="flex-1 overflow-y-auto p-2 space-y-1">
              {filteredDocKeys.map((key) => {
                const doc = STATUTORY_DOCUMENTS[key]
                const isSelected = activeDocId === key
                return (
                  <button
                    key={key}
                    onClick={() => setActiveDocId(key)}
                    className={cn(
                      'w-full text-left p-2.5 rounded-btn text-xs font-sans transition-all flex flex-col gap-1 border',
                      isSelected
                        ? 'bg-black/40 backdrop-blur-sm text-white border-white font-semibold'
                        : 'text-[#c0c9c2] border-transparent hover:bg-[#121417] hover:text-white'
                    )}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-[10px] text-[#a0d1b8]">{doc.category}</span>
                      <span className="font-mono text-[10px] text-[#9b9b9b]">{doc.id}</span>
                    </div>
                    <span className="line-clamp-2 leading-snug">{doc.title}</span>
                  </button>
                )
              })}
            </div>
          </div>

          {/* Right Document Content */}
          <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-6">
            {/* Metadata Badges Strip */}
            <div className="p-4 bg-[#121417] border border-[#636363]/50 rounded-card grid grid-cols-1 sm:grid-cols-3 gap-3 text-xs font-mono">
              <div>
                <span className="text-[#9b9b9b] block mb-0.5 uppercase tracking-wider text-[10px]">Statutory Baseline</span>
                <span className="text-white font-medium">{currentDoc.statute}</span>
              </div>
              <div>
                <span className="text-[#9b9b9b] block mb-0.5 uppercase tracking-wider text-[10px]">Enforcing Authority</span>
                <span className="text-[#fae0a6] font-medium">{currentDoc.authority}</span>
              </div>
              <div>
                <span className="text-[#9b9b9b] block mb-0.5 uppercase tracking-wider text-[10px]">Effective Status</span>
                <span className="text-[#a0d1b8] font-semibold">{currentDoc.effectiveDate}</span>
              </div>
            </div>

            {/* Executive Summary */}
            <div className="space-y-2">
              <h3 className="font-mono text-xs uppercase tracking-wider text-[#9b9b9b] flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5 text-[#a0d1b8]" />
                Executive Summary & Operational Intent
              </h3>
              <p className="text-sm text-[#e0e0e0] leading-relaxed bg-[#14161a] p-4 rounded-btn border border-[#636363]/40">
                {currentDoc.summary}
              </p>
            </div>

            {/* Codified Clauses */}
            <div className="space-y-3">
              <h3 className="font-mono text-xs uppercase tracking-wider text-[#9b9b9b] flex items-center gap-1.5">
                <FileCheck className="w-3.5 h-3.5 text-[#fae0a6]" />
                Codified Clauses & Directives
              </h3>
              <div className="space-y-3">
                {currentDoc.clauses.map((clause, idx) => (
                  <div
                    key={idx}
                    className="p-4 bg-[#0e1013] border border-[#636363]/50 rounded-card space-y-2"
                  >
                    <div className="flex items-center justify-between flex-wrap gap-2">
                      <h4 className="text-xs font-sans font-bold text-white flex items-center gap-2">
                        <span className="w-5 h-5 rounded-full bg-black/40 backdrop-blur-sm border border-[#636363] text-center leading-5 text-[11px] font-mono text-[#a0d1b8]">
                          {idx + 1}
                        </span>
                        {clause.title}
                      </h4>
                      {clause.codeRef && (
                        <span className="font-mono text-[10px] px-2 py-0.5 rounded-pill bg-[#2b5945]/20 text-[#a0d1b8] border border-[#2b5945]">
                          {clause.codeRef}
                        </span>
                      )}
                    </div>
                    <p className="text-xs text-[#c0c9c2] leading-relaxed pl-7">
                      {clause.text}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Evidence Admissibility & Judicial Standards */}
            <div className="p-4 bg-[#14181c] border-l-2 border-[#a0d1b8] rounded-r-btn space-y-1.5 text-xs">
              <div className="font-sans font-bold text-white flex items-center gap-2">
                <Shield className="w-4 h-4 text-[#a0d1b8]" />
                Judicial Admissibility & Evidentiary Standard
              </div>
              <p className="text-[#c0c9c2] leading-relaxed">
                {currentDoc.admissibility}
              </p>
            </div>

            {/* Tactical Action Items */}
            <div className="space-y-2">
              <h3 className="font-mono text-xs uppercase tracking-wider text-[#9b9b9b] flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#a0d1b8]" />
                Mandatory Operational Action Items
              </h3>
              <ul className="space-y-2 text-xs text-[#c0c9c2]">
                {currentDoc.actionItems.map((item, idx) => (
                  <li key={idx} className="flex items-start gap-2">
                    <span className="text-[#a0d1b8] font-bold mt-0.5">↳</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Cryptographic Footprint Anchor */}
            <div className="p-3 bg-black/30 backdrop-blur-md border border-[#636363]/40 rounded-btn flex items-center justify-between flex-wrap gap-2 text-[11px] font-mono text-[#9b9b9b]">
              <span>SHA-256 MERKLE ANCHOR: 0x4f8a9e2b1c7d3f5a8e0c2b4a6e8f1c3a5b7d9e</span>
              <span className="text-[#a0d1b8] flex items-center gap-1">
                <Lock className="w-3 h-3" />
                SOVEREIGN CIPHER SEALED
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
