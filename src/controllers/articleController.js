/**
 * 🎮 کنترلر مقالات
 */

class ArticleController {
  async getAll(req, res) {
    try {
      const db = req.db.db;
      const page = parseInt(req.query.page) || 1;
      const limit = parseInt(req.query.limit) || 12;
      const offset = (page - 1) * limit;
      
      // دریافت مقالات
      const articles = db.prepare(`
        SELECT * FROM articles 
        WHERE status = 'published' 
        ORDER BY created_at DESC 
        LIMIT ? OFFSET ?
      `).all(limit, offset);
      
      // تعداد کل
      const totalResult = db.prepare(`
        SELECT COUNT(*) as total FROM articles WHERE status = 'published'
      `).get();
      
      const total = totalResult.total;
      const totalPages = Math.ceil(total / limit);
      
      res.json({
        success: true,
        data: articles,
        pagination: {
          page,
          limit,
          total,
          pages: totalPages,
          has_next: page < totalPages,
          has_prev: page > 1
        }
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: 'خطا در دریافت مقالات'
      });
    }
  }
  
  async getOne(req, res) {
    try {
      const db = req.db.db;
      const { id } = req.params;
      
      const article = db.prepare('SELECT * FROM articles WHERE id = ?').get(id);
      
      if (!article) {
        return res.status(404).json({
          success: false,
          error: 'مقاله یافت نشد'
        });
      }
      
      // افزایش بازدید
      db.prepare('UPDATE articles SET views = views + 1 WHERE id = ?').run(id);
      
      res.json({
        success: true,
        data: article
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: 'خطا در دریافت مقاله'
      });
    }
  }
  
  async search(req, res) {
    try {
      const db = req.db.db;
      const { q } = req.query;
      
      if (!q || q.length < 2) {
        return res.status(400).json({
          success: false,
          error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد'
        });
      }
      
      const articles = db.prepare(`
        SELECT * FROM articles 
        WHERE status = 'published' 
        AND (title LIKE ? OR content LIKE ?)
        ORDER BY created_at DESC
        LIMIT 20
      `).all(`%${q}%`, `%${q}%`);
      
      res.json({
        success: true,
        data: articles,
        query: q
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: 'خطا در جستجو'
      });
    }
  }
  
  async getStats(req, res) {
    try {
      const db = req.db.db;
      
      const stats = db.prepare(`
        SELECT 
          COUNT(*) as total_articles,
          SUM(views) as total_views,
          SUM(likes) as total_likes,
          SUM(shares) as total_shares
        FROM articles 
        WHERE status = 'published'
      `).get();
      
      res.json({
        success: true,
        data: stats
      });
    } catch (error) {
      res.status(500).json({
        success: false,
        error: 'خطا در دریافت آمار'
      });
    }
  }
}

module.exports = ArticleController;
