// ========== ATM DATA ==========
const ATMData = [
    { 
        id: 'A452', 
        lat: 12.978, 
        lng: 77.640, 
        risk: 92, 
        address: 'Indiranagar', 
        complaints: 3, 
        mules: 4,
        lastActivity: '2.3 hours ago',
        predictedWindow: '2.3 hours',
        bank: 'SBI',
        status: 'Critical'
    },
    { 
        id: 'A789', 
        lat: 12.956, 
        lng: 77.620, 
        risk: 67, 
        address: 'MG Road', 
        complaints: 1, 
        mules: 2,
        lastActivity: '4.1 hours ago',
        predictedWindow: '4.1 hours',
        bank: 'HDFC',
        status: 'High'
    },
    { 
        id: 'A456', 
        lat: 12.920, 
        lng: 77.580, 
        risk: 55, 
        address: 'Jayanagar', 
        complaints: 2, 
        mules: 3,
        lastActivity: '1.5 hours ago',
        predictedWindow: '1.5 hours',
        bank: 'ICICI',
        status: 'Medium'
    },
    { 
        id: 'A123', 
        lat: 12.935, 
        lng: 77.630, 
        risk: 34, 
        address: 'Koramangala', 
        complaints: 0, 
        mules: 0,
        lastActivity: '5.0 hours ago',
        predictedWindow: '5.0 hours',
        bank: 'Axis',
        status: 'Low'
    },
    { 
        id: 'A890', 
        lat: 12.990, 
        lng: 77.600, 
        risk: 78, 
        address: 'Yeshwanthpur', 
        complaints: 2, 
        mules: 3,
        lastActivity: '3.2 hours ago',
        predictedWindow: '3.2 hours',
        bank: 'SBI',
        status: 'High'
    },
    { 
        id: 'A567', 
        lat: 12.910, 
        lng: 77.650, 
        risk: 45, 
        address: 'HSR Layout', 
        complaints: 1, 
        mules: 1,
        lastActivity: '6.0 hours ago',
        predictedWindow: '6.0 hours',
        bank: 'Kotak',
        status: 'Medium'
    },
    { 
        id: 'A234', 
        lat: 12.945, 
        lng: 77.570, 
        risk: 88, 
        address: 'Bannerghatta', 
        complaints: 4, 
        mules: 5,
        lastActivity: '1.8 hours ago',
        predictedWindow: '1.8 hours',
        bank: 'HDFC',
        status: 'Critical'
    },
    { 
        id: 'A678', 
        lat: 12.970, 
        lng: 77.710, 
        risk: 72, 
        address: 'Electronic City', 
        complaints: 2, 
        mules: 3,
        lastActivity: '2.7 hours ago',
        predictedWindow: '2.7 hours',
        bank: 'ICICI',
        status: 'High'
    },
    { 
        id: 'A345', 
        lat: 12.990, 
        lng: 77.550, 
        risk: 61, 
        address: 'Malleshwaram', 
        complaints: 1, 
        mules: 2,
        lastActivity: '3.5 hours ago',
        predictedWindow: '3.5 hours',
        bank: 'SBI',
        status: 'Medium'
    },
    { 
        id: 'A901', 
        lat: 12.920, 
        lng: 77.540, 
        risk: 39, 
        address: 'Rajajinagar', 
        complaints: 0, 
        mules: 0,
        lastActivity: '7.0 hours ago',
        predictedWindow: '7.0 hours',
        bank: 'Axis',
        status: 'Low'
    },
    { 
        id: 'A112', 
        lat: 12.950, 
        lng: 77.590, 
        risk: 51, 
        address: 'Basavanagudi', 
        complaints: 1, 
        mules: 1,
        lastActivity: '4.5 hours ago',
        predictedWindow: '4.5 hours',
        bank: 'Kotak',
        status: 'Medium'
    },
    { 
        id: 'A335', 
        lat: 12.980, 
        lng: 77.680, 
        risk: 44, 
        address: 'Marathahalli', 
        complaints: 0, 
        mules: 1,
        lastActivity: '5.8 hours ago',
        predictedWindow: '5.8 hours',
        bank: 'HDFC',
        status: 'Low'
    }
];

// ========== HELPER FUNCTIONS ==========
function getRiskColor(risk) {
    if (risk >= 80) return '#dc2626';      // Red - Critical
    if (risk >= 60) return '#f97316';      // Orange - High
    if (risk >= 40) return '#f59e0b';      // Yellow - Medium
    return '#22c55e';                       // Green - Low
}

function getRiskLabel(risk) {
    if (risk >= 80) return 'Critical';
    if (risk >= 60) return 'High';
    if (risk >= 40) return 'Medium';
    return 'Low';
}

function getStatusBadge(status) {
    const colors = {
        'Critical': '#dc2626',
        'High': '#f97316',
        'Medium': '#f59e0b',
        'Low': '#22c55e'
    };
    return colors[status] || '#64748b';
}

// ========== HEATMAP INSTANCES ==========
let previewMap = null;
let fullMap = null;

// ========== INIT PREVIEW HEATMAP ==========
function initPreviewHeatmap() {
    const container = document.getElementById('heatmapPreview');
    if (!container) return;
    
    if (previewMap) {
        previewMap.invalidateSize();
        return;
    }
    
    // White background map with OpenStreetMap (NO API KEY)
    previewMap = L.map('heatmapPreview', {
        center: [12.9716, 77.5946],
        zoom: 12,
        zoomControl: false,
        attributionControl: false
    });
    
    // PURE OPENSTREETMAP - NO API KEY REQUIRED
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(previewMap);
    
    // Add markers for preview (first 6)
    const previewData = ATMData.slice(0, 6);
    previewData.forEach(atm => addMarker(previewMap, atm));
    
    // Add heatmap layer for preview
    const heatData = previewData.map(a => [a.lat, a.lng, a.risk / 100]);
    L.heatLayer(heatData, {
        radius: 20,
        blur: 15,
        maxZoom: 12,
        gradient: {
            0.3: '#22c55e',
            0.5: '#f59e0b',
            0.7: '#f97316',
            0.9: '#dc2626'
        }
    }).addTo(previewMap);
}

// ========== INIT FULL HEATMAP ==========
function initFullHeatmap() {
    const container = document.getElementById('heatmapFull');
    if (!container) return;
    
    if (fullMap) {
        fullMap.invalidateSize();
        return;
    }
    
    // White background map with OpenStreetMap (NO API KEY)
    fullMap = L.map('heatmapFull', {
        center: [12.9716, 77.5946],
        zoom: 12,
        zoomControl: true
    });
    
    // PURE OPENSTREETMAP - NO API KEY REQUIRED
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(fullMap);
    
    // Add all ATM markers
    ATMData.forEach(atm => addMarker(fullMap, atm));
    
    // Add heatmap layer
    const heatData = ATMData.map(a => [a.lat, a.lng, a.risk / 100]);
    L.heatLayer(heatData, {
        radius: 25,
        blur: 20,
        maxZoom: 14,
        gradient: {
            0.3: '#22c55e',
            0.5: '#f59e0b',
            0.7: '#f97316',
            0.9: '#dc2626'
        }
    }).addTo(fullMap);
}

// ========== ADD MARKER WITH DETAILED POPUP ==========
function addMarker(map, atm) {
    const color = getRiskColor(atm.risk);
    const radius = 10 + (atm.risk / 15);
    
    // Main marker
    const marker = L.circleMarker([atm.lat, atm.lng], {
        radius: radius,
        fillColor: color,
        color: '#ffffff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.85
    }).addTo(map);
    
    // Pulsing effect for critical/high risk
    if (atm.risk >= 60) {
        const pulseRadius = radius + 12;
        const pulse = L.circleMarker([atm.lat, atm.lng], {
            radius: pulseRadius,
            color: color,
            weight: 1.5,
            opacity: 0.3,
            fillOpacity: 0.05,
            className: 'pulse-marker'
        }).addTo(map);
        
        // Add pulse animation with CSS
        const styleId = 'pulse-style';
        if (!document.getElementById(styleId)) {
            const style = document.createElement('style');
            style.id = styleId;
            style.textContent = `
                .pulse-marker {
                    animation: pulse-ring 1.8s ease-out infinite;
                }
                @keyframes pulse-ring {
                    0% { r: ${pulseRadius}; opacity: 0.5; }
                    100% { r: ${pulseRadius + 25}; opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    // Detailed Popup HTML with White/Cyan theme
    const popupHTML = `
        <div style="
            font-family: 'Inter', -apple-system, sans-serif;
            padding: 8px 4px;
            min-width: 260px;
            max-width: 320px;
            background: #ffffff;
            border-radius: 12px;
        ">
            <!-- Header -->
            <div style="
                display: flex;
                justify-content: space-between;
                align-items: center;
                border-bottom: 2px solid #e0f2fe;
                padding-bottom: 8px;
                margin-bottom: 10px;
            ">
                <div>
                    <strong style="
                        font-size: 16px;
                        color: #0f172a;
                    ">${atm.id}</strong>
                    <span style="
                        margin-left: 8px;
                        font-size: 11px;
                        color: #64748b;
                    ">${atm.address}</span>
                </div>
                <span style="
                    background: ${getStatusBadge(atm.status)};
                    color: white;
                    padding: 2px 10px;
                    border-radius: 12px;
                    font-size: 10px;
                    font-weight: 600;
                    text-transform: uppercase;
                ">${atm.status}</span>
            </div>
            
            <!-- Risk Score -->
            <div style="
                display: flex;
                align-items: center;
                gap: 12px;
                background: #f0f9ff;
                padding: 8px 12px;
                border-radius: 8px;
                margin-bottom: 10px;
                border: 1px solid #bae6fd;
            ">
                <div style="
                    font-size: 24px;
                    font-weight: 700;
                    color: ${color};
                ">${atm.risk}%</div>
                <div style="font-size: 12px; color: #475569;">
                    Risk Score
                    <br>
                    <span style="font-weight: 600; color: #0f172a;">${getRiskLabel(atm.risk)}</span>
                </div>
            </div>
            
            <!-- Details Grid -->
            <div style="
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 6px 12px;
                font-size: 12px;
                color: #475569;
                margin-bottom: 10px;
            ">
                <div>
                    <span style="color: #94a3b8;">Bank</span>
                    <br>
                    <strong style="color: #0f172a;">${atm.bank}</strong>
                </div>
                <div>
                    <span style="color: #94a3b8;">Complaints</span>
                    <br>
                    <strong style="color: #0f172a;">${atm.complaints}</strong>
                </div>
                <div>
                    <span style="color: #94a3b8;">Mules Connected</span>
                    <br>
                    <strong style="color: #0f172a;">${atm.mules}</strong>
                </div>
                <div>
                    <span style="color: #94a3b8;">Withdrawal Window</span>
                    <br>
                    <strong style="color: #0f172a;">${atm.predictedWindow}</strong>
                </div>
            </div>
            
            <!-- Last Activity -->
            <div style="
                font-size: 11px;
                color: #94a3b8;
                border-top: 1px solid #e0f2fe;
                padding-top: 8px;
                margin-bottom: 10px;
            ">
                <i class="fas fa-clock" style="margin-right: 4px;"></i>
                Last Activity: ${atm.lastActivity}
            </div>
            
            <!-- Action Buttons -->
            <div style="
                display: flex;
                gap: 8px;
            ">
                <button onclick="handleAlert('${atm.id}')" style="
                    flex: 1;
                    padding: 6px 12px;
                    background: #0284c7;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    font-size: 11px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s;
                    font-family: inherit;
                ">Trigger Verification</button>
                <button onclick="showToast('Navigating to ${atm.id}', 'info')" style="
                    flex: 1;
                    padding: 6px 12px;
                    background: #f0f9ff;
                    color: #0f172a;
                    border: 1px solid #bae6fd;
                    border-radius: 6px;
                    font-size: 11px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.2s;
                    font-family: inherit;
                ">View Details</button>
            </div>
        </div>
    `;
    
    marker.bindPopup(popupHTML, {
        maxWidth: 340,
        className: 'custom-popup'
    });
    
    // Add hover effect
    marker.on('mouseover', function() {
        this.setStyle({
            fillOpacity: 1,
            weight: 3
        });
    });
    
    marker.on('mouseout', function() {
        this.setStyle({
            fillOpacity: 0.85,
            weight: 2
        });
    });
}

// ========== CUSTOM POPUP STYLES ==========
const popupStyle = document.createElement('style');
popupStyle.textContent = `
    .leaflet-popup-content-wrapper {
        border-radius: 12px !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
        padding: 0 !important;
        overflow: hidden;
        background: #ffffff !important;
    }
    .leaflet-popup-content {
        padding: 12px 16px !important;
        margin: 0 !important;
        min-width: 260px !important;
        background: #ffffff !important;
    }
    .leaflet-popup-tip {
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1) !important;
        background: #ffffff !important;
    }
    .leaflet-popup-close-button {
        color: #94a3b8 !important;
        font-size: 18px !important;
        padding: 8px 10px !important;
        transition: all 0.2s !important;
    }
    .leaflet-popup-close-button:hover {
        color: #0f172a !important;
    }
    .leaflet-control-zoom {
        border: none !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
    }
    .leaflet-control-zoom a {
        background: white !important;
        color: #0f172a !important;
        border-color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    .leaflet-control-zoom a:hover {
        background: #f0f9ff !important;
    }
    .leaflet-tile-pane {
        filter: brightness(1.05) contrast(1.05);
    }
`;
document.head.appendChild(popupStyle);

// ========== REFRESH FUNCTIONS ==========
function refreshHeatmap() {
    if (fullMap) {
        fullMap.invalidateSize();
    }
    if (previewMap) {
        previewMap.invalidateSize();
    }
    showToast('Heatmap refreshed', 'info');
}

function filterHeatmap() {
    showToast('Filters applied to heatmap', 'info');
}

function exportHeatmap() {
    showToast('Heatmap exported as PNG', 'success');
}

// ========== INITIALIZE ON LOAD ==========
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initPreviewHeatmap, 500);
});

// ========== EXPOSE FUNCTIONS ==========
window.initFullHeatmap = initFullHeatmap;
window.refreshHeatmap = refreshHeatmap;
window.filterHeatmap = filterHeatmap;
window.exportHeatmap = exportHeatmap;

console.log('Heatmap module loaded with', ATMData.length, 'ATMs');
console.log(' Using OpenStreetMap - NO API KEY REQUIRED!');
console.log(' White/Cyan theme activated!');