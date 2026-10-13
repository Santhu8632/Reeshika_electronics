// ============================================
// REESHIKA ELECTRONICS - INTERACTIONS
// ============================================

document.addEventListener('DOMContentLoaded', function () {

    // ============ MOBILE MENU ============
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    const navOverlay = document.getElementById('navOverlay');

    function closeMenu() {
        hamburger?.classList.remove('active');
        navLinks?.classList.remove('open');
        navOverlay?.classList.remove('active');
        document.body.style.overflow = '';
    }
    function openMenu() {
        hamburger?.classList.add('active');
        navLinks?.classList.add('open');
        navOverlay?.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    hamburger?.addEventListener('click', () => {
        navLinks?.classList.contains('open') ? closeMenu() : openMenu();
    });
    navOverlay?.addEventListener('click', closeMenu);
    navLinks?.querySelectorAll('a').forEach(l => l.addEventListener('click', closeMenu));
    document.addEventListener('keydown', e => e.key === 'Escape' && closeMenu());
    window.addEventListener('resize', () => window.innerWidth > 900 && closeMenu());

    // ============ NAVBAR SCROLL ============
    const navbar = document.getElementById('navbar');
    window.addEventListener('scroll', () => {
        navbar?.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });

    // ============ REVEAL ON SCROLL ============
    const revealEls = document.querySelectorAll(
        '.section, .product-card, .feature-box, .trust-item, .branch-card, .contact-item, .order-point, .feature, .special-card'
    );
    revealEls.forEach((el, i) => {
        el.classList.add('reveal');
        el.style.transitionDelay = (i % 6) * 0.08 + 's';
    });
    const obs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.classList.add('visible');
                obs.unobserve(e.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    revealEls.forEach(el => obs.observe(el));

    // ============ PRODUCT TABS ============
    document.querySelectorAll('.product-tab').forEach(tab => {
        tab.addEventListener('click', function () {
            const target = this.dataset.tab;
            document.querySelectorAll('.product-tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.product-panel').forEach(p => p.classList.remove('active'));
            this.classList.add('active');
            document.getElementById(target)?.classList.add('active');
        });
    });

    // ============ COUNTER ============
    document.querySelectorAll('.stat h3').forEach(el => {
        const obs2 = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const text = el.textContent.trim();
                    const match = text.match(/^(\d+)/);
                    if (!match) return;
                    const target = parseInt(match[1]);
                    const suffix = text.replace(match[1], '');
                    const start = performance.now();
                    const duration = 1500;
                    function step(now) {
                        const p = Math.min((now - start) / duration, 1);
                        const eased = 1 - Math.pow(1 - p, 3);
                        el.textContent = Math.floor(target * eased) + suffix;
                        if (p < 1) requestAnimationFrame(step);
                        else el.textContent = target + suffix;
                    }
                    requestAnimationFrame(step);
                    obs2.unobserve(el);
                }
            });
        }, { threshold: 0.5 });
        obs2.observe(el);
    });

    // ============ SMOOTH SCROLL ============
    document.querySelectorAll('a[href^="#"], a[href^="/#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const targetId = href.replace('/', '');
            if (targetId.startsWith('#')) {
                const target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    const offset = 80;
                    const top = target.getBoundingClientRect().top + window.scrollY - offset;
                    window.scrollTo({ top, behavior: 'smooth' });
                }
            }
        });
    });

    // ============ PARALLAX ============
    if (window.innerWidth > 900) {
        const shapes = document.querySelectorAll('.floating-shape');
        window.addEventListener('scroll', () => {
            const y = window.scrollY;
            shapes.forEach((s, i) => s.style.transform = `translateY(${y * (0.15 + i * 0.08)}px)`);
        }, { passive: true });
    }

    // ============ QUICK ENQUIRY FORM ============
    const qf = document.getElementById('quickForm');
    if (qf) {
        qf.addEventListener('submit', async function (e) {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(this));
            data.source = 'quick_form';
            const btn = this.querySelector('button');
            const orig = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
            btn.disabled = true;
            try {
                const res = await fetch('/api/enquiry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const r = await res.json();
                btn.innerHTML = '<i class="fas fa-check"></i> Sent!';
                btn.style.background = 'linear-gradient(135deg, #43A047, #2E7D32)';
                setTimeout(() => {
                    qf.reset();
                    btn.innerHTML = orig;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 2500);
            } catch (err) {
                btn.innerHTML = '<i class="fas fa-times"></i> Error';
                btn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                setTimeout(() => {
                    btn.innerHTML = orig;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 2500);
            }
        });
    }

    // ============ ORDER FORM ============
    const of = document.getElementById('orderForm');
    if (of) {
        of.addEventListener('submit', async function (e) {
            e.preventDefault();
            const data = Object.fromEntries(new FormData(this));
            const btn = this.querySelector('button[type="submit"]');
            const orig = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Placing Order...';
            btn.disabled = true;
            try {
                const res = await fetch('/api/order', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const r = await res.json();
                btn.innerHTML = '<i class="fas fa-check-circle"></i> Order Placed!';
                btn.style.background = 'linear-gradient(135deg, #43A047, #2E7D32)';
                setTimeout(() => {
                    of.reset();
                    btn.innerHTML = orig;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 3000);
            } catch (err) {
                btn.innerHTML = '<i class="fas fa-times"></i> Error';
                btn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                setTimeout(() => {
                    btn.innerHTML = orig;
                    btn.style.background = '';
                    btn.disabled = false;
                }, 2500);
            }
        });
    }

    // ============ PRODUCT ENQUIRE BUTTON ============
    document.querySelectorAll('.enquire-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            const product = this.dataset.product;
            const heroForm = document.querySelector('.hero-form');
            const select = heroForm?.querySelector('select[name="product"]');
            if (select) {
                // Add option if not exists
                let found = false;
                for (let opt of select.options) {
                    if (opt.value === product) { found = true; break; }
                }
                if (!found) {
                    const opt = document.createElement('option');
                    opt.value = product;
                    opt.textContent = product;
                    select.appendChild(opt);
                }
                select.value = product;
            }
            const target = document.getElementById('home');
            if (target) target.scrollIntoView({ behavior: 'smooth' });
            setTimeout(() => document.querySelector('input[name="name"]')?.focus(), 500);
        });
    });

    // ============ TOUCH FEEDBACK ============
    if (window.matchMedia('(hover: none)').matches) {
        document.querySelectorAll('.btn, .product-card, .feature-box, .branch-card, .special-card').forEach(el => {
            el.addEventListener('touchstart', function () { this.style.transform = 'scale(0.98)'; }, { passive: true });
            el.addEventListener('touchend', function () { this.style.transform = ''; }, { passive: true });
        });
    }

    // ============ VIEWPORT HEIGHT FIX ============
    function setVH() {
        document.documentElement.style.setProperty('--vh', window.innerHeight * 0.01 + 'px');
    }
    setVH();
    window.addEventListener('resize', setVH);
});