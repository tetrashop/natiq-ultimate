/**
 * 🗄️ مدیریت دیتابیس SQLite
 */

const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

class NatiqDatabase {
  constructor(config) {
    this.config = config;
    this.db = null;
  }
  
  async init() {
    try {
      // ایجاد پوشه data اگر وجود ندارد
      const dataDir = path.dirname(this.config.path);
      if (!fs.existsSync(dataDir)) {
        fs.mkdirSync(dataDir, { recursive: true });
      }
      
      // اتصال به دیتابیس
      this.db = new Database(this.config.path, {
        verbose: this.config.verbose ? console.log : null
      });
      
      // تنظیم پراگماهای بهینه‌سازی
      this.setPragmas();
      
      // ایجاد جداول
      this.createTables();
      
      // ایجاد ایندکس‌ها
      this.createIndexes();
      
      console.log('✅ دیتابیس راه‌اندازی شد');
      return this;
    } catch (error) {
      console.error('❌ خطا در راه‌اندازی دیتابیس:', error);
      throw error;
    }
  }
  
  setPragmas() {
    const pragmas = this.config.pragmas;
    Object.entries(pragmas).forEach(([key, value]) => {
      this.db.pragma(`${key} = ${value}`);
    });
  }
  
  createTables() {
    // جدول مقالات
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        content TEXT NOT NULL,
        excerpt TEXT,
        author TEXT DEFAULT 'تیم نطق مصطلح',
        category TEXT DEFAULT 'عمومی',
        tags TEXT DEFAULT '[]',
        views INTEGER DEFAULT 0,
        likes INTEGER DEFAULT 0,
        shares INTEGER DEFAULT 0,
        featured BOOLEAN DEFAULT 0,
        status TEXT DEFAULT 'published',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        published_at TIMESTAMP
      )
    `);
    
    // جدول دسته‌بندی‌ها
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        description TEXT,
        article_count INTEGER DEFAULT 0
      )
    `);
    
    // جدول آمار
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE UNIQUE NOT NULL,
        total_articles INTEGER DEFAULT 0,
        total_views INTEGER DEFAULT 0,
        total_likes INTEGER DEFAULT 0
      )
    `);
  }
  
  createIndexes() {
    // ایندکس‌های مقالات
    this.db.exec(`
      CREATE INDEX IF NOT EXISTS idx_articles_status ON articles(status);
      CREATE INDEX IF NOT EXISTS idx_articles_category ON articles(category);
      CREATE INDEX IF NOT EXISTS idx_articles_created ON articles(created_at DESC);
      CREATE INDEX IF NOT EXISTS idx_articles_views ON articles(views DESC);
      CREATE INDEX IF NOT EXISTS idx_articles_featured ON articles(featured);
    `);
  }
  
  // آماده‌سازی کوئری‌های پرکاربرد
  prepareStatements() {
    this.statements = {
      getArticleById: this.db.prepare('SELECT * FROM articles WHERE id = ?'),
      getArticlesPaginated: this.db.prepare(`
        SELECT * FROM articles 
        WHERE status = 'published' 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
      `),
      getArticlesCount: this.db.prepare(`
        SELECT COUNT(*) as count FROM articles WHERE status = 'published'
      `)
    };
  }
  
  close() {
    if (this.db) {
      this.db.close();
      console.log('🔒 دیتابیس بسته شد');
    }
  }
  
  // متدهای کمکی
  async isDatabaseEmpty() {
    const result = this.db.prepare('SELECT COUNT(*) as count FROM articles').get();
    return result.count === 0;
  }
}

module.exports = NatiqDatabase;
