const http = require('http');
const fs = require('fs');

console.log('🚀 شروع سرور فوق ساده نطق مصطلح...');

// خواندن مقالات
let articles = [];
try {
    const data = fs.readFileSync('./data/articles.json', 'utf8');
    articles = JSON.parse(data);
    console.log('✅ مقالات بارگذاری شد: ' + articles.length + ' مقاله');
} catch (e) {
    console.log('⚠️  خطا در بارگذاری مقالات');
    articles = [];
}

// تابع جستجوی ساده
function simpleSearch(query) {
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
    console.log('📥 درخواست: ' + req.url);
    
    // هدرهای CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    const url = require('url');
    const parsedUrl = url.parse(req.url, true);
    
    if (parsedUrl.pathname === '/api/health') {
        res.end(JSON.stringify({
            status: 'healthy',
            service: 'natiq-super-simple',
            articles: { total: articles.length },
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    if (parsedUrl.pathname === '/api/search' && req.method === 'GET') {
        const query = parsedUrl.query.q || '';
        const result = simpleSearch(query);
        
        if (result.error) {
            res.statusCode = 400;
            res.end(JSON.stringify({ success: false, error: result.error }, null, 2));
        } else {
            res.end(JSON.stringify(result, null, 2));
        }
        return;
    }
    
    if (parsedUrl.pathname === '/api/articles' && req.method === 'GET') {
        const page = parseInt(parsedUrl.query.page) || 1;
        const limit = Math.min(parseInt(parsedUrl.query.limit) || 10, 50);
        const offset = (page - 1) * limit;
        
        const paginated = articles.slice(offset, offset + limit).map(a => ({
            id: a.id,
            title: a.title,
            excerpt: a.excerpt || (a.content ? a.content.substring(0, 150) + '...' : '')
        }));
        
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
    if (parsedUrl.pathname === '/' || parsedUrl.pathname === '/index.html') {
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.end([
            '<!DOCTYPE html>',
            '<html dir="rtl" lang="fa">',
            '<head>',
            '<meta charset="UTF-8">',
            '<title>نطق مصطلح - نسخه فوق ساده</title>',
            '<style>',
            'body { font-family: sans-serif; padding: 20px; }',
            'h1 { color: #333; }',
            'input { padding: 10px; width: 300px; }',
            'button { padding: 10px 20px; background: #4361ee; color: white; border: none; }',
            '</style>',
            '</head>',
            '<body>',
            '<h1>نطق مصطلح - نسخه فوق ساده</h1>',
            '<p>' + articles.length + ' مقاله NLP فارسی</p>',
            '<div>',
            '<input id="search" placeholder="جستجو در مقالات..." />',
            '<button onclick="search()">جستجو</button>',
            '</div>',
            '<div id="results"></div>',
            '<script>',
            'function search() {',
            '  var query = document.getElementById("search").value;',
            '  fetch("/api/search?q=" + encodeURIComponent(query))',
            '    .then(r => r.json())',
            '    .then(data => {',
            '      var html = "<h3>" + (data.totalResults || 0) + " نتیجه</h3>";',
            '      if (data.results) {',
            '        data.results.forEach(r => {',
            '          html += "<div><h4>" + r.article.title + "</h4><p>" + r.article.excerpt + "</p></div>";',
            '        });',
            '      }',
            '      document.getElementById("results").innerHTML = html;',
            '    });',
            '}',
            '</script>',
            '</body>',
            '</html>'
        ].join('\n'));
        return;
    }
    
    // 404
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'مسیر یافت نشد' }, null, 2));
});

// شروع سرور
const PORT = 3003;
server.listen(PORT, () => {
    console.log('\n🚀 ============================================');
    console.log('    نطق مصطلح - نسخه فوق ساده');
    console.log('============================================');
    console.log('');
    console.log('📍 آدرس: http://localhost:' + PORT);
    console.log('📊 مقالات: ' + articles.length + ' مقاله NLP فارسی');
    console.log('🔍 جستجو: فعال');
    console.log('');
    console.log('✅ سیستم آماده استفاده است!');
    console.log('============================================\n');
});

// مدیریت خطا
server.on('error', (error) => {
    console.error('❌ خطای سرور: ' + error.message);
});

// مدیریت خاموشی
process.on('SIGTERM', () => {
    console.log('\n🛑 سرور خاموش می‌شود...');
    server.close(() => {
        console.log('✅ سرور خاموش شد');
        process.exit(0);
    });
});
