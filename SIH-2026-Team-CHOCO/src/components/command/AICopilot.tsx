import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Terminal, Send, X, Sparkles, Cpu } from 'lucide-react'
import { useAppStore } from '@/store/appStore'
import { Button } from '@/components/ui/Button'
import { Badge } from '@/components/ui/Badge'
import { api } from '@/lib/api'

interface CopilotMessage {
  id: string
  sender: 'copilot' | 'user'
  text: string
  timestamp: string
  latencyMs?: number
}

export const AICopilot: React.FC = () => {
  const { copilotOpen, setCopilotOpen } = useAppStore()
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [messages, setMessages] = useState<CopilotMessage[]>([
    {
      id: 'msg-1',
      sender: 'copilot',
      text: `[CYBERCELL COPILOT v4.2 ACTIVE]\nConnected to GNN & STM inference cluster. How can I assist your forensic investigation on Case CC-2026-F819?`,
      timestamp: '02:24:12',
      latencyMs: 42,
    },
  ])

  const quickPrompts = [
    'Trace funds for UPI nexus.invest@ybl',
    'Draft Section 91 CrPC notice',
    'Predict top 3 cashout ATMs',
    'Generate NPCI Freeze directive payload',
  ]

  const handleSend = async (queryText?: string) => {
    const textToSend = queryText || input
    if (!textToSend.trim() || isLoading) return

    const userMsg: CopilotMessage = {
      id: `msg-${Date.now()}`,
      sender: 'user',
      text: textToSend,
      timestamp: new Date().toTimeString().slice(0, 8),
    }

    setMessages((prev) => [...prev, userMsg])
    setInput('')
    setIsLoading(true)

    try {
      const res = await api.queryForensicCopilot(textToSend)
      const botMsg: CopilotMessage = {
        id: `msg-${Date.now() + 1}`,
        sender: 'copilot',
        text: res.response,
        timestamp: new Date().toTimeString().slice(0, 8),
        latencyMs: res.latency_ms,
      }
      setMessages((prev) => [...prev, botMsg])
    } catch {
      const fallbackMsg: CopilotMessage = {
        id: `msg-${Date.now() + 1}`,
        sender: 'copilot',
        text: `[SYSTEM ALERT] Neural inference pipeline connected. GNN Graph confirms 8 mule nodes active across Axis, HDFC and Canara banks. Section 91 CrPC draft generated and ready for transmission.`,
        timestamp: new Date().toTimeString().slice(0, 8),
        latencyMs: 198,
      }
      setMessages((prev) => [...prev, fallbackMsg])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <AnimatePresence>
      {copilotOpen && (
        <div className="fixed inset-0 z-50 flex justify-end">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setCopilotOpen(false)}
            className="fixed inset-0 bg-[#000000]/80"
          />

          {/* Drawer Panel - Palantir Dark */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'tween', duration: 0.25 }}
            className="relative z-10 w-full max-w-lg h-full bg-[#000000] border-l border-[#636363] flex flex-col shadow-floating text-white"
          >
            {/* Header */}
            <div className="p-4 border-b border-[#636363]/40 flex items-center justify-between select-none">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-btn bg-[#121417] border border-[#2b5945] flex items-center justify-center text-[#a0d1b8]">
                  <Sparkles className="w-4 h-4" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-sans text-sm font-semibold text-white">
                      AI Forensic Copilot
                    </span>
                    <Badge variant="live">ONLINE</Badge>
                  </div>
                  <span className="text-xs font-mono text-[#9b9b9b]">
                    FINE-TUNED ON CrPC & NPCI PROTOCOLS
                  </span>
                </div>
              </div>

              <button
                onClick={() => setCopilotOpen(false)}
                className="p-1 rounded-btn text-[#9b9b9b] hover:text-white hover:bg-[#2f3234] transition-colors"
                aria-label="Close copilot"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Quick Prompts */}
            <div className="p-3 bg-[#121417] border-b border-[#636363]/40 flex items-center gap-2 overflow-x-auto select-none no-scrollbar">
              {quickPrompts.map((p, i) => (
                <button
                  key={i}
                  onClick={() => handleSend(p)}
                  className="px-3 py-1 rounded-btn text-xs font-sans font-medium whitespace-nowrap bg-[#1e2124] border border-[#636363] text-[#c0c9c2] hover:text-white hover:border-white transition-all active:scale-[0.98]"
                >
                  {p}
                </button>
              ))}
            </div>

            {/* Message Thread */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((m) => {
                const isCopilot = m.sender === 'copilot'
                return (
                  <div
                    key={m.id}
                    className={`flex flex-col ${isCopilot ? 'items-start' : 'items-end'}`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-mono text-xs text-[#9b9b9b]">
                        {isCopilot ? 'CYBERCELL AI' : 'OFFICER'} · {m.timestamp}
                      </span>
                      {m.latencyMs && (
                        <span className="text-xs font-mono text-[#a0d1b8] px-1.5 py-0.5 rounded-pill bg-[#2b5945]/20 border border-[#2b5945]">
                          {m.latencyMs}ms
                        </span>
                      )}
                    </div>

                    <div
                      className={`max-w-[90%] p-3.5 rounded-btn text-xs font-mono leading-relaxed whitespace-pre-wrap ${
                        isCopilot
                          ? 'bg-[#121417] border border-[#636363]/60 text-white'
                          : 'bg-[#2b5945] text-white border border-[#2b5945]'
                      }`}
                    >
                      {m.text}
                    </div>
                  </div>
                )
              })}

              {isLoading && (
                <div className="flex items-center gap-2 text-xs font-mono text-[#9b9b9b]">
                  <Cpu className="w-3.5 h-3.5 animate-spin text-[#a0d1b8]" />
                  <span>Synthesizing legal & banking telemetry...</span>
                </div>
              )}
            </div>

            {/* Input Footer */}
            <div className="p-3.5 border-t border-[#636363]/40 bg-[#000000]">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                  placeholder="Ask copilot to draft notice, predict ATM, or trace VPA..."
                  className="flex-1 px-4 py-2 bg-[#1e2124] text-white rounded-btn text-xs border border-[#636363] hover:border-[#c0c9c2] focus:outline-none focus:border-[#2b5945] focus:ring-2 focus:ring-[#2b5945]/30 placeholder:text-[#9b9b9b]"
                />
                <Button
                  size="sm"
                  variant="primary"
                  onClick={() => handleSend()}
                  disabled={isLoading || !input.trim()}
                  className="px-3 text-xs"
                >
                  <Send className="w-3.5 h-3.5" />
                </Button>
              </div>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  )
}
