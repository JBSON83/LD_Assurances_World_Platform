/**
 * LD Config System
 * Handles dynamic content, SEO, and maintenance mode.
 */

const LD_Config = {
    API_BASE: 'http://localhost:8001',

    async init() {
        try {
            const resp = await fetch(`${this.API_BASE}/config/public`);
            const config = await resp.json();
            
            this.applyConfig(config);
            this.handleMaintenance(config.MAINTENANCE_MODE);
            this.applySEO(config);
        } catch (e) {
            console.warn("[LD Config] Impossible de charger la configuration dynamique:", e);
        }
    },

    applyConfig(config) {
        // Update all elements with data-config attribute
        // Example: <span data-config="SITE_PHONE"></span>
        const elements = document.querySelectorAll('[data-config]');
        elements.forEach(el => {
            const key = el.getAttribute('data-config');
            if (config[key]) {
                if (el.tagName === 'A' && key.includes('LINK')) {
                    el.href = config[key];
                } else if (el.tagName === 'A' && key === 'SITE_PHONE') {
                    el.href = `tel:${config[key]}`;
                    el.innerText = config[key];
                } else if (el.tagName === 'A' && key === 'SITE_EMAIL') {
                    el.href = `mailto:${config[key]}`;
                    el.innerText = config[key];
                } else {
                    el.innerText = config[key];
                }
            }
        });
    },

    handleMaintenance(isMaintenance) {
        if (isMaintenance === 'true' && !window.location.pathname.includes('/admin/')) {
            document.body.innerHTML = `
                <div style="height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #0f172a; color: white; font-family: sans-serif; text-align: center; padding: 20px;">
                    <img src="/assets/logo.svg" style="height: 80px; margin-bottom: 2rem;">
                    <h1 style="font-size: 2.5rem; margin-bottom: 1rem;">Maintenance en cours</h1>
                    <p style="font-size: 1.2rem; color: #94a3b8; max-width: 600px;">
                        Nous mettons à jour Jemassurance pour vous offrir une meilleure expérience. 
                        Revenez dans quelques instants !
                    </p>
                    <div style="margin-top: 2rem; padding: 10px 20px; border: 1px solid #334155; border-radius: 8px; color: #64748b;">
                        Jemassurance &copy; 2026
                    </div>
                </div>
            `;
            document.body.style.overflow = 'hidden';
        }
    },

    applySEO(config) {
        if (config.SEO_TITLE) document.title = config.SEO_TITLE;
        if (config.SEO_DESCRIPTION) {
            let meta = document.querySelector('meta[name="description"]');
            if (!meta) {
                meta = document.createElement('meta');
                meta.name = 'description';
                document.head.appendChild(meta);
            }
            meta.content = config.SEO_DESCRIPTION;
        }
    }
};

LD_Config.init();
