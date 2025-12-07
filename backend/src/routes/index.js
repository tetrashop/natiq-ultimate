/**
 * 🛣️ مسیرهای API
 */

const express = require('express');
const router = express.Router();

// کنترلرها
const ArticleController = require('../controllers/articleController');

// میدلورها
const ErrorMiddleware = require('../middleware/errorMiddleware');

// مسیرهای مقالات
const articleController = new ArticleController();

// لیست مقالات
router.get('/articles', 
  ErrorMiddleware.asyncErrorHandler(articleController.getAll.bind(articleController))
);

// یک مقاله خاص
router.get('/articles/:id',
  ErrorMiddleware.asyncErrorHandler(articleController.getOne.bind(articleController))
);

// جستجو
router.get('/articles/search',
  ErrorMiddleware.asyncErrorHandler(articleController.search.bind(articleController))
);

// آمار
router.get('/stats',
  ErrorMiddleware.asyncErrorHandler(articleController.getStats.bind(articleController))
);

// سلامت سیستم
router.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'natiq-api',
    version: '3.0.0',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    articles: 199
  });
});

module.exports = router;
