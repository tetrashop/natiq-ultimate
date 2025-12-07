/**
 * 🚀 فایل اصلی سرور نطق مصطلح
 * نسخه ۳.۰.۰ - مدیریت ۱۹۹ مقاله NLP فارسی
 */

// بارگذاری متغیرهای محیطی
require('dotenv').config();

const express = require('express');
const helmet = require('helmet');
const cors = require('cors');
const compression = require('compression');
const path = require('path');
const pino = require('pino');

// لودرهای داخلی
const Database = require('../database/database');
const config = require('./config');

// ایجاد اپلیکیشن
const app = express();

// لاگر
const logger = pino({
  level: config.logLevel,
  transport: {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'HH:MM:ss',
      ignore: 'pid,hostname'
    }
  }
});

// میدلورهای امنیتی
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
      scriptSrc: ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"]
    }
  }
}));

app.use(cors(config.cors));
app.use(compression());
app.use(express.json({ limit: '1mb' }));
app.use(express.urlencoded({ extended: true }));

// فایل‌های استاتیک
app.use(express.static(path.join(__dirname, '../../public')));

// راه‌اندازی دیتابیس
const db = new Database(config.database);
db.init().then(() => {
  logger.info('✅ دیتابیس راه‌اندازی شد');
  
  // تزریق دیتابیس به request
  app.use((req, res, next) => {
    req.db = db;
    next();
  });
  
  // مسیرهای API
  const routes = require('../routes');
  app.use('/api', routes);
  
  // صفحه اصلی
  app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../../public/index.html'));
  });
  
  // خطای ۴۰۴ برای API
  app.use('/api/*', (req, res) => {
    res.status(404).json({
      success: false,
      error: 'مسیر API یافت نشد'
    });
  });
  
  // SPA routing
  app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, '../../public/index.html'));
  });
  
  // شروع سرور
  const server = app.listen(config.port, () => {
    logger.info(`
    🚀 ============================================
        نطق مصطلح - نسخه ۳.۰
    ============================================
    
    📍 آدرس: http://localhost:${config.port}
    📊 مقالات: ۱۹۹ مقاله NLP فارسی
    🗄️  دیتابیس: SQLite بهینه‌شده
    🔐 امنیت: چندلایه
    
    ✅ سیستم آماده استفاده است!
    ============================================
    `);
  });
  
  // مدیریت graceful shutdown
  process.on('SIGTERM', () => {
    logger.info('🛑 دریافت سیگنال خاموشی...');
    server.close(() => {
      db.close();
      logger.info('✅ سرور خاموش شد');
      process.exit(0);
    });
  });
  
}).catch((error) => {
  logger.error('❌ خطا در راه‌اندازی دیتابیس:', error);
  process.exit(1);
});

module.exports = app;
