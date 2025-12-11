const https = require('https');

class AutoHealthCheck {
    constructor() {
        this.endpoints = [
            { url: 'https://natiq-ultimate.vercel.app/api/health', method: 'GET' },
            { url: 'https://natiq-ultimate.vercel.app/api/chat', method: 'POST' }
        ];
        this.healthStatus = { operational: true };
    }
    
    async checkEndpoint(endpoint) {
        return new Promise((resolve) => {
            const startTime = Date.now();
            
            const options = {
                method: endpoint.method,
                headers: endpoint.method === 'POST' ? {
                    'Content-Type': 'application/json',
                    'Content-Length': 27 // طول {"message":"سلام"}
                } : {}
            };
            
            const req = https.request(endpoint.url, options, (res) => {
                const latency = Date.now() - startTime;
                const data = { 
                    status: res.statusCode, 
                    latency, 
                    healthy: res.statusCode === 200 || res.statusCode === 201 
                };
                
                if (data.healthy) {
                    console.log(`✅ ${endpoint.method} ${endpoint.url} - ${latency}ms`);
                } else {
                    console.error(`🚨 ${endpoint.method} ${endpoint.url} - HTTP ${res.statusCode}`);
                    this.healthStatus.operational = false;
                }
                
                resolve(data);
            });
            
            req.on('error', (err) => {
                console.error(`❌ ${endpoint.url} - ${err.message}`);
                this.healthStatus.operational = false;
                resolve({ status: 0, latency: 0, healthy: false });
            });
            
            req.setTimeout(5000, () => {
                req.destroy();
                console.error(`⏱️ ${endpoint.url} - Timeout (5s)`);
                this.healthStatus.operational = false;
                resolve({ status: 0, latency: 0, healthy: false });
            });
            
            // برای POST، body ارسال کن
            if (endpoint.method === 'POST') {
                req.write(JSON.stringify({ message: 'سلام' }));
            }
            
            req.end();
        });
    }
    
    async run() {
        console.log('🏥 شروع بررسی سلامت خودکار ناتیق الماس...');
        console.log('=' .repeat(50));
        
        for (const endpoint of this.endpoints) {
            await this.checkEndpoint(endpoint);
            await new Promise(resolve => setTimeout(resolve, 1500));
        }
        
        console.log('=' .repeat(50));
        
        if (this.healthStatus.operational) {
            console.log('✨ تمام سرویس‌ها سالم هستند! سیستم الماس فعال.');
            console.log('🌐 آدرس: https://natiq-ultimate.vercel.app');
            console.log('💎 نسخه: 5.0.0-diamond-fixed');
        } else {
            console.log('⚠️ برخی سرویس‌ها نیاز به توجه دارند');
        }
        
        return this.healthStatus;
    }
}

// اجرای نظارت
if (require.main === module) {
    const monitor = new AutoHealthCheck();
    monitor.run();
}
