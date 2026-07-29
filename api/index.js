const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());

app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', '*');
    next();
});

app.use(express.static(path.join(__dirname, '..', 'public')));

// ---------- توابع تحلیل ----------
function analyzeText(text) {
    const words = text.split(/\s+/).filter(w => w.length > 0);
    const chars = text.replace(/\s/g, '').length;
    const sentences = text.split(/[.!?؟\n]+/).filter(s => s.trim().length > 0);
    let longestWord = '', shortestWord = '';
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
        shortest_word: shortestWord,
    };
}

function deepAnalyze(text) {
    const words = text.split(/\s+/).filter(w => w.length > 0);
    const chars = text.replace(/\s/g, '').length;
    const sentences = text.split(/[.!?؟\n]+/).filter(s => s.trim().length > 0);
    const basic = analyzeText(text);

    const freqMap = {};
    words.forEach(w => {
        const clean = w.replace(/[،؛,.?!:؛«»()"']/g, '').trim();
        if (clean.length >= 2) freqMap[clean] = (freqMap[clean] || 0) + 1;
    });
    const sortedFreq = Object.entries(freqMap).sort((a, b) => b[1] - a[1]).slice(0, 10);

    const uniqueWords = new Set(words.map(w => w.replace(/[،؛,.?!:؛«»()"']/g, '').trim()).filter(w => w.length > 0));

    let textType = 'عمومی';
    if (basic.average_word_length > 7) textType = 'رسمی / علمی';
    else if (basic.average_word_length > 5) textType = 'نیمه‌رسمی';
    else if (basic.average_word_length > 3) textType = 'محاوره‌ای';

    const ttr = words.length > 0 ? uniqueWords.size / words.length : 0;
    const charFreq = {};
    const cleanText = text.replace(/[\s،؛,.?!:؛«»()"']/g, '');
    for (let c of cleanText) charFreq[c] = (charFreq[c] || 0) + 1;
    const topChars = Object.entries(charFreq).sort((a, b) => b[1] - a[1]).slice(0, 5);

    const sentenceLengths = sentences.map(s => s.trim().split(/\s+/).filter(w => w.length > 0).length);
    const longestSentence = sentenceLengths.length > 0 ? Math.max(...sentenceLengths) : 0;
    const shortestSentence = sentenceLengths.length > 0 ? Math.min(...sentenceLengths) : 0;
    const avgSentenceLength = sentenceLengths.length > 0
        ? Math.round((sentenceLengths.reduce((a, b) => a + b, 0) / sentenceLengths.length) * 10) / 10 : 0;

    const positiveWords = ['خوب', 'عالی', 'زیبا', 'دوست', 'شاد', 'خوش', 'بهترین', 'محبوب', 'قشنگ', 'مهربان'];
    const negativeWords = ['بد', 'زشت', 'ناراحت', 'غم', 'ترس', 'دشمن', 'بدترین', 'نفرت', 'خشم', 'گریه'];
    let positiveCount = 0, negativeCount = 0;
    words.forEach(w => {
        const clean = w.replace(/[،؛,.?!:؛«»()"']/g, '').trim();
        if (positiveWords.includes(clean)) positiveCount++;
        if (negativeWords.includes(clean)) negativeCount++;
    });
    let sentiment = 'خنثی';
    if (positiveCount > negativeCount) sentiment = 'مثبت';
    else if (negativeCount > positiveCount) sentiment = 'منفی';

    const readingEase = Math.max(0, Math.min(100, 100 - (avgSentenceLength * 1.5 + basic.average_word_length * 2)));
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
            version: '4.2.0',
            page: '218',
            processed_at: new Date().toISOString()
        }
    };
}

// ---------- API Routes ----------
app.get('/api', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '4.2.0',
        page: '218',
        status: 'فعال',
        storage: 'localStorage (مرورگر)',
        endpoints: {
            health: '/api/health',
            chat: '/api/chat',
            process: '/api/process',
            deep: '/api/deep'
        }
    });
});

app.get('/api/health', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '4.2.0',
        page: '218',
        status: 'فعال',
        timestamp: new Date().toISOString()
    });
});

app.post('/api/process', (req, res) => {
    try {
        const { text } = req.body;
        if (!text || typeof text !== 'string' || text.trim().length === 0) {
            return res.status(400).json({ error: 'متن ورودی الزامی است.' });
        }
        const analysis = analyzeText(text);
        res.json({ success: true, analysis });
    } catch (error) {
        res.status(500).json({ error: 'خطا در پردازش متن.' });
    }
});

app.post('/api/deep', (req, res) => {
    try {
        const { text } = req.body;
        if (!text || typeof text !== 'string' || text.trim().length === 0) {
            return res.status(400).json({ error: 'متن ورودی الزامی است.' });
        }
        const result = deepAnalyze(text);
        res.json({ success: true, ...result });
    } catch (error) {
        res.status(500).json({ error: 'خطا در تحلیل عمیق.' });
    }
});

app.post('/api/chat', (req, res) => {
    try {
        const { message } = req.body;
        if (!message || typeof message !== 'string' || message.trim().length === 0) {
            return res.status(400).json({ error: 'پیام نمی‌تواند خالی باشد.' });
        }

        const lowerMsg = message.trim().toLowerCase();
        if (lowerMsg === 'سلام' || lowerMsg === 'hi' || lowerMsg === 'hello') {
            return res.json({
                reply: 'سلام! 🌟 من ناتیق هستم، دستیار هوشمند تحلیل متن فارسی. هر متنی بفرستی، آن را تحلیل عمیق می‌کنم.',
                version: '4.2.0'
            });
        }

        if (lowerMsg === 'راهنما' || lowerMsg === 'help') {
            return res.json({
                reply: '📘 راهنما:\n- متن بفرست تا تحلیل عمیق انجام شود.\n- دکمه «ذخیره» تحلیل را در مرورگر ذخیره می‌کند.\n- «سلامت» = وضعیت سیستم',
                version: '4.2.0'
            });
        }

        if (lowerMsg === 'سلامت' || lowerMsg === 'health') {
            return res.json({
                reply: '✅ ناتیق فعال است. ورژن ۴.۲.۰ | صفحه ۲۱۸ | ذخیره‌سازی در مرورگر',
                version: '4.2.0'
            });
        }

        const analysis = deepAnalyze(message);
        const a = analysis.analysis;
        const s = analysis.sentiment;
        const r = analysis.readability;
        const l = analysis.lexical_richness;
        const topWords = analysis.frequency.slice(0, 5).map(([w, c]) => `${w}(${c})`).join('، ');

        const reply = `
📊 **نتیجه تحلیل عمیق**:
- **کلمات**: ${a.words} | **کاراکترها**: ${a.characters} | **جملات**: ${a.sentences}
- **میانگین طول کلمه**: ${a.average_word_length} (${analysis.text_type})
- **زمان مطالعه**: ${analysis.reading_time_minutes} دقیقه
- **کلمات یکتا**: ${analysis.unique_word_count}
- **احساس**: ${s.label} (${s.positive_words}+ / ${s.negative_words}-)
- **خوانایی**: ${r.level} (${r.score}%)
- **غنای واژگانی**: ${l.interpretation} (TTR: ${l.ttr})
- **پرتکرارترین**: ${topWords}
        `.trim();

        res.json({ reply, analysis: { words: a.words, characters: a.characters, sentences: a.sentences, text_type: analysis.text_type, sentiment: s.label, readability: r.score, reading_time: analysis.reading_time_minutes }, version: '4.2.0' });

    } catch (error) {
        res.status(500).json({ error: 'خطا در پردازش چت.' });
    }
});

module.exports = app;
