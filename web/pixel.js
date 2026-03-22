/**
 * Jemassurance - Universal Pixel Manager
 * Centralized tracking for FB, Google, TikTok and internal analytics.
 */
const LD_Pixel = {
    config: {},
    init: async function () {
        console.log("🚀 LD Pixel Manager Initializing...");
        try {
            const resp = await fetch('http://localhost:8001/pixel-config');
            this.config = await resp.json();
            console.log("✅ Tracking Config Loaded:", this.config);
            this.setupExternalPixels();
        } catch (e) {
            console.warn("⚠️ Could not load tracking config, using defaults.");
        }
        this.trackPageLoad();
    },

    setupExternalPixels: function() {
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
                ttq.load(this.config.TIKTOK_ID);
                ttq.page();
            }(window, document, 'ttq');
        }
    },

    // Track standard page views
    trackPageLoad: function () {
        const path = window.location.pathname;
        this.emit("PageView", { path: path });
    },

    // Track Lead generation (Form submissions, chat starts)
    trackLead: function (type, details) {
        this.emit("Lead", { type: type, ...details });
    },

    // Track Purchase events
    trackPurchase: function (amount, currency = "XAF", product) {
        this.emit("Purchase", { value: amount, currency: currency, content_name: product });
    },

    // Internal emitter to external pixels
    emit: function (eventName, data) {
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
        if (typeof ttq === 'object') {
            ttq.track(eventName, data);
        }
    }
};

window.LD_Pixel = LD_Pixel;
LD_Pixel.init();
