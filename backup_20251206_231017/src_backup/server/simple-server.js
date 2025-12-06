const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3001;
const DATA_PATH = path.join(__dirname, '../../data/articles.json');

// خواندن مقالات
let articles = [];
try {
    articles = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));
    console.log(`✅ ${articles.length} مقاله بارگذاری شد`);
} catch (error) {
    console.error('❌ خطا در خواندن مقالات:', error.message);
}

// تابع ارسال JSON
function sendJSON(res, statusCode, data) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*'
    });
    res.end(JSON.stringify(data, null, 2));
}

// تابع جستجوی ساده
function simpleSearch(query, articles) {
    if (!query || query.length < 2) {
        return { error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد' };
    }
    
    const results = articles.filter(article => {
        const searchText = (article.title + ' ' + article.excerpt + ' ' + (article.tags || []).join(' ')).toLowerCase();
        return searchText.includes(query.toLowerCase());
    }).slice(0, 20);
    
    return {
        success: true,
        query: query,
        totalResults: results.length,
        results: results.map(article => ({
            article: article,
            score: 10,
            relevance: 'متوسط'
        }))
    };
}

// ایجاد سرور
const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);
    const pathname = url.pathname;
    
    // CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    
    if (pathname === '/api/health') {
        sendJSON(res, 200, {
            status: 'healthy',
            service: 'natiq-simple-api',
            articles: { total: articles.length },
            timestamp: new Date().toISOString()
        });
        return;
    }
    
    if (pathname === '/api/search' && req.method === 'GET') {
        const query = url.searchParams.get('q');
        const result = simpleSearch(query, articles);
        
        if (result.error) {
            sendJSON(res, 400, { success: false, error: result.error });
        } else {
            sendJSON(res, 200, result);
        }
        return;
    }
    
    if (pathname === '/api/articles' && req.method === 'GET') {
        const page = parseInt(url.searchParams.get('page')) || 1;
        const limit = parseInt(url.searchParams.get('limit')) || 10;
        const offset = (page - 1) * limit;
        
        sendJSON(res, 200, {
            success: true,
            data: articles.slice(offset, offset + limit),
            pagination: { page, limit, total: articles.length }
        });
        return;
    }
    
    // صفحه اصلی
    if (pathname === '/' || pathname === '/index.html') {
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(`
            <!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head><title>نطق مصطلح - نسخه ساده</title></head>
            <body>
                <h1>نطق مصطلح - نسخه ساده</h1>
                <p>${articles.length} مقاله NLP فارسی</p>
                <p>جستجو: <input id="search" placeholder="جستجو...">
                <button onclick="search()">جستجو</button></p>
                <div id="results"></div>
                <script>
                    async function search() {
                        const query = document.getElementById('search').value;
                        const res = await fetch('/api/search?q=' + encodeURIComponent(query));
                        const data = await res.json();
                        document.getElementById('results').innerHTML = 
                            data.results ? \`<h3>\${data.totalResults} نتیجه:</h3>
                            \${data.results.map(r => '<p>' + r.article.title + '</p>').join('')}\`
                            : data.error || 'خطا';
                    }
                </script>
            </body>
            </html>
        `);
        return;
    }
    
    // 404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'مسیر یافت نشد' }));
});

// شروع سرور
server.listen(PORT, () => {
    console.log(\`
    🚀 سرور ساده نطق مصطلح
    📍 آدرس: http://localhost:\${PORT}
    📊 مقالات: \${articles.length} مقاله
    🔍 جستجو: فعال (ساده)
    ✅ سیستم آماده استفاده است!
    \`);
});

// مدیریت خاموشی
process.on('SIGTERM', () => {
    console.log('\\n🛑 سرور خاموش می‌شود...');
    server.close(() => process.exit(0));
});
