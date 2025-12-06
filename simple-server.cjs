const http = require('http');
const fs = require('fs');

console.log('🚀 راه‌اندازی سرور ساده...');

// خواندن مقالات
let articles = [];
try {
    const data = fs.readFileSync('./data/articles.json', 'utf8');
    articles = JSON.parse(data);
    console.log('✅ ' + articles.length + ' مقاله بارگذاری شد');
} catch (e) {
    console.log('❌ خطا: ' + e.message);
    articles = [{id: 1, title: 'مقاله نمونه', excerpt: 'این یک مقاله نمونه است'}];
}

const server = http.createServer((req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    if (req.url.startsWith('/api/search')) {
        const urlParts = new URL(req.url, 'http://localhost');
        const query = urlParts.searchParams.get('q') || '';
        
        let results = [];
        if (query.length >= 2) {
            const queryLower = query.toLowerCase();
            for (let article of articles.slice(0, 50)) {
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
        }
        
        res.end(JSON.stringify({
            success: true,
            query: query,
            totalResults: results.length,
            results: results.slice(0, 10)
        }, null, 2));
        return;
    }
    
    if (req.url === '/api/health') {
        res.end(JSON.stringify({
            status: 'healthy',
            articles: articles.length,
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    res.statusCode = 404;
    res.end(JSON.stringify({error: 'Not found'}));
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log('\n✅ سرور ساده فعال شد!');
    console.log('🌐 آدرس: http://localhost:' + PORT);
    console.log('📊 مقالات: ' + articles.length);
    console.log('\nدستورات تست:');
    console.log('curl "http://localhost:3000/api/health"');
    console.log('curl "http://localhost:3000/api/search?q=پردازش"');
    console.log('');
});
