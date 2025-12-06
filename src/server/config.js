/**
 * ⚙️ تنظیمات سیستم
 */

const path = require('path');

const config = {
  // محیط اجرا
  env: process.env.NODE_ENV || 'development',
  
  // پورت سرور
  port: process.env.PORT || 3001,
  
  // لاگ‌گیری
  logLevel: process.env.LOG_LEVEL || 'info',
  
  // CORS
  cors: {
    origin: process.env.NODE_ENV === 'development' ? '*' : [
      'https://natiq.ir',
      'https://www.natiq.ir'
    ],
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    exposedHeaders: ['X-Total-Count']
  },
  
  // دیتابیس
  database: {
    path: path.join(__dirname, '../../data/natiq.db'),
    verbose: process.env.NODE_ENV === 'development',
    pragmas: {
      journal_mode: 'WAL',
      synchronous: 'NORMAL',
      cache_size: -2000,
      temp_store: 'MEMORY',
      foreign_keys: 'ON',
      busy_timeout: 5000
    }
  },
  
  // محدودیت درخواست
  rateLimit: {
    windowMs: 15 * 60 * 1000, // 15 دقیقه
    max: 100 // 100 درخواست
  },
  
  // کش
  cache: {
    ttl: 300, // 5 دقیقه
    maxKeys: 1000
  }
};

module.exports = config;
