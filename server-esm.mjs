import { createServer } from 'http';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🚀 سرور ESM نطق مصطلح راه‌اندازی می‌شود...');

// خواندن مقالات
let articles = [];
try {
    const data = readFileSync(join(__dirname, './data/articles.json'), 'utf8');
    articles = JSON.parse(data);
    console.log(`✅ ${articles.length} مقاله بارگذاری شد`);
} catch (e) {
    console.log('⚠️  خطا در بارگذاری مقالات:', e.message);
    articles = [];
}

// تابع جستجو
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
const server = createServer((req, res) => {
    const url = new URL(req.url, `http://${req.headers.host}`);
    
    // هدرهای CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    if (url.pathname === '/api/health') {
        res.end(JSON.stringify({
            status: 'healthy',
            service: 'natiq-esm',
            articles: { total: articles.length },
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    if (url.pathname === '/api/search' && req.method === 'GET') {
        const query = url.searchParams.get('q') || '';
        const result = simpleSearch(query);
        
        if (result.error) {
            res.statusCode = 400;
            res.end(JSON.stringify({ success: false, error: result.error }, null, 2));
        } else {
            res.end(JSON.stringify(result, null, 2));
        }
        return;
    }
    
    // پاسخ پیش‌فرض
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'مسیر یافت نشد' }, null, 2));
});

// شروع سرور
const PORT = 3004;
server.listen(PORT, () => {
    console.log('\n🚀 ============================================');
    console.log('    نطق مصطلح - نسخه ESM');
    console.log('============================================');
    console.log(`📍 آدرس: http://localhost:${PORT}`);
    console.log(`📊 مقالات: ${articles.length} مقاله NLP فارسی`);
    console.log('✅ سیستم آماده استفاده است!');
    console.log('============================================\n');
});
