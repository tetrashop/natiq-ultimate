// الگوریتم ساده NLP
module.exports = class SimpleNLP {
    constructor(articles) {
        this.articles = articles;
    }
    
    async processQuestion(question, articles) {
        console.log(`💬 پردازش NLP: "${question}"`);
        
        // از articles پارامتر استفاده می‌کنیم
        const searchArticles = articles || this.articles;
        
        // تحلیل ساده سوال
        const isQuestion = question.includes('؟') || 
                          question.includes('چیست') || 
                          question.includes('چگونه') || 
                          question.includes('چرا');
        
        // استخراج موضوع اصلی
        const words = question
            .replace(/[؟?]/g, '')
            .split(' ')
            .filter(word => word.length > 2);
        
        const topic = words.length > 0 ? words[0] : 'موضوع';
        
        // جستجو
        const matches = [];
        for (const article of searchArticles) {
            const relevance = this.calculateRelevance(question, article);
            if (relevance > 0) {
                matches.push({ article, relevance });
            }
        }
        
        matches.sort((a, b) => b.relevance - a.relevance);
        
        if (matches.length === 0) {
            return {
                success: false,
                answer: `در مورد "${topic}" اطلاعاتی در مقالات موجود نیست.`,
                isQuestion: isQuestion,
                topic: topic
            };
        }
        
        // ساخت پاسخ
        const topMatch = matches[0];
        const answer = `در مورد "${topic}":\n\n${topMatch.article.excerpt || 'اطلاعات بیشتری موجود نیست.'}\n\nاین اطلاعات از مقاله "${topMatch.article.title}" استخراج شده است.`;
        
        return {
            success: true,
            answer: answer,
            topic: topic,
            matchedArticle: topMatch.article.title,
            articlesFound: matches.length,
            relevance: topMatch.relevance,
            confidence: Math.min(100, topMatch.relevance * 10),
            algorithm: 'simple_nlp',
            isQuestion: isQuestion
        };
    }
    
    calculateRelevance(question, article) {
        let score = 0;
        const qLower = question.toLowerCase();
        const titleLower = article.title.toLowerCase();
        const excerptLower = article.excerpt.toLowerCase();
        
        // تطابق کلمات
        const words = qLower.split(' ').filter(w => w.length > 2);
        for (const word of words) {
            if (titleLower.includes(word)) score += 5;
            if (excerptLower.includes(word)) score += 3;
            if (article.content.toLowerCase().includes(word)) score += 1;
        }
        
        // امتیاز برای مقالات با عنوان مناسب
        if (qLower.includes('چیست') && titleLower.includes('چیست')) {
            score += 10;
        }
        
        if (qLower.includes('چگونه') && titleLower.includes('چگونه')) {
            score += 10;
        }
        
        return score;
    }
}
