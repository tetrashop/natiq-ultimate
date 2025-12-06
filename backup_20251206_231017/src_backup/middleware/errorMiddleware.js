/**
 * ⚠️ مدیریت خطاها
 */

class ErrorMiddleware {
  static errorHandler(err, req, res, next) {
    console.error('❌ خطای سرور:', err);
    
    res.status(err.statusCode || 500).json({
      success: false,
      error: err.message || 'خطای داخلی سرور'
    });
  }
  
  static asyncErrorHandler(fn) {
    return (req, res, next) => {
      Promise.resolve(fn(req, res, next)).catch(next);
    };
  }
}

module.exports = ErrorMiddleware;
