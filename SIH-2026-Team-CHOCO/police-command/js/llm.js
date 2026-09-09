// ========== LLM KNOWLEDGE BASE ==========
const KnowledgeBase = {
    complaints: {
        'C1001': {
            victim: 'Rahul Sharma',
            amount: '₹5,00,000',
            type: 'Investment Scam',
            status: 'AI Analyzing',
            details: 'Victim was lured into a fake investment scheme promising 200% returns. Money was transferred via UPI to mule accounts.',
            mules: ['Mule A (₹5.0L)', 'Mule B (₹4.5L)', 'Mule C (₹2.0L)'],
            atm: 'ATM #452 (92% risk)',
            timeline: 'Reported 2.3 hours ago',
            location: 'Indiranagar'
        },
        'C1002': {
            victim: 'Priya Mehta',
            amount: '₹2,50,000',
            type: 'UPI Fraud',
            status: 'Action Taken',
            details: 'Fraudster posed as bank representative and obtained UPI PIN. Money was transferred to multiple mule accounts.',
            mules: ['Mule D (₹2.5L)'],
            atm: 'ATM #789 (67% risk)',
            timeline: 'Reported 4.1 hours ago',
            location: 'MG Road'
        },
        'C1003': {
            victim: 'Vikram Patel',
            amount: '₹1,00,000',
            type: 'KYC Fraud',
            status: 'Resolved',
            details: 'Victim received fake KYC update link. Funds were recovered and mule accounts frozen.',
            mules: [],
            atm: 'None',
            timeline: 'Resolved 2 days ago',
            location: 'Koramangala'
        },
        'C1004': {
            victim: 'Ananya Krishnan',
            amount: '₹7,50,000',
            type: 'Investment Scam',
            status: 'AI Analyzing',
            details: 'Large-scale investment fraud involving multiple victims. Money traced to 5 different mule accounts.',
            mules: ['Mule A (₹5.0L)', 'Mule E (₹2.5L)'],
            atm: 'ATM #234 (88% risk)',
            timeline: 'Reported 1.8 hours ago',
            location: 'Bannerghatta'
        }
    },
    atms: {
        'ATM #452': { risk: 92, location: 'Indiranagar', mules: 4, complaints: 3, window: '2.3 hours', bank: 'SBI' },
        'ATM #789': { risk: 67, location: 'MG Road', mules: 2, complaints: 1, window: '4.1 hours', bank: 'HDFC' },
        'ATM #456': { risk: 55, location: 'Jayanagar', mules: 3, complaints: 2, window: '1.5 hours', bank: 'ICICI' },
        'ATM #123': { risk: 34, location: 'Koramangala', mules: 0, complaints: 0, window: '5.0 hours', bank: 'Axis' },
        'ATM #890': { risk: 78, location: 'Yeshwanthpur', mules: 3, complaints: 2, window: '3.2 hours', bank: 'SBI' },
        'ATM #567': { risk: 45, location: 'HSR Layout', mules: 1, complaints: 1, window: '6.0 hours', bank: 'Kotak' },
        'ATM #234': { risk: 88, location: 'Bannerghatta', mules: 5, complaints: 4, window: '1.8 hours', bank: 'HDFC' },
        'ATM #678': { risk: 72, location: 'Electronic City', mules: 3, complaints: 2, window: '2.7 hours', bank: 'ICICI' },
        'ATM #345': { risk: 61, location: 'Malleshwaram', mules: 2, complaints: 1, window: '3.5 hours', bank: 'SBI' },
        'ATM #901': { risk: 39, location: 'Rajajinagar', mules: 0, complaints: 0, window: '7.0 hours', bank: 'Axis' },
        'ATM #112': { risk: 51, location: 'Basavanagudi', mules: 1, complaints: 1, window: '4.5 hours', bank: 'Kotak' },
        'ATM #335': { risk: 44, location: 'Marathahalli', mules: 1, complaints: 0, window: '5.8 hours', bank: 'HDFC' }
    },
    mules: {
        'Mule A': { account: 'XXXX1234', bank: 'SBI', risk: 92, amount: '₹5,00,000', complaints: 3, status: 'Critical' },
        'Mule B': { account: 'XXXX5678', bank: 'HDFC', risk: 78, amount: '₹4,50,000', complaints: 2, status: 'High' },
        'Mule C': { account: 'XXXX9012', bank: 'ICICI', risk: 65, amount: '₹2,00,000', complaints: 2, status: 'Medium' },
        'Mule D': { account: 'XXXX3456', bank: 'Axis', risk: 45, amount: '₹2,50,000', complaints: 2, status: 'Medium' },
        'Mule E': { account: 'XXXX7890', bank: 'Kotak', risk: 28, amount: '₹2,50,000', complaints: 1, status: 'Low' }
    },
    fraudTypes: {
        'Investment Scam': 'Fraudsters promise high returns on investments. Typically involves fake companies or schemes. Common on social media and WhatsApp.',
        'UPI Fraud': 'Fraudsters trick victims into sharing UPI PIN or scanning malicious QR codes. Often involves fake payment requests.',
        'KYC Fraud': 'Fraudsters send fake KYC update links to steal banking credentials. Often via SMS or email.',
        'Phishing': 'Fraudsters send fake emails or messages impersonating legitimate organizations to steal credentials.',
        'Job Fraud': 'Fraudsters offer fake job opportunities and ask for money for processing or training.',
        'Other': 'Other types of cyber fraud not categorized above.'
    },
    trends: {
        'this week': {
            total: 47,
            investment: 24,
            upi: 18,
            kyc: 12,
            phishing: 8,
            job: 5,
            other: 3,
            peak_time: '2 PM - 6 PM',
            top_location: 'Indiranagar',
            avg_amount: '₹3,20,000',
            most_affected: 'Professionals aged 25-40'
        },
        'today': {
            total: 12,
            investment: 6,
            upi: 4,
            kyc: 2,
            peak_hour: '3 PM',
            top_location: 'Bannerghatta'
        },
        'this month': {
            total: 187,
            recovered: '₹8.2Cr',
            resolved: 43,
            pending: 144,
            top_fraud: 'Investment Scam'
        }
    },
    locations: {
        'Indiranagar': { atms: ['ATM #452'], complaints: 3, risk_level: 'High' },
        'MG Road': { atms: ['ATM #789'], complaints: 1, risk_level: 'Medium' },
        'Bannerghatta': { atms: ['ATM #234'], complaints: 4, risk_level: 'Critical' },
        'Koramangala': { atms: ['ATM #123'], complaints: 0, risk_level: 'Low' },
        'Jayanagar': { atms: ['ATM #456'], complaints: 2, risk_level: 'Medium' }
    }
};

// ========== LLM RESPONSE GENERATOR ==========
function generateLLMResponse(query) {
    const lower = query.toLowerCase().trim();
    
    // ===== Greeting / Help =====
    if (lower.match(/^(hi|hello|hey|good morning|good evening|help|what can you do)/)) {
        return `Hello! I am your Cyber Intelligence Analyst. I can help you with:\n\n` +
               `1. ATM Risk Analysis - "Show high risk ATMs" or "ATM 452 risk"\n` +
               `2. Mule Detection - "Find mules for C1001" or "Show mule accounts"\n` +
               `3. Fraud Trends - "Show fraud trends this week" or "Today's fraud report"\n` +
               `4. Case Intelligence - "Show complaint C1001" or "Details of C1002"\n` +
               `5. Location Analysis - "Show ATMs in Indiranagar"\n` +
               `6. Fraud Type Info - "What is Investment Scam" or "Explain UPI Fraud"\n\n` +
               `Ask me anything about cybercrime intelligence!`;
    }
    
    // ===== ATM Queries =====
    if (lower.includes('high risk') || lower.includes('highest risk') || lower.includes('top risk')) {
        if (lower.includes('indiranagar')) {
            const atms = Object.entries(KnowledgeBase.atms)
                .filter(([_, data]) => data.location === 'Indiranagar' && data.risk >= 70)
                .map(([id, data]) => `${id}: ${data.risk}% risk, ${data.mules} mules, ${data.complaints} complaints`)
                .join('\n');
            return `🔍 High-Risk ATMs in Indiranagar:\n\n${atms || 'None found in Indiranagar.'}`;
        }
        
        const sorted = Object.entries(KnowledgeBase.atms)
            .sort((a, b) => b[1].risk - a[1].risk)
            .slice(0, 5);
        const result = sorted.map(([id, data], i) => 
            `${i+1}. ${id}: ${data.risk}% risk | Location: ${data.location} | Mules: ${data.mules} | Complaints: ${data.complaints}`
        ).join('\n');
        return `📊 Top 5 Highest Risk ATMs:\n\n${result}\n\nRecommendation: Immediate verification recommended for ${sorted[0][0]}.`;
    }
    
    if (lower.includes('atm') && (lower.includes('risk') || lower.includes('risk of'))) {
        const atmMatch = lower.match(/atm\s*#?\s*(\d+)/i);
        if (atmMatch) {
            const atmId = `ATM #${atmMatch[1]}`;
            const data = KnowledgeBase.atms[atmId];
            if (data) {
                return `📍 ATM ${atmId} Report:\n\n` +
                       `Risk Score: ${data.risk}% (${data.risk >= 70 ? '🔴 HIGH' : data.risk >= 40 ? '🟡 MEDIUM' : '🟢 LOW'})\n` +
                       `Location: ${data.location}\n` +
                       `Mules Connected: ${data.mules}\n` +
                       `Complaints: ${data.complaints}\n` +
                       `Withdrawal Window: ${data.window}\n` +
                       `Bank: ${data.bank}\n\n` +
                       `Recommendation: ${data.risk >= 70 ? 'Immediate verification required.' : data.risk >= 40 ? 'Monitor closely.' : 'Routine check recommended.'}`;
            }
            return `❌ ATM ${atmId} not found in the system. Please check the ATM number.`;
        }
        return `Please specify an ATM number, e.g., "Show risk of ATM 452"`;
    }
    
    if (lower.includes('atm') && (lower.includes('list') || lower.includes('show'))) {
        const locationMatch = lower.match(/in\s+([a-z\s]+)/i);
        if (locationMatch) {
            const loc = locationMatch[1].trim();
            const atms = Object.entries(KnowledgeBase.atms)
                .filter(([_, data]) => data.location.toLowerCase().includes(loc.toLowerCase()))
                .map(([id, data]) => `${id}: ${data.risk}% risk, ${data.mules} mules`)
                .join('\n');
            if (atms) {
                return `📍 ATMs in ${loc}:\n\n${atms}`;
            }
            return `No ATMs found in ${loc}.`;
        }
        const allAtms = Object.entries(KnowledgeBase.atms)
            .map(([id, data]) => `${id}: ${data.risk}% risk at ${data.location}`)
            .join('\n');
        return `📋 All ATMs in the system:\n\n${allAtms}`;
    }
    
    // ===== Complaint Queries =====
    if (lower.match(/complaint\s*c\d+/i) || lower.match(/c\d+/i)) {
        const idMatch = lower.match(/c(\d+)/i);
        if (idMatch) {
            const id = `C${idMatch[1]}`;
            const data = KnowledgeBase.complaints[id];
            if (data) {
                return `📋 Complaint ${id} Details:\n\n` +
                       `Victim: ${data.victim}\n` +
                       `Amount: ${data.amount}\n` +
                       `Type: ${data.type}\n` +
                       `Status: ${data.status}\n` +
                       `Location: ${data.location || 'N/A'}\n` +
                       `Details: ${data.details}\n` +
                       `Mules: ${data.mules.join(', ') || 'None'}\n` +
                       `ATM: ${data.atm || 'None'}\n` +
                       `Timeline: ${data.timeline}`;
            }
            return `❌ Complaint ${id} not found. Please check the complaint ID.`;
        }
    }
    
    // ===== Mule Queries =====
    if (lower.includes('mule') || lower.includes('mules')) {
        if (lower.includes('all') || lower.includes('list') || lower.includes('show')) {
            const allMules = Object.entries(KnowledgeBase.mules)
                .map(([id, data]) => `${id}: ${data.account} (${data.bank}) - ${data.risk}% risk - ${data.amount}`)
                .join('\n');
            return `🔄 All Mule Accounts:\n\n${allMules}\n\n${Object.keys(KnowledgeBase.mules).length} mule accounts in the system.`;
        }
        if (lower.includes('high risk') || lower.includes('critical')) {
            const highMules = Object.entries(KnowledgeBase.mules)
                .filter(([_, data]) => data.risk >= 70)
                .map(([id, data]) => `${id}: ${data.account} (${data.bank}) - ${data.risk}% risk - ${data.amount}`)
                .join('\n');
            return `🔴 High-Risk Mule Accounts:\n\n${highMules || 'None found.'}\n\nRecommendation: Freeze immediately.`;
        }
        if (lower.includes('c1001')) {
            const mules = KnowledgeBase.complaints['C1001']?.mules || [];
            return `🔗 Mules connected to C1001:\n\n${mules.map(m => `• ${m}`).join('\n')}\n\nRecommendation: Freeze Mule A immediately.`;
        }
        const allMules = Object.entries(KnowledgeBase.mules)
            .map(([id, data]) => `${id}: ${data.account} (${data.bank}) - ${data.risk}% risk`)
            .join('\n');
        return `🔄 Mule Accounts:\n\n${allMules}`;
    }
    
    // ===== Trend Queries =====
    if (lower.includes('trend') || lower.includes('this week') || lower.includes('weekly')) {
        const data = KnowledgeBase.trends['this week'];
        return `📊 Weekly Fraud Trends Report:\n\n` +
               `Total Complaints: ${data.total}\n` +
               `Investment Scams: ${data.investment}\n` +
               `UPI Frauds: ${data.upi}\n` +
               `KYC Frauds: ${data.kyc}\n` +
               `Phishing: ${data.phishing}\n` +
               `Job Frauds: ${data.job}\n` +
               `Other: ${data.other}\n\n` +
               `Peak Time: ${data.peak_time}\n` +
               `Top Location: ${data.top_location}\n` +
               `Average Amount: ${data.avg_amount}\n` +
               `Most Affected: ${data.most_affected}`;
    }
    
    if (lower.includes('today') || lower.includes('daily')) {
        const data = KnowledgeBase.trends['today'];
        return `📊 Today's Fraud Report:\n\n` +
               `Total Complaints: ${data.total}\n` +
               `Investment: ${data.investment}\n` +
               `UPI: ${data.upi}\n` +
               `KYC: ${data.kyc}\n\n` +
               `Peak Hour: ${data.peak_hour}\n` +
               `Top Location: ${data.top_location}`;
    }
    
    if (lower.includes('month') || lower.includes('monthly')) {
        const data = KnowledgeBase.trends['this month'];
        return `📊 Monthly Report:\n\n` +
               `Total Complaints: ${data.total}\n` +
               `Funds Recovered: ${data.recovered}\n` +
               `Resolved Cases: ${data.resolved}\n` +
               `Pending Cases: ${data.pending}\n` +
               `Top Fraud Type: ${data.top_fraud}`;
    }
    
    // ===== Fraud Type Queries =====
    for (const [type, description] of Object.entries(KnowledgeBase.fraudTypes)) {
        if (lower.includes(type.toLowerCase().replace(' ', '')) || lower.includes(type.toLowerCase())) {
            return `📖 ${type}:\n\n${description}`;
        }
    }
    
    // ===== Location Queries =====
    if (lower.includes('location') || lower.includes('in')) {
        const locationMatch = lower.match(/in\s+([a-z\s]+)/i) || lower.match(/location\s+([a-z\s]+)/i);
        if (locationMatch) {
            const loc = locationMatch[1].trim();
            const data = KnowledgeBase.locations[loc];
            if (data) {
                return `📍 Location Analysis: ${loc}\n\n` +
                       `ATMs: ${data.atms.join(', ')}\n` +
                       `Complaints: ${data.complaints}\n` +
                       `Risk Level: ${data.risk_level}\n\n` +
                       `${data.risk_level === 'Critical' ? '🚨 Immediate action required.' : data.risk_level === 'High' ? '⚠️ High vigilance needed.' : '📊 Routine monitoring recommended.'}`;
            }
            const atms = Object.entries(KnowledgeBase.atms)
                .filter(([_, data]) => data.location.toLowerCase().includes(loc.toLowerCase()))
                .map(([id, data]) => `${id}: ${data.risk}% risk`)
                .join('\n');
            if (atms) {
                return `📍 ATMs in ${loc}:\n\n${atms}`;
            }
            return `No data found for ${loc}.`;
        }
    }
    
    // ===== Summary / Statistics =====
    if (lower.includes('summary') || lower.includes('stats') || lower.includes('statistics') || lower.includes('overview')) {
        const totalAtms = Object.keys(KnowledgeBase.atms).length;
        const totalComplaints = Object.keys(KnowledgeBase.complaints).length;
        const totalMules = Object.keys(KnowledgeBase.mules).length;
        const highRisk = Object.values(KnowledgeBase.atms).filter(a => a.risk >= 70).length;
        const avgRisk = Object.values(KnowledgeBase.atms).reduce((sum, a) => sum + a.risk, 0) / totalAtms;
        
        return `📊 System Overview:\n\n` +
               `ATMs Monitored: ${totalAtms}\n` +
               `Active Complaints: ${totalComplaints}\n` +
               `Mule Accounts: ${totalMules}\n` +
               `High-Risk ATMs: ${highRisk}\n` +
               `Average Risk Score: ${Math.round(avgRisk)}%\n\n` +
               `System Status: 🟢 Online\n` +
               `Last Update: ${new Date().toLocaleString()}`;
    }
    
    // ===== Default Response =====
    return `I understand you're asking about "${query}". Let me analyze...\n\n` +
           `I have information about:\n` +
           `• ${Object.keys(KnowledgeBase.atms).length} ATMs tracked\n` +
           `• ${Object.keys(KnowledgeBase.complaints).length} active complaints\n` +
           `• ${Object.keys(KnowledgeBase.mules).length} mule accounts\n` +
           `• ${Object.keys(KnowledgeBase.fraudTypes).length} fraud types\n\n` +
           `Please rephrase your question or ask something more specific. Try:\n` +
           `- "Show high risk ATMs"\n` +
           `- "Find mules for C1001"\n` +
           `- "Show fraud trends this week"\n` +
           `- "What is Investment Scam"`;
}

// ========== SEND LLM QUERY ==========
function sendLLMQuery() {
    const input = document.getElementById('llmInput');
    const query = input.value.trim();
    if (!query) {
        showToast('Please enter a question', 'warning');
        return;
    }
    
    const chat = document.getElementById('llmChatFull');
    if (!chat) return;
    
    // Add user message
    const userMsg = document.createElement('div');
    userMsg.className = 'llm-message user';
    userMsg.innerHTML = `
        <div class="message-avatar">👤</div>
        <div class="message-content"><p>${query}</p></div>
    `;
    chat.appendChild(userMsg);
    
    // Add typing indicator
    const typingMsg = document.createElement('div');
    typingMsg.className = 'llm-message assistant';
    typingMsg.id = 'typingIndicator';
    typingMsg.innerHTML = `
        <div class="message-avatar">AI</div>
        <div class="message-content"><p>⏳ Analyzing intelligence...</p></div>
    `;
    chat.appendChild(typingMsg);
    chat.scrollTop = chat.scrollHeight;
    
    input.value = '';
    input.disabled = true;
    
    // Generate response with realistic delay
    const delay = 800 + Math.random() * 700;
    setTimeout(() => {
        // Remove typing indicator
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
        
        // Generate response
        const response = generateLLMResponse(query);
        const formatted = response.replace(/\n/g, '<br>');
        
        const assistantMsg = document.createElement('div');
        assistantMsg.className = 'llm-message assistant';
        assistantMsg.innerHTML = `
            <div class="message-avatar">AI</div>
            <div class="message-content"><p>${formatted}</p></div>
        `;
        chat.appendChild(assistantMsg);
        chat.scrollTop = chat.scrollHeight;
        
        input.disabled = false;
        input.focus();
    }, delay);
}

// ========== EXPOSE FUNCTIONS ==========
window.sendLLMQuery = sendLLMQuery;
window.setLLMInput = setLLMInput;
window.clearLLMChat = clearLLMChat;

console.log('🧠 LLM Agent loaded with knowledge base');