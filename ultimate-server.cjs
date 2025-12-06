const http = require('http');
const fs = require('fs');

console.log('🚀 راه‌اندازی سرور نهایی نطق مصطلح...');

const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
console.log(`✅ ${articles.length} مقاله بارگذاری شد`);

const server = http.createServer((req, res) => {
    console.log(`\n📨 ${new Date().toISOString()} ${req.method} ${req.url}`);
    
    // هدرهای CORS کامل
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // OPTIONS برای CORS
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // سلامت
    if (req.url === '/api/health' || req.url === '/api/health/') {
        const response = {
            status: 'عالی',
            articles: articles.length,
            service: 'natiq-ultimate',
            version: '3.0.0',
            timestamp: new Date().toISOString()
        };
        console.log('   📊 پاسخ سلامت');
        res.end(JSON.stringify(response, null, 2));
        return;
    }
    
    // جستجو - با پردازش درست فارسی
    if (req.url.startsWith('/api/search')) {
        try {
            // استخراج query به صورت دستی
            let query = '';
            const urlParts = req.url.split('?');
            
            if (urlParts.length > 1) {
                const params = urlParts[1].split('&');
                for (const param of params) {
                    if (param.startsWith('q=')) {
                        query = decodeURIComponent(param.substring(2));
                        break;
                    }
                }
            }
            
            console.log(`   🔍 جستجوی عبارت: "${query}"`);
            
            if (!query || query.trim().length < 2) {
                res.end(JSON.stringify({
                    success: false,
                    error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد'
                }, null, 2));
                return;
            }
            
            const results = [];
            const queryLower = query.toLowerCase();
            
            // جستجو در همه مقالات
            for (let i = 0; i < articles.length; i++) {
                const article = articles[i];
                if (article.title && article.title.toLowerCase().includes(queryLower)) {
                    results.push({
                        article: {
                            id: article.id || i + 1,
                            title: article.title,
                            excerpt: article.excerpt || article.content?.substring(0, 100) + '...' || 'بدون خلاصه',
                            author: article.author || 'ناشناس',
                            category: article.category || 'عمومی',
                            views: article.views || 0,
                            likes: article.likes || 0
                        },
                        score: 100,
                        matchIndex: i
                    });
                }
            }
            
            const response = {
                success: true,
                query: query,
                totalResults: results.length,
                searchedArticles: articles.length,
                results: results.slice(0, 10),
                timestamp: new Date().toISOString(),
                message: results.length > 0 ? 
                    `یافت شد ${results.length} مقاله شامل "${query}"` :
                    `هیچ مقاله‌ای شامل "${query}" یافت نشد`
            };
            
            console.log(`   🎯 ${results.length} نتیجه یافت شد`);
            res.end(JSON.stringify(response, null, 2));
            
        } catch (error) {
            console.error('   💥 خطا:', error.message);
            res.end(JSON.stringify({
                success: false,
                error: 'خطای پردازش درخواست',
                details: error.message
            }, null, 2));
        }
        return;
    }
    
    // آمار
    if (req.url === '/api/stats' || req.url === '/api/stats/') {
        const totalViews = articles.reduce((sum, article) => sum + (article.views || 0), 0);
        const totalLikes = articles.reduce((sum, article) => sum + (article.likes || 0), 0);
        
        const response = {
            success: true,
            totalArticles: articles.length,
            totalViews: totalViews,
            totalLikes: totalLikes,
            totalShares: 0,
            avgViews: Math.round(totalViews / articles.length),
            avgLikes: Math.round(totalLikes / articles.length),
            lastUpdated: new Date().toISOString()
        };
        
        console.log('   📊 پاسخ آمار');
        res.end(JSON.stringify(response, null, 2));
        return;
    }
    
    // لیست مقالات
    if (req.url.startsWith('/api/articles')) {
        const urlParams = new URL(req.url, 'http://localhost:3000').searchParams;
        const page = parseInt(urlParams.get('page') || '1');
        const limit = parseInt(urlParams.get('limit') || '10');
        const start = (page - 1) * limit;
        
        const paginated = articles.slice(start, start + limit).map((article, index) => ({
            id: article.id || start + index + 1,
            title: article.title,
            excerpt: article.excerpt || article.content?.substring(0, 150) + '...' || 'بدون خلاصه',
            author: article.author || 'ناشناس',
            category: article.category || 'عمومی',
            date: article.created_at || '2024-01-01',
            views: article.views || 0,
            likes: article.likes || 0
        }));
        
        const response = {
            success: true,
            page: page,
            limit: limit,
            total: articles.length,
            totalPages: Math.ceil(articles.length / limit),
            articles: paginated,
            timestamp: new Date().toISOString()
        };
        
        console.log(`   📄 صفحه ${page} از مقالات`);
        res.end(JSON.stringify(response, null, 2));
        return;
    }
    
    // سایر
    res.writeHead(404);
    res.end(JSON.stringify({
        success: false,
        error: 'Endpoint یافت نشد',
        availableEndpoints: [
            '/api/health',
            '/api/search?q=عبارت',
            '/api/articles?page=1&limit=10',
            '/api/stats'
        ]
    }, null, 2));
});

// راه‌اندازی
const PORT = 3000;
server.listen(PORT, () => {
    console.log('\n' + '='.repeat(60));
    console.log('   🌐 نطق مصطلح - سیستم مدیریت مقالات NLP فارسی');
    console.log('='.repeat(60));
    console.log(`   آدرس: http://localhost:${PORT}`);
    console.log(`   مقالات: ${articles.length} مقاله تخصصی`);
    console.log('   نسخه: 3.0.0');
    console.log('');
    console.log('   📌 API های فعال:');
    console.log('      • /api/health          - سلامت سیستم');
    console.log('      • /api/search?q=عبارت - جستجوی مقالات');
    console.log('      • /api/articles        - لیست مقالات');
    console.log('      • /api/stats           - آمار سیستم');
    console.log('');
    console.log('   🧪 تست سریع:');
    console.log('      curl "http://localhost:3000/api/health"');
    console.log('      curl -G "http://localhost:3000/api/search" --data-urlencode "q=پردازش"');
    console.log('='.repeat(60) + '\n');
});

// مدیریت خطا
server.on('error', (err) => {
    console.error('❌ خطای سرور:', err.message);
});

// API جزئیات مقاله - بعد از API جستجو اضافه کن
if (req.url.startsWith('/api/article/')) {
    try {
        const id = parseInt(req.url.split('/')[3]);
        const article = articles.find(a => a.id === id);
        
        if (article) {
            // مقالات مرتبط (بر اساس دسته‌بندی)
            const related = articles
                .filter(a => a.id !== id && a.category === article.category)
                .slice(0, 5)
                .map(a => ({
                    id: a.id,
                    title: a.title,
                    excerpt: a.excerpt || a.content?.substring(0, 100) + '...'
                }));
            
            res.end(JSON.stringify({
                success: true,
                article: {
                    id: article.id,
                    title: article.title,
                    content: article.content || 'محتوایی موجود نیست',
                    excerpt: article.excerpt,
                    author: article.author || 'ناشناس',
                    category: article.category || 'عمومی',
                    tags: article.tags || [],
                    views: article.views || 0,
                    likes: article.likes || 0,
                    created_at: article.created_at || '2024-01-01'
                },
                related: related,
                totalRelated: related.length
            }, null, 2));
        } else {
            res.end(JSON.stringify({
                success: false,
                error: `مقاله با شناسه ${id} یافت نشد`
            }, null, 2));
        }
    } catch (error) {
        res.end(JSON.stringify({
            success: false,
            error: 'خطا در پردازش درخواست'
        }, null, 2));
    }
    return;
}
