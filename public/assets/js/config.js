// پیکربندی API برای محیط‌های مختلف
const CONFIG = {
    IS_PRODUCTION: window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1',
    
    getApiUrl: function(path) {
        if (this.IS_PRODUCTION) {
            return window.location.origin + path;
        } else {
            // در توسعه، از localhost:8081 استفاده کن
            return 'http://localhost:8081' + path;
        }
    }
};
