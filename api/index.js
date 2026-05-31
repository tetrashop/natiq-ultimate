const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());

// فعال‌سازی CORS
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', '*');
    next();
});

// سرو فایل‌های استاتیک
app.use(express.static(path.join(__dirname, '..', 'public')));

// مستندات API
app.get('/api', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '3.0.0',
        page: '218',
        status: 'فعال',
        endpoints: {
            health: '/api/health (GET)',
            process: '/api/process (POST)',
            deep: '/api/deep (POST)'
        }
    });
});

// سلامت سیستم
app.get('/api/health', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '3.0.0',
        page: '218',
        status: 'فعال',
        timestamp: new Date().toISOString()
    });
});

// تابع تحلیل پایه
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

// تحلیل عمیق
function deepAnalyze(text) {
    const words = text.split(/\s+/).filter(w => w.length > 0);
    const chars = text.replace(/\s/g, '').length;
    const sentences = text.split(/[.!?؟\n]+/).filter(s => s.trim().length > 0);

    const basic = analyzeText(text);

    // فراوانی کلمات
    const freqMap = {};
    words.forEach(w => {
        const clean = w.replace(/[،؛,.?!:؛«»()"']/g, '').trim();
        if (clean.length >= 2) freqMap[clean] = (freqMap[clean] || 0) + 1;
    });
    const sortedFreq = Object.entries(freqMap).sort((a, b) => b[1] - a[1]).slice(0, 10);

    // کلمات یکتا
    const uniqueWords = new Set(words.map(w => w.replace(/[،؛,.?!:؛«»()"']/g, '').trim()).filter(w => w.length > 0));

    // نوع متن
    let textType = 'عمومی';
    const avgWordLen = basic.average_word_length;
    if (avgWordLen > 7) textType = 'رسمی / علمی';
    else if (avgWordLen > 5) textType = 'نیمه‌رسمی';
    else if (avgWordLen > 3) textType = 'محاوره‌ای';

    // غنای واژگانی
    const ttr = words.length > 0 ? uniqueWords.size / words.length : 0;

    // فراوانی حروف
    const charFreq = {};
    const cleanText = text.replace(/[\s،؛,.?!:؛«»()"']/g, '');
    for (let c of cleanText) {
        charFreq[c] = (charFreq[c] || 0) + 1;
    }
    const topChars = Object.entries(charFreq).sort((a, b) => b[1] - a[1]).slice(0, 5);

    // طول جملات
    const sentenceLengths = sentences.map(s => s.trim().split(/\s+/).filter(w => w.length > 0).length);
    const longestSentence = sentenceLengths.length > 0 ? Math.max(...sentenceLengths) : 0;
    const shortestSentence = sentenceLengths.length > 0 ? Math.min(...sentenceLengths) : 0;
    const avgSentenceLength = sentenceLengths.length > 0 ? Math.round((sentenceLengths.reduce((a, b) => a + b, 0) / sentenceLengths.length) * 10) / 10 : 0;

    // تشخیص لحن
    const positiveWords = ['خوب', 'عالی', 'زیبا', 'دوست', 'شاد', 'خوش', 'بهترین', 'محبوب', 'قشنگ', 'مهربان'];
    const negativeWords = ['بد', 'زشت', 'ناراحت', 'غم', 'ترس', 'دشمن', 'بدترین', 'نفرت', 'خشم', 'گریه'];
    let positiveCount = 0;
    let negativeCount = 0;
    words.forEach(w => {
        const clean = w.replace(/[،؛,.?!:؛«»()"']/g, '').trim();
        if (positiveWords.includes(clean)) positiveCount++;
        if (negativeWords.includes(clean)) negativeCount++;
    });
    let sentiment = 'خنثی';
    if (positiveCount > negativeCount) sentiment = 'مثبت';
    else if (negativeCount > positiveCount) sentiment = 'منفی';

    // خوانایی
    const readingEase = Math.max(0, Math.min(100, 100 - (avgSentenceLength * 1.5 + avgWordLen * 2)));

    // زمان مطالعه
    const readingTimeMinutes = Math.ceil(words.length / 200);

    return {
        analysis: basic,
        frequency: sortedFreq,
        unique_word_count: uniqueWords.size,
        text_type: textType,
        lexical_richness: {
            ttr: Math.round(ttr * 100) / 100,
            interpretation: ttr > 0.7 ? 'بسیار غنی' : ttr > 0.5 ? 'غنی' : ttr > 0.3 ? 'متوسط' : 'ضعیف'
        },
        top_characters: topChars,
        sentence_analysis: {
            count: sentences.length,
            longest: longestSentence,
            shortest: shortestSentence,
            average_length: avgSentenceLength
        },
        sentiment: {
            label: sentiment,
            positive_words: positiveCount,
            negative_words: negativeCount
        },
        readability: {
            score: Math.round(readingEase),
            level: readingEase > 70 ? 'ساده' : readingEase > 50 ? 'متوسط' : 'دشوار'
        },
        reading_time_minutes: readingTimeMinutes,
        metadata: {
            version: '3.0.0',
            page: '218',
            processed_at: new Date().toISOString()
        }
    };
}

// پردازش پایه
app.post('/api/process', (req, res) => {
    try {
        const { text } = req.body;
        if (!text || typeof text !== 'string' || text.trim().length === 0) {
            return res.status(400).json({ error: 'متن ورودی الزامی است.', version: '3.0.0', page: '218' });
        }
        const analysis = analyzeText(text);
        res.json({ success: true, version: '3.0.0', page: '218', analysis });
    } catch (error) {
        res.status(500).json({ error: 'خطا در پردازش متن.', version: '3.0.0', page: '218' });
    }
});

// تحلیل عمیق
app.post('/api/deep', (req, res) => {
    try {
        const { text } = req.body;
        if (!text || typeof text !== 'string' || text.trim().length === 0) {
            return res.status(400).json({ error: 'متن ورودی الزامی است.', version: '3.0.0', page: '218' });
        }
        const deepResult = deepAnalyze(text);
        res.json({ success: true, version: '3.0.0', page: '218', ...deepResult });
    } catch (error) {
        res.status(500).json({ error: 'خطا در تحلیل عمیق.', version: '3.0.0', page: '218' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`ناتیق روی پورت ${PORT} فعال است`));
module.exports = app;
