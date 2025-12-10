// پیکربندی API - سازگار با localhost و Vercel
const API_CONFIG = {
    // در حالت توسعه (localhost) از پورت 8081 استفاده کن
    // در حالت تولید (Vercel) از آدرس اصلی سایت استفاده کن
    getBaseUrl: function() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return 'http://localhost:8081';
        } else {
            return window.location.origin;
        }
    },
    
    // یا اگر API شما همیشه در مسیر /api است
    getApiUrl: function(endpoint) {
        const base = this.getBaseUrl();
        // اگر روی Vercel هستیم، مسیر کامل را برگردان
        if (base === window.location.origin) {
            return `${base}/api${endpoint}`;
        }
        // اگر روی localhost هستیم
        return `${base}${endpoint}`;
    }
};
