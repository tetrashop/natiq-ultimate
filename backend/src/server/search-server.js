/**
 * 🚀 سرور نطق مصطلح با قابلیت جستجوی هوشمند
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

const PORT = 3001;
const DATA_PATH = path.join(__dirname, '../../data/articles.json');

// خواندن داده‌های مقالات
let articles = [];
try {
    if (fs.existsSync(DATA_PATH)) {
        const data = fs.readFileSync(DATA_PATH, 'utf8');
        articles = JSON.parse(data);
        console.log(`✅ ${articles.length} مقاله بارگذاری شد`);
    } else {
        console.log('⚠️  فایل مقالات یافت نشد. مقالات خالی آغاز می‌شود.');
    }
} catch (error) {
    console.error('❌ خطا در خواندن فایل مقالات:', error);
}

// بارگذاری سیستم جستجو
let searchAPI;
try {
    const SearchAPI = require('../search/search-api');
    searchAPI = new SearchAPI(articles);
    console.log('🔍 سیستم جستجوی هوشمند راه‌اندازی شد');
} catch (error) {
    console.error('❌ خطا در راه‌اندازی سیستم جستجو:', error);
    // Fallback به جستجوی ساده
    searchAPI = {
        search: (query) => ({
            query,
            totalResults: 0,
            inference: { summary: 'سیستم جستجو در دسترس نیست' },
            results: []
        })
    };
}

// HTML صفحه اصلی (به‌روزرسانی شده با قابلیت جستجو)
const indexHTML = fs.readFileSync(
    path.join(__dirname, '../../public/index.html'), 
    'utf8'
);

// ایجاد سرور HTTP
const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    // صفحه اصلی
    if (pathname === '/' || pathname === '/index.html') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(indexHTML);
        return;
    }
    
    // API مقالات
    if (pathname === '/api/articles') {
        const page = parseInt(parsedUrl.query.page) || 1;
        const limit = parseInt(parsedUrl.query.limit) || 10;
        const offset = (page - 1) * limit;
        
        // فیلتر مقالات منتشر شده
        const publishedArticles = articles.filter(article => article.status === 'published');
        
        // مرتب‌سازی بر اساس تاریخ ایجاد (نزولی)
        const sortedArticles = [...publishedArticles].sort((a, b) => 
            new Date(b.created_at) - new Date(a.created_at)
        );
        
        // صفحه‌بندی
        const paginatedArticles = sortedArticles.slice(offset, offset + limit);
        
        // محاسبه آمار
        const stats = {
            total_articles: publishedArticles.length,
            total_views: publishedArticles.reduce((sum, a) => sum + a.views, 0),
            total_likes: publishedArticles.reduce((sum, a) => sum + a.likes, 0),
            total_shares: publishedArticles.reduce((sum, a) => sum + a.shares, 0),
            categories: [...new Set(publishedArticles.map(a => a.category))],
            featured_count: publishedArticles.filter(a => a.featured).length
        };
        
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
            success: true,
            data: paginatedArticles,
            stats: stats,
            pagination: {
                page,
                limit,
                total: publishedArticles.length,
                pages: Math.ceil(publishedArticles.length / limit)
            }
        }));
        return;
    }
    
    // API جستجوی هوشمند
    if (pathname === '/api/search') {
        const query = parsedUrl.query.q || '';
        const mode = parsedUrl.query.mode || 'quick'; // quick, advanced
        
        if (!query || query.trim().length < 2) {
            res.writeHead(400, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: false,
                error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد'
            }));
            return;
        }
        
        try {
            let searchResult;
            
            if (mode === 'advanced') {
                searchResult = searchAPI.advancedSearch({
                    query: query,
                    category: parsedUrl.query.category,
                    minViews: parsedUrl.query.minViews ? parseInt(parsedUrl.query.minViews) : null,
                    minLikes: parsedUrl.query.minLikes ? parseInt(parsedUrl.query.minLikes) : null,
                    dateFrom: parsedUrl.query.dateFrom,
                    dateTo: parsedUrl.query.dateTo,
                    featuredOnly: parsedUrl.query.featured === 'true',
                    sortBy: parsedUrl.query.sortBy || 'relevance'
                });
            } else {
                searchResult = searchAPI.quickSearch(query);
            }
            
            res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: true,
                ...searchResult
            }));
        } catch (error) {
            console.error('❌ خطا در جستجو:', error);
            res.writeHead(500, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: false,
                error: 'خطا در پردازش جستجو'
            }));
        }
        return;
    }
    
    // API پیشنهادات جستجو
    if (pathname === '/api/search/suggest') {
        const query = parsedUrl.query.q || '';
        
        try {
            const suggestions = searchAPI.getSuggestions(query);
            res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: true,
                ...suggestions
            }));
        } catch (error) {
            res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: true,
                suggestions: [],
                popular: []
            }));
        }
        return;
    }
    
    // API آمار جستجو
    if (pathname === '/api/search/stats') {
        try {
            const stats = searchAPI.getSearchStats();
            res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: true,
                stats: stats
            }));
        } catch (error) {
            res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: true,
                stats: { error: 'آمار در دسترس نیست' }
            }));
        }
        return;
    }
    
    // API مقاله خاص
    if (pathname.startsWith('/api/articles/')) {
        const id = parseInt(pathname.split('/').pop());
        const article = articles.find(a => a.id === id && a.status === 'published');
        
        if (article) {
            res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: true,
                data: article,
                related: this.getRelatedArticles(article)
            }));
        } else {
            res.writeHead(404, { 'Content-Type': 'application/json; charset=utf-8' });
            res.end(JSON.stringify({
                success: false,
                error: 'مقاله یافت نشد'
            }));
        }
        return;
    }
    
    // API سلامت
    if (pathname === '/api/health') {
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
            status: 'healthy',
            service: 'natiq-search-api',
            version: '3.1.0',
            articles: articles.length,
            searchEnabled: !!searchAPI,
            timestamp: new Date().toISOString()
        }));
        return;
    }
    
    // API آمار کلی
    if (pathname === '/api/stats') {
        const publishedArticles = articles.filter(a => a.status === 'published');
        
        const stats = {
            total_articles: publishedArticles.length,
            total_views: publishedArticles.reduce((sum, a) => sum + a.views, 0),
            total_likes: publishedArticles.reduce((sum, a) => sum + a.likes, 0),
            total_shares: publishedArticles.reduce((sum, a) => sum + a.shares, 0),
            avg_views: Math.round(publishedArticles.reduce((sum, a) => sum + a.views, 0) / publishedArticles.length),
            avg_likes: Math.round(publishedArticles.reduce((sum, a) => sum + a.likes, 0) / publishedArticles.length),
            categories: publishedArticles.reduce((cats, a) => {
                cats[a.category] = (cats[a.category] || 0) + 1;
                return cats;
            }, {}),
            featured_count: publishedArticles.filter(a => a.featured).length,
            last_updated: new Date().toISOString()
        };
        
        res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
        res.end(JSON.stringify({
            success: true,
            data: stats
        }));
        return;
    }
    
    // فایل‌های استاتیک
    const publicPath = path.join(__dirname, '../../public');
    const filePath = path.join(publicPath, pathname);
    
    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        const ext = path.extname(filePath);
        const contentType = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.json': 'application/json',
            '.png': 'image/png',
            '.jpg': 'image/jpeg'
        }[ext] || 'text/plain';
        
        res.writeHead(200, { 'Content-Type': contentType + '; charset=utf-8' });
        res.end(fs.readFileSync(filePath));
        return;
    }
    
    // 404
    res.writeHead(404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end('<h1>404 - صفحه یافت نشد</h1><p>صفحه مورد نظر وجود ندارد.</p>');
});

// Helper: دریافت مقالات مرتبط
function getRelatedArticles(article, limit = 5) {
    return articles
        .filter(a => 
            a.id !== article.id && 
            a.status === 'published' &&
            (a.category === article.category || 
             a.tags.some(tag => article.tags.includes(tag)))
        )
        .slice(0, limit)
        .map(a => ({
            id: a.id,
            title: a.title,
            excerpt: a.excerpt,
            category: a.category
        }));
}

// شروع سرور
server.listen(PORT, () => {
    console.log(`
    🚀 ============================================
        نطق مصطلح - نسخه جستجوی هوشمند
    ============================================
    
    📍 آدرس: http://localhost:${PORT}
    📊 مقالات: ${articles.length} مقاله NLP فارسی
    🔍 جستجو: هوشمند با استنتاج
    🧠 قابلیت‌ها: معنایی، مترادف، استدلال
    
    ✅ سیستم آماده استفاده است!
    ============================================
    `);
    
    // نمایش آمار اولیه
    console.log('📈 آمار اولیه:');
    console.log(`   مقالات: ${articles.length}`);
    console.log(`   دسته‌بندی‌ها: ${[...new Set(articles.map(a => a.category))].join(', ')}`);
    console.log(`   بازدید کل: ${articles.reduce((sum, a) => sum + a.views, 0).toLocaleString('fa-IR')}`);
    
    if (searchAPI.getSearchStats) {
        const searchStats = searchAPI.getSearchStats();
        console.log(`   کلمات کلیدی ایندکس شده: ${searchStats.indexedKeywords}`);
        console.log(`   مفاهیم معنایی: ${searchStats.semanticConcepts}`);
    }
});

// مدیریت خاموشی
process.on('SIGTERM', () => {
    console.log('🛑 دریافت سیگنال خاموشی...');
    server.close(() => {
        console.log('✅ سرور خاموش شد');
        process.exit(0);
    });
});
