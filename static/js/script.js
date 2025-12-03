// === HAPTIC FEEDBACK & UX JAZZ ===
function vibrate(ms = 10) {
    if (navigator.vibrate) navigator.vibrate(ms);
}

// Add vibration to all specific buttons
document.querySelectorAll('.haptic-btn').forEach(btn => {
    btn.addEventListener('click', () => vibrate(40));
});

// Custom Toast Notification (Instead of Alert)
function showToast(message, icon = "bi-check-circle-fill") {
    const container = document.getElementById('kuromi-toast-container');
    const toast = document.createElement('div');
    toast.className = 'k-toast';
    toast.innerHTML = `<i class="bi ${icon} text-warning"></i> <span>${message}</span>`;
    container.appendChild(toast);
    
    // Remove after 3 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Celebration Confetti
function celebrate() {
    vibrate([50, 50, 50]);
    if(typeof confetti !== 'undefined') {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#9c27b0', '#e91e63', '#000000']
        });
    }
}

// === FIXED NAV LOGIC ===
const navBtns = document.querySelectorAll('.nav-btn');
const tabPanes = document.querySelectorAll('.tab-pane');
navBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.preventDefault();
        vibrate(20); // Light tap on nav
        navBtns.forEach(b => b.classList.remove('active'));
        this.classList.add('active');
        tabPanes.forEach(pane => pane.classList.remove('show', 'active'));
        const targetId = this.getAttribute('data-bs-target');
        const targetPane = document.querySelector(targetId);
        if(targetPane) { targetPane.classList.add('show', 'active'); window.scrollTo(0, 0); }
    });
});

// === WORTHINESS LOGIC ===
if(document.getElementById('w_hourly')) {
    document.getElementById('w_hourly').addEventListener('input', function() { document.getElementById('hidden_wage').value = this.value; });
    document.getElementById('hidden_wage').value = document.getElementById('w_hourly').value;
}

function calcWorth() {
    let price = parseFloat(document.getElementById('w_price').value) || 0;
    let hourly = parseFloat(document.getElementById('w_hourly').value) || 0;
    
    if(hourly <= 0) { showToast("ระบุค่าแรงก่อนนะ!", "bi-exclamation-circle-fill"); return; }
    if(price <= 0) return;

    vibrate(30);
    let hours = price / hourly;
    let days = hours / 8; 

    document.getElementById('res_hours').innerText = hours.toFixed(1);
    document.getElementById('w_result').classList.remove('d-none');
    
    let badge = document.getElementById('w_badge');
    let title = document.getElementById('w_verdict_title');
    let desc = document.getElementById('w_verdict_desc');
    let ref = document.getElementById('w_ref_text');

    if (hours < 4) {
        badge.className = "position-absolute top-0 start-50 translate-middle badge rounded-pill bg-success px-3 py-2 shadow";
        badge.innerText = "BUY IT";
        title.innerText = "🥰 ความสุขเล็กๆ"; title.className = "fw-bold text-success";
        desc.innerText = `ใช้เวลาทำงานแค่ ${hours.toFixed(1)} ชม. ถือว่าน้อยมาก ถ้าช่วยให้มีแรงทำงานต่อก็จัดเลย!`;
        ref.innerText = "Ref: Micro-spending for mental health boost.";
        celebrate(); // Small purchase is a win!
    } else if (hours < 24) {
        badge.className = "position-absolute top-0 start-50 translate-middle badge rounded-pill bg-warning text-dark px-3 py-2 shadow";
        badge.innerText = "THINK";
        title.innerText = "🤔 คิดนิดนึงนะ"; title.className = "fw-bold text-warning";
        desc.innerText = `ต้องแลกด้วยงานประมาณ ${days.toFixed(1)} วัน ลองถามตัวเองว่า 'จำเป็น' หรือแค่ 'อยากได้'?`;
        ref.innerText = "Ref: Opportunity Cost";
    } else if (hours < 80) {
        badge.className = "position-absolute top-0 start-50 translate-middle badge rounded-pill bg-warning text-dark px-3 py-2 shadow";
        badge.innerText = "WAIT 48h";
        title.innerText = "⏳ กฎ 48 ชั่วโมง"; title.className = "fw-bold text-warning";
        desc.innerText = `ของชิ้นนี้ใช้เวลาหาเงินมา ${days.toFixed(0)} วัน! แนะนำให้ 'รอ 48 ชั่วโมง' ถ้ายังอยากได้ค่อยซื้อ`;
        ref.innerText = "Ref: The 48-Hour Rule for Impulse Buying";
    } else if (hours < 160) {
        badge.className = "position-absolute top-0 start-50 translate-middle badge rounded-pill bg-danger px-3 py-2 shadow";
        badge.innerText = "PLANNING";
        title.innerText = "💸 ของชิ้นใหญ่"; title.className = "fw-bold text-danger";
        desc.innerText = `นี่คือการทำงานเกือบเดือน! ตรวจสอบว่าเกินงบฟุ่มเฟือย (30% ของรายได้) หรือไม่?`;
        ref.innerText = "Ref: 50/30/20 Budgeting Rule";
    } else {
        badge.className = "position-absolute top-0 start-50 translate-middle badge rounded-pill bg-dark px-3 py-2 shadow";
        badge.innerText = "DANGER";
        title.innerText = "😱 ภาระระยะยาว"; title.className = "fw-bold text-dark";
        desc.innerText = `คุณต้องทำงานฟรีๆ ${days.toFixed(0)} วันเพื่อสิ่งนี้! มันคุ้มค่าเหนื่อยจริงๆ หรอ?`;
        ref.innerText = "Ref: Time Cost of Living Analysis";
    }
}

// === Common Utils & Init ===
const date = new Date();
const dateStr = date.toLocaleDateString('th-TH');
if(document.getElementById('currentDate')) document.getElementById('currentDate').innerText = dateStr;

function capture(id, filename) {
    vibrate(50);
    showToast("กำลังบันทึกภาพ...", "bi-camera-fill");
    const node = document.getElementById(id);
    html2canvas(node, { scale: 2, backgroundColor: null }).then(canvas => {
        const link = document.createElement('a');
        link.download = filename + '_' + Date.now() + '.png';
        link.href = canvas.toDataURL();
        link.click();
    });
}

// Categories & Modals Init
const cats = { expense: ["อาหาร", "เดินทาง", "ช้อปปิ้ง", "บิล/น้ำไฟ", "สุขภาพ", "อื่นๆ"], income: ["เงินเดือน", "โบนัส", "ขายของ", "ผู้ใหญ่ใจดี", "อื่นๆ"] };
function toggleCategories(targetId, preselect=null) {
    let typeEl, selEl;
    if(targetId === 'categorySelect') { typeEl = document.getElementById("typeSelect"); selEl = document.getElementById("categorySelect"); } 
    else { typeEl = document.getElementById("edit_type"); selEl = document.getElementById("edit_category"); }
    if(!typeEl || !selEl) return;
    selEl.innerHTML = "";
    cats[typeEl.value].forEach(c => {
        let opt = document.createElement("option"); opt.innerText = c; opt.value = c; 
        if(preselect && c === preselect) opt.selected = true;
        selEl.appendChild(opt);
    });
}
if(document.getElementById("typeSelect")) toggleCategories('categorySelect');

// Edit Modal
const editModalEl = document.getElementById('editModal');
let editModal;
if (editModalEl) editModal = new bootstrap.Modal(editModalEl);
function openEditModal(t) {
    document.getElementById('edit_id').value = t.id;
    document.getElementById('edit_amount').value = t.amount;
    document.getElementById('edit_note').value = t.note;
    document.getElementById('edit_type').value = t.type;
    toggleCategories('edit_category', t.category);
    if(editModal) editModal.show();
}

// Salary Logic (Math Core)
function fmt(num) { return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
function safeEvaluate(str) { try { let s = String(str).replace(/,/g, ''); if (!/^[0-9+\-*/.()\s]+$/.test(s)) return 0; return new Function('return ' + s)() || 0; } catch (e) { return 0; } }
function getVal(id) { let el = document.getElementById(id); if (!el) return 0; return safeEvaluate(el.value); }
function solve(el) { let val = el.value; if (/[+\-*/]/.test(val)) { el.value = safeEvaluate(val); calc(); } }
function handleEnter(e, el) { if(e.key === 'Enter') { solve(el); el.blur(); } }

function calc() {
    if(!document.getElementById('salary')) return;
    let salary = getVal('salary'); let col = getVal('col'); let level = getVal('level_pay');
    let diligence = getVal('diligence'); let food = getVal('food'); let other = getVal('other');
    let baseForOt = salary + col + level;
    let rate = baseForOt > 0 ? (baseForOt / 30) / 8 : 0;
    if(document.getElementById('hr_rate')) document.getElementById('hr_rate').innerText = fmt(rate);
    
    let h15 = getVal('ot15_hr'); let h13 = getVal('ot13_hr'); let h30 = getVal('ot30_hr');
    let amt15 = rate * 1.5 * h15; let amt13 = rate * 1.3 * h13; let amt30 = rate * 3.0 * h30;
    if(document.getElementById('ot15_amt')) document.getElementById('ot15_amt').innerText = fmt(amt15);
    if(document.getElementById('ot13_amt')) document.getElementById('ot13_amt').innerText = fmt(amt13);
    if(document.getElementById('ot30_amt')) document.getElementById('ot30_amt').innerText = fmt(amt30);
    
    let totalOtHrs = h15 + h13 + h30; let otFoodAmt = totalOtHrs * 20;
    if(document.getElementById('ot_food_amt')) document.getElementById('ot_food_amt').innerText = fmt(otFoodAmt);
    
    let totalIncome = baseForOt + diligence + food + other + amt15 + amt13 + amt30 + otFoodAmt;
    if(document.getElementById('total_income')) document.getElementById('total_income').innerText = fmt(totalIncome);
    
    let deductInputs = document.querySelectorAll('.deduct'); let totalDeduct = 0;
    deductInputs.forEach(el => totalDeduct += safeEvaluate(el.value));
    if(document.getElementById('total_deduct')) document.getElementById('total_deduct').innerText = fmt(totalDeduct);
    
    let netPay = totalIncome - totalDeduct;
    if(document.getElementById('net_pay')) document.getElementById('net_pay').innerText = fmt(netPay);
    if(document.getElementById('final_salary_amount')) document.getElementById('final_salary_amount').value = netPay.toFixed(2);
    
    let expInputs = document.querySelectorAll('.expense'); let privateExp = 0;
    expInputs.forEach(el => privateExp += safeEvaluate(el.value));
    let simBalance = totalIncome - (totalDeduct + privateExp);
    if(document.getElementById('sim_balance')) document.getElementById('sim_balance').innerText = fmt(simBalance);
    
    if(totalIncome > 0) {
        let expPct = ((totalDeduct + privateExp) / totalIncome) * 100;
        let balPct = (simBalance / totalIncome) * 100;
        if(expPct > 100) expPct = 100; if(balPct < 0) balPct = 0;
        if(document.getElementById('bar_expense')) document.getElementById('bar_expense').style.width = expPct + "%";
        if(document.getElementById('exp_pct')) document.getElementById('exp_pct').innerText = expPct.toFixed(1) + "%";
        if(document.getElementById('bar_balance')) document.getElementById('bar_balance').style.width = balPct + "%";
        if(document.getElementById('bal_pct')) document.getElementById('bal_pct').innerText = balPct.toFixed(1) + "%";
    }
}
function submitSalary() { 
    calc(); 
    if(confirm("ยืนยันยอด Net Pay เพื่อบันทึก?")) {
        celebrate(); // Trigger Confetti!
        setTimeout(() => document.getElementById('salaryForm').submit(), 800);
    }
}
function savePreset() { 
    const preset = {}; 
    document.querySelectorAll('#salary-slip-node input').forEach(input => preset[input.id] = input.value); 
    fetch('/save_salary_preset', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(preset) })
    .then(() => showToast("บันทึก Template แล้ว!", "bi-save-fill")); 
}

// Init
calc();
