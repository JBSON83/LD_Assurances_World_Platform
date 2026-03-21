/**
 * Jemassurance - Universal Pixel Manager
 * Centralized tracking for FB, Google, TikTok and internal analytics.
 */
const LD_Pixel = {
    init: function () {
        console.log("🚀 LD Pixel Manager Initialized");
        this.trackPageLoad();
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

        // Placeholder for real Facebook Pixel
        if (typeof fbq === 'function') fbq('track', eventName, data);

        // Placeholder for Google Ads
        if (typeof gtag === 'function') gtag('event', eventName, data);

        // Placeholder for TikTok Pixel
        if (typeof ttq === 'object') ttq.track(eventName, data);
    }
};

window.LD_Pixel = LD_Pixel;
LD_Pixel.init();
