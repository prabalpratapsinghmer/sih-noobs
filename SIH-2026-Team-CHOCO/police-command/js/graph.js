// ========== GRAPH DATA - BLACK THEME ==========
const GraphData = {
    nodes: [
        // ===== VICTIMS =====
        { 
            id: 'victim1', 
            label: 'Rahul S.\n(Victim)', 
            color: '#22c55e', 
            shape: 'dot', 
            size: 32, 
            font: { size: 11, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 2, 
            borderColor: '#16a34a',
            shadow: { enabled: true, color: 'rgba(34,197,94,0.4)', size: 12 },
            title: 'Victim: Rahul Sharma\nAmount Lost: ₹5,00,000\nComplaint: C1001'
        },
        { 
            id: 'victim2', 
            label: 'Priya M.\n(Victim)', 
            color: '#22c55e', 
            shape: 'dot', 
            size: 28, 
            font: { size: 11, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 2, 
            borderColor: '#16a34a',
            shadow: { enabled: true, color: 'rgba(34,197,94,0.4)', size: 12 },
            title: 'Victim: Priya Mehta\nAmount Lost: ₹2,50,000\nComplaint: C1002'
        },
        
        // ===== COMPLAINTS =====
        { 
            id: 'complaint1', 
            label: 'C1001\nInvestment', 
            color: '#3b82f6', 
            shape: 'box', 
            size: 22, 
            font: { size: 10, color: '#ffffff', face: 'Inter' },
            borderWidth: 2, 
            borderColor: '#2563eb',
            shadow: { enabled: true, color: 'rgba(59,130,246,0.3)', size: 10 },
            title: 'Complaint: C1001\nType: Investment Scam\nAmount: ₹5,00,000'
        },
        { 
            id: 'complaint2', 
            label: 'C1002\nUPI Fraud', 
            color: '#3b82f6', 
            shape: 'box', 
            size: 20, 
            font: { size: 10, color: '#ffffff', face: 'Inter' },
            borderWidth: 2, 
            borderColor: '#2563eb',
            shadow: { enabled: true, color: 'rgba(59,130,246,0.3)', size: 10 },
            title: 'Complaint: C1002\nType: UPI Fraud\nAmount: ₹2,50,000'
        },
        
        // ===== MULE ACCOUNTS - Black Theme with Risk Colors =====
        { 
            id: 'mule1', 
            label: 'Mule A\n92% Risk', 
            color: '#dc2626', 
            shape: 'dot', 
            size: 30, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 3, 
            borderColor: '#b91c1c',
            shadow: { enabled: true, color: 'rgba(220,38,38,0.5)', size: 14 },
            title: 'Mule Account: Mule A\nAccount: XXXX1234\nBank: SBI\nRisk: 92% (Critical)\nConnected: 3 complaints'
        },
        { 
            id: 'mule2', 
            label: 'Mule B\n78% Risk', 
            color: '#f97316', 
            shape: 'dot', 
            size: 26, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 3, 
            borderColor: '#ea580c',
            shadow: { enabled: true, color: 'rgba(249,115,22,0.4)', size: 12 },
            title: 'Mule Account: Mule B\nAccount: XXXX5678\nBank: HDFC\nRisk: 78% (High)\nConnected: 2 complaints'
        },
        { 
            id: 'mule3', 
            label: 'Mule C\n65% Risk', 
            color: '#f59e0b', 
            shape: 'dot', 
            size: 24, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 2, 
            borderColor: '#d97706',
            shadow: { enabled: true, color: 'rgba(245,158,11,0.3)', size: 10 },
            title: 'Mule Account: Mule C\nAccount: XXXX9012\nBank: ICICI\nRisk: 65% (Medium)\nConnected: 2 complaints'
        },
        { 
            id: 'mule4', 
            label: 'Mule D\n45% Risk', 
            color: '#f59e0b', 
            shape: 'dot', 
            size: 22, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 2, 
            borderColor: '#d97706',
            shadow: { enabled: true, color: 'rgba(245,158,11,0.3)', size: 10 },
            title: 'Mule Account: Mule D\nAccount: XXXX3456\nBank: Axis\nRisk: 45% (Medium)\nConnected: 2 complaints'
        },
        { 
            id: 'mule5', 
            label: 'Mule E\n28% Risk', 
            color: '#22c55e', 
            shape: 'dot', 
            size: 20, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 2, 
            borderColor: '#16a34a',
            shadow: { enabled: true, color: 'rgba(34,197,94,0.3)', size: 8 },
            title: 'Mule Account: Mule E\nAccount: XXXX7890\nBank: Kotak\nRisk: 28% (Low)\nConnected: 1 complaint'
        },
        
        // ===== ATMs =====
        { 
            id: 'atm1', 
            label: 'ATM #452\n92% Risk', 
            color: '#dc2626', 
            shape: 'triangle', 
            size: 34, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 3, 
            borderColor: '#b91c1c',
            shadow: { enabled: true, color: 'rgba(220,38,38,0.5)', size: 14 },
            title: 'ATM: #452\nLocation: Indiranagar\nRisk: 92% (Critical)\nMules: 4\nWindow: 2.3 hours'
        },
        { 
            id: 'atm2', 
            label: 'ATM #789\n67% Risk', 
            color: '#f97316', 
            shape: 'triangle', 
            size: 30, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 3, 
            borderColor: '#ea580c',
            shadow: { enabled: true, color: 'rgba(249,115,22,0.4)', size: 12 },
            title: 'ATM: #789\nLocation: MG Road\nRisk: 67% (High)\nMules: 2\nWindow: 4.1 hours'
        },
        { 
            id: 'atm3', 
            label: 'ATM #234\n88% Risk', 
            color: '#dc2626', 
            shape: 'triangle', 
            size: 32, 
            font: { size: 10, color: '#ffffff', face: 'Inter', bold: true },
            borderWidth: 3, 
            borderColor: '#b91c1c',
            shadow: { enabled: true, color: 'rgba(220,38,38,0.5)', size: 14 },
            title: 'ATM: #234\nLocation: Bannerghatta\nRisk: 88% (Critical)\nMules: 5\nWindow: 1.8 hours'
        },
        
        // ===== EVIDENCE NODES - Black Theme =====
        { 
            id: 'phone1', 
            label: 'Phone\n+91-XXX', 
            color: '#8b5cf6', 
            shape: 'dot', 
            size: 16, 
            font: { size: 9, color: '#ffffff', face: 'Inter' },
            borderWidth: 1, 
            borderColor: '#7c3aed',
            shadow: { enabled: true, color: 'rgba(139,92,246,0.3)', size: 6 },
            title: 'Phone Number: +91-XXX\nLinked to Mule A\nType: Evidence'
        },
        { 
            id: 'upi1', 
            label: 'UPI\npay@scam', 
            color: '#8b5cf6', 
            shape: 'dot', 
            size: 16, 
            font: { size: 9, color: '#ffffff', face: 'Inter' },
            borderWidth: 1, 
            borderColor: '#7c3aed',
            shadow: { enabled: true, color: 'rgba(139,92,246,0.3)', size: 6 },
            title: 'UPI ID: pay@scam\nLinked to Mule A\nType: Evidence'
        },
        { 
            id: 'bank1', 
            label: 'Bank\nSBI-XXXX1234', 
            color: '#06b6d4', 
            shape: 'dot', 
            size: 16, 
            font: { size: 9, color: '#ffffff', face: 'Inter' },
            borderWidth: 1, 
            borderColor: '#0891b2',
            shadow: { enabled: true, color: 'rgba(6,182,212,0.3)', size: 6 },
            title: 'Bank: SBI\nAccount: XXXX1234\nLinked to Mule A'
        },
        { 
            id: 'ip1', 
            label: 'IP\n192.168.x.x', 
            color: '#8b5cf6', 
            shape: 'dot', 
            size: 14, 
            font: { size: 9, color: '#ffffff', face: 'Inter' },
            borderWidth: 1, 
            borderColor: '#7c3aed',
            shadow: { enabled: true, color: 'rgba(139,92,246,0.3)', size: 6 },
            title: 'IP Address: 192.168.x.x\nLinked to Mule B\nType: Evidence'
        }
    ],
    edges: [
        // ===== VICTIM TO COMPLAINT =====
        { 
            from: 'victim1', 
            to: 'complaint1', 
            label: 'filed', 
            color: { color: '#4a5568', highlight: '#60a5fa' }, 
            width: 2, 
            font: { size: 9, color: '#94a3b8', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            title: 'Victim filed complaint C1001'
        },
        { 
            from: 'victim2', 
            to: 'complaint2', 
            label: 'filed', 
            color: { color: '#4a5568', highlight: '#60a5fa' }, 
            width: 2, 
            font: { size: 9, color: '#94a3b8', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
            title: 'Victim filed complaint C1002'
        },
        
        // ===== COMPLAINT TO MULES (Money Trail) =====
        { 
            from: 'complaint1', 
            to: 'mule1', 
            label: '₹5.0L', 
            color: { color: '#dc2626', highlight: '#ef4444' }, 
            width: 4, 
            font: { size: 10, color: '#dc2626', face: 'Inter', bold: true }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.7 } },
            title: '₹5,00,000 transferred to Mule A'
        },
        { 
            from: 'mule1', 
            to: 'mule2', 
            label: '₹4.5L', 
            color: { color: '#f97316', highlight: '#fb923c' }, 
            width: 3.5, 
            font: { size: 10, color: '#f97316', face: 'Inter', bold: true }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.6 } },
            title: '₹4,50,000 transferred from Mule A to Mule B'
        },
        { 
            from: 'mule2', 
            to: 'mule3', 
            label: '₹2.0L', 
            color: { color: '#f59e0b', highlight: '#fbbf24' }, 
            width: 2.5, 
            font: { size: 10, color: '#f59e0b', face: 'Inter', bold: true }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.6 } },
            title: '₹2,00,000 transferred from Mule B to Mule C'
        },
        { 
            from: 'mule2', 
            to: 'mule4', 
            label: '₹2.5L', 
            color: { color: '#f59e0b', highlight: '#fbbf24' }, 
            width: 2.5, 
            font: { size: 10, color: '#f59e0b', face: 'Inter', bold: true }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.6 } },
            title: '₹2,50,000 transferred from Mule B to Mule D'
        },
        { 
            from: 'complaint2', 
            to: 'mule4', 
            label: '₹2.5L', 
            color: { color: '#f59e0b', highlight: '#fbbf24' }, 
            width: 2.5, 
            font: { size: 10, color: '#f59e0b', face: 'Inter', bold: true }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.6 } },
            title: '₹2,50,000 transferred from C1002 to Mule D'
        },
        
        // ===== MULES TO ATMS =====
        { 
            from: 'mule3', 
            to: 'atm1', 
            label: 'withdrew', 
            color: { color: '#dc2626', highlight: '#ef4444' }, 
            width: 3.5, 
            font: { size: 9, color: '#dc2626', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.7 } },
            title: 'Cash withdrawal at ATM #452'
        },
        { 
            from: 'mule4', 
            to: 'atm2', 
            label: 'withdrew', 
            color: { color: '#f97316', highlight: '#fb923c' }, 
            width: 3, 
            font: { size: 9, color: '#f97316', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.6 } },
            title: 'Cash withdrawal at ATM #789'
        },
        { 
            from: 'mule1', 
            to: 'atm3', 
            label: 'withdrew', 
            color: { color: '#dc2626', highlight: '#ef4444' }, 
            width: 3.5, 
            font: { size: 9, color: '#dc2626', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.2 },
            arrows: { to: { enabled: true, scaleFactor: 0.7 } },
            title: 'Cash withdrawal at ATM #234'
        },
        
        // ===== EVIDENCE CONNECTIONS =====
        { 
            from: 'mule1', 
            to: 'phone1', 
            label: 'linked', 
            color: { color: '#8b5cf6', highlight: '#a78bfa' }, 
            width: 1.5, 
            font: { size: 8, color: '#8b5cf6', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.3 },
            dashes: true,
            title: 'Evidence: Phone number linked to Mule A'
        },
        { 
            from: 'mule1', 
            to: 'upi1', 
            label: 'linked', 
            color: { color: '#8b5cf6', highlight: '#a78bfa' }, 
            width: 1.5, 
            font: { size: 8, color: '#8b5cf6', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.3 },
            dashes: true,
            title: 'Evidence: UPI ID linked to Mule A'
        },
        { 
            from: 'mule1', 
            to: 'bank1', 
            label: 'account', 
            color: { color: '#06b6d4', highlight: '#22d3ee' }, 
            width: 1.5, 
            font: { size: 8, color: '#06b6d4', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.3 },
            title: 'Bank account linked to Mule A'
        },
        { 
            from: 'mule2', 
            to: 'ip1', 
            label: 'traced', 
            color: { color: '#8b5cf6', highlight: '#a78bfa' }, 
            width: 1.5, 
            font: { size: 8, color: '#8b5cf6', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.3 },
            dashes: true,
            title: 'Evidence: IP address traced to Mule B'
        },
        
        // ===== CROSS CONNECTIONS =====
        { 
            from: 'mule1', 
            to: 'mule4', 
            label: 'connected', 
            color: { color: '#4a5568', highlight: '#94a3b8' }, 
            width: 1.5, 
            font: { size: 8, color: '#4a5568', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.4 },
            dashes: true,
            title: 'Connection between Mule A and Mule D'
        },
        { 
            from: 'mule3', 
            to: 'complaint2', 
            label: 'linked', 
            color: { color: '#4a5568', highlight: '#94a3b8' }, 
            width: 1.5, 
            font: { size: 8, color: '#4a5568', face: 'Inter' }, 
            smooth: { type: 'curvedCW', roundness: 0.4 },
            dashes: true,
            title: 'Mule C linked to complaint C1002'
        }
    ]
};

// ========== GRAPH INSTANCES ==========
let previewNetwork = null;
let fullNetwork = null;
let graphPhysics = true;
let selectedNode = null;

// ========== RISK COLOR HELPER ==========
function getRiskColor(risk) {
    if (risk >= 80) return '#dc2626';
    if (risk >= 60) return '#f97316';
    if (risk >= 40) return '#f59e0b';
    return '#22c55e';
}

// ========== INIT PREVIEW GRAPH - BLACK THEME ==========
function initPreviewGraph() {
    const container = document.getElementById('graphPreview');
    if (!container) return;
    
    if (previewNetwork) {
        previewNetwork.fit();
        return;
    }
    
    const previewNodeIds = ['victim1', 'complaint1', 'mule1', 'mule2', 'mule3', 'atm1'];
    const previewNodes = new vis.DataSet(
        GraphData.nodes.filter(n => previewNodeIds.includes(n.id))
    );
    const previewEdges = new vis.DataSet(
        GraphData.edges.filter(e => 
            previewNodeIds.includes(e.from) && previewNodeIds.includes(e.to)
        )
    );
    
    const options = {
        nodes: {
            font: { color: '#ffffff', size: 10, face: 'Inter' },
            borderWidth: 2,
            shadow: { enabled: true, color: 'rgba(0,0,0,0.6)', size: 8 }
        },
        edges: {
            color: { color: '#4a5568', highlight: '#60a5fa' },
            smooth: { type: 'curvedCW', roundness: 0.2 },
            font: { color: '#94a3b8', size: 8, face: 'Inter', align: 'middle' },
            arrows: { to: { enabled: true, scaleFactor: 0.5 } }
        },
        physics: {
            enabled: true,
            stabilization: { iterations: 50 },
            barnesHut: { gravitationalConstant: -1500, centralGravity: 0.3 }
        },
        interaction: {
            hover: true,
            tooltipDelay: 200,
            navigationButtons: false,
            keyboard: { enabled: true }
        }
    };
    
    previewNetwork = new vis.Network(container, { nodes: previewNodes, edges: previewEdges }, options);
    
    previewNetwork.on('click', function(params) {
        if (params.nodes.length > 0) {
            const node = previewNodes.get(params.nodes[0]);
            if (node) {
                showNodeDetails(node);
            }
        }
    });
}

// ========== INIT FULL GRAPH - BLACK THEME ==========
function initFullGraph() {
    const container = document.getElementById('graphFull');
    if (!container) return;
    
    if (fullNetwork) {
        fullNetwork.fit();
        return;
    }
    
    const nodes = new vis.DataSet(GraphData.nodes);
    const edges = new vis.DataSet(GraphData.edges);
    
    const options = {
        nodes: {
            font: { color: '#ffffff', size: 11, face: 'Inter' },
            borderWidth: 2,
            shadow: { enabled: true, color: 'rgba(0,0,0,0.7)', size: 10 }
        },
        edges: {
            color: { color: '#4a5568', highlight: '#60a5fa' },
            smooth: { type: 'curvedCW', roundness: 0.2 },
            font: { color: '#94a3b8', size: 9, face: 'Inter', align: 'middle' },
            arrows: { to: { enabled: true, scaleFactor: 0.6 } }
        },
        physics: {
            enabled: true,
            stabilization: { iterations: 150 },
            barnesHut: { gravitationalConstant: -2000, centralGravity: 0.3, springLength: 150 }
        },
        interaction: {
            hover: true,
            tooltipDelay: 200,
            navigationButtons: true,
            keyboard: { enabled: true }
        }
    };
    
    fullNetwork = new vis.Network(container, { nodes, edges }, options);
    
    // ===== INTERACTIVE EVENTS =====
    
    // Click event - Show node details
    fullNetwork.on('click', function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = nodes.get(nodeId);
            if (node) {
                showNodeDetails(node);
                if (selectedNode) {
                    const prev = nodes.get(selectedNode);
                    if (prev) {
                        nodes.update({ id: selectedNode, borderWidth: 2 });
                    }
                }
                selectedNode = nodeId;
                nodes.update({ id: nodeId, borderWidth: 4, borderColor: '#ffffff' });
            }
        } else {
            if (selectedNode) {
                const prev = nodes.get(selectedNode);
                if (prev) {
                    nodes.update({ id: selectedNode, borderWidth: 2, borderColor: prev.borderColor || '#4a5568' });
                }
                selectedNode = null;
            }
        }
    });
    
    // Hover event - Glow effect
    fullNetwork.on('hoverNode', function(params) {
        if (params.node) {
            const node = nodes.get(params.node);
            if (node) {
                nodes.update({ 
                    id: params.node, 
                    shadow: { enabled: true, color: 'rgba(59,130,246,0.6)', size: 20 } 
                });
            }
        }
    });
    
    fullNetwork.on('blurNode', function(params) {
        if (params.node) {
            const node = nodes.get(params.node);
            if (node && params.node !== selectedNode) {
                const originalColor = node.color || '#3b82f6';
                const shadowColor = 'rgba(0,0,0,0.7)';
                nodes.update({ 
                    id: params.node, 
                    shadow: { enabled: true, color: shadowColor, size: 10 } 
                });
            }
        }
    });
    
    // Double click - Expand details
    fullNetwork.on('doubleClick', function(params) {
        if (params.nodes.length > 0) {
            const node = nodes.get(params.nodes[0]);
            if (node) {
                openActionModal(
                    'Node Details',
                    `Detailed information for ${node.label.replace(/\n/g, ' ')}`,
                    () => {
                        showToast('Node details exported', 'success');
                    },
                    'Export Details',
                    `<div style="margin-top:10px;padding:10px;background:var(--bg-primary);border-radius:6px;font-size:0.8rem;white-space:pre-wrap;color:var(--text-primary);">${node.title || 'No additional details available.'}</div>`
                );
            }
        }
    });
    
    // Store references
    window._fullNetwork = fullNetwork;
    window._fullNodes = nodes;
}

// ========== SHOW NODE DETAILS ==========
function showNodeDetails(node) {
    const label = node.label.replace(/\n/g, ' ');
    const title = node.title || 'No additional details available.';
    
    let type = 'Node';
    let icon = '📌';
    if (node.color === '#22c55e' && node.shape === 'dot') { type = 'Victim'; icon = '👤'; }
    else if (node.color === '#3b82f6') { type = 'Complaint'; icon = '📋'; }
    else if (node.color === '#dc2626' || node.color === '#f97316' || node.color === '#f59e0b') { 
        type = 'Mule Account'; 
        icon = '💰';
        if (node.shape === 'triangle') { type = 'ATM'; icon = '🏧'; }
    }
    else if (node.color === '#8b5cf6') { type = 'Evidence'; icon = '🔍'; }
    else if (node.color === '#06b6d4') { type = 'Bank Account'; icon = '🏦'; }
    
    openActionModal(
        `${icon} ${type}: ${label}`,
        title,
        () => {
            showToast(`Details exported for ${label}`, 'success');
        },
        'Export Details'
    );
}

// ========== GRAPH CONTROLS ==========
function resetGraph() {
    if (fullNetwork) {
        fullNetwork.fit();
        if (selectedNode && window._fullNodes) {
            const prev = window._fullNodes.get(selectedNode);
            if (prev) {
                window._fullNodes.update({ id: selectedNode, borderWidth: 2, borderColor: prev.borderColor || '#4a5568' });
            }
            selectedNode = null;
        }
        showToast('Graph view reset', 'info');
    }
}

function toggleGraphPhysics() {
    if (fullNetwork) {
        graphPhysics = !graphPhysics;
        fullNetwork.setOptions({ physics: { enabled: graphPhysics } });
        showToast(`Physics ${graphPhysics ? 'enabled' : 'disabled'}`, 'info');
    }
}

function exportGraph() {
    showToast('Graph exported as PNG successfully', 'success');
}

function zoomGraphIn() {
    if (fullNetwork) {
        fullNetwork.moveTo({ scale: fullNetwork.getScale() * 1.2 });
    }
}

function zoomGraphOut() {
    if (fullNetwork) {
        fullNetwork.moveTo({ scale: fullNetwork.getScale() * 0.8 });
    }
}

// ========== INITIALIZE ==========
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(initPreviewGraph, 600);
});

// ========== EXPOSE ==========
window.initFullGraph = initFullGraph;
window.resetGraph = resetGraph;
window.toggleGraphPhysics = toggleGraphPhysics;
window.exportGraph = exportGraph;
window.zoomGraphIn = zoomGraphIn;
window.zoomGraphOut = zoomGraphOut;

console.log('🕸️ Graph module loaded with', GraphData.nodes.length, 'nodes and', GraphData.edges.length, 'edges');
console.log('🎨 Black theme activated');
console.log('📊 Interactive features: Click nodes for details, hover for glow effect');