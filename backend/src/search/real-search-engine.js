/**
 * 🔍 موتور جستجوی واقعی نطق مصطلح
 * جستجوی کامل متن در مقالات
 */

const fs = require('fs');
const path = require('path');

class RealSearchEngine {
    constructor(articles) {
        this.articles = articles || [];
        this.searchIndex = this.buildSearchIndex();
        this.invertedIndex = this.buildInvertedIndex();
        console.log(`✅ موتور جستجوی واقعی با ${this.articles.length} مقاله راه‌اندازی شد`);
    }
    
    // ساخت ایندکس جستجو
    buildSearchIndex() {
        console.log('🔨 در حال ساخت ایندکس جستجو...');
        const index = {};
        
        this.articles.forEach((article, idx) => {
            const searchableText = `
                ${article.title || ''}
                ${article.content || ''}
                ${article.excerpt || ''}
                ${article.category || ''}
                ${(article.tags || []).join(' ')}
                ${article.author || ''}
            `.toLowerCase().replace(/\s+/g, ' ');
            
            index[article.id] = {
                id: article.id,
                text: searchableText,
                title: article.title,
                category: article.category,
                tags: article.tags || [],
                boost: article.featured ? 1.5 : 1.0,
                views: article.views || 0,
                likes: article.likes || 0,
                date: article.created_at
            };
        });
        
        console.log(`✅ ایندکس جستجو ساخته شد (${Object.keys(index).length} مقاله)`);
        return index;
    }
    
    // ساخت ایندکس معکوس
    buildInvertedIndex() {
        console.log('🔨 در حال ساخت ایندکس معکوس...');
        const invertedIndex = {};
        
        Object.values(this.searchIndex).forEach(article => {
            const words = this.tokenize(article.text);
            const uniqueWords = [...new Set(words)];
            
            uniqueWords.forEach(word => {
                if (!invertedIndex[word]) {
                    invertedIndex[word] = [];
                }
                
                const tf = words.filter(w => w === word).length / words.length;
                
                invertedIndex[word].push({
                    articleId: article.id,
                    tf: tf,
                    positions: words.reduce((positions, w, idx) => {
                        if (w === word) positions.push(idx);
                        return positions;
                    }, [])
                });
            });
        });
        
        const totalDocs = Object.keys(this.searchIndex).length;
        Object.keys(invertedIndex).forEach(word => {
            const docFrequency = invertedIndex[word].length;
            const idf = Math.log(totalDocs / (1 + docFrequency));
            
            invertedIndex[word].forEach(entry => {
                entry.tfidf = entry.tf * idf;
            });
            
            invertedIndex[word].sort((a, b) => b.tfidf - a.tfidf);
        });
        
        console.log(`✅ ایندکس معکوس ساخته شد (${Object.keys(invertedIndex).length} کلمه کلیدی)`);
        return invertedIndex;
    }
    
    tokenize(text) {
        const cleaned = text.replace(/[^\u0600-\u06FF\s]/g, '');
        const words = cleaned.split(/\s+/).filter(word => {
            if (word.length < 2) return false;
            
            const stopWords = [
                'در', 'با', 'به', 'از', 'که', 'این', 'آن', 'را',
                'برای', 'و', 'یا', 'هم', 'یک', 'های', 'هایی',
                'است', 'بود', 'شود', 'می', 'شده', 'کرد', 'کرده',
                'باشد', 'هایش', 'کردند', 'دارد', 'خواهد', 'بر'
            ];
            
            return !stopWords.includes(word);
        });
        
        return words;
    }
    
    // ========== متدهای جدید اضافه شده ==========
    
    // اجرای جستجو
    executeSearch(queryTokens, options) {
        const results = new Map();
        
        queryTokens.forEach(token => {
            if (this.invertedIndex[token]) {
                this.invertedIndex[token].forEach(entry => {
                    const currentScore = results.get(entry.articleId) || 0;
                    let score = entry.tfidf * 10;
                    
                    const article = this.searchIndex[entry.articleId];
                    if (article.title.toLowerCase().includes(token)) {
                        score *= 1.5;
                    }
                    
                    if (article.tags.some(tag => tag.toLowerCase().includes(token))) {
                        score *= 1.3;
                    }
                    
                    results.set(entry.articleId, currentScore + score);
                });
            }
        });
        
        return Array.from(results.entries()).map(([articleId, score]) => ({
            articleId: parseInt(articleId),
            score: score
        }));
    }
    
    // اعمال فیلترها
    applyFilters(results, options) {
        return results.filter(result => {
            const article = this.searchIndex[result.articleId];
            if (!article) return false;
            
            // فیلتر دسته‌بندی
            if (options.category && article.category !== options.category) {
                return false;
            }
            
            // فیلتر حداقل بازدید
            if (options.minViews && article.views < options.minViews) {
                return false;
            }
            
            // فیلتر حداقل لایک
            if (options.minLikes && article.likes < options.minLikes) {
                return false;
            }
            
            return true;
        });
    }
    
    // مرتب‌سازی نتایج
    sortResults(results, options) {
        const sortBy = options.sortBy || 'relevance';
        
        return results.sort((a, b) => {
            const articleA = this.searchIndex[a.articleId];
            const articleB = this.searchIndex[b.articleId];
            
            switch (sortBy) {
                case 'views':
                    return articleB.views - articleA.views;
                case 'likes':
                    return articleB.likes - articleA.likes;
                case 'date':
                    return new Date(articleB.date) - new Date(articleA.date);
                case 'relevance':
                default:
                    if (b.score !== a.score) {
                        return b.score - a.score;
                    }
                    return articleB.views - articleA.views;
            }
        });
    }
    
    // تولید استنتاج
    generateInference(results, query, queryTokens) {
        if (results.length === 0) {
            return {
                summary: `هیچ مقاله‌ای با جستجوی "${query}" یافت نشد.`,
                suggestions: [
                    'کلمات جستجو را بررسی کنید',
                    'از کلمات کلیدی دقیق‌تر استفاده کنید'
                ]
            };
        }
        
        return {
            summary: `بر اساس جستجوی "${query}"، ${results.length} مقاله مرتبط یافت شد.`,
            insights: [
                `مقاله‌ها در دسته‌بندی‌های مختلف یافت شدند`
            ]
        };
    }
    
    // جستجوی اصلی
    search(query, options = {}) {
        const startTime = Date.now();
        
        if (!query || query.trim().length < 2) {
            return this.emptyResult(query, 'عبارت جستجو باید حداقل ۲ کاراکتر باشد');
        }
        
        const normalizedQuery = query.toLowerCase().trim();
        const queryTokens = this.tokenize(normalizedQuery);
        
        if (queryTokens.length === 0) {
            return this.emptyResult(query, 'هیچ کلمه کلیدی معتبری یافت نشد');
        }
        
        // اجرای جستجو
        const searchResults = this.executeSearch(queryTokens, options);
        
        // اعمال فیلترها
        const filteredResults = this.applyFilters(searchResults, options);
        
        // مرتب‌سازی نهایی
        const sortedResults = this.sortResults(filteredResults, options);
        
        // محدود کردن تعداد نتایج
        const limit = options.limit || 20;
        const finalResults = sortedResults.slice(0, limit);
        
        // تولید استنتاج
        const inference = this.generateInference(finalResults, query, queryTokens);
        
        return {
            query: query,
            totalResults: finalResults.length,
            totalMatches: searchResults.length,
            searchTime: `${Date.now() - startTime}ms`,
            queryTokens: queryTokens,
            inference: inference,
            results: finalResults
        };
    }
    
    // نتیجه خالی
    emptyResult(query, reason) {
        return {
            query: query,
            totalResults: 0,
            totalMatches: 0,
            searchTime: '0ms',
            queryTokens: [],
            inference: {
                summary: reason,
                suggestions: [
                    'عبارت جستجو را تغییر دهید',
                    'از کلمات کلیدی متفاوت استفاده کنید'
                ]
            },
            results: []
        };
    }
    
    // دریافت آمار (متد جدید)
    getStats() {
        const words = Object.keys(this.invertedIndex).length;
        const avgWordsPerArticle = words / this.articles.length;
        
        return {
            totalArticles: this.articles.length,
            totalIndexedWords: words,
            avgWordsPerArticle: avgWordsPerArticle.toFixed(1),
            categories: [...new Set(this.articles.map(a => a.category))].length,
            featuredArticles: this.articles.filter(a => a.featured).length
        };
    }
}

module.exports = RealSearchEngine;
