/* ==========================================================================
   Police Field Dashboard — Application Logic
   All interactive functions are exposed on `window` so inline HTML
   handlers (onclick="...") and future modules can call them directly.
   ========================================================================== */

(function () {
  'use strict';

  /* ------------------------------------------------------------------ *
   *  DATA
   * ------------------------------------------------------------------ */

  const ALERTS = [
    {
      id: 'A001',
      atmName: 'MG Road Central ATM',
      location: 'MG Road, Bengaluru',
      lat: 12.9756,
      lng: 77.6068,
      risk: 92,
      priority: 'critical',
      timeWindow: '14:00 – 16:00',
      mules: 3,
      amount: 500000,
      verified: false,
      reviewed: false,
    },
    {
      id: 'A002',
      atmName: 'Koramangala Forum ATM',
      location: 'Koramangala, Bengaluru',
      lat: 12.9352,
      lng: 77.6146,
      risk: 78,
      priority: 'high',
      timeWindow: '10:00 – 12:00',
      mules: 2,
      amount: 250000,
      verified: false,
      reviewed: false,
    },
    {
      id: 'A003',
      atmName: 'Indiranagar 100ft Road ATM',
      location: 'Indiranagar, Bengaluru',
      lat: 12.9784,
      lng: 77.6408,
      risk: 55,
      priority: 'medium',
      timeWindow: '18:00 – 20:00',
      mules: 1,
      amount: 100000,
      verified: false,
      reviewed: false,
    },
    {
      id: 'A004',
      atmName: 'Whitefield ITPL ATM',
      location: 'Whitefield, Bengaluru',
      lat: 12.9698,
      lng: 77.7500,
      risk: 35,
      priority: 'low',
      timeWindow: '09:00 – 11:00',
      mules: 1,
      amount: 50000,
      verified: false,
      reviewed: false,
    },
    {
      id: 'A005',
      atmName: 'Electronic City ATM',
      location: 'Electronic City, Bengaluru',
      lat: 12.8452,
      lng: 77.6602,
      risk: 88,
      priority: 'critical',
      timeWindow: '20:00 – 22:00',
      mules: 4,
      amount: 750000,
      verified: false,
      reviewed: false,
    },
  ];

  const NOTIFICATIONS = [
    {
      id: 'N001',
      title: 'New critical alert',
      desc: 'MG Road Central ATM flagged with a risk score of 92.',
      time: '5 min ago',
      type: 'alert',
      read: false,
    },
    {
      id: 'N002',
      title: 'Verification confirmed',
      desc: 'Mule withdrawal pattern verified at Koramangala Forum ATM.',
      time: '22 min ago',
      type: 'success',
      read: false,
    },
    {
      id: 'N003',
      title: 'Team message',
      desc: 'Officer Priya: backup requested near Electronic City.',
      time: '1 hour ago',
      type: 'info',
      read: true,
    },
    {
      id: 'N004',
      title: 'Risk model updated',
      desc: 'Detection model retrained — accuracy improved to 94.2%.',
      time: '3 hours ago',
      type: 'system',
      read: true,
    },
    {
      id: 'N005',
      title: 'Weekly report ready',
      desc: 'Your sector performance summary for this week is ready to view.',
      time: 'Yesterday',
      type: 'warning',
      read: false,
    },
  ];

  let chatMessages = [
    { sender: 'Officer Priya', text: 'Team, we have unusual withdrawal activity building up at Electronic City ATM.', sent: false, time: '09:12 AM' },
    { sender: 'You', text: 'Copy that, heading there now.', sent: true, time: '09:13 AM' },
    { sender: 'Officer Arjun', text: 'Backup dispatched from MG Road station, ETA 12 minutes.', sent: false, time: '09:15 AM' },
  ];

  const AUTO_REPLIES = [
    { sender: 'Officer Priya', text: 'Copy that, standing by.' },
    { sender: 'Control Room', text: 'Received. Logging the update now.' },
    { sender: 'Officer Arjun', text: 'On my way, should be there shortly.' },
    { sender: 'Officer Priya', text: 'Confirmed, proceeding as planned.' },
    { sender: 'Control Room', text: 'Noted. Let us know if you need additional units.' },
    { sender: 'Officer Arjun', text: 'Understood, staying on channel.' },
  ];

  const REPORT_DATA = {
    fundsRecovered: 4250000,
    aiAccuracy: 94.2,
  };

  const ICONS = {
    alert: { bg: '#fee2e2', color: '#dc2626', svg: '<path d="M12 3l9 16H3L12 3z"/><path d="M12 10v4M12 17h.01"/>' },
    success: { bg: '#dcfce7', color: '#15803d', svg: '<path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/>' },
    info: { bg: '#e0f2fe', color: '#0284c7', svg: '<path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/>' },
    system: { bg: '#f1f5f9', color: '#475569', svg: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 00.34 1.87l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.7 1.7 0 00-1.87-.34 1.7 1.7 0 00-1 1.55V21a2 2 0 01-4 0v-.09A1.7 1.7 0 009 19.4a1.7 1.7 0 00-1.87.34l-.06.06a2 2 0 11-2.83-2.83l.06-.06A1.7 1.7 0 004.6 15a1.7 1.7 0 00-1.55-1H3a2 2 0 010-4h.09A1.7 1.7 0 004.6 9a1.7 1.7 0 00-.34-1.87l-.06-.06a2 2 0 112.83-2.83l.06.06A1.7 1.7 0 009 4.6a1.7 1.7 0 001-1.55V3a2 2 0 014 0v.09a1.7 1.7 0 001 1.55 1.7 1.7 0 001.87-.34l.06-.06a2 2 0 112.83 2.83l-.06.06A1.7 1.7 0 0019.4 9a1.7 1.7 0 001.55 1H21a2 2 0 010 4h-.09a1.7 1.7 0 00-1.51 1z"/>' },
    warning: { bg: '#fef3c7', color: '#92610a', svg: '<path d="M18 8a6 6 0 10-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 01-3.4 0"/>' },
  };

  const PRIORITY_COLOR = {
    critical: '#dc2626',
    high: '#f97316',
    medium: '#f59e0b',
    low: '#22c55e',
  };

  /* ------------------------------------------------------------------ *
   *  STATE
   * ------------------------------------------------------------------ */

  let currentTab = 'home';
  let map = null;
  let markerLayer = null;
  let userMarker = null;
  let modalConfirmCallback = null;

  /* ------------------------------------------------------------------ *
   *  UTILITIES
   * ------------------------------------------------------------------ */

  function formatINR(amount) {
    const num = Math.round(Math.abs(amount));
    const str = String(num);
    const lastThree = str.slice(-3);
    const rest = str.slice(0, -3);
    const grouped = rest ? rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + ',' + lastThree : lastThree;
    return (amount < 0 ? '-' : '') + '\u20B9' + grouped;
  }

  function nowTime() {
    const d = new Date();
    let h = d.getHours();
    const m = String(d.getMinutes()).padStart(2, '0');
    const ampm = h >= 12 ? 'PM' : 'AM';
    h = h % 12 || 12;
    return `${h}:${m} ${ampm}`;
  }

  function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function priorityLabel(p) {
    return p.charAt(0).toUpperCase() + p.slice(1);
  }

  function qs(id) { return document.getElementById(id); }

  /* ------------------------------------------------------------------ *
   *  SIDEBAR
   * ------------------------------------------------------------------ */

  function toggleSidebar() {
    const sidebar = qs('sidebar');
    sidebar.classList.contains('open') ? closeSidebar() : openSidebar();
  }

  function openSidebar() {
    qs('sidebar').classList.add('open');
    qs('sidebar').setAttribute('aria-hidden', 'false');
    qs('sidebarOverlay').classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeSidebar() {
    qs('sidebar').classList.remove('open');
    qs('sidebar').setAttribute('aria-hidden', 'true');
    qs('sidebarOverlay').classList.remove('show');
    document.body.style.overflow = '';
  }

  /* ------------------------------------------------------------------ *
   *  TAB SWITCHING
   * ------------------------------------------------------------------ */

  function switchTab(tab) {
    currentTab = tab;
    document.querySelectorAll('.tab-panel').forEach((p) => p.classList.remove('active'));
    qs('tab-' + tab).classList.add('active');

    document.querySelectorAll('.nav-item[data-tab]').forEach((n) => {
      n.classList.toggle('active', n.dataset.tab === tab);
    });
    document.querySelectorAll('.tabbar-item[data-tab]').forEach((n) => {
      n.classList.toggle('active', n.dataset.tab === tab);
    });

    closeSidebar();

    if (tab === 'map') {
      requestAnimationFrame(() => {
        if (!map) initMap();
        else map.invalidateSize();
      });
    }
    if (tab === 'chat') {
      requestAnimationFrame(scrollChatToBottom);
    }
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  /* ------------------------------------------------------------------ *
   *  ALERT CARDS
   * ------------------------------------------------------------------ */

  function renderAlertCard(a) {
    const fillColor = PRIORITY_COLOR[a.priority];
    return `
      <article class="alert-card alert-card--${a.priority}">
        <div class="alert-card-top">
          <div>
            <p class="alert-id">${a.id}</p>
            <p class="alert-name">${escapeHtml(a.atmName)}</p>
          </div>
          <span class="priority-badge priority-badge--${a.priority}">${priorityLabel(a.priority)}</span>
        </div>

        <div class="alert-meta">
          <span class="alert-meta-item">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M21 10c0 6.5-9 12-9 12S3 16.5 3 10a9 9 0 1118 0z" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="2.5" stroke="currentColor" stroke-width="1.8"/></svg>
            ${escapeHtml(a.location)}
          </span>
          <span class="alert-meta-item">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v5l3 3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
            ${a.timeWindow}
          </span>
          <span class="alert-meta-item">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M17 21v-2a4 4 0 00-4-4H7a4 4 0 00-4 4v2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/><circle cx="10" cy="7" r="4" stroke="currentColor" stroke-width="1.8"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
            ${a.mules} mule${a.mules > 1 ? 's' : ''}
          </span>
        </div>

        <div class="alert-risk-row">
          <div class="risk-track"><div class="risk-fill" style="width:${a.risk}%;background:${fillColor}"></div></div>
          <span class="risk-score">${a.risk}/100</span>
        </div>

        <div class="alert-amount-row">
          <span class="alert-amount-label">Flagged amount</span>
          <span class="alert-amount-value">${formatINR(a.amount)}</span>
        </div>

        <div class="alert-actions">
          <button class="btn ${a.verified ? 'btn-ghost' : 'btn-outline'}" ${a.verified ? 'disabled' : ''} onclick="triggerVerification('${a.id}')">
            ${a.verified
              ? '<svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/></svg> Verified'
              : '<svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"/></svg> Verify'}
          </button>
          <button class="btn btn-primary" onclick="navigateToATM('${a.id}')">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><path d="M3 11l18-8-8 18-2-8-8-2z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg> Navigate
          </button>
        </div>
      </article>`;
  }

  function renderAlerts() {
    const sorted = [...ALERTS].sort((a, b) => b.risk - a.risk);
    qs('homeAlertList').innerHTML = sorted.slice(0, 3).map(renderAlertCard).join('');
    qs('fullAlertList').innerHTML = sorted.map(renderAlertCard).join('');

    const unreviewed = ALERTS.filter((a) => !a.reviewed).length;
    const badge = qs('navAlertBadge');
    if (unreviewed > 0) {
      badge.textContent = unreviewed;
      badge.style.display = '';
    } else {
      badge.style.display = 'none';
    }

    const critical = ALERTS.filter((a) => a.priority === 'critical').length;
    qs('statActive').textContent = ALERTS.length;
    qs('statCritical').textContent = critical;
  }

  function triggerVerification(alertId) {
    const alert = ALERTS.find((a) => a.id === alertId);
    if (!alert || alert.verified) return;

    openModal({
      title: 'Trigger verification',
      message: `Send a manual verification request for ${alert.atmName}. This will confirm the flagged withdrawal pattern with the on-site device log.`,
      extraHTML: `
        <div class="detail-card" style="margin-top:0;">
          <div class="detail-row"><span class="detail-label">Alert ID</span><span class="detail-value">${alert.id}</span></div>
          <div class="detail-row"><span class="detail-label">Location</span><span class="detail-value">${escapeHtml(alert.location)}</span></div>
          <div class="detail-row"><span class="detail-label">Flagged amount</span><span class="detail-value">${formatINR(alert.amount)}</span></div>
        </div>`,
      confirmText: 'Verify now',
      confirmVariant: 'primary',
      onConfirm: () => {
        alert.verified = true;
        alert.reviewed = true;
        renderAlerts();
        showToast(`Verification confirmed for ${alert.id}`, 'success');
      },
    });
  }

  function navigateToATM(alertId) {
    const alert = ALERTS.find((a) => a.id === alertId);
    if (!alert) return;
    switchTab('map');
    setTimeout(() => {
      if (!map) initMap();
      map.flyTo([alert.lat, alert.lng], 15, { duration: 1.1 });
      const marker = markerLayer && markerLayer[alertId];
      if (marker) setTimeout(() => marker.openPopup(), 900);
    }, 120);
  }

  function markAllAlertsRead() {
    ALERTS.forEach((a) => (a.reviewed = true));
    renderAlerts();
    showToast('All alerts marked as read', 'success');
  }

  /* ------------------------------------------------------------------ *
   *  RECENT ACTIVITY
   * ------------------------------------------------------------------ */

  const ACTIVITY = [
    { icon: 'alert', title: 'Alert A001 triggered at MG Road Central ATM', time: '5 min ago' },
    { icon: 'success', title: 'Verification completed for A003', time: '40 min ago' },
    { icon: 'info', title: 'You joined Sector Team Chat', time: '2 hours ago' },
    { icon: 'system', title: 'Weekly report exported', time: 'Yesterday' },
  ];

  function renderActivity() {
    qs('activityList').innerHTML = ACTIVITY.map((item) => {
      const ic = ICONS[item.icon];
      return `
        <div class="activity-item">
          <div class="activity-icon" style="background:${ic.bg};color:${ic.color}">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">${ic.svg}</svg>
          </div>
          <div class="activity-text">
            <p class="activity-title">${escapeHtml(item.title)}</p>
            <p class="activity-time">${item.time}</p>
          </div>
        </div>`;
    }).join('');
  }

  /* ------------------------------------------------------------------ *
   *  MAP (Leaflet)
   * ------------------------------------------------------------------ */

  function buildAtmIcon(a) {
    const color = PRIORITY_COLOR[a.priority];
    const pulse = a.priority === 'critical'
      ? `<span class="atm-marker-pulse" style="background:${color}"></span>`
      : '';
    return L.divIcon({
      className: '',
      html: `<div class="atm-marker">${pulse}<span class="atm-marker-dot" style="background:${color}"></span></div>`,
      iconSize: [16, 16],
      iconAnchor: [8, 8],
      popupAnchor: [0, -10],
    });
  }

  function initMap() {
    if (map) return;
    map = L.map('leafletMap', { zoomControl: true, attributionControl: false }).setView([12.9716, 77.5946], 12);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
    }).addTo(map);

    userMarker = L.marker([12.9716, 77.5946], {
      icon: L.divIcon({
        className: '',
        html: '<div class="user-marker"></div>',
        iconSize: [18, 18],
        iconAnchor: [9, 9],
      }),
    }).addTo(map).bindPopup('<div class="map-popup"><p class="map-popup-title">Your location</p><p class="map-popup-row">MG Road Sector HQ</p></div>');

    markerLayer = {};
    ALERTS.forEach((a) => {
      const marker = L.marker([a.lat, a.lng], { icon: buildAtmIcon(a) }).addTo(map);
      marker.bindPopup(`
        <div class="map-popup">
          <p class="map-popup-title">${escapeHtml(a.atmName)}</p>
          <p class="map-popup-row">Risk score: <strong>${a.risk}/100</strong> &middot; ${priorityLabel(a.priority)}</p>
          <p class="map-popup-row">Flagged: ${formatINR(a.amount)}</p>
          <button class="map-popup-btn" onclick="triggerVerification('${a.id}')">Verify</button>
        </div>
      `);
      markerLayer[a.id] = marker;
    });

    setTimeout(() => map.invalidateSize(), 200);
  }

  function refreshMap() {
    if (!map) {
      initMap();
    } else {
      map.flyTo([12.9716, 77.5946], 12, { duration: 0.8 });
    }
    showToast('Map refreshed', 'info');
  }

  /* ------------------------------------------------------------------ *
   *  CHAT
   * ------------------------------------------------------------------ */

  function renderMsgRow(msg) {
    return `
      <div class="msg-row ${msg.sent ? 'msg-row--sent' : 'msg-row--received'}">
        ${!msg.sent ? `<p class="msg-sender">${escapeHtml(msg.sender)}</p>` : ''}
        <div class="msg-bubble">${escapeHtml(msg.text)}</div>
        <p class="msg-time">${msg.time}</p>
      </div>`;
  }

  function renderChat() {
    qs('chatMessages').innerHTML = chatMessages.map(renderMsgRow).join('');
    scrollChatToBottom();
  }

  function scrollChatToBottom() {
    const el = qs('chatMessages');
    if (el) el.scrollTop = el.scrollHeight;
  }

  function sendMessage(event) {
    if (event) event.preventDefault();
    const input = qs('chatInput');
    const text = input.value.trim();
    if (!text) return false;

    chatMessages.push({ sender: 'You', text, sent: true, time: nowTime() });
    renderChat();
    input.value = '';

    const delay = 900 + Math.random() * 1600;
    setTimeout(() => {
      const reply = AUTO_REPLIES[Math.floor(Math.random() * AUTO_REPLIES.length)];
      chatMessages.push({ sender: reply.sender, text: reply.text, sent: false, time: nowTime() });
      renderChat();
    }, delay);

    return false;
  }

  function clearChat() {
    openModal({
      title: 'Clear conversation',
      message: 'This will remove all messages from this device. Team members will still have their own copies.',
      confirmText: 'Clear chat',
      confirmVariant: 'danger',
      onConfirm: () => {
        chatMessages = [];
        renderChat();
        showToast('Chat cleared', 'success');
      },
    });
  }

  /* ------------------------------------------------------------------ *
   *  NOTIFICATIONS
   * ------------------------------------------------------------------ */

  function renderNotifications() {
    qs('notifList').innerHTML = NOTIFICATIONS.map((n) => {
      const ic = ICONS[n.type] || ICONS.info;
      return `
        <div class="notif-item ${!n.read ? 'notif-item--unread' : ''}">
          <div class="notif-icon" style="background:${ic.bg};color:${ic.color}">
            <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor">${ic.svg}</svg>
          </div>
          <div class="notif-body">
            <p class="notif-title">${escapeHtml(n.title)}</p>
            <p class="notif-desc">${escapeHtml(n.desc)}</p>
            <div class="notif-footer-row">
              <span class="notif-time">${n.time}</span>
              ${n.read
                ? '<span class="notif-read-badge"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="9"/></svg> Read</span>'
                : `<button class="notif-mark-btn" onclick="markNotificationRead('${n.id}')">Mark read</button>`}
            </div>
          </div>
        </div>`;
    }).join('');

    const dot = qs('notifDot');
    const anyUnread = NOTIFICATIONS.some((n) => !n.read);
    dot.classList.toggle('show', anyUnread);
  }

  function markNotificationRead(id) {
    const n = NOTIFICATIONS.find((x) => x.id === id);
    if (n) n.read = true;
    renderNotifications();
  }

  function markAllNotificationsRead() {
    NOTIFICATIONS.forEach((n) => (n.read = true));
    renderNotifications();
    showToast('All notifications marked as read', 'success');
  }

  function toggleNotifications() {
    const panel = qs('notifPanel');
    const open = panel.classList.contains('open');
    if (open) {
      panel.classList.remove('open');
      panel.setAttribute('aria-hidden', 'true');
      qs('notifOverlay').classList.remove('show');
      document.body.style.overflow = '';
    } else {
      panel.classList.add('open');
      panel.setAttribute('aria-hidden', 'false');
      qs('notifOverlay').classList.add('show');
      document.body.style.overflow = 'hidden';
    }
  }

  /* ------------------------------------------------------------------ *
   *  MODAL
   * ------------------------------------------------------------------ */

  function openModal({ title, message, extraHTML = '', confirmText = 'Confirm', cancelText = 'Cancel', confirmVariant = 'primary', hideCancel = false, onConfirm = null }) {
    qs('modalTitle').textContent = title;
    qs('modalMessage').textContent = message || '';
    qs('modalMessage').style.display = message ? '' : 'none';
    qs('modalExtra').innerHTML = extraHTML;

    const confirmBtn = qs('modalConfirmBtn');
    confirmBtn.textContent = confirmText;
    confirmBtn.className = 'btn ' + (confirmVariant === 'danger' ? 'btn-danger' : 'btn-primary');
    confirmBtn.style.display = onConfirm ? '' : 'none';

    const cancelBtn = qs('modalCancelBtn');
    cancelBtn.textContent = hideCancel ? 'Close' : cancelText;

    modalConfirmCallback = onConfirm;

    qs('modal').classList.add('open');
    qs('modalOverlay').classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    qs('modal').classList.remove('open');
    qs('modalOverlay').classList.remove('show');
    document.body.style.overflow = '';
    modalConfirmCallback = null;
  }

  function confirmModalAction() {
    if (typeof modalConfirmCallback === 'function') {
      modalConfirmCallback();
    }
    closeModal();
  }

  /* ------------------------------------------------------------------ *
   *  EMERGENCY
   * ------------------------------------------------------------------ */

  function emergencyCall() {
    openModal({
      title: 'Emergency helplines',
      message: 'Select a helpline to call immediately.',
      hideCancel: true,
      extraHTML: `
        <button class="emergency-option" onclick="callNumber('112','Police')">
          <div class="emergency-icon" style="background:var(--danger)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8"><path d="M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6 19.8 19.8 0 01-3.1-8.7A2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .3 2 .6 2.9a2 2 0 01-.5 2.1L7.9 10a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.5c.9.3 1.9.5 2.9.6a2 2 0 011.8 2.1z"/></svg>
          </div>
          <div>
            <p class="emergency-title">Police</p>
            <p class="emergency-sub">All-India emergency response</p>
          </div>
          <span class="emergency-number" style="color:var(--danger)">112</span>
        </button>
        <button class="emergency-option" onclick="callNumber('1930','Cyber Crime Helpline')">
          <div class="emergency-icon" style="background:var(--primary)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8"><rect x="4" y="2" width="16" height="20" rx="2"/><path d="M12 18h.01"/></svg>
          </div>
          <div>
            <p class="emergency-title">Cyber Crime Helpline</p>
            <p class="emergency-sub">Report financial fraud</p>
          </div>
          <span class="emergency-number" style="color:var(--primary)">1930</span>
        </button>
        <button class="emergency-option" onclick="callNumber('108','Medical')">
          <div class="emergency-icon" style="background:var(--success)">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1.8"><path d="M19 14c1.5-1.5 3-3.4 3-5.5A4.5 4.5 0 0017.5 4c-1.7 0-3 .8-4.5 2.5C11.5 4.8 10.2 4 8.5 4A4.5 4.5 0 004 8.5C4 13 12 20 12 20s3.5-3.1 5.8-5.4"/><path d="M8 12h2l1-2 2 4 1-2h2"/></svg>
          </div>
          <div>
            <p class="emergency-title">Medical</p>
            <p class="emergency-sub">Ambulance &amp; first response</p>
          </div>
          <span class="emergency-number" style="color:var(--success)">108</span>
        </button>`,
      onConfirm: null,
    });
  }

  function callNumber(number, label) {
    showToast(`Calling ${label} \u2014 ${number}`, 'warning');
    window.location.href = `tel:${number}`;
  }

  /* ------------------------------------------------------------------ *
   *  REPORTS
   * ------------------------------------------------------------------ */

  function viewReports() {
    const critical = ALERTS.filter((a) => a.priority === 'critical').length;
    const high = ALERTS.filter((a) => a.priority === 'high').length;
    const medium = ALERTS.filter((a) => a.priority === 'medium').length;
    const low = ALERTS.filter((a) => a.priority === 'low').length;

    openModal({
      title: 'Sector analytics',
      message: 'Live summary of your assigned ATM fraud sector.',
      extraHTML: `
        <div class="report-grid">
          <div class="report-stat"><p class="report-stat-value">${ALERTS.length}</p><p class="report-stat-label">Total active cases</p></div>
          <div class="report-stat"><p class="report-stat-value" style="color:var(--danger)">${critical + high}</p><p class="report-stat-label">High + critical</p></div>
          <div class="report-stat"><p class="report-stat-value" style="color:#92610a">${medium}</p><p class="report-stat-label">Medium priority</p></div>
          <div class="report-stat"><p class="report-stat-value" style="color:#15803d">${low}</p><p class="report-stat-label">Low priority</p></div>
          <div class="report-stat" style="grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;text-align:left;">
            <span class="report-stat-label" style="margin:0;">Funds recovered</span>
            <span class="report-stat-value" style="font-size:16px;">${formatINR(REPORT_DATA.fundsRecovered)}</span>
          </div>
          <div class="report-stat" style="grid-column:1/-1;display:flex;align-items:center;justify-content:space-between;text-align:left;">
            <span class="report-stat-label" style="margin:0;">AI prediction accuracy</span>
            <span class="report-stat-value" style="font-size:16px;color:var(--primary)">${REPORT_DATA.aiAccuracy}%</span>
          </div>
        </div>`,
      confirmText: 'Export report',
      confirmVariant: 'primary',
      onConfirm: exportReport,
    });
  }

  function exportReport() {
    showToast('Report exported to downloads', 'success');
  }

  /* ------------------------------------------------------------------ *
   *  LOGOUT
   * ------------------------------------------------------------------ */

  function handleLogout() {
    openModal({
      title: 'Log out',
      message: 'You will be signed out of Police Field on this device.',
      confirmText: 'Log out',
      confirmVariant: 'danger',
      onConfirm: () => {
        showToast('Logged out successfully', 'success');
        closeSidebar();
      },
    });
  }

  /* ------------------------------------------------------------------ *
   *  TOASTS
   * ------------------------------------------------------------------ */

  const TOAST_ICONS = {
    success: '<path d="M9 12l2 2 4-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/>',
    error: '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M15 9l-6 6M9 9l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    warning: '<path d="M12 3l9 16H3L12 3z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M12 10v4M12 17h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    info: '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 8h.01M11 12h1v5h1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
  };

  function showToast(message, type = 'info', duration = 3000) {
    const container = qs('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<svg width="17" height="17" viewBox="0 0 24 24" fill="none">${TOAST_ICONS[type] || TOAST_ICONS.info}</svg><span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.classList.add('hide');
      setTimeout(() => toast.remove(), 260);
    }, duration);
  }

  /* ------------------------------------------------------------------ *
   *  INIT
   * ------------------------------------------------------------------ */

  function init() {
    renderAlerts();
    renderActivity();
    renderChat();
    renderNotifications();
    switchTab('home');
  }

  document.addEventListener('DOMContentLoaded', init);

  /* ------------------------------------------------------------------ *
   *  EXPOSE GLOBALLY
   * ------------------------------------------------------------------ */

  window.toggleSidebar = toggleSidebar;
  window.openSidebar = openSidebar;
  window.closeSidebar = closeSidebar;
  window.switchTab = switchTab;
  window.triggerVerification = triggerVerification;
  window.navigateToATM = navigateToATM;
  window.markAllAlertsRead = markAllAlertsRead;
  window.initMap = initMap;
  window.refreshMap = refreshMap;
  window.sendMessage = sendMessage;
  window.clearChat = clearChat;
  window.toggleNotifications = toggleNotifications;
  window.markNotificationRead = markNotificationRead;
  window.markAllNotificationsRead = markAllNotificationsRead;
  window.openModal = openModal;
  window.closeModal = closeModal;
  window.confirmModalAction = confirmModalAction;
  window.emergencyCall = emergencyCall;
  window.callNumber = callNumber;
  window.viewReports = viewReports;
  window.exportReport = exportReport;
  window.handleLogout = handleLogout;
  window.showToast = showToast;
})();