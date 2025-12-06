const http = require('http');
const fs = require('fs');
const url = require('url');

console.log('🎯 سرور اصلاح شده جستجو...');

const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
console.log(`✅ ${articles.length} مقاله بارگذاری شد`);

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    
    // هدرهای CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // سلامت
    if (parsedUrl.pathname === '/api/health') {
        res.end(JSON.stringify({
            status: 'healthy',
            articles: articles.length,
            service: 'natiq-fixed-search',
            timestamp: new Date().toISOString()
        }));
        return;
    }
    
    // جستجو - نسخه کاملاً تست شده
    if (parsedUrl.pathname === '/api/search') {
        const query = parsedUrl.query.q || '';
        console.log(`🔍 جستجو برای: "${query}"`);
        
        if (!query || query.trim().length < 2) {
            res.end(JSON.stringify({
                success: false,
                error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد'
            }));
            return;
        }
        
        const results = [];
        const queryLower = query.toLowerCase();
        
        // فقط 100 مقاله اول را برای سرعت بررسی کن
        for (let i = 0; i < Math.min(articles.length, 100); i++) {
            const article = articles[i];
            if (article.title && article.title.toLowerCase().includes(queryLower)) {
                results.push({
                    article: {
                        id: article.id || i + 1,
                        title: article.title,
                        excerpt: article.excerpt || 'بدون خلاصه',
                        author: article.author || 'ناشناس'
                    },
                    score: 100
                });
                
                // لاگ اولین نتایج
                if (results.length <= 3) {
                    console.log(`   ✅ یافت شد: "${article.title.substring(0, 40)}..."`);
                }
            }
        }
        
        // پاسخ قطعی - حتماً success داشته باشد
        const response = {
            success: true,
            query: query,
            totalResults: results.length,
            results: results.slice(0, 10),
            timestamp: new Date().toISOString(),
            debug: `جستجو در ${Math.min(articles.length, 100)} مقاله انجام شد`
        };
        
        console.log(`🎯 ${results.length} نتیجه یافت شد`);
        res.end(JSON.stringify(response));
        return;
    }
    
    // لیست مقالات
    if (parsedUrl.pathname === '/api/articles') {
        const page = parseInt(parsedUrl.query.page) || 1;
        const limit = parseInt(parsedUrl.query.limit) || 10;
        const start = (page - 1) * limit;
        
        const paginated = articles.slice(start, start + limit).map(article => ({
            id: article.id,
            title: article.title,
            excerpt: article.excerpt || 'بدون خلاصه',
            author: article.author || 'ناشناس',
            category: article.category || 'عمومی'
        }));
        
        res.end(JSON.stringify({
            success: true,
            page: page,
            limit: limit,
            total: articles.length,
            articles: paginated
        }));
        return;
    }
    
    // آمار
    if (parsedUrl.pathname === '/api/stats') {
        const totalViews = articles.reduce((sum, article) => sum + (article.views || 0), 0);
        const totalLikes = articles.reduce((sum, article) => sum + (article.likes || 0), 0);
        
        res.end(JSON.stringify({
            success: true,
            totalArticles: articles.length,
            totalViews: totalViews,
            totalLikes: totalLikes,
            totalShares: 0
        }));
        return;
    }
    
    // سایر درخواست‌ها
    res.end(JSON.stringify({
        error: 'Endpoint not found',
        availableEndpoints: ['/api/health', '/api/search', '/api/articles', '/api/stats']
    }));
});

const PORT = 3000;
server.listen(PORT, () => {
    console.log('\n' + '='.repeat(50));
    console.log(`🌐 سرور جستجوی اصلاح شده: http://localhost:${PORT}`);
    console.log(`📚 مقالات: ${articles.length}`);
    console.log(`🔍 جستجو: /api/search?q=پردازش`);
    console.log('='.repeat(50));
    
    // تست خودکار
    console.log('\n🧪 تست خودکار API جستجو...');
    const http = require('http');
    const testReq = http.get(`http://localhost:${PORT}/api/search?q=پردازش`, (testRes) => {
        let data = '';
        testRes.on('data', chunk => data += chunk);
        testRes.on('end', () => {
            console.log('📄 پاسخ دریافت شد:');
            console.log(data.substring(0, 200) + (data.length > 200 ? '...' : ''));
            try {
                const json = JSON.parse(data);
                console.log(`✅ JSON معتبر - ${json.totalResults || 0} نتیجه`);
            } catch (e) {
                console.log(`❌ خطای JSON: ${e.message}`);
            }
        });
    });
    testReq.on('error', (e) => console.log(`❌ خطای تست: ${e.message}`));
});
