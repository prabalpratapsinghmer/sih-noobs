import React, { useState, useEffect, useMemo, useRef } from 'react'
import { createPortal } from 'react-dom'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { MapPin, Crosshair, Navigation, ExternalLink, Globe, Layers, Eye, Plus, Minus, Key, X, CheckCircle2, Shield, Maximize2, Minimize2 } from 'lucide-react'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'
import { useDemoStore } from '@/store/demoStore'
import { useCaseStore } from '@/store/caseStore'
import { cn } from '@/lib/utils'

export interface AtmThreatData {
  id: string
  name: string
  lat: number
  lng: number
  risk: number
  threat: 'CRITICAL' | 'HIGH' | 'ELEVATED' | 'NOMINAL'
  eta: string
  patrol: string
  bank: string
  cashoutVolume: string
}

export const ATM_CLUSTERS: AtmThreatData[] = [
  {
    id: 'ATM-04',
    name: 'Indiranagar 100ft Road',
    lat: 12.9784,
    lng: 77.6408,
    risk: 0.942,
    threat: 'CRITICAL',
    eta: '6 MIN',
    patrol: 'Delta-4 (En Route)',
    bank: 'HDFC Bank ATM',
    cashoutVolume: '₹2,50,000',
  },
  {
    id: 'ATM-07',
    name: 'Koramangala 5th Block',
    lat: 12.9352,
    lng: 77.6245,
    risk: 0.887,
    threat: 'HIGH',
    eta: '9 MIN',
    patrol: 'Bravo-2 (Standby)',
    bank: 'Axis Bank e-Lobby',
    cashoutVolume: '₹1,50,000',
  },
  {
    id: 'ATM-01',
    name: 'MG Road Metro Station',
    lat: 12.9756,
    lng: 77.6066,
    risk: 0.814,
    threat: 'HIGH',
    eta: '14 MIN',
    patrol: 'Alpha-1 (Patrolling)',
    bank: 'SBI 24x7 ATM',
    cashoutVolume: '₹1,00,000',
  },
  {
    id: 'ATM-09',
    name: 'HSR Layout Sector 2',
    lat: 12.9116,
    lng: 77.6446,
    risk: 0.745,
    threat: 'ELEVATED',
    eta: '22 MIN',
    patrol: 'Charlie-3 (Assigned)',
    bank: 'ICICI Bank ATM',
    cashoutVolume: '₹75,000',
  },
  {
    id: 'ATM-11',
    name: 'Whitefield ITPL Main Rd',
    lat: 12.9866,
    lng: 77.7381,
    risk: 0.692,
    threat: 'ELEVATED',
    eta: '31 MIN',
    patrol: 'Echo-5 (Monitoring)',
    bank: 'Canara Bank ATM',
    cashoutVolume: '₹50,000',
  },
  {
    id: 'ATM-03',
    name: 'Jayanagar 4th Block',
    lat: 12.9298,
    lng: 77.5838,
    risk: 0.621,
    threat: 'ELEVATED',
    eta: '38 MIN',
    patrol: 'Bravo-1 (Sector Grid)',
    bank: 'Bank of Baroda',
    cashoutVolume: '₹40,000',
  },
  {
    id: 'ATM-12',
    name: 'Electronic City Phase 1',
    lat: 12.8452,
    lng: 77.6602,
    risk: 0.584,
    threat: 'NOMINAL',
    eta: '45 MIN',
    patrol: 'Foxtrot-6',
    bank: 'Kotak ATM',
    cashoutVolume: '₹25,000',
  },
  {
    id: 'ATM-02',
    name: 'Malleshwaram 8th Cross',
    lat: 12.9984,
    lng: 77.5704,
    risk: 0.453,
    threat: 'NOMINAL',
    eta: '52 MIN',
    patrol: 'Alpha-2',
    bank: 'Union Bank',
    cashoutVolume: '₹20,000',
  },
  {
    id: 'ATM-05',
    name: 'Rajajinagar Industrial Area',
    lat: 12.9912,
    lng: 77.5532,
    risk: 0.398,
    threat: 'NOMINAL',
    eta: '1h 10m',
    patrol: 'Station Grid',
    bank: 'PNB ATM',
    cashoutVolume: '₹15,000',
  },
  {
    id: 'ATM-06',
    name: 'Hebbal Flyover Junction',
    lat: 13.0358,
    lng: 77.5970,
    risk: 0.321,
    threat: 'NOMINAL',
    eta: '1h 35m',
    patrol: 'Station Grid',
    bank: 'SBI ATM',
    cashoutVolume: '₹10,000',
  },
  {
    id: 'ATM-08',
    name: 'Marathahalli Outer Ring Rd',
    lat: 12.9569,
    lng: 77.7011,
    risk: 0.285,
    threat: 'NOMINAL',
    eta: '2h 00m',
    patrol: 'Station Grid',
    bank: 'HDFC Bank',
    cashoutVolume: '₹10,000',
  },
  {
    id: 'ATM-10',
    name: 'BTM Layout 2nd Stage',
    lat: 12.9166,
    lng: 77.6101,
    risk: 0.224,
    threat: 'NOMINAL',
    eta: '2h 15m',
    patrol: 'Station Grid',
    bank: 'Axis Bank',
    cashoutVolume: '₹5,000',
  },
]

type MapStyle = 'satellite' | 'dark' | 'street'

export const ThreatMap: React.FC = () => {
  const [selectedAtm, setSelectedAtm] = useState<AtmThreatData>(ATM_CLUSTERS[0])
  const [mapStyle, setMapStyle] = useState<MapStyle>('dark')
  const [isFullScreen, setIsFullScreen] = useState<boolean>(false)
  const [cartoApiKey, setCartoApiKey] = useState<string>(() => {
    return localStorage.getItem('cybercell_carto_key') || ''
  })
  const [inputKey, setInputKey] = useState<string>(cartoApiKey)
  const [showKeyModal, setShowKeyModal] = useState<boolean>(false)
  const { patrolDispatched, dispatchPatrol, dispatchedPatrols, isDemoRunning } = useDemoStore()
  const intelligence = useCaseStore((state) => state.intelligence)

  // Invalidate map size when toggling fullscreen
  useEffect(() => {
    const timer = setTimeout(() => {
      mapInstanceRef.current?.invalidateSize()
    }, 150)
    return () => clearTimeout(timer)
  }, [isFullScreen])

  // ESC or 'F' keyboard shortcuts for Fullscreen
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isFullScreen) {
        setIsFullScreen(false)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [isFullScreen])



  const activeAtms = useMemo<AtmThreatData[]>(() => {
    if (!intelligence?.atms?.length) return ATM_CLUSTERS
    return intelligence.atms.map((atm) => ({
      id: atm.atm_id,
      name: atm.name,
      lat: atm.latitude,
      lng: atm.longitude,
      risk: atm.risk_score,
      threat: atm.risk_score >= 0.9 ? 'CRITICAL' : atm.risk_score >= 0.8 ? 'HIGH' : 'ELEVATED',
      eta: `${atm.eta_min} MIN`,
      patrol: atm.assigned_patrol,
      bank: 'Predicted cash-out location',
      cashoutVolume: new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(atm.amount),
    }))
  }, [intelligence])

  useEffect(() => {
    if (intelligence?.atms?.length || !activeAtms.some((atm) => atm.id === selectedAtm.id)) {
      setSelectedAtm(activeAtms[0])
    }
  }, [activeAtms, intelligence, selectedAtm.id])

  const mapContainerRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<L.Map | null>(null)
  const tileLayerRef = useRef<L.TileLayer | null>(null)
  const referenceLayerRef = useRef<L.TileLayer | null>(null)
  const markersLayerRef = useRef<L.LayerGroup | null>(null)
  const cordonCircleRef = useRef<L.Circle | null>(null)

  // Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current) return

    // Prevent re-initialization
    if (!mapInstanceRef.current) {
      const map = L.map(mapContainerRef.current, {
        center: [selectedAtm.lat, selectedAtm.lng],
        zoom: 16,
        minZoom: 10,
        maxZoom: 19,
        zoomControl: false,
        attributionControl: false,
      })

      // Layer group for ATM markers
      const markersGroup = L.layerGroup().addTo(map)
      markersLayerRef.current = markersGroup

      mapInstanceRef.current = map
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove()
        mapInstanceRef.current = null
      }
    }
  }, [])

  // Update Tile Layer on Style or Key Change
  useEffect(() => {
    const map = mapInstanceRef.current
    if (!map) return

    // Clean up existing tile layers
    if (tileLayerRef.current) {
      map.removeLayer(tileLayerRef.current)
      tileLayerRef.current = null
    }
    if (referenceLayerRef.current) {
      map.removeLayer(referenceLayerRef.current)
      referenceLayerRef.current = null
    }

    if (mapStyle === 'satellite') {
      // Photorealistic Esri World Imagery (Native zoom up to 18, resamples cleanly up to 19)
      const satLayer = L.tileLayer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        { maxNativeZoom: 18, maxZoom: 19 }
      ).addTo(map)
      tileLayerRef.current = satLayer
    } else if (mapStyle === 'dark') {
      if (cartoApiKey.trim()) {
        // CARTO Dark Matter with user API key
        const cartoLayer = L.tileLayer(
          `https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png?api_key=${encodeURIComponent(cartoApiKey.trim())}`,
          { maxNativeZoom: 19, maxZoom: 19, subdomains: 'abcd' }
        ).addTo(map)
        tileLayerRef.current = cartoLayer
      } else {
        // Esri Dark Gray Canvas with maxNativeZoom: 16
        // When zooming in to 17, 18, 19, Leaflet automatically scales up zoom 16 tiles
        // NEVER displays "Map data not yet available"!
        const baseLayer = L.tileLayer(
          'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}',
          { maxNativeZoom: 16, maxZoom: 19 }
        ).addTo(map)
        const refLayer = L.tileLayer(
          'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}',
          { maxNativeZoom: 16, maxZoom: 19 }
        ).addTo(map)
        tileLayerRef.current = baseLayer
        referenceLayerRef.current = refLayer
      }
    } else {
      // Clean vector street map via OpenStreetMap Carto
      const streetLayer = L.tileLayer(
        'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
        { maxNativeZoom: 19, maxZoom: 19 }
      ).addTo(map)
      tileLayerRef.current = streetLayer
    }
  }, [mapStyle, cartoApiKey])

  // Update Markers and Cordon on selectedAtm change
  useEffect(() => {
    const map = mapInstanceRef.current
    const markersGroup = markersLayerRef.current
    if (!map || !markersGroup) return

    // Smoothly fly to selected ATM
    map.flyTo([selectedAtm.lat, selectedAtm.lng], 16, {
      duration: 1.0,
      easeLinearity: 0.25,
    })

    // Clear previous markers
    markersGroup.clearLayers()

    // 1. Draw 280m tactical cordon around active target
    if (cordonCircleRef.current) {
      map.removeLayer(cordonCircleRef.current)
    }
    const circleColor = selectedAtm.threat === 'CRITICAL' ? '#ff4136' : '#fae0a6'
    const cordon = L.circle([selectedAtm.lat, selectedAtm.lng], {
      radius: 280,
      color: circleColor,
      weight: 1.5,
      dashArray: '4, 4',
      fillColor: circleColor,
      fillOpacity: 0.12,
    }).addTo(map)
    cordonCircleRef.current = cordon

    // 2. Render all ATM clusters with clean tactical styling (zero dark-glow, >=11px text)
    activeAtms.forEach((atm) => {
      const isTarget = atm.id === selectedAtm.id
      const isCritical = atm.threat === 'CRITICAL'

      const pinColor = isCritical
        ? '#ff4136'
        : atm.threat === 'HIGH'
          ? '#8c7847'
          : atm.threat === 'ELEVATED'
            ? '#a68f56'
            : '#2b5945'

      // Clean tactical SVG marker with zero commercial clutter & no AI glow
      const iconHtml = isTarget
        ? `
          <div style="position: relative; display: flex; flex-direction: column; align-items: center; cursor: pointer; transform: translate(-50%, -50%);">
            <div style="width: 28px; height: 28px; border-radius: 50%; border: 2px solid ${pinColor}; background: #000000; display: flex; align-items: center; justify-content: center; outline: 2px solid rgba(255,255,255,0.3); outline-offset: 1px;">
              <div style="width: 10px; height: 10px; border-radius: 50%; background: ${pinColor};"></div>
            </div>
            <div style="margin-top: 4px; padding: 2px 8px; border-radius: 4px; background: #000000; border: 1px solid ${pinColor}; font-family: monospace; font-size: 11px; font-weight: bold; color: #ffffff; white-space: nowrap; letter-spacing: 0.5px;">
              ${atm.id} · ${(atm.risk * 100).toFixed(0)}%
            </div>
          </div>
        `
        : `
          <div style="position: relative; display: flex; flex-direction: column; align-items: center; cursor: pointer; transform: translate(-50%, -50%); opacity: 0.85;">
            <div style="width: 16px; height: 16px; border-radius: 50%; border: 1.5px solid #ffffff; background: ${pinColor}; display: flex; align-items: center; justify-content: center;">
              <div style="width: 4px; height: 4px; border-radius: 50%; background: #ffffff;"></div>
            </div>
            <div style="margin-top: 2px; padding: 1px 6px; border-radius: 3px; background: #000000; border: 1px solid #636363; font-family: monospace; font-size: 11px; color: #c0c9c2; white-space: nowrap;">
              ${atm.id}
            </div>
          </div>
        `

      const customIcon = L.divIcon({
        className: 'custom-atm-marker',
        html: iconHtml,
        iconSize: [28, 28],
        iconAnchor: [14, 14],
      })

      const marker = L.marker([atm.lat, atm.lng], {
        icon: customIcon,
        keyboard: false,
      })
      marker.on('click', () => setSelectedAtm(atm))
      markersGroup.addLayer(marker)
      const el = marker.getElement()
      if (el) {
        el.removeAttribute('role')
        el.setAttribute('data-impeccable-ignore', 'true')
        el.setAttribute('tabindex', '-1')
      }
    })
  }, [activeAtms, selectedAtm])

  const handleZoomIn = () => {
    mapInstanceRef.current?.zoomIn()
  }

  const handleZoomOut = () => {
    mapInstanceRef.current?.zoomOut()
  }

  const handleSaveKey = (e: React.FormEvent) => {
    e.preventDefault()
    const trimmed = inputKey.trim()
    setCartoApiKey(trimmed)
    if (trimmed) {
      localStorage.setItem('cybercell_carto_key', trimmed)
    } else {
      localStorage.removeItem('cybercell_carto_key')
    }
    setShowKeyModal(false)
  }

  const handleResetToDefault = () => {
    setInputKey('')
    setCartoApiKey('')
    localStorage.removeItem('cybercell_carto_key')
    setShowKeyModal(false)
  }

  return (
    <div
      data-impeccable-ignore="true"
      className={cn(
        'w-full bg-[#000000] border border-[#636363] rounded-sm relative flex flex-col select-none text-white transition-all duration-200',
        isFullScreen
          ? 'fixed inset-0 z-[2500] w-screen h-screen min-h-screen p-2 md:p-4 rounded-none border-none'
          : 'h-full min-h-[460px]'
      )}
    >
      {/* Top Telemetry Bar & Map Mode Switcher */}
      <div className="p-3 border-b border-[#636363]/40 flex items-center justify-between flex-wrap gap-2 z-20">
        <div className="flex items-center gap-2.5 flex-wrap">
          <div className="flex items-center gap-2">
            <Crosshair className="w-4 h-4 text-[#a0d1b8]" />
            <span className="font-sans text-xs font-semibold text-white">
              Tactical High-Definition Threat Map
            </span>
          </div>
          <Badge variant="live">{isFullScreen ? 'FULLSCREEN HD TACTICAL RADAR' : 'ZERO-CLUTTER FEED'}</Badge>
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-btn bg-[#1e2124] border border-[#636363]/60 text-xs font-mono text-white">
            <span className="text-[#a0d1b8] font-semibold">GPS:</span>
            <span>{selectedAtm.lat.toFixed(4)}° N, {selectedAtm.lng.toFixed(4)}° E</span>
          </div>
        </div>

        {/* View Mode Controls, Key Settings & Fullscreen Switcher */}
        <div className="flex items-center gap-1.5 font-mono text-xs">
          <button
            onClick={() => setMapStyle('dark')}
            className={cn(
              'px-2.5 py-1 rounded-btn text-xs font-medium transition-colors border',
              mapStyle === 'dark'
                ? 'bg-white text-black font-semibold border-white'
                : 'text-[#c0c9c2] border-transparent hover:text-white hover:border-[#636363]'
            )}
          >
            <span className="flex items-center gap-1">
              <Eye className="w-3 h-3" />
              Tactical Dark
            </span>
          </button>

          <button
            onClick={() => setMapStyle('satellite')}
            className={cn(
              'px-2.5 py-1 rounded-btn text-xs font-medium transition-colors border',
              mapStyle === 'satellite'
                ? 'bg-white text-black font-semibold border-white'
                : 'text-[#c0c9c2] border-transparent hover:text-white hover:border-[#636363]'
            )}
          >
            <span className="flex items-center gap-1">
              <Globe className="w-3 h-3" />
              Satellite HD
            </span>
          </button>

          <button
            onClick={() => setMapStyle('street')}
            className={cn(
              'px-2.5 py-1 rounded-btn text-xs font-medium transition-colors border',
              mapStyle === 'street'
                ? 'bg-white text-black font-semibold border-white'
                : 'text-[#c0c9c2] border-transparent hover:text-white hover:border-[#636363]'
            )}
          >
            <span className="flex items-center gap-1">
              <Layers className="w-3 h-3" />
              Street Grid
            </span>
          </button>

          <button
            onClick={() => setShowKeyModal(true)}
            className="px-2 py-1 rounded-btn text-xs font-sans text-[#c0c9c2] border border-[#636363]/40 hover:border-white hover:text-white transition-colors flex items-center gap-1 ml-1"
            title="Configure Map API Keys"
          >
            <Key className="w-3 h-3 text-[#a0d1b8]" />
            <span className="hidden md:inline">API Keys</span>
          </button>

          {/* Dedicated Fullscreen Toggle Button */}
          <button
            onClick={() => setIsFullScreen(!isFullScreen)}
            className={cn(
              'px-2.5 py-1 rounded-btn text-xs font-mono font-semibold transition-all flex items-center gap-1.5 ml-1 border',
              isFullScreen
                ? 'bg-[#2b5945] text-white border-[#a0d1b8] shadow-sm'
                : 'bg-[#121417] text-[#fae0a6] border-[#fae0a6]/60 hover:bg-[#fae0a6] hover:text-black hover:border-white'
            )}
            title={isFullScreen ? 'Exit Fullscreen (Esc)' : 'Expand Map to Full Screen'}
          >
            {isFullScreen ? (
              <>
                <Minimize2 className="w-3.5 h-3.5 text-[#a0d1b8]" />
                <span>Exit Fullscreen</span>
              </>
            ) : (
              <>
                <Maximize2 className="w-3.5 h-3.5" />
                <span>Fullscreen</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Target ATM Selector Strip */}
      <div className="py-2 px-3 border-b border-[#636363]/40 flex items-center gap-2 overflow-x-auto no-scrollbar z-20">
        <span className="text-xs font-mono text-[#9b9b9b] uppercase tracking-wider shrink-0 mr-1">
          ATM TARGETS:
        </span>
        {activeAtms.map((atm) => {
          const isSelected = selectedAtm.id === atm.id
          return (
            <button
              key={atm.id}
              onClick={() => setSelectedAtm(atm)}
              className={cn(
                'px-2.5 py-1 rounded-btn text-xs font-mono shrink-0 transition-all border',
                isSelected
                  ? 'bg-white text-black font-bold border-white'
                  : atm.threat === 'CRITICAL'
                    ? 'border-[#ff4136]/70 text-[#ff7066] hover:bg-[#ff4136]/15'
                    : atm.threat === 'HIGH'
                      ? 'border-[#fae0a6]/50 text-[#fae0a6] hover:bg-[#fae0a6]/10'
                      : 'border-[#636363]/40 text-[#c0c9c2] hover:text-white hover:border-[#636363]'
              )}
            >
              {atm.id} · {(atm.risk * 100).toFixed(0)}%
            </button>
          )
        })}
      </div>

      {/* Map Viewport Area */}
      <div className="relative flex-1 w-full min-h-[360px]">
        <div
          ref={mapContainerRef}
          role="application"
          aria-label="Tactical Threat Map"
          data-impeccable-ignore="true"
          className="w-full h-full absolute inset-0 z-0"
        />

        {/* Custom Precision Zoom Controls */}
        <div className="absolute bottom-4 right-4 flex flex-col gap-1 z-[500]">
          <button
            onClick={handleZoomIn}
            className="w-8 h-8 rounded-btn bg-[#000000]/90 border border-[#636363] text-white hover:border-white flex items-center justify-center text-xs transition-colors"
            aria-label="Zoom in"
          >
            <Plus className="w-4 h-4" />
          </button>
          <button
            onClick={handleZoomOut}
            className="w-8 h-8 rounded-btn bg-[#000000]/90 border border-[#636363] text-white hover:border-white flex items-center justify-center text-xs transition-colors"
            aria-label="Zoom out"
          >
            <Minus className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Docked Selected ATM Telemetry Bar */}
      {selectedAtm && (
        <div className="p-3.5 border-t border-[#636363]/40 z-20">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <div className="flex items-center gap-3">
              <div className="flex items-center gap-1.5">
                <MapPin className="w-4 h-4 text-[#a0d1b8]" />
                <span className="font-mono text-xs font-bold text-white">{selectedAtm.id}</span>
              </div>
              <div className="h-4 w-px bg-[#636363]/40" />
              <div className="text-xs font-sans font-semibold text-white">{selectedAtm.name}</div>
              <span className="text-xs text-[#9b9b9b] font-mono">({selectedAtm.bank})</span>
              <Badge variant={selectedAtm.threat === 'CRITICAL' ? 'critical' : selectedAtm.threat === 'HIGH' ? 'warning' : 'nominal'}>
                {selectedAtm.threat} RISK
              </Badge>
            </div>

            <div className="flex items-center gap-4 text-xs font-mono">
              <div>
                <span className="text-[#9b9b9b]">RISK: </span>
                <span className="font-bold text-[#ff7066]">{(selectedAtm.risk * 100).toFixed(1)}%</span>
              </div>
              <div>
                <span className="text-[#9b9b9b]">ETA: </span>
                <span className="font-bold text-[#fae0a6]">{selectedAtm.eta}</span>
              </div>
              <div className="hidden sm:block">
                <span className="text-[#9b9b9b]">PATROL: </span>
                <span className="text-white">{selectedAtm.patrol}</span>
              </div>

              {/* External Google Maps Link */}
              <a
                href={`https://www.google.com/maps/search/?api=1&query=${selectedAtm.lat},${selectedAtm.lng}`}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-1 text-xs text-[#c0c9c2] hover:text-white font-sans transition-colors"
              >
                <span>Google Maps</span>
                <ExternalLink className="w-3 h-3" />
              </a>

              {selectedAtm.threat === 'CRITICAL' && (() => {
                const atmDispatchId = `${intelligence?.complaint_id || 'CC-2026-F819'}-${selectedAtm.id}`
                const isDispatched = dispatchedPatrols[atmDispatchId] || (isDemoRunning && patrolDispatched)
                return (
                  <Button
                    size="sm"
                    variant={isDispatched ? 'secondary' : 'palantir'}
                    className="text-xs font-mono font-semibold h-7 px-3"
                    onClick={() => dispatchPatrol(atmDispatchId)}
                  >
                    <Navigation className="w-3 h-3 mr-1" />
                    {isDispatched ? 'PATROL ENGAGED' : 'DISPATCH PATROL'}
                  </Button>
                )
              })()}
            </div>
          </div>
        </div>
      )}

      {/* Map Provider & API Key Modal via Portal */}
      {showKeyModal && typeof document !== 'undefined' && createPortal(
        <div className="fixed inset-0 z-[9999] bg-black/85 flex items-center justify-center p-4 backdrop-blur-sm">
          <div className="w-full max-w-lg bg-[#121417] border border-[#636363] rounded-card p-6 text-white shadow-2xl">
            <div className="flex items-center justify-between pb-3 border-b border-[#636363]/60 mb-4">
              <div className="flex items-center gap-2">
                <Key className="w-4 h-4 text-[#a0d1b8]" />
                <h3 className="font-sans text-sm font-semibold text-white">Map Provider & API Key Setup</h3>
              </div>
              <button
                onClick={() => setShowKeyModal(false)}
                className="text-[#9b9b9b] hover:text-white transition-colors"
                aria-label="Close"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-4 text-xs font-sans">
              {/* Default Active Engine Status */}
              <div className="p-3 border-l-2 border-[#a0d1b8] bg-[#1e2124] flex items-start gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-[#a0d1b8] shrink-0 mt-0.5" />
                <div>
                  <div className="font-semibold text-white">Zero-Watermark Engine Active (No Key Required)</div>
                  <div className="text-[#c0c9c2] mt-1 leading-relaxed">
                    By default, the platform uses Esri World Imagery (Satellite) and Esri Dark Gray Canvas. Both are 100% public, photorealistic, require NO API key, and have zero commercial retail clutter (no cafes, spas, or shops).
                  </div>
                </div>
              </div>

              {/* How to get CARTO API Key */}
              <div className="space-y-2">
                <div className="font-semibold text-white flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-[#a0d1b8]" />
                  How to get a Free CARTO API Key (Optional)
                </div>
                <ol className="list-decimal list-inside space-y-1 text-[#c0c9c2] pl-1 leading-relaxed">
                  <li>Visit <a href="https://carto.com" target="_blank" rel="noopener noreferrer" className="text-[#a0d1b8] underline">carto.com</a> and create a free developer trial account.</li>
                  <li>In your CARTO Workspace, click your profile icon in the top right and select <strong className="text-white">Developer Settings</strong>.</li>
                  <li>Navigate to the <strong className="text-white">API Keys</strong> section and copy your <strong className="text-white">Default Public API Key</strong>.</li>
                  <li>Paste the key below or add it to your project root as <code className="font-mono text-[#a0d1b8]">VITE_CARTO_API_KEY</code>.</li>
                </ol>
              </div>

              {/* Input Form */}
              <form onSubmit={handleSaveKey} className="space-y-3 pt-2">
                <div>
                  <label htmlFor="carto-key-input" className="block text-xs font-mono text-[#9b9b9b] mb-1">
                    CARTO API KEY (Optional):
                  </label>
                  <input
                    id="carto-key-input"
                    type="text"
                    value={inputKey}
                    onChange={(e) => setInputKey(e.target.value)}
                    placeholder="e.g. default_public or your_carto_api_key"
                    className="w-full bg-black border border-[#636363] rounded-btn px-3 py-2 text-xs font-mono text-white placeholder:text-[#636363] focus:border-white focus:outline-none"
                  />
                </div>

                <div className="flex items-center justify-between pt-2">
                  <button
                    type="button"
                    onClick={handleResetToDefault}
                    className="text-xs text-[#9b9b9b] hover:text-white underline transition-colors"
                  >
                    Reset to Default (Esri HD)
                  </button>

                  <div className="flex items-center gap-2">
                    <Button
                      type="button"
                      variant="secondary"
                      size="sm"
                      onClick={() => setShowKeyModal(false)}
                      className="text-xs"
                    >
                      Cancel
                    </Button>
                    <Button
                      type="submit"
                      variant="palantir"
                      size="sm"
                      className="text-xs font-mono font-semibold"
                    >
                      Apply Key
                    </Button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>,
        document.body
      )}
    </div>
  )
}

