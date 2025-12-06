/**
 * 🚀 سرور ساده نطق مصطلح
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const { execSync } = require('child_process');

const PORT = 3001;
const DB_PATH = path.join(__dirname, '../../data/natiq.db');

// تابع برای اجرای کوئری SQL
function runQuery(sql) {
  try {
    const tempFile = path.join(__dirname, 'temp_query.sql');
    fs.writeFileSync(tempFile, sql);
    const result = execSync(`sqlite3 ${DB_PATH} < ${tempFile}`).toString();
    fs.unlinkSync(tempFile);
    return result;
  } catch (error) {
    console.error('خطا در اجرای کوئری:', error);
    return null;
  }
}

// تابع برای اجرای کوئری و برگرداندن JSON
function runQueryJSON(sql) {
  const result = runQuery(sql);
  if (!result) return [];
  
  const lines = result.trim().split('\n');
  if (lines.length === 0) return [];
  
  // تبدیل به آرایه از اشیا
  const data = lines.map(line => {
    const obj = {};
    const parts = line.split('|');
    obj.id = parseInt(parts[0]) || 0;
    obj.title = parts[1] || '';
    obj.slug = parts[2] || '';
    obj.content = parts[3] || '';
    obj.excerpt = parts[4] || '';
    obj.author = parts[5] || 'تیم نطق مصطلح';
    obj.category = parts[6] || '';
    obj.views = parseInt(parts[7]) || 0;
    obj.likes = parseInt(parts[8]) || 0;
    obj.created_at = parts[9] || new Date().toISOString();
    return obj;
  });
  
  return data;
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
            <p>مدیریت، جستجو و تحلیل مقالات تخصصی در حوزه NLP با قابلیت‌های پیشرفته</p>
        </div>
    </section>
    
    <main class="articles">
        <div class="container">
            <h2 style="margin-bottom: 2rem; text-align: center;">مقالات تخصصی NLP</h2>
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
                const articles = await response.json();
                
                const container = document.getElementById('articles');
                container.innerHTML = '';
                
                articles.forEach(article => {
                    const articleHTML = \`
                        <div class="article-card">
                            <h3 class="article-title">\${article.title}</h3>
                            <p class="article-excerpt">\${article.excerpt}</p>
                            <div class="article-meta">
                                <span>\${article.category}</span>
                                <span>\${new Date(article.created_at).toLocaleDateString('fa-IR')}</span>
                            </div>
                            <div style="margin-top: 1rem; display: flex; justify-content: space-between;">
                                <span>👁️ \${article.views} بازدید</span>
                                <span>❤️ \${article.likes} لایک</span>
                            </div>
                        </div>
                    \`;
                    container.innerHTML += articleHTML;
                });
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
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(indexHTML);
    return;
  }
  
  // API مقالات
  if (pathname === '/api/articles') {
    const page = parseInt(parsedUrl.query.page) || 1;
    const limit = parseInt(parsedUrl.query.limit) || 10;
    const offset = (page - 1) * limit;
    
    // تعداد کل مقالات
    const countResult = runQuery('SELECT COUNT(*) as count FROM articles;');
    const total = countResult ? parseInt(countResult.split('|')[0]) || 0 : 0;
    
    // دریافت مقالات
    const sql = `SELECT id, title, slug, content, excerpt, author, category, views, likes, created_at FROM articles WHERE status = 'published' ORDER BY created_at DESC LIMIT ${limit} OFFSET ${offset};`;
    const articles = runQueryJSON(sql);
    
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      success: true,
      data: articles,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    }));
    return;
  }
  
  // API سلامت
  if (pathname === '/api/health') {
    res.writeHead(200, { 'Content-Type': 'application/json; charset=utf-8' });
    res.end(JSON.stringify({
      status: 'healthy',
      service: 'natiq-api',
      version: '1.0.0',
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
        نطق مصطلح - نسخه ساده
    ============================================
    
    📍 آدرس: http://localhost:${PORT}
    📊 مقالات: ۵۰ مقاله NLP فارسی
    🗄️  دیتابیس: SQLite
    
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
