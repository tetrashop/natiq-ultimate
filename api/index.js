const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());

// فعال‌سازی CORS برای ارتباط با فرانت‌اند
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', '*');
    next();
});

// سرو فایل‌های استاتیک از پوشهٔ public (اولویت را از مسیر '/' می‌گیرد)
app.use(express.static(path.join(__dirname, '..', 'public')));

// مستندات سادهٔ API (حالا در مسیر /api)
app.get('/api', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '2.0.0',
        page: '218',
        status: 'فعال',
        endpoints: {
            health: '/api/health (GET)',
            process: '/api/process (POST)'
        }
    });
});

// سلامت سیستم
app.get('/api/health', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '2.0.0',
        page: '218',
        status: 'فعال',
        timestamp: new Date().toISOString()
    });
});

// تابع کمکی برای تحلیل پیشرفته‌تر متن فارسی
function analyzeText(text) {
    const words = text.split(/\s+/).filter(w => w.length > 0);
    const chars = text.replace(/\s/g, '').length;
    const sentences = text.split(/[.!?؟\n]+/).filter(s => s.trim().length > 0);

    let longestWord = '';
    let shortestWord = '';
    if (words.length > 0) {
        longestWord = words.reduce((a, b) => a.length > b.length ? a : b);
        shortestWord = words.reduce((a, b) => a.length < b.length ? a : b);
    }

    return {
        words: words.length,
        characters: chars,
        sentences: sentences.length,
        average_word_length: words.length > 0 ? Math.round((chars / words.length) * 10) / 10 : 0,
        longest_word: longestWord,
        shortest_word: shortestWord
    };
}

// پردازش متن (نسخه بهبودیافته)
app.post('/api/process', (req, res) => {
    try {
        const { text } = req.body;
        if (!text || typeof text !== 'string' || text.trim().length === 0) {
            return res.status(400).json({
                error: 'متن ورودی الزامی است و نمی‌تواند خالی باشد.',
                version: '2.0.0',
                page: '218'
            });
        }

        const analysis = analyzeText(text);
        res.json({
            success: true,
            version: '2.0.0',
            page: '218',
            analysis: analysis
        });
    } catch (error) {
        res.status(500).json({
            error: 'خطایی در پردازش متن رخ داد. لطفاً دوباره تلاش کنید.',
            version: '2.0.0',
            page: '218'
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`ناتیق روی پورت ${PORT} فعال است`));

module.exports = app;
