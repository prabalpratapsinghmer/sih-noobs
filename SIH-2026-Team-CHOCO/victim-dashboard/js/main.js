// ========== STATE MANAGEMENT ==========
const state = {
    currentStep: 1,
    totalSteps: 4,
    files: [],
    complaintId: null,
    status: 'submitted',
    updateInterval: null
};

// ========== DOM REFS ==========
const form = document.getElementById('complaintForm');
const steps = document.querySelectorAll('.form-step');
const progressSteps = document.querySelectorAll('.step');
const uploadZone = document.getElementById('uploadZone');
const fileInput = document.getElementById('screenshots');
const fileList = document.getElementById('fileList');

// ========== STEP NAVIGATION ==========
function goToStep(step) {
    if (step < 1 || step > state.totalSteps) return;

    // Validate current step before proceeding
    if (step > state.currentStep) {
        if (!validateStep(state.currentStep)) {
            return;
        }
    }

    state.currentStep = step;

    // Update steps visibility
    steps.forEach((el, index) => {
        el.classList.toggle('active', index + 1 === step);
    });

    // Update progress indicators
    progressSteps.forEach((el, index) => {
        const stepNum = index + 1;
        el.classList.remove('active', 'completed');
        if (stepNum === step) {
            el.classList.add('active');
        } else if (stepNum < step) {
            el.classList.add('completed');
        }
    });

    // If on step 4, populate review
    if (step === 4) {
        populateReview();
    }

    // Scroll to form
    document.getElementById('complaint-form').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ========== VALIDATION ==========
function validateStep(step) {
    let isValid = true;

    switch(step) {
        case 1:
            isValid = validatePersonalDetails();
            break;
        case 2:
            isValid = validateFraudDetails();
            break;
        case 3:
            isValid = validateFraudsterDetails();
            break;
    }

    return isValid;
}

function validatePersonalDetails() {
    let valid = true;
    const name = document.getElementById('fullName');
    const phone = document.getElementById('phone');
    const address = document.getElementById('address');

    // Name validation
    if (!name.value.trim()) {
        name.classList.add('error');
        document.getElementById('nameError').classList.add('visible');
        valid = false;
    } else {
        name.classList.remove('error');
        document.getElementById('nameError').classList.remove('visible');
    }

    // Phone validation
    const phoneRegex = /^[0-9]{10}$/;
    if (!phoneRegex.test(phone.value)) {
        phone.classList.add('error');
        document.getElementById('phoneError').classList.add('visible');
        valid = false;
    } else {
        phone.classList.remove('error');
        document.getElementById('phoneError').classList.remove('visible');
    }

    // Address validation
    if (!address.value.trim()) {
        address.classList.add('error');
        document.getElementById('addressError').classList.add('visible');
        valid = false;
    } else {
        address.classList.remove('error');
        document.getElementById('addressError').classList.remove('visible');
    }

    return valid;
}

function validateFraudDetails() {
    let valid = true;
    const amount = document.getElementById('fraudAmount');
    const date = document.getElementById('fraudDate');
    const time = document.getElementById('fraudTime');
    const type = document.getElementById('fraudType');
    const desc = document.getElementById('description');

    if (!amount.value || parseFloat(amount.value) <= 0) {
        amount.classList.add('error');
        document.getElementById('amountError').classList.add('visible');
        valid = false;
    } else {
        amount.classList.remove('error');
        document.getElementById('amountError').classList.remove('visible');
    }

    if (!date.value) {
        date.classList.add('error');
        document.getElementById('dateError').classList.add('visible');
        valid = false;
    } else {
        date.classList.remove('error');
        document.getElementById('dateError').classList.remove('visible');
    }

    if (!time.value) {
        time.classList.add('error');
        document.getElementById('timeError').classList.add('visible');
        valid = false;
    } else {
        time.classList.remove('error');
        document.getElementById('timeError').classList.remove('visible');
    }

    if (!type.value) {
        type.classList.add('error');
        document.getElementById('typeError').classList.add('visible');
        valid = false;
    } else {
        type.classList.remove('error');
        document.getElementById('typeError').classList.remove('visible');
    }

    if (!desc.value.trim()) {
        desc.classList.add('error');
        document.getElementById('descError').classList.add('visible');
        valid = false;
    } else {
        desc.classList.remove('error');
        document.getElementById('descError').classList.remove('visible');
    }

    return valid;
}

function validateFraudsterDetails() {
    // Optional fields, always valid
    return true;
}

// ========== REVIEW POPULATION ==========
function populateReview() {
    const fields = {
        'reviewName': 'fullName',
        'reviewPhone': 'phone',
        'reviewEmail': 'email',
        'reviewAddress': 'address',
        'reviewAmount': 'fraudAmount',
        'reviewDate': 'fraudDate',
        'reviewTime': 'fraudTime',
        'reviewType': 'fraudType',
        'reviewDesc': 'description',
        'reviewUpi': 'upiId',
        'reviewBank': 'bankAccount',
        'reviewFraudPhone': 'fraudPhone'
    };

    Object.entries(fields).forEach(([reviewId, inputId]) => {
        const el = document.getElementById(reviewId);
        const input = document.getElementById(inputId);
        if (el && input) {
            el.textContent = input.value || '-';
        }
    });

    // Format amount
    const amountEl = document.getElementById('reviewAmount');
    const amount = document.getElementById('fraudAmount').value;
    if (amount) {
        amountEl.textContent = '₹' + parseFloat(amount).toLocaleString('en-IN');
    }

    // Format date
    const dateEl = document.getElementById('reviewDate');
    const date = document.getElementById('fraudDate').value;
    if (date) {
        const d = new Date(date);
        dateEl.textContent = d.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
    }

    // Format type
    const typeEl = document.getElementById('reviewType');
    const type = document.getElementById('fraudType');
    if (type.value) {
        const types = {
            'investment': 'Investment Scam',
            'kfc': 'KYC Fraud',
            'upi': 'UPI Fraud',
            'job': 'Fake Job Offer',
            'phishing': 'Phishing',
            'other': 'Other'
        };
        typeEl.textContent = types[type.value] || type.value;
    }

    // Files
    document.getElementById('reviewFiles').textContent = state.files.length + ' files';
}

// ========== FILE UPLOAD ==========
uploadZone.addEventListener('click', () => fileInput.click());

uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.classList.add('dragover');
});

uploadZone.addEventListener('dragleave', () => {
    uploadZone.classList.remove('dragover');
});

uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

function handleFiles(files) {
    const maxSize = 10 * 1024 * 1024; // 10MB
    const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf'];

    Array.from(files).forEach(file => {
        if (file.size > maxSize) {
            alert(`File ${file.name} exceeds 10MB limit.`);
            return;
        }
        if (!allowedTypes.includes(file.type)) {
            alert(`File ${file.name} type not supported. Use JPG, PNG, or PDF.`);
            return;
        }
        state.files.push(file);
    });

    renderFileList();
    fileInput.value = '';
}

function renderFileList() {
    fileList.innerHTML = state.files.map((file, index) => `
        <div class="file-item">
            <span>${file.name} (${(file.size / 1024).toFixed(1)} KB)</span>
            <span class="remove-file" onclick="removeFile(${index})">
                <i class="fas fa-times"></i>
            </span>
        </div>
    `).join('');
}

function removeFile(index) {
    state.files.splice(index, 1);
    renderFileList();
}

// ========== FORM SUBMISSION ==========
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validate consent
    const consent = document.getElementById('consentCheck');
    if (!consent.checked) {
        document.getElementById('consentError').classList.add('visible');
        return;
    } else {
        document.getElementById('consentError').classList.remove('visible');
    }

    // Disable submit button
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

    try {
        // Collect form data
        const formData = new FormData();
        formData.append('name', document.getElementById('fullName').value);
        formData.append('phone', document.getElementById('phone').value);
        formData.append('email', document.getElementById('email').value);
        formData.append('address', document.getElementById('address').value);
        formData.append('amount', document.getElementById('fraudAmount').value);
        formData.append('date', document.getElementById('fraudDate').value);
        formData.append('time', document.getElementById('fraudTime').value);
        formData.append('fraudType', document.getElementById('fraudType').value);
        formData.append('description', document.getElementById('description').value);
        formData.append('upiId', document.getElementById('upiId').value);
        formData.append('bankAccount', document.getElementById('bankAccount').value);
        formData.append('fraudPhone', document.getElementById('fraudPhone').value);

        // Append files
        state.files.forEach(file => {
            formData.append('files', file);
        });

        // Simulate API call (replace with actual backend URL)
        const response = await simulateAPICall(formData);

        // Generate complaint ID
        state.complaintId = 'C' + String(Math.floor(Math.random() * 90000) + 10000);

        // Show status page
        showStatusPage(state.complaintId);

        // Start simulated status updates
        startStatusSimulation(state.complaintId);

    } catch (error) {
        console.error('Submission error:', error);
        alert('Something went wrong. Please try again.');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Complaint';
    }
});

// ========== SIMULATE API CALL ==========
function simulateAPICall(formData) {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({ success: true });
        }, 1500);
    });
}

// ========== STATUS PAGE ==========
function showStatusPage(complaintId) {
    document.getElementById('complaint-form').style.display = 'none';
    document.getElementById('statusSection').style.display = 'block';
    document.getElementById('complaintId').textContent = complaintId;

    // Set initial time
    const now = new Date();
    document.getElementById('submittedTime').textContent = formatTime(now);

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function startStatusSimulation(complaintId) {
    const statuses = [
        { status: 'analyzing', label: 'AI Analyzing', message: 'AI is analyzing transaction patterns...' },
        { status: 'action', label: 'Action Taken', message: '🚨 High-risk ATM identified. Police notified.' },
        { status: 'resolved', label: 'Resolved', message: '✅ Complaint resolved. Funds recovered.' }
    ];

    let index = 0;
    state.updateInterval = setInterval(() => {
        if (index >= statuses.length) {
            clearInterval(state.updateInterval);
            return;
        }

        const update = statuses[index];
        updateStatus(update.status, update.label, update.message);
        index++;
    }, 5000);

    // Store interval ID for cleanup
    window.statusInterval = state.updateInterval;
}

function updateStatus(statusKey, label, message) {
    // Update tracker
    document.querySelectorAll('.tracker-step').forEach(el => {
        if (el.dataset.status === statusKey) {
            el.classList.add('active', 'completed');
            const time = document.getElementById(el.dataset.status + 'Time');
            if (time) time.textContent = formatTime(new Date());
        }
    });

    // Update status header
    const statusIcons = {
        'analyzing': 'fa-robot',
        'action': 'fa-shield',
        'resolved': 'fa-flag'
    };

    const statusTitles = {
        'analyzing': 'AI Analyzing Complaint',
        'action': 'Action Taken!',
        'resolved': 'Complaint Resolved 🎉'
    };

    document.getElementById('statusIcon').innerHTML = `<i class="fas ${statusIcons[statusKey]}"></i>`;
    document.getElementById('statusTitle').textContent = statusTitles[statusKey];
    document.getElementById('statusSubtitle').textContent = label;

    // Add feed update
    const feed = document.getElementById('feedContainer');
    const item = document.createElement('div');
    item.className = 'feed-item';
    item.innerHTML = `
        <span class="feed-time">Just now</span>
        <span class="feed-message">${message}</span>
    `;
    feed.appendChild(item);
    feed.scrollTop = feed.scrollHeight;
}

// ========== UTILITY FUNCTIONS ==========
function formatTime(date) {
    return date.toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ========== KEYBOARD NAVIGATION ==========
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const activeStep = document.querySelector('.form-step.active');
        if (activeStep) {
            const nextBtn = activeStep.querySelector('.btn-next');
            const submitBtn = activeStep.querySelector('.btn-submit');
            if (nextBtn) nextBtn.click();
            else if (submitBtn) submitBtn.click();
        }
    }
});

// ========== MODAL FUNCTIONS ==========

/**
 * Open a modal by ID
 * @param {string} modalId - The ID of the modal to open
 */
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
        // Close modal on background click
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal(modalId);
            }
        });
        // Close modal on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal(modalId);
            }
        });
    }
}

/**
 * Close a modal by ID
 * @param {string} modalId - The ID of the modal to close
 */
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// Expose functions globally
window.openModal = openModal;
window.closeModal = closeModal;

// ========== KEYBOARD SHORTCUTS FOR MODALS ==========
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        document.querySelectorAll('.modal-overlay.active').forEach(modal => {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
});

// ========== INITIALIZATION ==========
// Start with step 1 active
goToStep(1);

console.log('🚀 Cyber Complaint Portal loaded successfully!');
console.log('📱 Mobile-first, accessible, and ready to use.');
console.log('✅ Modal system initialized successfully!');