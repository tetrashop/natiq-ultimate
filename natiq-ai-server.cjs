const http = require('http');
const fs = require('fs');
const NatiqAI = require('./ai-features.js');

const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
const ai = new NatiqAI();

const server = http.createServer(async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // جستجوی هوشمند با AI
    if (req.url.startsWith('/api/ai/search')) {
        const query = new URL(req.url, 'http://localhost:3000').searchParams.get('q');
        
        // بهبود query با AI
        const improvedQuery = await ai.improveSearchQuery(query);
        
        // جستجوی معنایی
        const semanticResults = await semanticSearch(query);
        
        // جستجوی متنی معمولی
        const textResults = articles.filter(a => 
            a.title.includes(query) || 
            a.content.includes(query)
        );
        
        // ترکیب نتایج
        const allResults = [...semanticResults, ...textResults];
        const uniqueResults = removeDuplicates(allResults);
        
        res.end(JSON.stringify({
            success: true,
            originalQuery: query,
            improvedQuery: improvedQuery,
            results: uniqueResults.slice(0, 20),
            searchType: 'hybrid_ai'
        }, null, 2));
    }
    
    // تحلیل مقاله با AI
    if (req.url.startsWith('/api/ai/analyze')) {
        const id = parseInt(req.url.split('/').pop());
        const article = articles.find(a => a.id === id);
        
        if (article) {
            const analysis = await ai.analyzeText(article.content);
            
            res.end(JSON.stringify({
                success: true,
                article: article,
                ai_analysis: {
                    keywords: analysis.keywords,
                    summary: analysis.summary,
                    difficulty: analysis.difficulty,
                    suggested_tags: analysis.tags
                }
            }, null, 2));
        }
    }
});

server.listen(3001, () => {
    console.log('🤖 سرور هوشمند نطق مصطلح روی پورت 3001');
});
