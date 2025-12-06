const http = require('http');
const fs = require('fs');
const url = require('url');

console.log('🚀 راه‌اندازی نهایی نطق مصطلح...');

// خواندن مقالات
let articles = [];
try {
    const data = fs.readFileSync('./data/articles.json', 'utf8');
    articles = JSON.parse(data);
    console.log('✅ ' + articles.length + ' مقاله بارگذاری شد');
} catch (e) {
    console.log('❌ خطا در بارگذاری مقالات: ' + e.message);
    articles = [];
}

// تابع جستجو
function searchArticles(query) {
    if (!query || query.length < 2) {
        return { error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد' };
    }
    
    const results = [];
    const queryLower = query.toLowerCase();
    
    for (let i = 0; i < Math.min(articles.length, 100); i++) {
        const article = articles[i];
        if (article.title && article.title.toLowerCase().includes(queryLower)) {
            results.push({
                article: {
                    id: article.id,
                    title: article.title,
                    excerpt: article.excerpt || 'بدون خلاصه'
                },
                score: 100
            });
        }
    }
    
    return {
        success: true,
        query: query,
        totalResults: results.length,
        results: results.slice(0, 10)
    };
}

// ایجاد سرور
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    if (parsedUrl.pathname === '/api/health') {
        res.end(JSON.stringify({
            status: 'healthy',
            service: 'natiq-final',
            articles: { total: articles.length },
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    if (parsedUrl.pathname === '/api/search' && req.method === 'GET') {
        const query = parsedUrl.query.q || '';
        const result = searchArticles(query);
        
        if (result.error) {
            res.statusCode = 400;
            res.end(JSON.stringify({ success: false, error: result.error }, null, 2));
        } else {
            res.end(JSON.stringify(result, null, 2));
        }
        return;
    }
    
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'مسیر یافت نشد' }, null, 2));
});

// شروع سرور
const PORT = 3001;
server.listen(PORT, () => {
    console.log('\n=============================================');
    console.log('    نطق مصطلح - نسخه نهایی');
    console.log('=============================================');
    console.log('');
    console.log('📍 آدرس: http://localhost:' + PORT);
    console.log('📊 مقالات: ' + articles.length + ' مقاله');
    console.log('🔍 جستجو: فعال');
    console.log('');
    console.log('✅ سیستم آماده استفاده است!');
    console.log('=============================================\n');
});

server.on('error', (err) => {
    console.error('❌ خطای سرور:', err.message);
});
