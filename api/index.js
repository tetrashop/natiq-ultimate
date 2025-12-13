const express = require('express');
const app = express();

app.use(express.json());

// CORS فعال‌سازی
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', '*');
    next();
});

// صفحه اصلی
app.get('/', (req, res) => {
    res.json({
        name: "ناتیق اولتیمیت",
        version: "2.0.0",
        page: "218",
        status: "فعال",
        endpoints: {
            health: "/api/health (GET)",
            process: "/api/process (POST)"
        }
    });
});

// سلامت سیستم
app.get('/api/health', (req, res) => {
    res.json({
        name: "ناتیق اولتیمیت",
        version: "2.0.0",
        page: "218",
        status: "فعال",
        timestamp: new Date().toISOString()
    });
});

// پردازش متن
app.post('/api/process', (req, res) => {
    try {
        const { text } = req.body;
        
        if (!text || typeof text !== 'string') {
            return res.status(400).json({
                error: "متن الزامی است",
                version: "2.0.0",
                page: "218"
            });
        }

        // پردازش ساده
        const words = text.split(/\s+/).filter(w => w.length > 0);
        const chars = text.replace(/\s/g, '').length;
        
        res.json({
            success: true,
            version: "2.0.0",
            page: "218",
            analysis: {
                words: words.length,
                characters: chars,
                average_word_length: words.length > 0 ? 
                    Math.round(chars / words.length) : 0
            }
        });
    } catch (error) {
        res.status(500).json({
            error: "خطا در پردازش",
            version: "2.0.0",
            page: "218"
        });
    }
});

module.exports = app;
