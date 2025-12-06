const http = require('http');
const fs = require('fs');
const url = require('url');

console.log('🚀 راه‌اندازی سرور دیباگ...');

// خواندن مقالات
let articles = [];
try {
    const data = fs.readFileSync('./data/articles.json', 'utf8');
    articles = JSON.parse(data);
    console.log('✅ ' + articles.length + ' مقاله بارگذاری شد');
} catch (e) {
    console.log('❌ خطا در بارگذاری مقالات: ' + e.message);
    articles = [];
}

// تابع جستجو
function searchArticles(query) {
    console.log('🔍 جستجو برای: "' + query + '"');
    
    if (!query || query.length < 2) {
        return { error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد' };
    }
    
    const results = [];
    const queryLower = query.toLowerCase();
    let count = 0;
    
    console.log('📊 بررسی ' + Math.min(articles.length, 100) + ' مقاله...');
    
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
            count++;
            if (count <= 3) {
                console.log('   ✅ یافت شد: "' + article.title.substring(0, 50) + '"');
            }
        }
    }
    
    console.log('🎯 کل نتایج: ' + results.length);
    
    return {
        success: true,
        query: query,
        totalResults: results.length,
        results: results.slice(0, 10)
    };
}

// ایجاد سرور
const server = http.createServer((req, res) => {
    console.log('\n📨 درخواست دریافت شد:');
    console.log('   URL: ' + req.url);
    console.log('   Method: ' + req.method);
    
    const parsedUrl = url.parse(req.url, true);
    
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    if (parsedUrl.pathname === '/api/health') {
        console.log('   📊 پاسخ سلامت ارسال شد');
        res.end(JSON.stringify({
            status: 'healthy',
            service: 'natiq-debug',
            articles: { total: articles.length },
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    if (parsedUrl.pathname === '/api/search' && req.method === 'GET') {
        const query = parsedUrl.query.q || '';
        console.log('   🔍 عبارت جستجو: "' + query + '"');
        
        const result = searchArticles(query);
        
        if (result.error) {
            console.log('   ❌ خطا: ' + result.error);
            res.statusCode = 400;
            res.end(JSON.stringify({ success: false, error: result.error }, null, 2));
        } else {
            console.log('   ✅ نتایج ارسال شد: ' + result.totalResults + ' نتیجه');
            res.end(JSON.stringify(result, null, 2));
        }
        return;
    }
    
    console.log('   ❌ مسیر نامعتبر');
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'مسیر یافت نشد' }, null, 2));
});

// شروع سرور
const PORT = 3002;  // تغییر پورت برای جلوگیری از تداخل
server.listen(PORT, () => {
    console.log('\n=============================================');
    console.log('    نطق مصطلح - نسخه دیباگ');
    console.log('=============================================');
    console.log('');
    console.log('📍 آدرس: http://localhost:' + PORT);
    console.log('📊 مقالات: ' + articles.length + ' مقاله');
    console.log('🔍 جستجو: فعال با لاگینگ کامل');
    console.log('');
    console.log('✅ سیستم آماده استفاده است!');
    console.log('=============================================\n');
});

server.on('error', (err) => {
    console.error('❌ خطای سرور:', err.message);
});
