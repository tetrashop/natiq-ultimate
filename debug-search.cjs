const http = require('http');
const fs = require('fs');

console.log('🔧 سرور دیباگ با لاگ کامل...');

// بارگذاری مقالات
let articles = [];
try {
    const data = fs.readFileSync('./data/articles.json', 'utf8');
    articles = JSON.parse(data);
    console.log(`✅ ${articles.length} مقاله بارگذاری شد`);
    
    // نمایش نمونه‌ای از مقالات
    console.log('📝 نمونه مقالات:');
    for (let i = 0; i < Math.min(3, articles.length); i++) {
        console.log(`   ${i+1}. "${articles[i].title.substring(0, 40)}..."`);
    }
} catch (e) {
    console.log('❌ خطای بارگذاری: ' + e.message);
    articles = [];
}

const server = http.createServer((req, res) => {
    console.log(`\n📨 ${new Date().toISOString()} - درخواست: ${req.url}`);
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // سلامت
    if (req.url === '/api/health' || req.url === '/api/health/') {
        const response = {
            status: 'healthy',
            articles: articles.length,
            search_available: true,
            timestamp: new Date().toISOString()
        };
        console.log('   📊 پاسخ سلامت:', JSON.stringify(response).substring(0, 100));
        res.end(JSON.stringify(response, null, 2));
        return;
    }
    
    // جستجو
    if (req.url.startsWith('/api/search')) {
        try {
            const urlObj = new URL(req.url, 'http://localhost:3000');
            const query = urlObj.searchParams.get('q') || '';
            
            console.log(`   🔍 جستجوی عبارت: "${query}"`);
            
            if (!query || query.length < 2) {
                const errorResponse = {
                    success: false,
                    error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد',
                    query: query
                };
                console.log('   ❌ خطا: عبارت کوتاه');
                res.end(JSON.stringify(errorResponse, null, 2));
                return;
            }
            
            const results = [];
            const queryLower = query.toLowerCase();
            console.log(`   📊 بررسی ${Math.min(articles.length, 50)} مقاله...`);
            
            for (let i = 0; i < Math.min(articles.length, 50); i++) {
                const article = articles[i];
                if (article.title && article.title.toLowerCase().includes(queryLower)) {
                    results.push({
                        article: {
                            id: article.id || i,
                            title: article.title,
                            excerpt: article.excerpt || article.title.substring(0, 100) + '...'
                        },
                        score: 100,
                        match_position: article.title.toLowerCase().indexOf(queryLower)
                    });
                    console.log(`   ✅ یافت شد: "${article.title.substring(0, 50)}"`);
                }
            }
            
            const response = {
                success: true,
                query: query,
                totalResults: results.length,
                results: results.slice(0, 10),
                searched_articles: Math.min(articles.length, 50)
            };
            
            console.log(`   🎯 ${results.length} نتیجه یافت شد`);
            console.log('   📤 ارسال پاسخ...');
            
            res.end(JSON.stringify(response, null, 2));
            
        } catch (e) {
            console.log('   💥 خطای پردازش:', e.message);
            res.end(JSON.stringify({
                success: false,
                error: 'خطای سرور: ' + e.message,
                stack: e.stack
            }, null, 2));
        }
        return;
    }
    
    // سایر مسیرها
    res.end(JSON.stringify({ 
        info: 'سرور نطق مصطلح - از /api/search?q=عبارت استفاده کن',
        endpoints: ['/api/health', '/api/search?q=عبارت']
    }, null, 2));
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log('\n===========================================');
    console.log('   نطق مصطلح - نسخه دیباگ کامل');
    console.log('===========================================');
    console.log(`🌐 آدرس: http://localhost:${PORT}`);
    console.log(`📚 مقالات: ${articles.length}`);
    console.log('🔍 جستجو: فعال با لاگ کامل');
    console.log('');
    console.log('🧪 دستورات تست:');
    console.log(`curl "http://localhost:${PORT}/api/health"`);
    console.log(`curl "http://localhost:${PORT}/api/search?q=پردازش"`);
    console.log(`curl "http://localhost:${PORT}/api/search?q=آموزش"`);
    console.log('===========================================\n');
});

server.on('error', (err) => {
    console.error('❌ خطای سرور:', err.message);
});
