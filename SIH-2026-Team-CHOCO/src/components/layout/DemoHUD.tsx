import { Play, Pause, Square, RotateCcw, Zap, Shield, MapPin, UserCheck, CheckCircle2, X, ChevronLeft, ChevronRight, Volume2 } from 'lucide-react'
import { useDemoStore } from '@/store/demoStore'
import { DEMO_STAGES } from '@/store/demoStore'
import { useState, useEffect } from 'react'
import { cn } from '@/lib/utils'

export function DemoHUD() {
  const {
    isDemoActive,
    isDemoRunning,
    isPlaying,
    currentStage,
    caseId,
    amount,
    allNodesFrozen,
    patrolDispatched,
    caseResolved,
    startDemo,
    stopDemo,
    pauseDemo,
    resumeDemo,
    resetDemo,
    setStage,
  } = useDemoStore()

  const [isExpanded, setIsExpanded] = useState(false)
  const [audioEnabled, setAudioEnabled] = useState(true)
  const [progress, setProgress] = useState(0)

  const currentStageInfo = DEMO_STAGES[currentStage - 1]

  // Audio context for chimes
  useEffect(() => {
    if (!audioEnabled) return

    const playChime = (frequency: number, duration: number) => {
      try {
        const audioCtx = new (window.AudioContext || (window as any).webkitAudioContext)()
        const oscillator = audioCtx.createOscillator()
        const gainNode = audioCtx.createGain()
        oscillator.connect(gainNode)
        gainNode.connect(audioCtx.destination)
        oscillator.frequency.value = frequency
        oscillator.type = 'sine'
        gainNode.gain.setValueAtTime(0.08, audioCtx.currentTime)
        gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration)
        oscillator.start(audioCtx.currentTime)
        oscillator.stop(audioCtx.currentTime + duration)
      } catch {
        // Audio not permitted without user gesture
      }
    }

    if (isPlaying && isDemoRunning) {
      playChime(880, 0.15)
      setTimeout(() => playChime(1320, 0.15), 150)
    }
  }, [currentStage, isPlaying, isDemoRunning, audioEnabled])

  // Auto-advance demo stages
  useEffect(() => {
    if (!isPlaying || !isDemoRunning) return

    const stageDuration = (currentStageInfo?.durationSec || 10) * 1000
    const startTime = Date.now()

    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime
      setProgress(Math.min(elapsed / stageDuration, 1))

      if (elapsed >= stageDuration) {
        if (currentStage < DEMO_STAGES.length) {
          setStage(currentStage + 1)
          setProgress(0)
        } else {
          pauseDemo()
          setProgress(1)
        }
      }
    }, 100)

    return () => clearInterval(interval)
  }, [currentStage, isPlaying, isDemoRunning, setStage, pauseDemo, currentStageInfo])

  if (!isDemoActive && !isDemoRunning) {
    return (
      <button
        onClick={startDemo}
        className="fixed bottom-6 right-6 z-50 inline-flex items-center gap-2 bg-white text-black hover:bg-black hover:text-white border border-white font-sans font-semibold text-xs px-4 py-2.5 rounded-btn shadow-floating transition-all duration-200"
        aria-label="Start Demo Scenario"
      >
        <Zap className="w-4 h-4 text-[#2b5945]" />
        <span>Run 5-Min Scenario</span>
      </button>
    )
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Collapsed HUD */}
      <div
        className={cn(
          'bg-black/30 backdrop-blur-md border border-[#636363] rounded-card shadow-floating transition-all duration-300 text-white',
          isExpanded ? 'w-96' : 'w-16'
        )}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-3 border-b border-[#636363]/40">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-[#38d39f]" />
            <span className="font-mono text-[11px] font-bold text-[#a0d1b8]">DEMO</span>
            {isExpanded && (
              <>
                <span className="font-mono text-mono-xs text-[#9b9b9b]">|</span>
                <span className="font-mono text-mono-xs font-medium text-white">
                  {isPlaying ? 'RUNNING' : isDemoRunning ? 'PAUSED' : 'READY'}
                </span>
              </>
            )}
          </div>
          <div className="flex items-center gap-1">
            {isExpanded && (
              <button
                onClick={() => setAudioEnabled(!audioEnabled)}
                className="p-1 rounded-btn hover:bg-[#2f3234] text-[#9b9b9b] hover:text-white transition-colors"
                aria-label={audioEnabled ? 'Mute demo audio' : 'Enable demo audio'}
              >
                <Volume2 className={cn('w-3.5 h-3.5', audioEnabled ? 'text-white' : 'text-[#636363]')} />
              </button>
            )}
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="p-1 rounded-btn hover:bg-[#2f3234] text-[#9b9b9b] hover:text-white transition-colors"
              aria-label={isExpanded ? 'Collapse demo panel' : 'Expand demo panel'}
            >
              {isExpanded ? <ChevronRight className="w-4 h-4" /> : <ChevronLeft className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Expanded Content */}
        {isExpanded && (
          <div className="p-3.5 space-y-3 animate-in fade-in duration-200">
            {/* Case Info */}
            <div className="bg-[#121417] border border-[#636363]/50 rounded-btn p-3">
              <div className="flex items-center justify-between mb-1.5">
                <span className="font-mono text-[11px] text-[#9b9b9b]">INCIDENT ID</span>
                <span className="font-mono text-xs font-bold text-white">{caseId}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="font-mono text-[11px] text-[#9b9b9b]">PRESERVED AT-RISK</span>
                <span className="font-mono text-sm font-bold text-[#fae0a6]">
                  ₹{amount.toLocaleString('en-IN')}
                </span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="space-y-1">
              <div className="flex items-center justify-between text-[11px] font-mono">
                <span className="text-[#9b9b9b]">STAGE PROGRESS</span>
                <span className="text-white">{Math.round(progress * 100)}%</span>
              </div>
              <div className="h-1 bg-black/40 backdrop-blur-sm rounded-pill overflow-hidden">
                <div
                  className="h-full bg-[#2b5945] transition-all duration-100 ease-linear"
                  style={{ width: `${progress * 100}%` }}
                />
              </div>
            </div>

            {/* Stage Timeline */}
            <div className="space-y-1.5 max-h-56 overflow-y-auto pr-1">
              {DEMO_STAGES.map((stage, index) => {
                const isCurrent = index + 1 === currentStage
                const isComplete = index + 1 < currentStage
                const stageStatus = isComplete ? 'complete' : isCurrent ? 'current' : 'pending'

                return (
                  <div
                    key={stage.stage}
                    className={cn(
                      'flex items-start gap-2.5 px-2.5 py-2 border-l-2 transition-colors',
                      isCurrent
                        ? 'bg-[#2b5945]/20 border-[#38d39f]'
                        : isComplete
                        ? 'bg-transparent border-[#2b5945]'
                        : 'bg-transparent border-transparent hover:bg-[#121417]'
                    )}
                  >
                    <div
                      className={cn(
                        'flex-shrink-0 w-5 h-5 rounded-full flex items-center justify-center font-mono text-[11px] font-bold mt-0.5',
                        stageStatus === 'complete' && 'bg-[#2b5945] text-white',
                        stageStatus === 'current' && 'bg-white text-black font-bold',
                        stageStatus === 'pending' && 'bg-black/40 backdrop-blur-sm border border-[#636363] text-[#9b9b9b]'
                      )}
                    >
                      {stageStatus === 'complete' ? (
                        <CheckCircle2 className="w-3 h-3 text-white" />
                      ) : (
                        stage.stage
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p
                        className={cn(
                          'font-mono text-xs font-semibold truncate',
                          stageStatus === 'complete' && 'text-[#a0d1b8]',
                          stageStatus === 'current' && 'text-white',
                          stageStatus === 'pending' && 'text-[#9b9b9b]'
                        )}
                      >
                        {stage.label}
                      </p>
                      <p className="font-sans text-[11px] text-[#9b9b9b] truncate">
                        {stage.desc}
                      </p>
                    </div>
                  </div>
                )
              })}
            </div>

            {/* Status Indicators */}
            <div className="grid grid-cols-3 divide-x divide-[#636363]/40 pt-2 border-t border-[#636363]/40">
              <div
                className={cn(
                  'py-2 px-1 text-center',
                  allNodesFrozen
                    ? 'text-[#a0d1b8]'
                    : 'text-[#9b9b9b]'
                )}
              >
                <Shield className="w-3.5 h-3.5 mx-auto mb-1" />
                <p className="font-mono text-[11px] font-bold">
                  {allNodesFrozen ? 'FROZEN' : 'ACTIVE'}
                </p>
              </div>
              <div
                className={cn(
                  'py-2 px-1 text-center',
                  patrolDispatched
                    ? 'text-[#fae0a6]'
                    : 'text-[#9b9b9b]'
                )}
              >
                <MapPin className="w-3.5 h-3.5 mx-auto mb-1" />
                <p className="font-mono text-[11px] font-bold">
                  {patrolDispatched ? 'DISPATCHED' : 'STANDBY'}
                </p>
              </div>
              <div
                className={cn(
                  'py-2 px-1 text-center',
                  caseResolved
                    ? 'text-[#a0d1b8]'
                    : 'text-[#9b9b9b]'
                )}
              >
                <UserCheck className="w-3.5 h-3.5 mx-auto mb-1" />
                <p className="font-mono text-[11px] font-bold">
                  {caseResolved ? 'RECOVERED' : 'INVESTIGATING'}
                </p>
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center gap-2 pt-2 border-t border-[#636363]/40">
              {isPlaying ? (
                <button
                  onClick={pauseDemo}
                  className="flex-1 inline-flex items-center justify-center gap-2 bg-[#121417] text-white border border-[#636363] hover:border-white text-xs font-semibold py-2 rounded-btn transition-colors"
                >
                  <Pause className="w-3.5 h-3.5" />
                  <span>Pause</span>
                </button>
              ) : (
                <button
                  onClick={isDemoRunning ? resumeDemo : startDemo}
                  className="flex-1 inline-flex items-center justify-center gap-2 bg-white text-black hover:bg-black hover:text-white border border-white text-xs font-semibold py-2 rounded-btn transition-colors"
                >
                  <Play className="w-3.5 h-3.5" />
                  <span>{isDemoRunning ? 'Resume' : 'Start'}</span>
                </button>
              )}
              <button
                onClick={stopDemo}
                className="p-2 bg-transparent text-[#ff4136] border border-[#994500] hover:bg-[#994500] hover:text-white rounded-btn transition-colors"
                aria-label="Stop demo"
                title="Stop Scenario"
              >
                <Square className="w-3.5 h-3.5" />
              </button>
              <button
                onClick={resetDemo}
                className="p-2 bg-transparent text-[#9b9b9b] border border-[#636363] hover:text-white hover:border-white rounded-btn transition-colors"
                aria-label="Reset demo"
                title="Reset Scenario"
              >
                <RotateCcw className="w-3.5 h-3.5" />
              </button>
            </div>

            {/* Stage Selector Pills */}
            <div className="grid grid-cols-3 gap-1 pt-1">
              {DEMO_STAGES.map((stage) => (
                <button
                  key={stage.stage}
                  onClick={() => setStage(stage.stage)}
                  className={cn(
                    'py-1 text-center font-mono text-[11px] rounded-btn border transition-colors',
                    currentStage === stage.stage
                      ? 'bg-white text-black border-white font-bold'
                      : 'bg-[#121417] text-[#9b9b9b] border-[#636363]/40 hover:text-white hover:border-[#636363]'
                  )}
                >
                  {stage.stage.toString().padStart(2, '0')}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}