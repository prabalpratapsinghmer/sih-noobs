# Leaflet Heatmap — Implementation Spec

> Feature: `features/map/` in Command Center.
> Library: Leaflet.js + leaflet.heat + leaflet.markercluster.
> Tiles: OpenStreetMap (no API key). Mapbox GL is the upgrade path behind a thin wrapper.

---

## 1. Stack

| Package | Version | Purpose |
|---------|---------|---------|
| `leaflet` | ^1.9 | Core map |
| `react-leaflet` | ^4 | React bindings |
| `leaflet.heat` | bundled | Heatmap layer |
| `leaflet.markercluster` | bundled | Marker clustering |

---

## 2. MapProvider

Wraps the Leaflet map instance in React context so all child components can access it:

```tsx
// MapProvider.tsx
const MapContext = createContext<L.Map | null>(null);

export function MapProvider({ children, center, zoom }: Props) {
  const mapRef = useRef<L.Map>(null);
  useEffect(() => {
    mapRef.current = L.map('map-container', {
      center: [center.lat, center.lng], // default: Bangalore 12.97, 77.59
      zoom: zoom ?? 12,
      zoomControl: true,
      attributionControl: true,
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
      maxZoom: 18,
    }).addTo(mapRef.current);
    return () => mapRef.current?.remove();
  }, []);
  return <MapContext.Provider value={mapRef.current}>{children}</MapContext.Provider>;
}
```

---

## 3. ATM Markers

Each ATM from `GET /api/atms` becomes a circle marker:

```tsx
function AtmMarker({ atm }: { atm: AtmRisk }) {
  const color = atm.priority === 'crit' ? '#c02f45'
              : atm.priority === 'warn' ? '#a8640a'
              : '#16815f';
  const radius = atm.priority === 'crit' ? 10 : atm.priority === 'warn' ? 7 : 5;
  const marker = L.circleMarker([atm.lat, atm.lng], {
    radius,
    fillColor: color,
    color: '#fff',
    weight: 2,
    opacity: 1,
    fillOpacity: 0.85,
  });
  marker.bindPopup(() => ReactDOMServer.renderToString(<AtmPopup atm={atm} />));
  return null; // managed by react-leaflet
}
```

---

## 4. Heatmap Layer

```tsx
function HeatmapLayer({ atms }: { atms: AtmRisk[] }) {
  const heatRef = useRef<L.HeatLayer>();
  useEffect(() => {
    if (!map) return;
    const points = atms.map(a => [a.lat, a.lng, a.risk_score / 100] as [number, number, number]);
    heatRef.current = L.heatLayer(points, {
      radius: 25,
      blur: 15,
      maxZoom: 15,
      max: 1.0,
      gradient: { 0.2: '#16815f', 0.5: '#a8640a', 0.8: '#c02f45', 1.0: '#c02f45' },
    }).addTo(map);
    return () => { heatRef.current?.remove(); };
  }, [atms]);
  return null;
}
```

---

## 5. Clustering

```tsx
const clusterGroup = L.markerClusterGroup({
  maxClusterRadius: 50,
  spiderfyOnMaxZoom: true,
  showCoverageOnHover: false,
  iconCreateFunction: (cluster) => {
    const count = cluster.getChildCount();
    const maxRisk = getMaxRiskInCluster(cluster);
    const color = maxRisk >= 70 ? '#c02f45' : maxRisk >= 40 ? '#a8640a' : '#16815f';
    return L.divIcon({
      html: `<div class="cluster-icon" style="background:${color}">${count}</div>`,
      className: '',
      iconSize: [36, 36],
    });
  },
});
```

---

## 6. Filters

| Filter | Type | Default | API param |
|--------|------|---------|-----------|
| Min risk score | Slider (0–100) | 0 | `?min_risk=` |
| Area | Dropdown (from data) | All | `?area=` |
| Fraud type | Dropdown | All | `?fraud_type=` |
| Time range | Date range picker | Last 24h | `?since=` |

Filters debounced (300ms) → refetch `GET /api/atms?...` → update markers + heatmap.

---

## 7. Realtime Updates

On `prediction.new` WS event:
1. Parse new ATM data from payload.
2. Find existing marker by `atm_id` → update position/color/size.
3. If new ATM → add marker + animate entrance.
4. Update heatmap layer.
5. If high-risk → toast notification.

---

## 8. Performance

- **Marker clustering:** keep 500+ markers at 60fps.
- **Viewport culling:** only render markers visible in current viewport bounds (Leaflet handles this).
- **Debounced filters:** 300ms debounce prevents API spam on slider drag.
- **Heatmap recalc:** throttle to 500ms during filter changes.

---

## 9. Swap Path to Mapbox

All Leaflet usage is behind `MapProvider` + `HeatmapLayer` + `AtmMarker`. To swap:
1. Replace tile provider URL (requires Mapbox token).
2. Replace `L.heatLayer` with Mapbox `addLayer` heatmap style.
3. Replace circle markers with Mapbox `CircleMarker` equivalent.
4. Feature code (filters, popups, realtime) stays unchanged.
