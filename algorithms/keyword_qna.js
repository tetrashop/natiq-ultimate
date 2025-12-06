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
