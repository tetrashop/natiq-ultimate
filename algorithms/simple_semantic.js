// الگوریتم ساده معنایی
module.exports = class SimpleSemantic {
    constructor(articles) {
        this.articles = articles;
        this.questionPatterns = {
            'چیست': 'definition',
            'چگونه': 'howto',
            'چرا': 'reason',
            'تفاوت': 'comparison',
            'مزایا': 'advantages',
            'معایب': 'disadvantages'
        };
    }
    
    async processQuestion(question) {
        console.log(`🧠 پردازش معنایی: "${question}"`);
        
        // تشخیص نوع سوال
        let questionType = 'general';
        for (const [pattern, type] of Object.entries(this.questionPatterns)) {
            if (question.includes(pattern)) {
                questionType = type;
                break;
            }
        }
        
        // استخراج کلمات کلیدی
        const keywords = question
            .toLowerCase()
            .replace(/[^\u0600-\u06FF\s]/g, '')
            .split(/\s+/)
            .filter(word => word.length > 2 && !['چیست', 'چگونه', 'چرا', 'تفاوت'].includes(word));
        
        // جستجوی مقالات
        const matches = [];
        for (const article of this.articles) {
            let score = 0;
            const text = (article.title + ' ' + article.excerpt + ' ' + article.content).toLowerCase();
            
            for (const keyword of keywords) {
                if (text.includes(keyword)) {
                    score += 3;
                }
            }
            
            // امتیاز بر اساس نوع سوال
            if (questionType === 'definition' && article.content.toLowerCase().includes('تعریف')) {
                score += 10;
            }
            
            if (score > 0) {
                matches.push({ article, score, questionType });
            }
        }
        
        matches.sort((a, b) => b.score - a.score);
        
        if (matches.length === 0) {
            return {
                success: false,
                answer: `پاسخی برای سوال "${question}" یافت نشد.`,
                questionType: questionType,
                keywords: keywords
            };
        }
        
        // ساخت پاسخ بر اساس نوع سوال
        const topMatch = matches[0];
        let answer = '';
        
        switch (questionType) {
            case 'definition':
                answer = `در تعریف "${keywords[0] || 'موضوع'}":\n\n${topMatch.article.excerpt || 'تعریف دقیقی یافت نشد.'}`;
                break;
            case 'howto':
                answer = `برای "${keywords[0] || 'این کار'}":\n\n${topMatch.article.excerpt || 'راهنمایی یافت نشد.'}`;
                break;
            default:
                answer = `در پاسخ به سوال شما:\n\n${topMatch.article.excerpt || 'پاسخ دقیقی یافت نشد.'}`;
        }
        
        return {
            success: true,
            answer: answer,
            questionType: questionType,
            matchedArticle: topMatch.article.title,
            articlesFound: matches.length,
            confidence: Math.min(100, topMatch.score * 15),
            algorithm: 'simple_semantic'
        };
    }
}
