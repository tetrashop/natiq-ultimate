/**
 * 🚀 سرور نطق مصطلح با ذخیره‌سازی JSON
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
  } else {
    console.log('⚠️  فایل مقالات یافت نشد. مقالات خالی آغاز می‌شود.');
  }
} catch (error) {
  console.error('❌ خطا در خواندن فایل مقالات:', error);
}

// HTML صفحه اصلی
const indexHTML = `
<!DOCTYPE html>
<html dir="rtl" lang="fa">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نطق مصطلح | مقالات NLP فارسی</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: system-ui, -apple-system, sans-serif; background: #f5f5f5; color: #333; line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }
        
        header { background: #4361ee; color: white; padding: 1rem 0; }
        .header-content { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.5rem; font-weight: bold; text-decoration: none; color: white; }
        
        .hero { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 3rem 0; text-align: center; }
        .hero h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        .hero p { font-size: 1.2rem; opacity: 0.9; }
        
        .articles { padding: 3rem 0; }
        .article-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 2rem; }
        .article-card { background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .article-title { font-size: 1.25rem; margin-bottom: 0.5rem; color: #333; }
        .article-excerpt { color: #666; margin-bottom: 1rem; }
        .article-meta { display: flex; justify-content: space-between; color: #888; font-size: 0.9rem; }
        
        footer { background: #333; color: white; padding: 2rem 0; text-align: center; margin-top: 3rem; }
        
        @media (max-width: 768px) {
            .article-grid { grid-template-columns: 1fr; }
            .hero h1 { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <a href="/" class="logo">نطق مصطلح</a>
                <div>مدیریت مقالات NLP فارسی</div>
            </div>
        </div>
    </header>
    
    <section class="hero">
        <div class="container">
            <h1>سیستم مدیریت مقالات پردازش زبان طبیعی فارسی</h1>
            <p>مدیریت، جستجو و تحلیل مقالات تخصصی در حوزه NLP</p>
        </div>
    </section>
    
    <main class="articles">
        <div class="container">
            <h2 style="margin-bottom: 2rem; text-align: center;">مقالات تخصصی NLP (${articles.length} مقاله)</h2>
            <div id="articles" class="article-grid">
                <!-- مقالات با JavaScript بارگذاری می‌شوند -->
            </div>
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>© ۲۰۲۴ نطق مصطلح. تمامی حقوق محفوظ است.</p>
        </div>
    </footer>
    
    <script>
        // بارگذاری مقالات
        async function loadArticles() {
            try {
                const response = await fetch('/api/articles');
                const result = await response.json();
                
                const container = document.getElementById('articles');
                container.innerHTML = '';
                
                if (result.data && result.data.length > 0) {
                    result.data.forEach(article => {
                        const articleHTML = \`
                            <div class="article-card">
                                <h3 class="article-title">\${article.title}</h3>
                                <p class="article-excerpt">\${article.excerpt}</p>
                                <div class="article-meta">
                                    <span>\${article.category}</span>
                                    <span>\${new Date(article.created_at).toLocaleDateString('fa-IR')}</span>
                                </div>
                                <div style="margin-top: 1rem; display: flex; justify-content: space-between;">
                                    <span>👁️ \${article.views.toLocaleString('fa-IR')} بازدید</span>
                                    <span>❤️ \${article.likes.toLocaleString('fa-IR')} لایک</span>
                                </div>
                            </div>
                        \`;
                        container.innerHTML += articleHTML;
                    });
                } else {
                    container.innerHTML = '<p style="text-align: center; color: #666;">مقاله‌ای یافت نشد</p>';
                }
            } catch (error) {
                console.error('خطا در بارگذاری مقالات:', error);
                document.getElementById('articles').innerHTML = 
                    '<p style="text-align: center; color: #666;">خطا در بارگذاری مقالات</p>';
            }
        }
        
        // بارگذاری اولیه
        document.addEventListener('DOMContentLoaded', loadArticles);
    </script>
</body>
</html>
`;

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
    const html = indexHTML.replace('${articles.length}', articles.length);
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(html);
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
    
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      success: true,
      data: paginatedArticles,
      pagination: {
        page,
        limit,
        total: publishedArticles.length,
        pages: Math.ceil(publishedArticles.length / limit)
      }
    }));
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
        data: article
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
      service: 'natiq-json-api',
      version: '1.0.0',
      articles: articles.length,
      timestamp: new Date().toISOString()
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

// شروع سرور
server.listen(PORT, () => {
  console.log(`
    🚀 ============================================
        نطق مصطلح - نسخه JSON
    ============================================
    
    📍 آدرس: http://localhost:${PORT}
    📊 مقالات: ${articles.length} مقاله NLP فارسی
    💾 ذخیره‌سازی: JSON
    
    ✅ سیستم آماده استفاده است!
    ============================================
    `);
});

// مدیریت خاموشی
process.on('SIGTERM', () => {
  console.log('🛑 دریافت سیگنال خاموشی...');
  server.close(() => {
    console.log('✅ سرور خاموش شد');
    process.exit(0);
  });
});
