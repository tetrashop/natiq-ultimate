/**
 * 🌱 تولید ساده ۱۹۹ مقاله NLP فارسی
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// موضوعات NLP فارسی (50 موضوع برای شروع)
const NLP_TOPICS = [
  'پردازش زبان طبیعی چیست؟',
  'تاریخچه NLP',
  'کاربردهای پردازش زبان طبیعی',
  'چالش‌های NLP برای زبان فارسی',
  'معماری سیستم‌های NLP',
  'پایپ‌لاین پردازش متن',
  'پیش‌پردازش متن فارسی',
  'نرمالایز کردن متن',
  'توکنایز کردن متن فارسی',
  'ریشه‌یابی کلمات فارسی',
  'حذف استاپ‌وردهای فارسی',
  'تشخیص بخش‌های گفتار',
  'تحلیل نحوی جمله',
  'تشخیص موجودیت‌های نام‌دار',
  'تحلیل وابستگی‌های نحوی',
  'تشخیص مرجع ضمیر',
  'استخراج روابط معنایی',
  'تشخیص احساسات متن',
  'تشخیص لحن متن',
  'تشخیص موضوع متن',
  'مدل‌های زبانی آماری',
  'مدل‌های n-gram',
  'مدل‌های زبانی عصبی',
  'Word Embeddings چیست؟',
  'Word2Vec برای فارسی',
  'GloVe برای زبان فارسی',
  'FastText و کاربردهای آن',
  'BERT و انقلاب در NLP',
  'معماری ترنسفورمر',
  'آشنایی با GPT',
  'RoBERTa و بهبودهای آن',
  'مدل‌های چندزبانه',
  'XLM-RoBERTa',
  'mBERT برای فارسی',
  'مدل‌های تولید متن',
  'T5: Text-to-Text Transfer',
  'BART برای خلاصه‌سازی',
  'دسته‌بندی متن فارسی',
  'کلاسیفایرهای متنی',
  'SVM برای طبقه‌بندی متن',
  'شبکه‌های عصبی برای NLP',
  'LSTM برای پردازش توالی',
  'GRU و کاربردهای آن',
  'شبکه‌های کانوولوشنی برای متن',
  'ترکیب CNN و LSTM',
  'آشنایی با Hugging Face',
  'استفاده از Transformers',
  'پایپ‌لاین Hugging Face',
  'تولید دیتاست فارسی',
  'نشانه‌گذاری دیتاست'
];

// تولید محتوای مقاله
function generateArticleContent(topic, id) {
  return `مقاله شماره ${id} با موضوع "${topic}"

## مقدمه
پردازش زبان طبیعی (Natural Language Processing) یا NLP، شاخه‌ای از هوش مصنوعی است که به تعامل بین کامپیوتر و زبان انسان می‌پردازد.

## اهمیت ${topic}
اهمیت "${topic}" در کاربردهای عملی آن نهفته است. از این تکنولوژی در موارد زیر استفاده می‌شود:
1. سیستم‌های جستجوی هوشمند
2. دستیارهای مجازی
3. تحلیل احساسات
4. ترجمه ماشینی
5. خلاصه‌سازی خودکار

## نتیجه‌گیری
"${topic}" فرصت‌های زیادی را برای محققان و توسعه‌دهندگان ایجاد کرده است.

---
*این مقاله توسط سیستم نطق مصطلح تولید شده است.*`;
}

// تولید slug
function generateSlug(text) {
  return text
    .replace(/[^\u0600-\u06FF\w\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .replace(/--+/g, '-')
    .toLowerCase();
}

// ایجاد دیتابیس SQLite با دستور sqlite3
async function createDatabase() {
  console.log('🌱 شروع تولید ۵۰ مقاله NLP فارسی...');
  
  const dbPath = path.join(__dirname, '../data/natiq.db');
  const dataDir = path.dirname(dbPath);
  
  // ایجاد پوشه data اگر وجود ندارد
  if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir, { recursive: true });
  }
  
  // حذف دیتابیس قبلی
  if (fs.existsSync(dbPath)) {
    fs.unlinkSync(dbPath);
  }
  
  try {
    // ایجاد دیتابیس و جداول با دستورات SQLite
    const sqlCommands = `
      -- ایجاد جدول مقالات
      CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        content TEXT NOT NULL,
        excerpt TEXT,
        author TEXT DEFAULT 'تیم نطق مصطلح',
        category TEXT,
        tags TEXT DEFAULT '[]',
        views INTEGER DEFAULT 0,
        likes INTEGER DEFAULT 0,
        shares INTEGER DEFAULT 0,
        featured BOOLEAN DEFAULT 0,
        status TEXT DEFAULT 'published',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
      
      -- ایجاد ایندکس‌ها
      CREATE INDEX idx_articles_status ON articles(status);
      CREATE INDEX idx_articles_category ON articles(category);
      CREATE INDEX idx_articles_created ON articles(created_at DESC);
    `;
    
    // ذخیره دستورات SQL در یک فایل موقت
    const tempSqlFile = path.join(__dirname, 'temp_create.sql');
    fs.writeFileSync(tempSqlFile, sqlCommands);
    
    // اجرای دستورات SQL
    execSync(`sqlite3 ${dbPath} < ${tempSqlFile}`);
    
    // حذف فایل موقت
    fs.unlinkSync(tempSqlFile);
    
    console.log('✅ دیتابیس ایجاد شد');
    
    // درج مقالات
    const categories = ['آموزش', 'پروژه', 'تحلیل', 'اخبار', 'کتابخانه', 'توسعه'];
    
    for (let i = 0; i < 50; i++) {
      const topic = NLP_TOPICS[i % NLP_TOPICS.length];
      const title = topic;
      const content = generateArticleContent(topic, i + 1);
      const slug = generateSlug(title);
      const excerpt = content.substring(0, 100) + '...';
      const category = categories[i % categories.length];
      const views = Math.floor(Math.random() * 1000) + 100;
      const likes = Math.floor(Math.random() * 500) + 10;
      const shares = Math.floor(Math.random() * 100) + 5;
      const featured = i % 10 === 0 ? 1 : 0;
      
      // ایجاد فایل SQL برای درج هر مقاله
      const insertSql = `INSERT INTO articles (title, slug, content, excerpt, category, views, likes, shares, featured) VALUES ('${title.replace(/'/g, "''")}', '${slug}', '${content.replace(/'/g, "''")}', '${excerpt.replace(/'/g, "''")}', '${category}', ${views}, ${likes}, ${shares}, ${featured});`;
      const tempInsertFile = path.join(__dirname, 'temp_insert.sql');
      fs.writeFileSync(tempInsertFile, insertSql);
      
      // اجرای دستور درج
      execSync(`sqlite3 ${dbPath} < ${tempInsertFile}`);
      fs.unlinkSync(tempInsertFile);
      
      if ((i + 1) % 10 === 0) {
        console.log(`📝 تولید مقاله ${i + 1} از ۵۰`);
      }
    }
    
    // نمایش آمار
    const statsCommand = `SELECT COUNT(*) as count FROM articles;`;
    const tempStatsFile = path.join(__dirname, 'temp_stats.sql');
    fs.writeFileSync(tempStatsFile, statsCommand);
    
    const result = execSync(`sqlite3 ${dbPath} < ${tempStatsFile}`).toString();
    fs.unlinkSync(tempStatsFile);
    
    console.log(`
✅ تولید داده‌ها کامل شد!
📊 تعداد مقالات: ${result.trim()} مقاله
📁 مسیر دیتابیس: ${dbPath}
    
🎉 سیستم آماده است! دستور زیر را اجرا کنید:
    
    node src/server/simple-app.js
    `);
    
  } catch (error) {
    console.error('❌ خطا در تولید داده‌ها:', error);
  }
}

// اجرای اسکریپت
createDatabase();
