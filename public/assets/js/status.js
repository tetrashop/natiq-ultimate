class SystemStatus {
    constructor() {
        this.apiBase = window.location.origin;
        this.statusElements = {
            'api': document.getElementById('apiStatus'),
            'db': document.getElementById('dbStatus'), 
            'nlp': document.getElementById('nlpStatus'),
            'auth': document.getElementById('authStatus'),
            'storage': document.getElementById('storageStatus')
        };
    }
    
    async checkAll() {
        console.log('🔍 بررسی وضعیت سیستم...');
        
        // بررسی سلامت API
        await this.checkAPI();
        
        // بررسی وضعیت سیستم
        await this.checkSystemStatus();
        
        // بررسی اتصال
        await this.checkConnection();
    }
    
    async checkAPI() {
        try {
            const response = await fetch(`${this.apiBase}/api/health`);
            const data = await response.json();
            
            this.updateStatus('api', 'success', 'API سالم است');
            console.log('✅ API:', data);
            
            // نمایش ورژن
            const versionEl = document.getElementById('apiVersion');
            if (versionEl) {
                versionEl.textContent = `ورژن: ${data.version}`;
            }
            
            return true;
        } catch (error) {
            this.updateStatus('api', 'error', 'API قطع است');
            console.error('❌ API Error:', error);
            return false;
        }
    }
    
    async checkSystemStatus() {
        try {
            const response = await fetch(`${this.apiBase}/api/status`);
            const data = await response.json();
            
            // آپدیت وضعیت کامپوننت‌ها
            if (data.components) {
                data.components.forEach(comp => {
                    const key = comp.component.toLowerCase().replace(' ', '');
                    if (this.statusElements[key]) {
                        const status = comp.status === 'running' || comp.status === 'connected' ? 'success' : 'warning';
                        this.updateStatus(key, status, comp.message);
                    }
                });
            }
            
            console.log('✅ System Status:', data);
            return true;
        } catch (error) {
            console.error('❌ System Status Error:', error);
            return false;
        }
    }
    
    async checkConnection() {
        const connectionEl = document.getElementById('connectionStatus');
        if (!connectionEl) return;
        
        try {
            // تست چند endpoint
            const endpoints = [
                '/api/health',
                '/api/test',
                '/api/status'
            ];
            
            let working = 0;
            for (const endpoint of endpoints) {
                try {
                    await fetch(this.apiBase + endpoint);
                    working++;
                } catch (e) {
                    console.warn(`Endpoint ${endpoint} failed:`, e);
                }
            }
            
            const percentage = Math.round((working / endpoints.length) * 100);
            if (percentage >= 80) {
                connectionEl.className = 'status-item success';
                connectionEl.innerHTML = '<span class="status-dot"></span> اتصال کامل';
            } else if (percentage >= 50) {
                connectionEl.className = 'status-item warning';
                connectionEl.innerHTML = '<span class="status-dot"></span> اتصال ناپایدار';
            } else {
                connectionEl.className = 'status-item error';
                connectionEl.innerHTML = '<span class="status-dot"></span> قطع ارتباط';
            }
            
            // نمایش درصد
            const percentEl = document.getElementById('connectionPercent');
            if (percentEl) {
                percentEl.textContent = `${percentage}%`;
            }
            
        } catch (error) {
            connectionEl.className = 'status-item error';
            connectionEl.innerHTML = '<span class="status-dot"></span> قطع ارتباط';
        }
    }
    
    updateStatus(elementId, status, message) {
        const element = this.statusElements[elementId];
        if (!element) return;
        
        element.className = `status-item ${status}`;
        element.innerHTML = `<span class="status-dot"></span> ${message}`;
    }
}

// راه‌اندازی هنگام لود صفحه
document.addEventListener('DOMContentLoaded', () => {
    const statusChecker = new SystemStatus();
    statusChecker.checkAll();
    
    // رفرش هر 30 ثانیه
    setInterval(() => statusChecker.checkAll(), 30000);
});
