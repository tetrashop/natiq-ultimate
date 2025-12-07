const http = require('http');
const fs = require('fs');
const path = require('path');

console.log('🚀 سرور مستقل نطق مصطلح راه‌اندازی می‌شود...');

// خواندن مقالات
const articlesPath = path.join(__dirname, './data/articles.json');
let articles = [];
try {
    const data = fs.readFileSync(articlesPath, 'utf8');
    articles = JSON.parse(data);
    console.log(`✅ ${articles.length} مقاله بارگذاری شد`);
} catch (error) {
    console.error('❌ خطا در خواندن مقالات:', error.message);
    articles = [{ id: 1, title: 'مقاله تست', content: 'محتوای تست' }];
}

// تابع جستجوی ساده
function searchArticles(query) {
    if (!query || query.length < 2) {
        return { error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد' };
    }
    
    const results = articles.filter(article => {
        const searchText = (article.title + ' ' + (article.excerpt || '') + ' ' + 
                           (article.tags ? article.tags.join(' ') : '')).toLowerCase();
        return searchText.includes(query.toLowerCase());
    }).slice(0, 10);
    
    return {
        success: true,
        query: query,
        totalResults: results.length,
        results: results.map(article => ({
            article: { 
                id: article.id,
                title: article.title,
                excerpt: article.excerpt || article.content?.substring(0, 100) || ''
            },
            score: 10,
            relevance: 'متوسط'
        }))
    };
}

// ایجاد سرور
const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);
    
    // تنظیم هدرهای CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(204);
        res.end();
        return;
    }
    
    const pathname = url.pathname;
    
    if (pathname === '/api/health') {
        res.writeHead(200);
        res.end(JSON.stringify({
            status: 'healthy',
            service: 'natiq-standalone',
            articles: { total: articles.length },
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    if (pathname === '/api/search' && req.method === 'GET') {
        const query = url.searchParams.get('q');
        const result = searchArticles(query);
        
        if (result.error) {
            res.writeHead(400);
            res.end(JSON.stringify({ success: false, error: result.error }, null, 2));
        } else {
            res.writeHead(200);
            res.end(JSON.stringify(result, null, 2));
        }
        return;
    }
    
    if (pathname === '/api/articles' && req.method === 'GET') {
        const page = parseInt(url.searchParams.get('page')) || 1;
        const limit = Math.min(parseInt(url.searchParams.get('limit')) || 10, 50);
        const offset = (page - 1) * limit;
        
        const paginated = articles.slice(offset, offset + limit).map(a => ({
            id: a.id,
            title: a.title,
            excerpt: a.excerpt || a.content?.substring(0, 150) || '',
            category: a.category || 'عمومی',
            views: a.views || 0
        }));
        
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            data: paginated,
            pagination: {
                page: page,
                limit: limit,
                total: articles.length,
                pages: Math.ceil(articles.length / limit)
            }
        }, null, 2));
        return;
    }
    
    // صفحه اصلی
    if (pathname === '/' || pathname === '/index.html') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(`
            <!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>نطق مصطلح - نسخه مستقل</title>
                <style>
                    body { font-family: system-ui; padding: 20px; max-width: 800px; margin: 0 auto; }
                    h1 { color: #333; }
                    input { padding: 10px; width: 300px; margin: 10px 0; }
                    button { padding: 10px 20px; background: #4361ee; color: white; border: none; cursor: pointer; }
                    .result { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }
                </style>
            </head>
            <body>
                <h1>نطق مصطلح - نسخه مستقل</h1>
                <p>${articles.length} مقاله NLP فارسی</p>
                
                <div>
                    <input id="searchInput" placeholder="جستجو در مقالات..." />
                    <button onclick="search()">جستجو</button>
                </div>
                
                <div id="results"></div>
                
                <script>
                    async function search() {
                        const query = document.getElementById('searchInput').value;
                        if (!query || query.length < 2) {
                            alert('حداقل ۲ کاراکتر وارد کنید');
                            return;
                        }
                        
                        const resultsDiv = document.getElementById('results');
                        resultsDiv.innerHTML = '<p>در حال جستجو...</p>';
                        
                        try {
                            const response = await fetch('/api/search?q=' + encodeURIComponent(query));
                            const data = await response.json();
                            
                            if (data.success) {
                                resultsDiv.innerHTML = \`
                                    <h3>\${data.totalResults} نتیجه یافت شد:</h3>
                                    \${data.results.map(r => \`
                                        <div class="result">
                                            <h4>\${r.article.title}</h4>
                                            <p>\${r.article.excerpt}</p>
                                        </div>
                                    \`).join('')}
                                \`;
                            } else {
                                resultsDiv.innerHTML = '<p>خطا: ' + (data.error || 'خطای ناشناخته') + '</p>';
                            }
                        } catch (error) {
                            resultsDiv.innerHTML = '<p>خطا در ارتباط با سرور</p>';
                        }
                    }
                </script>
            </body>
            </html>
        `);
        return;
    }
    
    // 404
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'مسیر یافت نشد' }, null, 2));
});

// شروع سرور
const PORT = 3001;
server.listen(PORT, () => {
    console.log(\`
    🚀 ============================================
        نطق مصطلح - نسخه مستقل
    ============================================
    
    📍 آدرس: http://localhost:\${PORT}
    📊 مقالات: \${articles.length} مقاله NLP فارسی
    🔍 جستجو: فعال (ساده)
    
    ✅ سیستم آماده استفاده است!
    ============================================
    \`);
});

// مدیریت خطا
server.on('error', (error) => {
    console.error('❌ خطای سرور:', error.message);
});

// مدیریت خاموشی
process.on('SIGTERM', () => {
    console.log('\\n🛑 سرور خاموش می‌شود...');
    server.close(() => {
        console.log('✅ سرور خاموش شد');
        process.exit(0);
    });
});
