// الگوریتم ساده مبتنی بر کلیدواژه
module.exports = class SimpleKeyword {
    constructor(articles) {
        this.articles = articles;
    }
    
    async answerQuestion(question) {
        console.log(`🔍 جستجو برای: "${question}"`);
        
        // استخراج کلمات کلیدی ساده
        const keywords = question
            .toLowerCase()
            .replace(/[^\u0600-\u06FF\s]/g, '')
            .split(/\s+/)
            .filter(word => word.length > 2);
        
        // جستجوی مقالات
        const matches = [];
        for (const article of this.articles) {
            let score = 0;
            const text = (article.title + ' ' + article.excerpt).toLowerCase();
            
            for (const keyword of keywords) {
                if (text.includes(keyword)) {
                    score++;
                }
            }
            
            if (score > 0) {
                matches.push({ article, score });
            }
        }
        
        // مرتب‌سازی بر اساس امتیاز
        matches.sort((a, b) => b.score - a.score);
        
        if (matches.length === 0) {
            return {
                success: false,
                answer: 'متاسفانه پاسخی برای سوال شما یافت نشد.',
                keywords: keywords
            };
        }
        
        // ساخت پاسخ
        const topMatch = matches[0];
        const answer = `بر اساس جستجو در مقالات، مقاله "${topMatch.article.title}" مرتبط ترین نتیجه است.\n\n${topMatch.article.excerpt}\n\nبرای مطالعه کامل مقاله، به صفحه مقاله مراجعه کنید.`;
        
        return {
            success: true,
            answer: answer,
            matchedArticle: topMatch.article.title,
            articlesFound: matches.length,
            confidence: Math.min(100, topMatch.score * 20),
            algorithm: 'simple_keyword'
        };
    }
}
