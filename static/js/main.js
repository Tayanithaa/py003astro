/**
 * AstroGuy AI — main.js
 * UI functions for the Flask multi-page version.
 * Handles: stars, loading screen, language toggle,
 *          mobile menu, birth chart form submission,
 *          and alert popups.
 */

// ── Stars background ─────────────────────────────────────────────────────
function initStars() {
    const container = document.getElementById('starsBg');
    if (!container) return;

    for (let i = 0; i < 100; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.left = Math.random() * 100 + '%';
        star.style.top  = Math.random() * 100 + '%';
        star.style.setProperty('--duration', (Math.random() * 3 + 2) + 's');
        star.style.setProperty('--opacity',  Math.random() * 0.7 + 0.3);
        container.appendChild(star);
    }

    // Shooting stars
    setInterval(() => {
        const s = document.createElement('div');
        s.className   = 'shooting-star';
        s.style.top   = Math.random() * 50 + '%';
        s.style.left  = Math.random() * 50 + '%';
        container.appendChild(s);
        setTimeout(() => s.remove(), 3000);
    }, 5000);
}

// ── Loading screen ───────────────────────────────────────────────────────
function hideLoading() {
    const screen = document.getElementById('loadingScreen');
    if (screen) {
        setTimeout(() => screen.classList.add('hidden'), 800);
    }
}

// ── Mobile menu ──────────────────────────────────────────────────────────
function toggleMobileMenu() {
    const nav = document.getElementById('navLinks');
    if (nav) nav.classList.toggle('active');
}

// ── Language toggle ──────────────────────────────────────────────────────
async function toggleLanguage() {
    try {
        const res  = await fetch('/api/toggle-language', { method: 'POST' });
        const data = await res.json();
        if (data.success) {
            // Reload page to apply new language (Flask re-renders template)
            window.location.reload();
        }
    } catch (e) {
        console.error('Language toggle error:', e);
    }
}

// ── Alert popup ──────────────────────────────────────────────────────────
function showAlert(message, type = 'info') {
    const alert = document.createElement('div');
    alert.className = 'alert';
    alert.innerHTML = `
        <div class="alert-title">${type === 'error' ? '⚠️ Error' : '✨ Info'}</div>
        <div class="alert-message">${message}</div>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 3500);
}

// ── Birth chart form (on index / home page) ──────────────────────────────
async function saveUser(event) {
    if (event) event.preventDefault();

    const name   = document.getElementById('userName')?.value  || '';
    const dob    = document.getElementById('userDob')?.value   || '';
    const time   = document.getElementById('userTime')?.value  || '';
    const place  = document.getElementById('userPlace')?.value || '';
    const gender = document.getElementById('userGender')?.value || '';

    if (!name || !dob || !time || !place || !gender) {
        showAlert('Please fill all required details', 'error');
        return;
    }

    const btn = document.querySelector('.btn-primary[onclick*="saveUser"], .btn-primary[type="submit"]');
    if (btn) {
        btn.disabled   = true;
        btn.innerHTML  = '<i class="fas fa-spinner fa-spin"></i> Calculating...';
    }

    try {
        const res = await fetch('/api/calculate-chart', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ name, dob, time, place, gender })
        });
        const data = await res.json();

        if (btn) {
            btn.disabled  = false;
            btn.innerHTML = '<i class="fas fa-star"></i> Generate My Chart';
        }

        if (!data.success) {
            showAlert('Error: ' + (data.error || 'Calculation failed'), 'error');
            return;
        }

        const chart = data.chart;

        // Show welcome message
        const welcomeEl = document.getElementById('welcomeMsg');
        if (welcomeEl) {
            welcomeEl.textContent =
                `🙏 Welcome ${name}! ` +
                `Rasi: ${chart.rasi?.english_name || chart.rasi?.englishName}, ` +
                `Nakshatra: ${chart.nakshatra?.name}`;
        }

        showAlert('✨ Chart calculated! Redirecting to Horoscope...', 'info');

        // Navigate to horoscope page after short delay
        setTimeout(() => { window.location.href = '/horoscope'; }, 1500);

    } catch (err) {
        if (btn) {
            btn.disabled  = false;
            btn.innerHTML = '<i class="fas fa-star"></i> Generate My Chart';
        }
        showAlert('Connection error: ' + err.message, 'error');
    }
}

// ── Compatibility form (on compatibility page) ───────────────────────────
async function calculateCompatibility() {
    const dob1  = document.getElementById('compatDob1')?.value;
    const time1 = document.getElementById('compatTime1')?.value;
    const dob2  = document.getElementById('compatDob2')?.value;
    const time2 = document.getElementById('compatTime2')?.value;

    if (!dob1 || !time1 || !dob2 || !time2) {
        showAlert('Please fill all details', 'error');
        return;
    }

    const btn = document.querySelector('#compatBtn');
    if (btn) { btn.disabled = true; btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...'; }

    try {
        const res = await fetch('/api/calculate-compatibility', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            body:    JSON.stringify({ dob1, time1, dob2, time2 })
        });
        const data = await res.json();

        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-heart"></i> Analyze Compatibility'; }

        if (!data.success) {
            showAlert('Error: ' + (data.error || 'Calculation failed'), 'error');
            return;
        }

        displayCompatResult(data.result);

    } catch (err) {
        if (btn) { btn.disabled = false; btn.innerHTML = '<i class="fas fa-heart"></i> Analyze Compatibility'; }
        showAlert('Error: ' + err.message, 'error');
    }
}

function displayCompatResult(compat) {
    const resultDiv = document.getElementById('compatResult');
    if (!resultDiv) return;
    resultDiv.style.display = 'block';

    // Score circle
    const circle = document.getElementById('scoreCircle');
    if (circle) circle.style.setProperty('--score-deg', `${(compat.percentage / 100) * 360}deg`);

    const scoreEl = document.getElementById('compatScore');
    if (scoreEl) scoreEl.textContent = `${compat.total}/${compat.max}`;

    const verdictEl = document.getElementById('compatVerdict');
    if (verdictEl) verdictEl.textContent = compat.verdict;

    const descEl = document.getElementById('compatDesc');
    if (descEl) descEl.textContent = compat.description;

    // Koota grid
    const kootaGrid = document.getElementById('kootaGrid');
    if (kootaGrid) {
        const kootaNames = {
            varna:'Varna', vashya:'Vashya', tara:'Tara', yoni:'Yoni',
            grahaMaitri:'Graha Maitri', gana:'Gana', bhakoot:'Bhakoot', nadi:'Nadi'
        };
        const kootaMax = { varna:1, vashya:2, tara:3, yoni:4, grahaMaitri:5, gana:6, bhakoot:7, nadi:8 };

        kootaGrid.innerHTML = Object.entries(compat)
            .filter(([k]) => k in kootaNames)
            .map(([k, v]) => `
                <div class="koota-item">
                    <span class="koota-name">${kootaNames[k]}</span>
                    <span class="koota-score">${Array.isArray(v) ? v[0] : v}/${kootaMax[k]}</span>
                </div>`)
            .join('');
    }

    // Doshas
    const doshaSection = document.getElementById('doshaSection');
    if (doshaSection && compat.doshas?.length) {
        doshaSection.innerHTML = `
            <div class="dosha-warning">
                <h4><i class="fas fa-exclamation-triangle"></i> Doshas Detected</h4>
                ${compat.doshas.map(d => `
                    <div class="dosha-remedy" style="margin-top:0.5rem">
                        <strong>${d.name}:</strong> ${d.remedy}
                    </div>`).join('')}
            </div>`;
    } else if (doshaSection) {
        doshaSection.innerHTML = '';
    }

    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Init on page load ────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    initStars();
    hideLoading();
});
