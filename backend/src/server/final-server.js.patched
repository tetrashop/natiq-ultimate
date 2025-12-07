/**
 * 🚀 سرور نهایی نطق مصطلح با جستجوی واقعی
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const querystring = require('querystring');

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

// بارگذاری سیستم جستجوی واقعی
let searchAPI;
try {
    const RealSearchAPI = require('../search/real-search-api');
    searchAPI = new RealSearchAPI(articles);
    console.log('🔍 سیستم جستجوی واقعی راه‌اندازی شد');
    
    // نمایش آمار اولیه
    const stats = searchAPI.getStats();
    console.log('📊 آمار جستجو:');
    console.log(`   مقالات: ${stats.engine.totalArticles}`);
    console.log(`   کلمات کلیدی: ${stats.engine.totalIndexedWords}`);
    console.log(`   دسته‌بندی‌ها: ${stats.engine.categories}`);
    
} catch (error) {
    console.error('❌ خطا در راه‌اندازی سیستم جستجو:', error);
    console.error(error.stack);
    searchAPI = null;
}

// خواندن فایل HTML اصلی
const indexHTML = fs.readFileSync(
    path.join(__dirname, '../../public/index.html'), 
    'utf8'
);

// تابع برای ارسال پاسخ JSON
function sendJSON(res, statusCode, data) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
    });
    res.end(JSON.stringify(data, null, 2));
}

// تابع برای ارسال خطا
function sendError(res, statusCode, message) {
    sendJSON(res, statusCode, {
        success: false,
        error: message,
        timestamp: new Date().toISOString()
    });
}

// ایجاد سرور HTTP
const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    // CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
    
    // OPTIONS request
    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }
    
    // صفحه اصلی
    if (pathname === '/' || pathname === '/index.html') {
        res.writeHead(200, {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'no-cache'
        });
        res.end(indexHTML);
        return;
    }
    
    // API مقالات
    if (pathname === '/api/articles' && req.method === 'GET') {
        try {
            const page = parseInt(parsedUrl.query.page) || 1;
            const limit = parseInt(parsedUrl.query.limit) || 12;
            const offset = (page - 1) * limit;
            const category = parsedUrl.query.category;
            const featured = parsedUrl.query.featured;
            
            // فیلتر مقالات
            let filteredArticles = articles.filter(article => 
                article.status === 'published'
            );
            
            // اعمال فیلترهای اضافی
            if (category) {
                filteredArticles = filteredArticles.filter(article => 
                    article.category === category
                );
            }
            
            if (featured === 'true') {
                filteredArticles = filteredArticles.filter(article => 
                    article.featured === true
                );
            }
            
            // مرتب‌سازی
            filteredArticles.sort((a, b) => 
                new Date(b.created_at) - new Date(a.created_at)
            );
            
            // صفحه‌بندی
            const paginatedArticles = filteredArticles.slice(offset, offset + limit);
            
            // محاسبه آمار
            const stats = {
                total_articles: filteredArticles.length,
                total_views: filteredArticles.reduce((sum, a) => sum + a.views, 0),
                total_likes: filteredArticles.reduce((sum, a) => sum + a.likes, 0),
                total_shares: filteredArticles.reduce((sum, a) => sum + a.shares, 0),
                categories: [...new Set(filteredArticles.map(a => a.category))],
                featured_count: filteredArticles.filter(a => a.featured).length
            };
            
            sendJSON(res, 200, {
                success: true,
                data: paginatedArticles,
                stats: stats,
                pagination: {
                    page: page,
                    limit: limit,
                    total: filteredArticles.length,
                    pages: Math.ceil(filteredArticles.length / limit),
                    has_next: offset + limit < filteredArticles.length,
                    has_prev: page > 1
                }
            });
        } catch (error) {
            console.error('❌ خطا در API مقالات:', error);
            sendError(res, 500, 'خطا در دریافت مقالات');
        }
        return;
    }
    
    // API جستجوی واقعی

    // API جستجوی واقعی
    if (pathname === '/api/search' && req.method === 'GET') {
        if (!searchAPI) {
            sendError(res, 503, 'سیستم جستجو در دسترس نیست');
            return;
        }
        
        try {
            const query = parsedUrl.query.q;
            
            if (!query || query.trim().length < 2) {
                sendError(res, 400, 'عبارت جستجو باید حداقل ۲ کاراکتر باشد');
                return;
            }
            
            // تشخیص نوع جستجو
            const mode = parsedUrl.query.mode || 'quick';
            
            let result;
            if (mode === 'advanced') {
                result = searchAPI.advancedSearch({
                    query: query,
                    category: parsedUrl.query.category,
                    minViews: parsedUrl.query.minViews,
                    minLikes: parsedUrl.query.minLikes,
                    dateFrom: parsedUrl.query.dateFrom,
                    dateTo: parsedUrl.query.dateTo,
                    featured: parsedUrl.query.featured,
                    sortBy: parsedUrl.query.sortBy,
                    limit: parsedUrl.query.limit || 20
                });
            } else {
                result = searchAPI.search(query, {
                    limit: parsedUrl.query.limit || 20,
                    category: parsedUrl.query.category,
                    sortBy: parsedUrl.query.sortBy || 'relevance'
                });
            }
            
            sendJSON(res, 200, result);
        } catch (error) {
            console.error('❌ خطا در پردازش جستجو:', error.message);
            console.error('جزئیات خطا:', error.stack);
            sendError(res, 500, 'خطا در پردازش جستجو: ' + error.message);
        }
        return;
    }

    
    // API جستجوی سریع (برای autocomplete)
    if (pathname === '/api/search/quick' && req.method === 'GET') {
        if (!searchAPI) {
            sendJSON(res, 200, {
                success: true,
                suggestions: [],
                popular: []
            });
            return;
        }
        
        try {
            const query = parsedUrl.query.q || '';
            const limit = parseInt(parsedUrl.query.limit) || 8;
            
            const result = searchAPI.quickSearch(query, limit);
            sendJSON(res, 200, result);
        } catch (error) {
            console.error('❌ خطا در جستجوی سریع:', error);
            sendJSON(res, 200, {
                success: true,
                suggestions: [],
                popular: []
            });
        }
        return;
    }
    
    // API پیشنهادات جستجو
    if (pathname === '/api/search/suggest' && req.method === 'GET') {
        if (!searchAPI) {
            sendJSON(res, 200, {
                success: true,
                suggestions: [],
                popular: []
            });
            return;
        }
        
        try {
            const query = parsedUrl.query.q || '';
            const keywords = searchAPI.suggestKeywords(query);
            const popular = searchAPI.getPopularSearches(5);
            
            sendJSON(res, 200, {
                success: true,
                query: query,
                suggestions: keywords,
                popular: popular
            });
        } catch (error) {
            sendJSON(res, 200, {
                success: true,
                suggestions: [],
                popular: []
            });
        }
        return;
    }
    
    // API آمار جستجو
    if (pathname === '/api/search/stats' && req.method === 'GET') {
        if (!searchAPI) {
            sendJSON(res, 200, {
                success: true,
                stats: { error: 'سیستم جستجو در دسترس نیست' }
            });
            return;
        }
        
        try {
            const stats = searchAPI.getStats();
            sendJSON(res, 200, {
                success: true,
                stats: stats
            });
        } catch (error) {
            sendJSON(res, 200, {
                success: true,
                stats: { error: 'خطا در دریافت آمار' }
            });
        }
        return;
    }
    
    // API مقاله خاص
    if (pathname.match(/^\/api\/articles\/\d+$/) && req.method === 'GET') {
        try {
            const id = parseInt(pathname.split('/').pop());
            const article = articles.find(a => a.id === id && a.status === 'published');
            
            if (article) {
                // افزایش تعداد بازدید
                article.views = (article.views || 0) + 1;
                
                // ذخیره تغییرات
                fs.writeFileSync(DATA_PATH, JSON.stringify(articles, null, 2));
                
                // یافتن مقالات مرتبط
                const relatedArticles = this.getRelatedArticles(article, 4);
                
                sendJSON(res, 200, {
                    success: true,
                    data: article,
                    related: relatedArticles,
                    metadata: {
                        served_at: new Date().toISOString(),
                        view_count: article.views
                    }
                });
            } else {
                sendError(res, 404, 'مقاله یافت نشد');
            }
        } catch (error) {
            console.error('❌ خطا در دریافت مقاله:', error);
            sendError(res, 500, 'خطا در دریافت مقاله');
        }
        return;
    }
    
    // افزودن مقاله جدید (POST)
    if (pathname === '/api/articles' && req.method === 'POST') {
        let body = '';
        
        req.on('data', chunk => {
            body += chunk.toString();
        });
        
        req.on('end', () => {
            try {
                const articleData = JSON.parse(body);
                
                // اعتبارسنجی
                if (!articleData.title || !articleData.content) {
                    sendError(res, 400, 'عنوان و محتوا الزامی هستند');
                    return;
                }
                
                // ایجاد مقاله جدید
                const newArticle = {
                    id: articles.length > 0 ? Math.max(...articles.map(a => a.id)) + 1 : 1,
                    title: articleData.title,
                    slug: this.generateSlug(articleData.title),
                    content: articleData.content,
                    excerpt: articleData.excerpt || articleData.content.substring(0, 150) + '...',
                    author: articleData.author || 'تیم نطق مصطلح',
                    category: articleData.category || 'عمومی',
                    tags: articleData.tags || [],
                    views: 0,
                    likes: 0,
                    shares: 0,
                    featured: articleData.featured || false,
                    status: articleData.status || 'published',
                    created_at: new Date().toISOString(),
                    updated_at: new Date().toISOString()
                };
                
                // افزودن به مقالات
                articles.push(newArticle);
                
                // ذخیره در فایل
                fs.writeFileSync(DATA_PATH, JSON.stringify(articles, null, 2));
                
                // به‌روزرسانی سیستم جستجو
                if (searchAPI) {
                    searchAPI.searchEngine.articles = articles;
                    searchAPI.searchEngine.searchIndex = searchAPI.searchEngine.buildSearchIndex();
                    searchAPI.searchEngine.invertedIndex = searchAPI.searchEngine.buildInvertedIndex();
                }
                
                sendJSON(res, 201, {
                    success: true,
                    message: 'مقاله با موفقیت اضافه شد',
                    data: newArticle,
                    metadata: {
                        total_articles: articles.length,
                        timestamp: new Date().toISOString()
                    }
                });
            } catch (error) {
                console.error('❌ خطا در افزودن مقاله:', error);
                sendError(res, 500, 'خطا در افزودن مقاله');
            }
        });
        return;
    }
    
    // به‌روزرسانی مقاله (PUT)
    if (pathname.match(/^\/api\/articles\/\d+$/) && req.method === 'PUT') {
        const id = parseInt(pathname.split('/').pop());
        let body = '';
        
        req.on('data', chunk => {
            body += chunk.toString();
        });
        
        req.on('end', () => {
            try {
                const articleIndex = articles.findIndex(a => a.id === id);
                
                if (articleIndex === -1) {
                    sendError(res, 404, 'مقاله یافت نشد');
                    return;
                }
                
                const updates = JSON.parse(body);
                
                // به‌روزرسانی مقاله
                articles[articleIndex] = {
                    ...articles[articleIndex],
                    ...updates,
                    updated_at: new Date().toISOString()
                };
                
                // ذخیره در فایل
                fs.writeFileSync(DATA_PATH, JSON.stringify(articles, null, 2));
                
                // به‌روزرسانی سیستم جستجو
                if (searchAPI) {
                    searchAPI.searchEngine.articles = articles;
                    searchAPI.searchEngine.searchIndex = searchAPI.searchEngine.buildSearchIndex();
                    searchAPI.searchEngine.invertedIndex = searchAPI.searchEngine.buildInvertedIndex();
                }
                
                sendJSON(res, 200, {
                    success: true,
                    message: 'مقاله با موفقیت به‌روزرسانی شد',
                    data: articles[articleIndex]
                });
            } catch (error) {
                console.error('❌ خطا در به‌روزرسانی مقاله:', error);
                sendError(res, 500, 'خطا در به‌روزرسانی مقاله');
            }
        });
        return;
    }
    
    // حذف مقاله (DELETE)
    if (pathname.match(/^\/api\/articles\/\d+$/) && req.method === 'DELETE') {
        try {
            const id = parseInt(pathname.split('/').pop());
            const articleIndex = articles.findIndex(a => a.id === id);
            
            if (articleIndex === -1) {
                sendError(res, 404, 'مقاله یافت نشد');
                return;
            }
            
            // حذف مقاله
            const deletedArticle = articles.splice(articleIndex, 1)[0];
            
            // ذخیره در فایل
            fs.writeFileSync(DATA_PATH, JSON.stringify(articles, null, 2));
            
            // به‌روزرسانی سیستم جستجو
            if (searchAPI) {
                searchAPI.searchEngine.articles = articles;
                searchAPI.searchEngine.searchIndex = searchAPI.searchEngine.buildSearchIndex();
                searchAPI.searchEngine.invertedIndex = searchAPI.searchEngine.buildInvertedIndex();
            }
            
            sendJSON(res, 200, {
                success: true,
                message: 'مقاله با موفقیت حذف شد',
                data: deletedArticle,
                metadata: {
                    remaining_articles: articles.length
                }
            });
        } catch (error) {
            console.error('❌ خطا در حذف مقاله:', error);
            sendError(res, 500, 'خطا در حذف مقاله');
        }
        return;
    }
    
    // API سلامت
    if (pathname === '/api/health' && req.method === 'GET') {
        sendJSON(res, 200, {
            status: 'healthy',
            service: 'natiq-final-api',
            version: '3.2.0',
            articles: {
                total: articles.length,
                published: articles.filter(a => a.status === 'published').length,
                featured: articles.filter(a => a.featured).length
            },
            search: {
                enabled: !!searchAPI,
                engine: searchAPI ? 'real-search-v1.0' : 'disabled'
            },
            timestamp: new Date().toISOString(),
            uptime: process.uptime().toFixed(2) + 's'
        });
        return;
    }
    
    // API آمار کلی
    if (pathname === '/api/stats' && req.method === 'GET') {
        try {
            const publishedArticles = articles.filter(a => a.status === 'published');
            
            const stats = {
                total_articles: publishedArticles.length,
                total_views: publishedArticles.reduce((sum, a) => sum + a.views, 0),
                total_likes: publishedArticles.reduce((sum, a) => sum + a.likes, 0),
                total_shares: publishedArticles.reduce((sum, a) => sum + a.shares, 0),
                avg_views: Math.round(publishedArticles.reduce((sum, a) => sum + a.views, 0) / publishedArticles.length || 0),
                avg_likes: Math.round(publishedArticles.reduce((sum, a) => sum + a.likes, 0) / publishedArticles.length || 0),
                categories: publishedArticles.reduce((cats, a) => {
                    cats[a.category] = (cats[a.category] || 0) + 1;
                    return cats;
                }, {}),
                featured_count: publishedArticles.filter(a => a.featured).length,
                last_updated: new Date().toISOString()
            };
            
            sendJSON(res, 200, {
                success: true,
                data: stats
            });
        } catch (error) {
            sendError(res, 500, 'خطا در دریافت آمار');
        }
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
            '.jpg': 'image/jpeg',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.ttf': 'font/ttf',
            '.woff': 'font/woff',
            '.woff2': 'font/woff2'
        }[ext] || 'text/plain';
        
        res.writeHead(200, {
            'Content-Type': contentType + '; charset=utf-8',
            'Cache-Control': 'public, max-age=3600'
        });
        res.end(fs.readFileSync(filePath));
        return;
    }
    
    // 404
    res.writeHead(404, {
        'Content-Type': 'text/html; charset=utf-8'
    });
    res.end(`
        <!DOCTYPE html>
        <html dir="rtl" lang="fa">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>۴۰۴ - صفحه یافت نشد</title>
            <style>
                body { font-family: system-ui; text-align: center; padding: 50px; background: #f8f9fa; }
                h1 { color: #dc3545; font-size: 3rem; }
                p { font-size: 1.2rem; color: #666; }
                a { color: #4361ee; text-decoration: none; }
                .container { max-width: 600px; margin: 0 auto; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>۴۰۴</h1>
                <p>صفحه مورد نظر یافت نشد.</p>
                <p><a href="/">بازگشت به صفحه اصلی</a></p>
            </div>
        </body>
        </html>
    `);
});

// Helper functions
function getRelatedArticles(article, limit = 4) {
    return articles
        .filter(a => 
            a.id !== article.id && 
            a.status === 'published' &&
            (a.category === article.category || 
             a.tags.some(tag => article.tags.includes(tag)))
        )
        .sort((a, b) => b.views - a.views)
        .slice(0, limit)
        .map(a => ({
            id: a.id,
            title: a.title,
            excerpt: a.excerpt,
            category: a.category,
            views: a.views
        }));
}

function generateSlug(text) {
    return text
        .replace(/[^\u0600-\u06FF\w\s-]/g, '')
        .trim()
        .replace(/\s+/g, '-')
        .replace(/--+/g, '-')
        .toLowerCase();
}

// شروع سرور
server.listen(PORT, () => {
    console.log(`
    🚀 ============================================
        نطق مصطلح - نسخه نهایی با جستجوی واقعی
    ============================================
    
    📍 آدرس: http://localhost:${PORT}
    📊 مقالات: ${articles.length} مقاله NLP فارسی
    🔍 جستجو: واقعی با TF-IDF
    📝 مدیریت: افزودن، ویرایش، حذف
    🧠 هوشمند: تحلیل و استنتاج
    
    ✅ سیستم آماده استفاده است!
    ============================================
    `);
    
    // نمایش آمار اولیه
    console.log('📈 آمار اولیه:');
    console.log(`   مقالات کل: ${articles.length}`);
    console.log(`   مقالات منتشر شده: ${articles.filter(a => a.status === 'published').length}`);
    console.log(`   مقالات ویژه: ${articles.filter(a => a.featured).length}`);
    console.log(`   بازدید کل: ${articles.reduce((sum, a) => sum + a.views, 0).toLocaleString('fa-IR')}`);
    
    if (searchAPI) {
        const stats = searchAPI.getStats();
        console.log(`   کلمات کلیدی ایندکس شده: ${stats.engine.totalIndexedWords}`);
        console.log(`   دسته‌بندی‌های مختلف: ${stats.engine.categories}`);
    }
    
    console.log('\n🔗 آدرس‌های مهم:');
    console.log(`   وب‌اپلیکیشن: http://localhost:${PORT}`);
    console.log(`   API سلامت: http://localhost:${PORT}/api/health`);
    console.log(`   API جستجو: http://localhost:${PORT}/api/search?q=پردازش`);
    console.log(`   API مقالات: http://localhost:${PORT}/api/articles`);
    console.log('=============================================');
});

// مدیریت خاموشی
process.on('SIGTERM', () => {
    console.log('\n🛑 دریافت سیگنال خاموشی...');
    server.close(() => {
        console.log('✅ سرور خاموش شد');
        process.exit(0);
    });
});

// مدیریت خطاهای پردازش نشده
process.on('uncaughtException', (error) => {
    console.error('❌ خطای پردازش نشده:', error);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Promise رد شده پردازش نشده:', reason);
});
