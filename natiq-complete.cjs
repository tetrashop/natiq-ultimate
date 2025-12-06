const http = require('http');
const fs = require('fs');

console.log('🚀 راه‌اندازی سرور کامل نطق مصطلح...');

// بارگذاری مقالات
const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
console.log(`✅ ${articles.length} مقاله بارگذاری شد`);

const server = http.createServer((req, res) => {
    // هدرهای CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // گرفتن مسیر
    const url = new URL(req.url, 'http://localhost:3000');
    const pathname = url.pathname;
    
    console.log(`📨 ${req.method} ${req.url}`);
    
    // سلامت
    if (pathname === '/api/health' || pathname === '/api/health/') {
        res.end(JSON.stringify({
            status: 'عالی',
            articles: articles.length,
            service: 'natiq-complete',
            version: '3.0.0',
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    // جستجو
    if (pathname === '/api/search') {
        const query = url.searchParams.get('q') || '';
        
        if (!query || query.trim().length < 2) {
            res.end(JSON.stringify({
                success: false,
                error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد'
            }, null, 2));
            return;
        }
        
        const results = [];
        const queryLower = query.toLowerCase();
        
        for (let i = 0; i < Math.min(articles.length, 100); i++) {
            const article = articles[i];
            if (article.title && article.title.toLowerCase().includes(queryLower)) {
                results.push({
                    article: {
                        id: article.id || i + 1,
                        title: article.title,
                        excerpt: article.excerpt || 'بدون خلاصه',
                        author: article.author || 'ناشناس',
                        category: article.category || 'عمومی'
                    },
                    score: 100
                });
            }
        }
        
        res.end(JSON.stringify({
            success: true,
            query: query,
            totalResults: results.length,
            results: results.slice(0, 10),
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    // جزئیات مقاله
    if (pathname.startsWith('/api/article/')) {
        const id = parseInt(pathname.split('/')[3]);
        const article = articles.find(a => a.id === id);
        
        if (article) {
            // مقالات مرتبط
            const related = articles
                .filter(a => a.id !== id && a.category === article.category)
                .slice(0, 3)
                .map(a => ({
                    id: a.id,
                    title: a.title,
                    excerpt: a.excerpt || 'بدون خلاصه'
                }));
            
            res.end(JSON.stringify({
                success: true,
                article: {
                    id: article.id,
                    title: article.title,
                    content: article.content || 'محتوای کامل مقاله',
                    excerpt: article.excerpt,
                    author: article.author || 'ناشناس',
                    category: article.category || 'عمومی',
                    tags: article.tags || [],
                    views: article.views || 0,
                    likes: article.likes || 0,
                    date: article.created_at || '2024-01-01'
                },
                related: related,
                message: 'مقاله با موفقیت دریافت شد'
            }, null, 2));
        } else {
            res.statusCode = 404;
            res.end(JSON.stringify({
                success: false,
                error: `مقاله با شناسه ${id} یافت نشد`
            }, null, 2));
        }
        return;
    }
    
    // لیست مقالات
    if (pathname === '/api/articles') {
        const page = parseInt(url.searchParams.get('page')) || 1;
        const limit = parseInt(url.searchParams.get('limit')) || 10;
        const start = (page - 1) * limit;
        
        const paginated = articles.slice(start, start + limit).map(article => ({
            id: article.id,
            title: article.title,
            excerpt: article.excerpt || 'بدون خلاصه',
            author: article.author || 'ناشناس',
            category: article.category || 'عمومی',
            date: article.created_at || '2024-01-01'
        }));
        
        res.end(JSON.stringify({
            success: true,
            page: page,
            limit: limit,
            total: articles.length,
            totalPages: Math.ceil(articles.length / limit),
            articles: paginated
        }, null, 2));
        return;
    }
    
    // آمار
    if (pathname === '/api/stats') {
        const totalViews = articles.reduce((sum, article) => sum + (article.views || 0), 0);
        const totalLikes = articles.reduce((sum, article) => sum + (article.likes || 0), 0);
        
        res.end(JSON.stringify({
            success: true,
            totalArticles: articles.length,
            totalViews: totalViews,
            totalLikes: totalLikes,
            totalShares: 0,
            avgViews: Math.round(totalViews / articles.length),
            avgLikes: Math.round(totalLikes / articles.length),
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    // سایر مسیرها
    res.statusCode = 404;
    res.end(JSON.stringify({
        success: false,
        error: 'Endpoint یافت نشد',
        availableEndpoints: [
            '/api/health',
            '/api/search?q=عبارت',
            '/api/article/{id}',
            '/api/articles?page=1&limit=10',
            '/api/stats'
        ]
    }, null, 2));
});

// راه‌اندازی سرور
const PORT = 3000;
server.listen(PORT, () => {
    console.log('\n' + '='.repeat(60));
    console.log('   🌐 سرور کامل نطق مصطلح');
    console.log('='.repeat(60));
    console.log(`   آدرس: http://localhost:${PORT}`);
    console.log(`   مقالات: ${articles.length}`);
    console.log('');
    console.log('   📌 API های فعال:');
    console.log('      • GET /api/health');
    console.log('      • GET /api/search?q=عبارت');
    console.log('      • GET /api/article/{id}');
    console.log('      • GET /api/articles?page=1&limit=10');
    console.log('      • GET /api/stats');
    console.log('='.repeat(60));
});

// مدیریت خطا
server.on('error', (err) => {
    console.error('❌ خطای سرور:', err.message);
});
