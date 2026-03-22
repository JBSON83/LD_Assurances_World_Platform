/**
 * Jemassurance - Universal Pixel Manager
 * Centralized tracking for FB, Google, TikTok and internal analytics.
 * Includes Cookie Consent Management.
 */
const LD_Pixel = {
    config: {},
    hasConsent: false,

    init: async function () {
        console.log("🚀 LD Pixel Manager Initializing...");
        
        // Fetch config from admin backend
        try {
            // Using relative or absolute path based on environment
            const apiHost = window.location.hostname === "localhost" ? "http://localhost:8001" : "/api";
            const resp = await fetch(`${apiHost}/pixel-config`);
            this.config = await resp.json();
            console.log("✅ Tracking Config Loaded:", this.config);
        } catch (e) {
            console.warn("⚠️ Could not load tracking config, using defaults or cached.");
        }

        this.checkConsent();
    },

    checkConsent: function() {
        const consent = localStorage.getItem("ld_cookie_consent");
        if (consent === "accepted") {
            this.hasConsent = true;
            this.setupExternalPixels();
            this.trackPageLoad();
        } else if (!consent) {
            this.showConsentBanner();
        }
    },

    showConsentBanner: function() {
        if (document.getElementById('cookie-consent-banner')) return;

        const banner = document.createElement('div');
        banner.id = 'cookie-consent-banner';
        banner.style.cssText = `
            position: fixed; bottom: 0; left: 0; width: 100%;
            background: rgba(10, 10, 10, 0.95); backdrop-filter: blur(10px);
            color: #fff; padding: 20px; text-align: center;
            z-index: 9999; border-top: 1px solid rgba(255,255,255,0.1);
            font-family: 'Inter', sans-serif; display: flex; 
            flex-direction: column; align-items: center; justify-content: center; gap: 15px;
        `;

        banner.innerHTML = `
            <div style="max-width: 800px; font-size: 0.9rem; line-height: 1.5; color: rgba(255,255,255,0.8);">
                En poursuivant votre navigation sur ce site, vous acceptez l'utilisation de traceurs (cookies) 
                afin de vous proposer des services et une publicité ciblée adaptés à vos centres d'intérêts 
                (Facebook, Google, TikTok). <a href="/politique-confidentialite.html" style="color: #10b981; text-decoration: underline;">En savoir plus</a>.
            </div>
            <div style="display: flex; gap: 15px;">
                <button id="btn-refuse-cookies" style="background: transparent; color: #fff; border: 1px solid rgba(255,255,255,0.3); padding: 8px 20px; border-radius: 5px; cursor: pointer; transition: 0.3s;">Refuser</button>
                <button id="btn-accept-cookies" style="background: #10b981; color: #fff; border: none; padding: 8px 20px; border-radius: 5px; cursor: pointer; transition: 0.3s; font-weight: 600;">Accepter & Continuer</button>
            </div>
        `;

        document.body.appendChild(banner);

        document.getElementById('btn-accept-cookies').addEventListener('click', () => {
            localStorage.setItem("ld_cookie_consent", "accepted");
            this.hasConsent = true;
            banner.remove();
            this.setupExternalPixels();
            this.trackPageLoad();
        });

        document.getElementById('btn-refuse-cookies').addEventListener('click', () => {
            localStorage.setItem("ld_cookie_consent", "refused");
            banner.remove();
            // No pixels will be loaded
        });
    },

    setupExternalPixels: function() {
        if (!this.hasConsent) return;

        const self = this;

        // Dynamic GA4 Injection
        if (this.config.GA4_ID) {
            const script = document.createElement('script');
            script.src = `https://www.googletagmanager.com/gtag/js?id=${this.config.GA4_ID}`;
            script.async = true;
            document.head.appendChild(script);
            window.dataLayer = window.dataLayer || [];
            window.gtag = function(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', this.config.GA4_ID);
        }

        // Dynamic Facebook Pixel Injection
        if (this.config.FB_ID) {
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', this.config.FB_ID);
            fbq('track', 'PageView');
        }

        // Dynamic TikTok Pixel Injection
        if (this.config.TIKTOK_ID) {
            !function (w, d, t) {
                w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","trackSelf","untrackSelf"],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=i,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=i;var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
                ttq.load(self.config.TIKTOK_ID);
                ttq.page();
            }(window, document, 'ttq');
        }
    },

    // Track standard page views
    trackPageLoad: function () {
        if (!this.hasConsent) return;
        const path = window.location.pathname;
        this.emit("PageView", { path: path });
    },

    // Track Lead generation (Form submissions, chat starts)
    trackLead: function (type, details) {
        if (!this.hasConsent) return;
        this.emit("Lead", { type: type, ...details });
    },

    // Track Purchase events
    trackPurchase: function (amount, currency = "XAF", product) {
        if (!this.hasConsent) return;
        this.emit("Purchase", { value: amount, currency: currency, content_name: product });
    },

    // Internal emitter to external pixels
    emit: function (eventName, data) {
        if (!this.hasConsent) return;
        console.log(`[PIXEL EVENT] ${eventName}:`, data);

        // Google Analytics / Google Ads
        if (typeof gtag === 'function') {
            gtag('event', eventName, data);
        }

        // Facebook Pixel
        if (typeof fbq === 'function') {
            fbq('track', eventName, data);
        }

        // TikTok Pixel
        if (typeof ttq === 'object' && typeof ttq.track === 'function') {
            ttq.track(eventName, data);
        }
    }
};

window.LD_Pixel = LD_Pixel;
// Wait for DOM to be ready to append the banner cleanly
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => LD_Pixel.init());
} else {
    LD_Pixel.init();
}
