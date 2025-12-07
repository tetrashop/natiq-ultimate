class NatiqAI {
    constructor() {
        this.apiKey = process.env.OPENROUTER_API_KEY;
        this.baseURL = 'https://openrouter.ai/api/v1';
    }
    
    async analyzeText(text) {
        const response = await fetch(`${this.baseURL}/chat/completions`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.apiKey}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                model: 'meta-llama/llama-3.1-8b-instruct:free',
                messages: [
                    {
                        role: 'user',
                        content: `این متن را تحلیل کن و کلیدواژه‌های اصلی را استخراج کن:\n${text}`
                    }
                ]
            })
        });
        
        return await response.json();
    }
    
    async improveSearchQuery(query) {
        // بهبود query جستجو
        const prompt = `
        query اصلی: ${query}
        معادل‌های بهتر برای جستجوی مقالات فارسی NLP:
        `;
        
        return await this.callAI(prompt);
    }
}

module.exports = NatiqAI;
