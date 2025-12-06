const http = require('http');
const fs = require('fs');
const url = require('url');

console.log('🎯 سرور نطق مصطلح با CORS کامل...');

// بارگذاری مقالات
const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
console.log(`✅ ${articles.length} مقاله بارگذاری شد`);

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    // هدرهای CORS کامل
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // پاسخ به OPTIONS برای CORS preflight
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // API سلامت
    if (parsedUrl.pathname === '/api/health') {
        res.end(JSON.stringify({
            status: 'healthy',
            articles: articles.length,
            service: 'natiq-cors',
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    // API جستجو
    if (parsedUrl.pathname === '/api/search') {
        const query = parsedUrl.query.q || '';
        
        if (!query || query.length < 2) {
            res.end(JSON.stringify({
                success: false,
                error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد'
            }, null, 2));
            return;
        }
        
        const results = [];
        const queryLower = query.toLowerCase();
        
        // فقط ۵۰ مقاله اول را برای سرعت بررسی کن
        for (let i = 0; i < Math.min(articles.length, 50); i++) {
            const article = articles[i];
            if (article.title && article.title.toLowerCase().includes(queryLower)) {
                results.push({
                    id: article.id,
                    title: article.title,
                    excerpt: article.excerpt || article.content?.substring(0, 100) || 'بدون خلاصه',
                    author: article.author || 'ناشناس',
                    category: article.category || 'عمومی',
                    views: article.views || 0,
                    likes: article.likes || 0
                });
            }
        }
        
        res.end(JSON.stringify({
            success: true,
            query: query,
            total: results.length,
            results: results.slice(0, 10)
        }, null, 2));
        return;
    }
    
    // API لیست مقالات
    if (parsedUrl.pathname === '/api/articles') {
        const page = parseInt(parsedUrl.query.page) || 1;
        const limit = parseInt(parsedUrl.query.limit) || 10;
        const start = (page - 1) * limit;
        const end = start + limit;
        
        const paginated = articles.slice(start, end).map(article => ({
            id: article.id,
            title: article.title,
            excerpt: article.excerpt || article.content?.substring(0, 150) || 'بدون خلاصه',
            author: article.author || 'ناشناس',
            category: article.category || 'عمومی',
            date: article.created_at || '2024-01-01'
        }));
        
        res.end(JSON.stringify({
            success: true,
            page: page,
            limit: limit,
            total: articles.length,
            articles: paginated
        }, null, 2));
        return;
    }
    
    // API آمار
    if (parsedUrl.pathname === '/api/stats') {
        const totalViews = articles.reduce((sum, article) => sum + (article.views || 0), 0);
        const totalLikes = articles.reduce((sum, article) => sum + (article.likes || 0), 0);
        
        res.end(JSON.stringify({
            success: true,
            totalArticles: articles.length,
            totalViews: totalViews,
            totalLikes: totalLikes,
            totalShares: 0,
            lastUpdated: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    // سایر درخواست‌ها
    res.end(JSON.stringify({
        error: 'Endpoint not found',
        availableEndpoints: [
            '/api/health',
            '/api/search?q=عبارت',
            '/api/articles?page=1&limit=10',
            '/api/stats'
        ]
    }, null, 2));
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log('\n' + '='.repeat(50));
    console.log('   🌐 سرور فعال: http://localhost:' + PORT);
    console.log('   📚 مقالات: ' + articles.length);
    console.log('   🔍 جستجو: /api/search?q=عبارت');
    console.log('   📄 لیست: /api/articles?page=1&limit=10');
    console.log('   📊 آمار: /api/stats');
    console.log('='.repeat(50));
    
    // تست خودکار
    console.log('\n🧪 تست خودکار API ها...');
    const testApis = [
        '/api/health',
        '/api/stats',
        '/api/search?q=پردازش',
        '/api/articles?page=1&limit=5'
    ];
    
    testApis.forEach(api => {
        setTimeout(() => {
            const req = http.get(`http://localhost:${PORT}${api}`, (res) => {
                let data = '';
                res.on('data', chunk => data += chunk);
                res.on('end', () => {
                    try {
                        const json = JSON.parse(data);
                        console.log(`   ✅ ${api}: ${json.success !== false ? 'موفق' : 'خطا'}`);
                    } catch {
                        console.log(`   ❌ ${api}: پاسخ JSON نامعتبر`);
                    }
                });
            });
            req.on('error', () => console.log(`   ❌ ${api}: خطای اتصال`));
        }, 500);
    });
});
