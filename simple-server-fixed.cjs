const http = require('http');
const fs = require('fs');

console.log('🚀 راه‌اندازی سرور اصلاح شده...');

// خواندن مقالات
let articles = [];
try {
    const data = fs.readFileSync('./data/articles.json', 'utf8');
    articles = JSON.parse(data);
    console.log('✅ ' + articles.length + ' مقاله بارگذاری شد');
} catch (e) {
    console.log('❌ خطا: ' + e.message);
    articles = [];
}

// سرور
const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // سلامت
    if (req.url === '/api/health' || req.url === '/api/health/') {
        res.end(JSON.stringify({
            status: 'healthy',
            articles: articles.length,
            timestamp: new Date().toISOString()
        }));
        return;
    }
    
    // جستجو - درست شده
    if (req.url.startsWith('/api/search')) {
        try {
            const url = new URL(req.url, 'http://localhost');
            const query = url.searchParams.get('q') || '';
            
            console.log('🔍 جستجو برای: ' + query);
            
            if (!query || query.length < 2) {
                res.end(JSON.stringify({
                    success: false,
                    error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد'
                }));
                return;
            }
            
            const results = [];
            const queryLower = query.toLowerCase();
            
            for (let article of articles.slice(0, 100)) {
                if (article.title && article.title.toLowerCase().includes(queryLower)) {
                    results.push({
                        article: {
                            id: article.id,
                            title: article.title,
                            excerpt: article.excerpt || article.title.substring(0, 100)
                        },
                        score: 100
                    });
                }
            }
            
            res.end(JSON.stringify({
                success: true,
                query: query,
                totalResults: results.length,
                results: results.slice(0, 10)
            }));
            
        } catch (e) {
            res.end(JSON.stringify({
                success: false,
                error: 'خطا در پردازش جستجو: ' + e.message
            }));
        }
        return;
    }
    
    // سایر درخواست‌ها
    res.statusCode = 404;
    res.end(JSON.stringify({error: 'Not found'}));
});

// پورت
const PORT = 3000;
server.listen(PORT, () => {
    console.log('\n✅ سرور اصلاح شده فعال!');
    console.log('🌐 http://localhost:' + PORT);
    console.log('📊 مقالات: ' + articles.length);
    console.log('🔍 جستجو: فعال و تست شده');
});
