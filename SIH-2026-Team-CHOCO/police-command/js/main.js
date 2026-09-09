// ========== DATA STORE ==========
const AppData = {
    complaints: [
        { id: 'C1001', victim: 'Rahul Sharma', amount: 500000, type: 'Investment Scam', status: 'analyzing', assigned: 'Inspector Singh' },
        { id: 'C1002', victim: 'Priya Mehta', amount: 250000, type: 'UPI Fraud', status: 'action_taken', assigned: 'Constable Kumar' },
        { id: 'C1003', victim: 'Vikram Patel', amount: 100000, type: 'KYC Fraud', status: 'resolved', assigned: 'Inspector Singh' },
        { id: 'C1004', victim: 'Ananya Krishnan', amount: 750000, type: 'Investment Scam', status: 'analyzing', assigned: 'Constable Sharma' },
        { id: 'C1005', victim: 'Deepak Reddy', amount: 300000, type: 'Phishing', status: 'investigating', assigned: 'Inspector Singh' },
        { id: 'C1006', victim: 'Sneha Patel', amount: 150000, type: 'Job Fraud', status: 'action_taken', assigned: 'Constable Kumar' }
    ],
    alerts: [
        { id: 'A001', atm: 'ATM #452', risk: 92, location: 'Indiranagar', mules: 3, window: '2.3 hours', priority: 'critical', time: '2 min ago' },
        { id: 'A002', atm: 'ATM #789', risk: 67, location: 'MG Road', mules: 1, window: '4.1 hours', priority: 'high', time: '15 min ago' },
        { id: 'A003', atm: 'ATM #456', risk: 55, location: 'Jayanagar', mules: 2, window: '1.5 hours', priority: 'medium', time: '32 min ago' },
        { id: 'A004', atm: 'ATM #123', risk: 34, location: 'Koramangala', mules: 0, window: '5.0 hours', priority: 'low', time: '1.2 hours ago' },
        { id: 'A005', atm: 'ATM #890', risk: 78, location: 'Yeshwanthpur', mules: 2, window: '3.2 hours', priority: 'high', time: '45 min ago' },
        { id: 'A006', atm: 'ATM #567', risk: 45, location: 'HSR Layout', mules: 1, window: '6.0 hours', priority: 'medium', time: '2.1 hours ago' },
        { id: 'A007', atm: 'ATM #234', risk: 88, location: 'Bannerghatta', mules: 4, window: '1.8 hours', priority: 'critical', time: '5 min ago' },
        { id: 'A008', atm: 'ATM #678', risk: 72, location: 'Electronic City', mules: 2, window: '2.7 hours', priority: 'critical', time: '18 min ago' },
        { id: 'A009', atm: 'ATM #345', risk: 61, location: 'Malleshwaram', mules: 1, window: '3.5 hours', priority: 'high', time: '55 min ago' },
        { id: 'A010', atm: 'ATM #901', risk: 39, location: 'Rajajinagar', mules: 0, window: '7.0 hours', priority: 'low', time: '3.2 hours ago' }
    ],
    cases: [
        { id: 'CS001', victim: 'Rahul Sharma', amount: 500000, type: 'Investment Scam', status: 'open', assigned: 'Inspector Singh' },
        { id: 'CS002', victim: 'Priya Mehta', amount: 250000, type: 'UPI Fraud', status: 'investigating', assigned: 'Constable Kumar' },
        { id: 'CS003', victim: 'Vikram Patel', amount: 100000, type: 'KYC Fraud', status: 'resolved', assigned: 'Inspector Singh' },
        { id: 'CS004', victim: 'Ananya Krishnan', amount: 750000, type: 'Investment Scam', status: 'open', assigned: 'Constable Sharma' },
        { id: 'CS005', victim: 'Deepak Reddy', amount: 300000, type: 'Phishing', status: 'investigating', assigned: 'Inspector Singh' },
        { id: 'CS006', victim: 'Sneha Patel', amount: 150000, type: 'Job Fraud', status: 'open', assigned: 'Constable Kumar' }
    ],
    mules: [
        { id: 'M1001', account: 'XXXX1234', bank: 'SBI', risk: 92, connectedComplaints: 3, amount: 500000, status: 'Critical' },
        { id: 'M1002', account: 'XXXX5678', bank: 'HDFC', risk: 78, connectedComplaints: 2, amount: 450000, status: 'High' },
        { id: 'M1003', account: 'XXXX9012', bank: 'ICICI', risk: 65, connectedComplaints: 2, amount: 200000, status: 'Medium' },
        { id: 'M1004', account: 'XXXX3456', bank: 'Axis', risk: 45, connectedComplaints: 1, amount: 100000, status: 'Medium' },
        { id: 'M1005', account: 'XXXX7890', bank: 'Kotak', risk: 28, connectedComplaints: 0, amount: 50000, status: 'Low' }
    ],
    notifications: [
        { id: 'N001', title: 'New Critical Alert', desc: 'ATM #234 in Bannerghatta has 88% risk score', time: '5 min ago', type: 'danger' },
        { id: 'N002', title: 'Verification Triggered', desc: 'Step-Up verification enabled for ATM #452', time: '12 min ago', type: 'success' },
        { id: 'N003', title: 'Mule Account Flagged', desc: 'Mule account M1001 has been flagged for review', time: '25 min ago', type: 'warning' },
        { id: 'N004', title: 'Case Resolved', desc: 'Case CS003 has been resolved successfully', time: '1 hour ago', type: 'success' },
        { id: 'N005', title: 'New Complaint Filed', desc: 'Complaint C1006 filed by Sneha Patel', time: '1.5 hours ago', type: 'info' },
        { id: 'N006', title: 'System Update', desc: 'AI model retrained with new fraud patterns', time: '2 hours ago', type: 'info' }
    ]
};

// ========== CURRENT STATE ==========
let currentPage = 'dashboard';
let pendingAction = null;
let currentFilter = 'all';
let currentCaseFilter = 'all';
let chatHistory = [];
let isDarkMode = false;

// ========== PAGE SWITCHING ==========
function switchPage(page) {
    currentPage = page;
    
    document.querySelectorAll('.page-content').forEach(p => p.classList.remove('active'));
    
    const target = document.getElementById(`page-${page}`);
    if (target) target.classList.add('active');
    
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    document.querySelector(`.nav-item[data-page="${page}"]`)?.classList.add('active');
    
    const titles = {
        dashboard: 'Command Center',
        heatmap: 'ATM Heatmap',
        graph: 'Mule Network',
        llm: 'LLM Intelligence Agent',
        alerts: 'Alerts',
        cases: 'Cases'
    };
    document.getElementById('pageTitle').textContent = titles[page] || 'Command Center';
    
    if (page === 'heatmap') {
        setTimeout(() => {
            if (typeof initFullHeatmap === 'function') initFullHeatmap();
        }, 100);
    }
    if (page === 'graph') {
        setTimeout(() => {
            if (typeof initFullGraph === 'function') initFullGraph();
        }, 100);
    }
}

// ========== TOAST NOTIFICATIONS ==========
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    clearTimeout(toast._timeout);
    toast._timeout = setTimeout(() => toast.classList.remove('show'), 3500);
}

// ========== NOTIFICATIONS ==========
function showNotifications() {
    const modal = document.getElementById('notificationsModal');
    const list = document.getElementById('notificationsList');
    
    list.innerHTML = AppData.notifications.map(n => `
        <div class="notification-item">
            <div class="notif-icon ${n.type}">
                <i class="fas ${n.type === 'danger' ? 'fa-exclamation-triangle' : n.type === 'success' ? 'fa-check' : n.type === 'warning' ? 'fa-exclamation' : 'fa-info'}"></i>
            </div>
            <div class="notif-content">
                <div class="notif-title">${n.title}</div>
                <div class="notif-desc">${n.desc}</div>
                <div class="notif-time">${n.time}</div>
            </div>
        </div>
    `).join('');
    
    modal.classList.add('active');
}

function closeNotifications() {
    document.getElementById('notificationsModal').classList.remove('active');
}

function markAllNotificationsRead() {
    showToast('All notifications marked as read', 'success');
    closeNotifications();
}

// ========== SETTINGS ==========
function showSettings() {
    document.getElementById('settingsModal').classList.add('active');
}

function closeSettings() {
    document.getElementById('settingsModal').classList.remove('active');
}

function saveSettings() {
    showToast('Settings saved successfully!', 'success');
    closeSettings();
}

// ========== ACTION MODAL ==========
function openActionModal(title, message, action, actionLabel = 'Confirm', extraContent = '') {
    document.getElementById('modalTitle').textContent = title;
    document.getElementById('modalMessage').textContent = message;
    document.getElementById('modalExtraContent').innerHTML = extraContent;
    document.getElementById('modalConfirmBtn').textContent = actionLabel;
    pendingAction = action;
    document.getElementById('actionModal').classList.add('active');
}

function closeActionModal() {
    document.getElementById('actionModal').classList.remove('active');
    pendingAction = null;
}

function confirmAction() {
    if (pendingAction) {
        pendingAction();
        pendingAction = null;
    }
    closeActionModal();
}

// ========== STAT CARD ACTIONS ==========
function showComplaints() {
    const active = AppData.complaints.filter(c => c.status !== 'resolved').length;
    showToast(`Total active complaints: ${active}`, 'info');
    switchPage('cases');
}

function showHighRiskATMs() {
    const highRisk = AppData.alerts.filter(a => a.risk >= 70);
    showToast(`Found ${highRisk.length} high-risk ATMs`, 'warning');
    switchPage('alerts');
}

function showRecoveredFunds() {
    const total = AppData.complaints
        .filter(c => c.status === 'resolved')
        .reduce((sum, c) => sum + c.amount, 0);
    showToast(`Total funds recovered: ₹${(total/100000).toFixed(1)} Lakhs`, 'success');
}

function showResponseTime() {
    showToast('Average response time: 2.3 minutes', 'info');
}

// ========== ALERT FUNCTIONS ==========
function handleAlert(atmId) {
    const alert = AppData.alerts.find(a => a.atm === atmId);
    if (!alert) return;
    
    openActionModal(
        'Step-Up Verification',
        `Trigger Step-Up Verification for ${atmId}? This will enable facial recognition and OTP verification at this ATM.`,
        () => {
            showToast(`✅ Step-Up Verification triggered for ${atmId}`, 'success');
            alert.priority = 'resolved';
            renderAlerts();
            renderAllAlerts();
            updateAlertBadge();
        },
        'Trigger Verification'
    );
}

function renderAlerts() {
    const container = document.getElementById('alertList');
    if (!container) return;
    
    const alerts = AppData.alerts.filter(a => a.priority !== 'resolved').slice(0, 4);
    container.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.priority}" onclick="handleAlert('${alert.atm}')">
            <div class="alert-icon">
                <i class="fas ${getAlertIcon(alert.priority)}"></i>
            </div>
            <div class="alert-content">
                <span class="alert-title">${alert.atm} - ${alert.risk}% Risk</span>
                <span class="alert-desc">${alert.location} | ${alert.mules} mules | ${alert.window}</span>
            </div>
            <button class="alert-action" onclick="event.stopPropagation(); handleAlert('${alert.atm}')">
                <i class="fas fa-shield"></i>
            </button>
        </div>
    `).join('');
    
    updateAlertBadge();
}

function getAlertIcon(priority) {
    const icons = {
        critical: 'fa-skull',
        high: 'fa-exclamation',
        medium: 'fa-exclamation-triangle',
        low: 'fa-info',
        resolved: 'fa-check'
    };
    return icons[priority] || 'fa-bell';
}

function renderAllAlerts() {
    const container = document.getElementById('allAlertsList');
    if (!container) return;
    
    let alerts = AppData.alerts;
    if (currentFilter !== 'all') {
        alerts = alerts.filter(a => a.priority === currentFilter);
    }
    
    container.innerHTML = alerts.map(alert => `
        <div class="alert-item ${alert.priority}" onclick="handleAlert('${alert.atm}')">
            <div class="alert-icon">
                <i class="fas ${getAlertIcon(alert.priority)}"></i>
            </div>
            <div class="alert-content">
                <span class="alert-title">${alert.atm} - ${alert.risk}% Risk</span>
                <span class="alert-desc">${alert.location} | ${alert.mules} mules | Window: ${alert.window}</span>
                <span class="alert-desc" style="font-size:0.6rem;color:var(--text-muted);">${alert.time}</span>
            </div>
            <button class="alert-action" onclick="event.stopPropagation(); handleAlert('${alert.atm}')">
                <i class="fas fa-shield"></i>
            </button>
        </div>
    `).join('');
}

function filterAlerts(filter) {
    currentFilter = filter;
    document.querySelectorAll('.alert-filters .filter-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.alert-filters .filter-btn[onclick*="'${filter}'"]`)?.classList.add('active');
    renderAllAlerts();
}

function markAllRead() {
    AppData.alerts.forEach(a => a.priority = 'resolved');
    renderAlerts();
    renderAllAlerts();
    updateAlertBadge();
    showToast('All alerts marked as read', 'success');
}

function refreshAlerts() {
    showToast('Alerts refreshed', 'info');
    renderAlerts();
    renderAllAlerts();
}

function updateAlertBadge() {
    const count = AppData.alerts.filter(a => a.priority !== 'resolved').length;
    document.getElementById('alertCount').textContent = count;
    document.getElementById('alertBadge').textContent = count;
}

// ========== ACTION BUTTONS - FULLY FUNCTIONAL ==========
function triggerVerification() {
    const highRiskATM = AppData.alerts.find(a => a.risk >= 80 && a.priority !== 'resolved');
    if (highRiskATM) {
        openActionModal(
            'Step-Up Verification',
            `Trigger Step-Up Verification for ${highRiskATM.atm} (${highRiskATM.risk}% risk) at ${highRiskATM.location}? This will enable biometric verification at this ATM.`,
            () => {
                showToast(`✅ Step-Up Verification triggered for ${highRiskATM.atm}`, 'success');
                highRiskATM.priority = 'resolved';
                renderAlerts();
                renderAllAlerts();
                updateAlertBadge();
            },
            'Trigger Now',
            `<div style="margin-top:10px;padding:10px;background:var(--bg-primary);border-radius:6px;font-size:0.8rem;">
                <strong>ATM Details:</strong><br>
                ID: ${highRiskATM.atm}<br>
                Risk: ${highRiskATM.risk}%<br>
                Location: ${highRiskATM.location}<br>
                Mules: ${highRiskATM.mules}<br>
                Window: ${highRiskATM.window}
            </div>`
        );
    } else {
        const mediumRisk = AppData.alerts.filter(a => a.risk >= 40 && a.risk < 80 && a.priority !== 'resolved');
        if (mediumRisk.length > 0) {
            openActionModal(
                'Step-Up Verification',
                `No critical-risk ATMs found. Would you like to trigger verification on ${mediumRisk.length} medium-risk ATMs?`,
                () => {
                    mediumRisk.forEach(a => a.priority = 'resolved');
                    renderAlerts();
                    renderAllAlerts();
                    updateAlertBadge();
                    showToast(`✅ Verification triggered on ${mediumRisk.length} medium-risk ATMs`, 'success');
                },
                `Trigger ${mediumRisk.length} ATMs`
            );
        } else {
            showToast('No active ATMs requiring verification', 'info');
        }
    }
}

function freezeMule() {
    const highRiskMule = AppData.mules.find(m => m.risk >= 70);
    if (highRiskMule) {
        openActionModal(
            'Freeze Mule Account',
            `Freeze mule account ${highRiskMule.account} (${highRiskMule.bank})? This account has a risk score of ${highRiskMule.risk}% and is connected to ${highRiskMule.connectedComplaints} complaints.`,
            () => {
                showToast(`✅ Account ${highRiskMule.account} frozen successfully`, 'success');
                highRiskMule.status = 'Frozen';
            },
            'Freeze Account',
            `<div style="margin-top:10px;padding:10px;background:var(--bg-primary);border-radius:6px;font-size:0.8rem;">
                <strong>Account Details:</strong><br>
                Account: ${highRiskMule.account}<br>
                Bank: ${highRiskMule.bank}<br>
                Risk: ${highRiskMule.risk}%<br>
                Connected Complaints: ${highRiskMule.connectedComplaints}<br>
                Amount: ₹${highRiskMule.amount.toLocaleString('en-IN')}
            </div>`
        );
    } else {
        const mediumMules = AppData.mules.filter(m => m.risk >= 40 && m.risk < 70);
        if (mediumMules.length > 0) {
            openActionModal(
                'Freeze Mule Account',
                `No critical-risk mule accounts. Would you like to freeze ${mediumMules.length} medium-risk accounts?`,
                () => {
                    mediumMules.forEach(m => m.status = 'Frozen');
                    showToast(`✅ ${mediumMules.length} medium-risk accounts frozen`, 'success');
                },
                `Freeze ${mediumMules.length} Accounts`
            );
        } else {
            showToast('No mule accounts require freezing', 'info');
        }
    }
}

function generateFIR() {
    const activeCases = AppData.cases.filter(c => c.status !== 'resolved');
    if (activeCases.length === 0) {
        showToast('No active cases to generate FIR for', 'info');
        return;
    }
    
    openActionModal(
        'Generate FIR',
        `Generate First Information Report (FIR) for ${activeCases.length} active case(s)? This will create a legally documented complaint.`,
        () => {
            const firNumber = 'FIR-' + new Date().getFullYear() + '-' + String(Math.floor(Math.random() * 9000) + 1000);
            showToast(`✅ FIR ${firNumber} generated successfully`, 'success');
        },
        'Generate FIR',
        `<div style="margin-top:10px;padding:10px;background:var(--bg-primary);border-radius:6px;font-size:0.8rem;">
            <strong>Cases to be filed:</strong><br>
            ${activeCases.map(c => `${c.id} - ${c.victim} (₹${c.amount.toLocaleString('en-IN')})`).join('<br>')}
        </div>`
    );
}

function dispatchPatrol() {
    const highRiskATM = AppData.alerts.find(a => a.risk >= 70 && a.priority !== 'resolved');
    if (!highRiskATM) {
        showToast('No high-risk locations requiring patrol', 'info');
        return;
    }
    
    openActionModal(
        'Dispatch Patrol',
        `Dispatch a police patrol to ${highRiskATM.atm} at ${highRiskATM.location}? This ATM has a ${highRiskATM.risk}% risk score.`,
        () => {
            showToast(`🚔 Patrol dispatched to ${highRiskATM.location}`, 'success');
        },
        'Dispatch Now',
        `<div style="margin-top:10px;padding:10px;background:var(--bg-primary);border-radius:6px;font-size:0.8rem;">
            <strong>Dispatch Details:</strong><br>
            Location: ${highRiskATM.location}<br>
            ATM: ${highRiskATM.atm}<br>
            Risk: ${highRiskATM.risk}%<br>
            Estimated Response: ${highRiskATM.window}
        </div>`
    );
}

// ========== COMPLAINT TABLE ==========
function renderComplaints() {
    const tbody = document.getElementById('complaintTableBody');
    if (!tbody) return;
    
    tbody.innerHTML = AppData.complaints.map(c => `
        <tr onclick="viewCase('${c.id}')" style="cursor:pointer;">
            <td><strong>${c.id}</strong></td>
            <td>${c.victim}</td>
            <td>₹${c.amount.toLocaleString('en-IN')}</td>
            <td>${c.type}</td>
            <td><span class="status-badge ${getStatusClass(c.status)}">${getStatusLabel(c.status)}</span></td>
            <td><button class="btn-sm" onclick="event.stopPropagation(); viewCase('${c.id}')">View</button></td>
        </tr>
    `).join('');
}

function getStatusClass(status) {
    const classes = {
        'analyzing': 'critical',
        'action_taken': 'warning',
        'investigating': 'info',
        'resolved': 'success',
        'open': 'info'
    };
    return classes[status] || 'info';
}

function getStatusLabel(status) {
    const labels = {
        'analyzing': 'AI Analyzing',
        'action_taken': 'Action Taken',
        'investigating': 'Investigating',
        'resolved': 'Resolved',
        'open': 'Open'
    };
    return labels[status] || status;
}

// ========== CASES TABLE ==========
function renderCases() {
    const tbody = document.getElementById('casesTableBody');
    if (!tbody) return;
    
    let cases = AppData.cases;
    if (currentCaseFilter !== 'all') {
        cases = cases.filter(c => c.status === currentCaseFilter);
    }
    
    tbody.innerHTML = cases.map(c => `
        <tr onclick="viewCase('${c.id}')" style="cursor:pointer;">
            <td><strong>${c.id}</strong></td>
            <td>${c.victim}</td>
            <td>₹${c.amount.toLocaleString('en-IN')}</td>
            <td>${c.type}</td>
            <td><span class="status-badge ${getStatusClass(c.status)}">${getStatusLabel(c.status)}</span></td>
            <td>${c.assigned}</td>
            <td>
                <button class="btn-sm" onclick="event.stopPropagation(); viewCase('${c.id}')">View</button>
                <button class="btn-sm" onclick="event.stopPropagation(); updateCaseStatus('${c.id}')">Update</button>
            </td>
        </tr>
    `).join('');
}

function filterCases(filter) {
    currentCaseFilter = filter;
    document.querySelectorAll('.case-filters .filter-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`.case-filters .filter-btn[onclick*="'${filter}'"]`)?.classList.add('active');
    renderCases();
}

function viewCase(caseId) {
    const caseData = AppData.cases.find(c => c.id === caseId) || AppData.complaints.find(c => c.id === caseId);
    if (caseData) {
        openActionModal(
            `Case ${caseId} Details`,
            `Victim: ${caseData.victim}\nAmount: ₹${caseData.amount.toLocaleString('en-IN')}\nType: ${caseData.type}\nStatus: ${getStatusLabel(caseData.status)}\nAssigned To: ${caseData.assigned || 'Unassigned'}`,
            () => {
                showToast(`Case ${caseId} details exported`, 'success');
            },
            'Export Details'
        );
    } else {
        showToast(`Case ${caseId} not found`, 'error');
    }
}

function updateCaseStatus(caseId) {
    const statuses = ['open', 'investigating', 'action_taken', 'resolved'];
    const caseData = AppData.cases.find(c => c.id === caseId);
    if (caseData) {
        const currentIndex = statuses.indexOf(caseData.status);
        const nextIndex = (currentIndex + 1) % statuses.length;
        caseData.status = statuses[nextIndex];
        renderCases();
        showToast(`Case ${caseId} updated to ${getStatusLabel(caseData.status)}`, 'success');
    }
}

function addCase() {
    openActionModal(
        'New Case',
        'Create a new case file for investigation? This will generate a new case ID.',
        () => {
            const newCase = {
                id: `CS${String(AppData.cases.length + 1).padStart(3, '0')}`,
                victim: 'New Victim',
                amount: 0,
                type: 'Under Investigation',
                status: 'open',
                assigned: 'Unassigned'
            };
            AppData.cases.push(newCase);
            renderCases();
            showToast(`New case ${newCase.id} created successfully`, 'success');
        },
        'Create Case'
    );
}

function exportCases() {
    showToast('Cases exported as CSV successfully', 'success');
}

// ========== THEME TOGGLE ==========
function toggleTheme() {
    isDarkMode = !isDarkMode;
    const themeBtn = document.getElementById('themeBtn');
    themeBtn.querySelector('i').className = isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
    
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.body.style.background = '#0a0e17';
    } else {
        document.documentElement.removeAttribute('data-theme');
        document.body.style.background = '#f1f5f9';
    }
    
    showToast(`Theme switched to ${isDarkMode ? 'dark' : 'light'} mode`, 'info');
}

// ========== SIDEBAR TOGGLE ==========
function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('collapsed');
}

// ========== LOGOUT ==========
function handleLogout() {
    openActionModal(
        'Logout',
        'Are you sure you want to logout of the Command Center?',
        () => {
            showToast('Logged out successfully', 'success');
        },
        'Logout'
    );
}

// ========== TIME UPDATE ==========
function updateTime() {
    const now = new Date();
    document.getElementById('currentTime').textContent = now.toLocaleString('en-IN', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ========== LLM FUNCTIONS ==========
function setLLMInput(text) {
    document.getElementById('llmInput').value = text;
    sendLLMQuery();
}

function clearLLMChat() {
    const chat = document.getElementById('llmChatFull');
    if (chat) {
        chat.innerHTML = `
            <div class="llm-message assistant">
                <div class="message-avatar">AI</div>
                <div class="message-content">
                    <p>Hello! I am your intelligence analyst. Ask me about:</p>
                    <ul>
                        <li>ATM risk predictions</li>
                        <li>Mule account connections</li>
                        <li>Complaint analysis</li>
                        <li>Fraud patterns and trends</li>
                        <li>Case intelligence</li>
                    </ul>
                </div>
            </div>
        `;
        chatHistory = [];
    }
    showToast('Chat cleared', 'info');
}

// ========== SEND LLM QUERY (Stub - Implemented in llm.js) ==========
// This is defined in llm.js

// ========== INITIALIZATION ==========
document.addEventListener('DOMContentLoaded', function() {
    updateTime();
    setInterval(updateTime, 30000);
    renderComplaints();
    renderCases();
    renderAlerts();
    renderAllAlerts();
    updateAlertBadge();
    
    // Initialize LLM chat if available
    if (typeof clearLLMChat === 'function') clearLLMChat();
    
    console.log('🚀 Cyber Command Center initialized');
    console.log(`📊 Loaded ${AppData.complaints.length} complaints, ${AppData.alerts.length} alerts, ${AppData.cases.length} cases`);
});

// Expose functions globally
window.switchPage = switchPage;
window.showToast = showToast;
window.openActionModal = openActionModal;
window.closeActionModal = closeActionModal;
window.confirmAction = confirmAction;
window.showComplaints = showComplaints;
window.showHighRiskATMs = showHighRiskATMs;
window.showRecoveredFunds = showRecoveredFunds;
window.showResponseTime = showResponseTime;
window.handleAlert = handleAlert;
window.triggerVerification = triggerVerification;
window.freezeMule = freezeMule;
window.generateFIR = generateFIR;
window.dispatchPatrol = dispatchPatrol;
window.viewCase = viewCase;
window.updateCaseStatus = updateCaseStatus;
window.addCase = addCase;
window.exportCases = exportCases;
window.filterAlerts = filterAlerts;
window.filterCases = filterCases;
window.markAllRead = markAllRead;
window.refreshAlerts = refreshAlerts;
window.setLLMInput = setLLMInput;
window.clearLLMChat = clearLLMChat;
window.toggleSidebar = toggleSidebar;
window.toggleTheme = toggleTheme;
window.handleLogout = handleLogout;
window.showNotifications = showNotifications;
window.closeNotifications = closeNotifications;
window.markAllNotificationsRead = markAllNotificationsRead;
window.showSettings = showSettings;
window.closeSettings = closeSettings;
window.saveSettings = saveSettings;