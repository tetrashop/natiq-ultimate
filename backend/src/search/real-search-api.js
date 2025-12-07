/**
 * 🌐 API جستجوی واقعی
 */

const RealSearchEngine = require('./real-search-engine');

class RealSearchAPI {
    constructor(articles) {
        this.searchEngine = new RealSearchEngine(articles);
        this.searchHistory = [];
        this.popularQueries = new Map();
        
        console.log('🔍 API جستجوی واقعی راه‌اندازی شد');
    }
    
    // جستجوی عمومی
    search(query, options = {}) {
        if (!query || query.trim().length < 2) {
            return {
                success: false,
                error: 'عبارت جستجو باید حداقل ۲ کاراکتر باشد',
                query: query
            };
        }
        
        const searchResult = this.searchEngine.search(query, options);
        
        const enhancedResults = searchResult.results.map(result => {
            const article = this.getArticleById(result.articleId);
            if (!article) return null;
            
            return {
                article: article,
                score: result.score,
                relevance: this.calculateRelevance(result.score)
            };
        }).filter(Boolean);
        
        return {
            success: true,
            query: query,
            totalResults: enhancedResults.length,
            searchTime: searchResult.searchTime,
            inference: searchResult.inference,
            results: enhancedResults
        };
    }
    
    // دریافت مقاله بر اساس ID
    getArticleById(id) {
        return this.searchEngine.articles.find(a => a.id === id);
    }
    
    // محاسبه میزان ارتباط
    calculateRelevance(score) {
        if (score > 50) return 'خیلی زیاد';
        if (score > 30) return 'زیاد';
        if (score > 15) return 'متوسط';
        if (score > 5) return 'کم';
        return 'خیلی کم';
    }
    
    // دریافت آمار (متد جدید)
    getStats() {
        const engineStats = this.searchEngine.getStats();
        
        return {
            engine: engineStats,
            history: {
                totalSearches: this.searchHistory.length,
                uniqueQueries: this.popularQueries.size
            }
        };
    }
    
    // ثبت جستجو
    recordSearch(query) {
        const timestamp = new Date().toISOString();
        this.searchHistory.unshift({
            query: query,
            timestamp: timestamp,
            count: 1
        });
        
        if (this.searchHistory.length > 100) {
            this.searchHistory = this.searchHistory.slice(0, 50);
        }
        
        const currentCount = this.popularQueries.get(query) || 0;
        this.popularQueries.set(query, currentCount + 1);
    }
}

module.exports = RealSearchAPI;
