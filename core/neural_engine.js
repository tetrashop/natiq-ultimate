/**
 * الگوریتم ترکیبی با یادگیری تقویتی
 * مسیر: ~/natiq-ultimate/algorithms/hybrid_qna.js
 * 
 * این الگوریتم از ترکیب چند روش و یادگیری از بازخورد کاربران استفاده می‌کند.
 */

class HybridQnA {
    constructor(articles) {
        this.articles = articles;
        this.feedbackLog = [];
        this.algorithmPerformance = {
            keyword: { correct: 0, total: 0 },
            semantic: { correct: 0, total: 0 },
            hybrid: { correct: 0, total: 0 }
        };
    }

    /**
     * یادگیری از بازخورد کاربران
     */
    learnFromFeedback(feedback) {
        this.feedbackLog.push({
            ...feedback,
            timestamp: new Date().toISOString()
        });

        // به‌روزرسانی عملکرد الگوریتم‌ها
        if (feedback.algorithm && feedback.correct !== undefined) {
            if (this.algorithmPerformance[feedback.algorithm]) {
                this.algorithmPerformance[feedback.algorithm].total++;
                if (feedback.correct) {
                    this.algorithmPerformance[feedback.algorithm].correct++;
                }
            }
        }

        // ذخیره لاگ یادگیری
        if (this.feedbackLog.length % 10 === 0) {
            this.saveLearningData();
        }
    }

    /**
     * محاسبه امتیاز الگوریتم‌ها
     */
    calculateAlgorithmScores() {
        const scores = {};
        
        for (const [algo, perf] of Object.entries(this.algorithmPerformance)) {
            if (perf.total > 0) {
                scores[algo] = (perf.correct / perf.total) * 100;
            } else {
                scores[algo] = 50; // امتیاز اولیه
            }
        }
        
        return scores;
    }

    /**
     * ترکیب نتایج الگوریتم‌های مختلف
     */
    async combineAlgorithmsResults(question, keywordResult, semanticResult) {
        const algorithmScores = this.calculateAlgorithmScores();
        
        // وزن‌دهی بر اساس عملکرد تاریخی
        const keywordWeight = algorithmScores.keyword / 100;
        const semanticWeight = algorithmScores.semantic / 100;
        
        // ارزیابی هر نتیجه
        const keywordScore = this.evaluateResult(keywordResult);
        const semanticScore = this.evaluateResult(semanticResult);
        
        // محاسبه امتیاز نهایی
        const finalScore = (keywordScore * keywordWeight) + (semanticScore * semanticWeight);
        
        // انتخاب بهترین پاسخ
        let bestResult;
        if (keywordScore * keywordWeight >= semanticScore * semanticWeight) {
            bestResult = keywordResult;
        } else {
            bestResult = semanticResult;
        }

        // بهبود پاسخ با اطلاعات اضافی
        const improvedAnswer = await this.enhanceAnswer(bestResult, question);

        return {
            ...improvedAnswer,
            confidence: finalScore,
            algorithm: 'Hybrid QnA',
            componentScores: {
                keyword: keywordScore,
                semantic: semanticScore,
                final: finalScore
            },
            usedAlgorithms: {
                keyword: keywordResult.success,
                semantic: semanticResult.success
            }
        };
    }

    /**
     * ارزیابی کیفیت یک پاسخ
     */
    evaluateResult(result) {
        if (!result.success) return 0;
        
        let score = 0;
        
        // طول پاسخ مناسب (نه خیلی کوتاه، نه خیلی طولانی)
        const answerLength = result.answer ? result.answer.length : 0;
        if (answerLength > 100 && answerLength < 1000) {
            score += 30;
        } else if (answerLength > 50) {
            score += 20;
        }
        
        // وجود کلیدواژه‌های مرتبط
        if (result.keywords && result.keywords.length > 0) {
            score += Math.min(30, result.keywords.length * 5);
        }
        
        // تعداد مقالات یافت شده
        if (result.articlesFound > 0) {
            score += Math.min(40, result.articlesFound * 10);
        }
        
        return Math.min(100, score);
    }

    /**
     * بهبود پاسخ با اطلاعات تکمیلی
     */
    async enhanceAnswer(baseResult, question) {
        let enhancedAnswer = baseResult.answer;
        
        // اضافه کردن مقدمه
        enhancedAnswer = `سوال شما: "${question}"\n\n` + enhancedAnswer;
        
        // اضافه کردن منابع بیشتر در صورت نیاز
        if (baseResult.articlesFound < 2) {
            const additionalArticles = await this.findAdditionalResources(question);
            if (additionalArticles.length > 0) {
                enhancedAnswer += `\n\n📚 مقالات مرتبط دیگر:\n`;
                additionalArticles.forEach((article, idx) => {
                    enhancedAnswer += `${idx + 1}. ${article.title}\n`;
                });
            }
        }
        
        // اضافه کردن پیوند به مقالات
        enhancedAnswer += `\n🔗 برای اطلاعات بیشتر می‌توانید مقالات کامل را در سایت مطالعه کنید.`;
        
        return {
            ...baseResult,
            answer: enhancedAnswer,
            enhanced: true
        };
    }

    /**
     * یافتن منابع اضافی
     */
    async findAdditionalResources(question) {
        // استخراج کلیدواژه‌ها
        const keywords = question
            .toLowerCase()
            .replace(/[^\u0600-\u06FF\s]/g, '')
            .split(/\s+/)
            .filter(word => word.length > 2);
        
        const additional = [];
        
        for (const article of this.articles) {
            const title = article.title.toLowerCase();
            let matchCount = 0;
            
            for (const keyword of keywords) {
                if (title.includes(keyword)) {
                    matchCount++;
                }
            }
            
            if (matchCount > 0) {
                additional.push({
                    article,
                    matchCount
                });
            }
        }
        
        return additional
            .sort((a, b) => b.matchCount - a.matchCount)
            .slice(0, 3)
            .map(item => item.article);
    }

    /**
     * پردازش اصلی سوال
     */
    async processQuestion(question) {
        try {
            // اجرای الگوریتم‌های مختلف به صورت موازی
            const [keywordResult, semanticResult] = await Promise.all([
                this.runKeywordAlgorithm(question),
                this.runSemanticAlgorithm(question)
            ]);

            // ترکیب نتایج
            const finalResult = await this.combineAlgorithmsResults(
                question, 
                keywordResult, 
                semanticResult
            );

            // ذخیره در لاگ برای یادگیری
            this.learnFromFeedback({
                question,
                algorithmsUsed: ['keyword', 'semantic'],
                chosenAlgorithm: 'hybrid',
                confidence: finalResult.confidence,
                timestamp: new Date().toISOString()
            });

            return finalResult;

        } catch (error) {
            return {
                success: false,
                answer: "خطا در پردازش سوال با الگوریتم ترکیبی.",
                error: error.message,
                algorithm: "Hybrid QnA",
                confidence: 0
            };
        }
    }

    /**
     * اجرای الگوریتم کلیدواژه
     */
    async runKeywordAlgorithm(question) {
        // شبیه‌سازی اجرای الگوریتم کلیدواژه
        // در عمل باید ماژول واقعی را فراخوانی کنیم
        return {
            success: true,
            answer: "پاسخ از الگوریتم کلیدواژه",
            keywords: ['test'],
            articlesFound: 2,
            algorithm: "keyword"
        };
    }

    /**
     * اجرای الگوریتم معنایی
     */
    async runSemanticAlgorithm(question) {
        // شبیه‌سازی اجرای الگوریتم معنایی
        return {
            success: true,
            answer: "پاسخ از الگوریتم معنایی",
            keywords: ['test'],
            articlesFound: 3,
            algorithm: "semantic"
        };
    }

    /**
     * ذخیره داده‌های یادگیری
     */
    saveLearningData() {
        const learningData = {
            algorithmPerformance: this.algorithmPerformance,
            feedbackLog: this.feedbackLog.slice(-100), // آخرین ۱۰۰ بازخورد
            lastUpdated: new Date().toISOString()
        };
        
        // در عمل باید در فایل ذخیره شود
        console.log('داده‌های یادگیری به‌روز شدند.');
        return learningData;
    }

    /**
     * دریافت گزارش عملکرد
     */
    getPerformanceReport() {
        const scores = this.calculateAlgorithmScores();
        const totalQuestions = Object.values(this.algorithmPerformance)
            .reduce((sum, perf) => sum + perf.total, 0);
        
        return {
            totalQuestionsProcessed: totalQuestions,
            algorithmScores: scores,
            bestAlgorithm: Object.keys(scores).reduce((a, b) => 
                scores[a] > scores[b] ? a : b
            ),
            feedbackCount: this.feedbackLog.length,
            lastFeedback: this.feedbackLog[this.feedbackLog.length - 1]
        };
    }
}

module.exports = HybridQnA;
class KeywordQnA {
    constructor(articles) { this.articles = articles; }
    
    async answerQuestion(question) {
        return {
            success: true,
            answer: "این یک پاسخ تستی است. سیستم در حال توسعه است.",
            confidence: 75,
            algorithm: "keyword"
        };
    }
}
module.exports = KeywordQnA;
