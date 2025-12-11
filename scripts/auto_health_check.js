// سیستم نظارت خودکار ناتیق الماس
const https = require('https');

class AutoHealthCheck {
    constructor() {
        this.endpoints = [
            'https://natiq-ultimate.vercel.app/api/health',
            'https://natiq-ultimate.vercel.app/api/chat'
        ];
        this.healthStatus = { operational: true };
    }
    
    async checkEndpoint(url) {
        return new Promise((resolve) => {
            const startTime = Date.now();
            
            const req = https.get(url, (res) => {
                const latency = Date.now() - startTime;
                const data = { status: res.statusCode, latency, healthy: res.statusCode === 200 };
                
                if (res.statusCode !== 200) {
                    console.error(`🚨 ${url} - HTTP ${res.statusCode}`);
                    this.healthStatus.operational = false;
                } else {
                    console.log(`✅ ${url} - ${latency}ms`);
                }
                
                resolve(data);
            });
            
            req.on('error', (err) => {
                console.error(`❌ ${url} - ${err.message}`);
                this.healthStatus.operational = false;
                resolve({ status: 0, latency: 0, healthy: false });
            });
            
            req.setTimeout(10000, () => {
                req.destroy();
                console.error(`⏱️ ${url} - Timeout`);
                resolve({ status: 0, latency: 0, healthy: false });
            });
        });
    }
    
    async run() {
        console.log('🏥 شروع بررسی سلامت خودکار...');
        
        for (const endpoint of this.endpoints) {
            await this.checkEndpoint(endpoint);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        
        if (this.healthStatus.operational) {
            console.log('✨ تمام سرویس‌ها سالم هستند');
        } else {
            console.log('⚠️ برخی سرویس‌ها مشکل دارند');
        }
        
        return this.healthStatus;
    }
}

// اجرای نظارت
if (require.main === module) {
    const monitor = new AutoHealthCheck();
    monitor.run();
}
