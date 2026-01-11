const API_URL = '/api/v1';

// State
let token = localStorage.getItem('access_token');

// DOM Elements
const authView = document.getElementById('auth-view');
const dashboardView = document.getElementById('dashboard-view');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const walletBalance = document.getElementById('wallet-balance');
const loadModal = document.getElementById('load-modal');
const notification = document.getElementById('notification');

// Initialization
function init() {
    if (token) {
        showDashboard();
    } else {
        showAuth();
    }
}

// Navigation
function toggleAuthMode() {
    loginForm.classList.toggle('hidden');
    registerForm.classList.toggle('hidden');
}

function showAuth() {
    authView.classList.remove('hidden');
    dashboardView.classList.add('hidden');
}

function showDashboard() {
    authView.classList.add('hidden');
    dashboardView.classList.remove('hidden');
    fetchWalletBalance();
}

function showLoadModal() {
    loadModal.classList.remove('hidden');
}

function hideLoadModal() {
    loadModal.classList.add('hidden');
}

// Notifications
function showNotification(message, type = 'success') {
    const msgEl = document.getElementById('notification-message');
    msgEl.textContent = message;
    notification.className = `notification show ${type}`;
    
    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Auth Actions
async function handleLogin(e) {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    try {
        const formData = new URLSearchParams();
        formData.append('username', email); // OAuth2 expects username
        formData.append('password', password);

        const res = await fetch(`${API_URL}/auth/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!res.ok) throw new Error('Invalid credentials');

        const data = await res.json();
        token = data.access_token;
        localStorage.setItem('access_token', token);
        showNotification('Login successful!');
        showDashboard();
    } catch (err) {
        showNotification(err.message, 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    const name = document.getElementById('reg-name').value;
    const email = document.getElementById('reg-email').value;
    const password = document.getElementById('reg-password').value;

    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ full_name: name, email, password })
        });

        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.detail || 'Registration failed');
        }

        showNotification('Account created! Please sign in.');
        toggleAuthMode();
        // Pre-fill login
        document.getElementById('login-email').value = email;
    } catch (err) {
        showNotification(err.message, 'error');
    }
}

function handleLogout() {
    token = null;
    localStorage.removeItem('access_token');
    showAuth();
}

// Dashboard Actions
async function authenticatedFetch(endpoint, options = {}) {
    if (!options.headers) options.headers = {};
    options.headers['Authorization'] = `Bearer ${token}`;

    const res = await fetch(`${API_URL}${endpoint}`, options);
    
    if (res.status === 401) {
        handleLogout();
        throw new Error('Session expired');
    }
    
    return res;
}

async function fetchWalletBalance() {
    try {
        const res = await authenticatedFetch('/wallet/balance');
        if (res.ok) {
            const data = await res.json();
            walletBalance.textContent = data.balance.toFixed(2);
        }
    } catch (err) {
        console.error(err);
    }
}

async function handleTopUp(e) {
    e.preventDefault();
    const amount = parseFloat(document.getElementById('load-amount').value);

    try {
        const res = await authenticatedFetch('/wallet/load', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount })
        });

        if (!res.ok) throw new Error('Top up failed');

        const data = await res.json();
        walletBalance.textContent = data.balance.toFixed(2);
        showNotification(`Successfully added R${amount}`);
        hideLoadModal();
    } catch (err) {
        showNotification(err.message, 'error');
    }
}

async function checkUsage() {
    // Placeholder for usage check
    showNotification('Usage monitoring coming soon!', 'success');
}

// Start
init();
