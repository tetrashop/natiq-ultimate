// Natiq Ultimate - API Communication Module
// استفاده از API base URL نسبی

const NatiqAPI = (function() {
    // استفاده از مسیر نسبی برای API
    const config = {
        baseURL: '/api',  // مسیر نسبی
        timeout: 15000,
        retryAttempts: 3,
        retryDelay: 1000
    };
    
    // کش درخواست‌ها
    const requestCache = new Map();
    const CACHE_TTL = 30000; // 30 ثانیه
    
    /**
     * ارسال درخواست HTTP
     */
    async function sendRequest(endpoint, options = {}) {
        const cacheKey = `${endpoint}:${JSON.stringify(options)}`;
        const now = Date.now();
        
        // بررسی کش برای GET requests
        if ((!options.method || options.method === 'GET') && requestCache.has(cacheKey)) {
            const cached = requestCache.get(cacheKey);
            if (now - cached.timestamp < CACHE_TTL) {
                console.log(`استفاده از کش برای: ${endpoint}`);
                return Promise.resolve(cached.data);
            }
            requestCache.delete(cacheKey);
        }
        
        try {
            const url = `${config.baseURL}${endpoint}`;
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), config.timeout);
            
            const defaultHeaders = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            };
            
            const response = await fetch(url, {
                ...options,
                signal: controller.signal,
                headers: {
                    ...defaultHeaders,
                    ...options.headers
                }
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                const errorText = await response.text();
                let errorData;
                try {
                    errorData = JSON.parse(errorText);
                } catch {
                    errorData = { detail: errorText };
                }
                throw new Error(errorData.detail || `HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            // ذخیره در کش برای GET requests
            if (!options.method || options.method === 'GET') {
                requestCache.set(cacheKey, {
                    data,
                    timestamp: now
                });
            }
            
            return data;
            
        } catch (error) {
            console.error(`خطا در ارسال درخواست به ${endpoint}:`, error);
            throw error;
        }
    }
    
    /**
     * ارسال درخواست با قابلیت تلاش مجدد
     */
    async function sendRequestWithRetry(endpoint, options = {}, attempt = 1) {
        try {
            return await sendRequest(endpoint, options);
        } catch (error) {
            if (attempt < config.retryAttempts && 
                (error.name === 'TypeError' || error.name === 'AbortError' || error.message.includes('Network'))) {
                console.log(`تلاش مجدد (${attempt + 1}/${config.retryAttempts}) برای: ${endpoint}`);
                
                await new Promise(resolve => 
                    setTimeout(resolve, config.retryDelay * attempt)
                );
                
                return sendRequestWithRetry(endpoint, options, attempt + 1);
            }
            throw error;
        }
    }
    
    /**
     * بررسی اتصال به سرور
     */
    async function checkConnection() {
        try {
            const startTime = Date.now();
            const response = await sendRequest('/health', { timeout: 5000 });
            const latency = Date.now() - startTime;
            
            return {
                connected: true,
                latency,
                response,
                timestamp: new Date().toISOString()
            };
        } catch (error) {
            return {
                connected: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }
    
    /**
     * دریافت اطلاعات اصلی API
     */
    async function getAPIRoot() {
        return sendRequestWithRetry('/');
    }
    
    /**
     * دریافت وضعیت سلامت
     */
    async function getHealthStatus() {
        return sendRequestWithRetry('/health');
    }
    
    /**
     * پردازش متن
     */
    async function processText(text, options = {}) {
        return sendRequestWithRetry('/process', {
            method: 'POST',
            body: JSON.stringify({
                text,
                options
            })
        });
    }
    
    /**
     * دریافت اطلاعات فایل
     */
    async function getFileInfo(path = 'requirements.txt') {
        return sendRequestWithRetry(`/file-info?path=${encodeURIComponent(path)}`);
    }
    
    /**
     * دریافت لاگ‌های سیستم
     */
    async function getLogs(limit = 50, type = 'all') {
        return sendRequestWithRetry(`/logs?limit=${limit}`);
    }
    
    /**
     * دریافت اطلاعات سیستم
     */
    async function getSystemInfo() {
        return sendRequestWithRetry('/system-info');
    }
    
    /**
     * پاکسازی کش
     */
    function clearCache() {
        requestCache.clear();
        console.log('کش API پاک شد');
    }
    
    /**
     * دریافت وضعیت فعلی API
     */
    function getStatus() {
        return {
            baseURL: config.baseURL,
            cacheSize: requestCache.size,
            config: config
        };
    }
    
    // API عمومی
    return {
        // متدهای اصلی
        checkConnection,
        getHealthStatus,
        getAPIRoot,
        processText,
        getFileInfo,
        getLogs,
        getSystemInfo,
        
        // ابزارها
        clearCache,
        getStatus,
        
        // تست
        testAllEndpoints: async function() {
            const endpoints = [
                () => this.getAPIRoot(),
                () => this.getHealthStatus(),
                () => this.processText('تست اتصال API'),
                () => this.getFileInfo()
            ];
            
            const results = [];
            
            for (const endpoint of endpoints) {
                try {
                    const startTime = Date.now();
                    const result = await endpoint();
                    const latency = Date.now() - startTime;
                    
                    results.push({
                        success: true,
                        latency: `${latency}ms`,
                        data: result
                    });
                } catch (error) {
                    results.push({
                        success: false,
                        error: error.message
                    });
                }
            }
            
            return results;
        }
    };
})();

// اضافه کردن به global scope
window.NatiqAPI = NatiqAPI;

// تست اولیه اتصال
document.addEventListener('DOMContentLoaded', async () => {
    try {
        const connection = await NatiqAPI.checkConnection();
        console.log('اتصال API:', connection.connected ? 'برقرار' : 'قطع');
        console.log('تأخیر:', connection.latency ? `${connection.latency}ms` : 'N/A');
    } catch (error) {
        console.error('خطا در تست اتصال:', error);
    }
});
