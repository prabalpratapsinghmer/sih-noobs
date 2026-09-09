import { useEffect } from 'react';
import { MapContainer, TileLayer, useMap, Marker, Popup } from 'react-leaflet';
import MarkerClusterGroup from 'react-leaflet-cluster';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.heat';

// Fix for default Leaflet marker icons in React setups
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

L.Icon.Default.mergeOptions({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
});

// Custom Heatmap Layer Hook
function HeatmapLayer({ points }: { points: [number, number, number][] }) {
  const map = useMap();
  useEffect(() => {
    if (!points || points.length === 0) return;
    
    
    const heat = L.heatLayer(points, { 
      radius: 25, 
      blur: 15, 
      maxZoom: 17,
      gradient: { 0.4: 'blue', 0.6: 'cyan', 0.7: 'lime', 0.8: 'yellow', 1.0: 'red' }
    }).addTo(map);

    return () => { map.removeLayer(heat); };
  }, [map, points]);
  
  return null;
}

// Mock ATM Data (Bengaluru Coordinates to match Member 1's ML synthesis strategy)
const MOCK_ATMS = [
  { id: 'A1', lat: 12.9716, lng: 77.5946, risk: 95, name: 'Indiranagar ATM #452' },
  { id: 'A2', lat: 12.9352, lng: 77.6245, risk: 45, name: 'Koramangala ATM #112' },
  { id: 'A3', lat: 12.9279, lng: 77.6271, risk: 88, name: 'Madiwala ATM #99' },
  { id: 'A4', lat: 12.9783, lng: 77.6408, risk: 92, name: 'CV Raman Nagar ATM' },
];

export function LiveMap() {
  const center: [number, number] = [12.95, 77.61]; // Bengaluru Center
  
  // Format for heat layer: [lat, lng, intensity (0 to 1)]
  const heatPoints = MOCK_ATMS.map(atm => [atm.lat, atm.lng, atm.risk / 100] as [number, number, number]);

  return (
    <div className="w-full h-full relative z-0">
      <MapContainer center={center} zoom={12} className="w-full h-full rounded-md" zoomControl={false}>
        <TileLayer
          attribution='&copy; OpenStreetMap'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {/* Render the Heatmap gradients underneath the pins */}
        <HeatmapLayer points={heatPoints} />
        
        {/* Render the pins with automatic clustering for high density */}
        <MarkerClusterGroup chunkedLoading>
          {MOCK_ATMS.map(atm => (
            <Marker key={atm.id} position={[atm.lat, atm.lng]}>
              <Popup>
                <div className="font-sans min-w-[150px]">
                  <h4 className="font-bold text-sm text-ink">{atm.name}</h4>
                  <div className="flex justify-between items-center mt-2">
                    <span className="text-xs text-muted">Risk Score:</span>
                    <span className={`text-xs font-bold ${atm.risk > 80 ? 'text-crit' : 'text-warn'}`}>
                      {atm.risk}%
                    </span>
                  </div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MarkerClusterGroup>
      </MapContainer>
    </div>
  );
}
