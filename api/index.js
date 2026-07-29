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

// ─────────────────── دیکشنری غلط‌های رایج ───────────────────
const SPELLING_DICT = {
    'میباشد': 'می‌باشد',
    'میباشدند': 'می‌باشند',
    'میباشم': 'می‌باشم',
    'میباشی': 'می‌باشی',
    'میباشیم': 'می‌باشیم',
    'میباشید': 'می‌باشید',
    'می کند': 'می‌کند',
    'می کندم': 'می‌کنم',
    'می کندی': 'می‌کنی',
    'می کندیم': 'می‌کنیم',
    'می کندید': 'می‌کنید',
    'می کنند': 'می‌کنند',
    'می شود': 'می‌شود',
    'می شوم': 'می‌شوم',
    'می شوی': 'می‌شوی',
    'می شویم': 'می‌شویم',
    'می شوید': 'می‌شوید',
    'می شوند': 'می‌شوند',
    'می گیرد': 'می‌گیرد',
    'می دهم': 'می‌دهم',
    'می دهی': 'می‌دهی',
    'می دهد': 'می‌دهد',
    'می دهیم': 'می‌دهیم',
    'می دهید': 'می‌دهید',
    'می دهند': 'می‌دهند',
    'می گیرم': 'می‌گیرم',
    'می گیری': 'می‌گیری',
    'می گیریم': 'می‌گیریم',
    'می گیرید': 'می‌گیرید',
    'می گیرند': 'می‌گیرند',
    'می گویم': 'می‌گویم',
    'می گویی': 'می‌گویی',
    'می گوید': 'می‌گوید',
    'می گوییم': 'می‌گوییم',
    'می گویید': 'می‌گویید',
    'می گویند': 'می‌گویند',
    'می آیم': 'می‌آیم',
    'می آیی': 'می‌آیی',
    'می آید': 'می‌آید',
    'می آییم': 'می‌آییم',
    'می آیید': 'می‌آیید',
    'می آیند': 'می‌آیند',
    'می اندازم': 'می‌اندازم',
    'می اندازی': 'می‌اندازی',
    'می اندازد': 'می‌اندازد',
    'نمی کند': 'نمی‌کند',
    'نمی شود': 'نمی‌شود',
    'نمی گیرد': 'نمی‌گیرد',
    'نمی دهد': 'نمی‌دهد',
    'خواهم': 'خواهم',
    'خواهی': 'خواهی',
    'خواهد': 'خواهد',
    'خواهیم': 'خواهیم',
    'خواهید': 'خواهید',
    'خواهند': 'خواهند',
    'آنها': 'آن‌ها',
    'آنان': 'آنان',
    'اینها': 'این‌ها',
    'اینان': 'اینان',
    'آنچه': 'آنچه',
    'آنکه': 'آنکه',
    'آنگاه': 'آن‌گاه',
    'چنانچه': 'چنانچه',
    'چنانکه': 'چنانکه',
    'هرگاه': 'هرگاه',
    'هرچه': 'هرچه',
    'هرکه': 'هرکه',
    'همین': 'همین',
    'همان': 'همان',
    'همینطور': 'همین‌طور',
    'همانطور': 'همان‌طور',
    'همچنین': 'همچنین',
    'همچون': 'همچون',
    'بنابر این': 'بنابراین',
    'بنابرین': 'بنابراین',
    'بدین': 'بدین',
    'بدین ترتیب': 'بدین‌ترتیب',
    'بدین صورت': 'بدین‌صورت',
    'بدین وسیله': 'بدین‌وسیله',
    'دربین': 'در بین',
    'بوسیله': 'به‌وسیله',
    'بوسیله ی': 'به‌وسیلهٔ',
    'توسط': 'توسط',
    'باین': 'به این',
    'بآن': 'به آن',
    'ازآن': 'از آن',
    'ازاین': 'از این',
    'برایشان': 'برایشان',
    'برایم': 'برایم',
    'برایمان': 'برایمان',
    'برای تان': 'برایتان',
    'بگویید': 'بگویید',
    'بگوید': 'بگوید',
    'میشود': 'می‌شود',
    'میکند': 'می‌کند',
    'میکنم': 'می‌کنم',
    'میکنی': 'می‌کنی',
    'میکنیم': 'می‌کنیم',
    'میکنید': 'می‌کنید',
    'میکنند': 'می‌کنند',
    'میشوم': 'می‌شوم',
    'میشوی': 'می‌شوی',
    'میشویم': 'می‌شویم',
    'میشوید': 'می‌شوید',
    'میشوند': 'می‌شوند',
    'میدهم': 'می‌دهم',
    'میدهی': 'می‌دهی',
    'میدهد': 'می‌دهد',
    'میدهیم': 'می‌دهیم',
    'میدهید': 'می‌دهید',
    'میدهند': 'می‌دهند',
    'میگیرم': 'می‌گیرم',
    'میگیری': 'می‌گیری',
    'میگیرد': 'می‌گیرد',
    'میگیریم': 'می‌گیریم',
    'میگیرید': 'می‌گیرید',
    'میگیرند': 'می‌گیرند',
    'میگویم': 'می‌گویم',
    'میگویی': 'می‌گویی',
    'میگوید': 'می‌گوید',
    'میگوییم': 'می‌گوییم',
    'میگویید': 'می‌گویید',
    'میگویند': 'می‌گویند',
    'بیاور': 'بیاور',
    'بیاورد': 'بیاورد',
    'بیاورم': 'بیاورم',
    'بیاوری': 'بیاوری',
    'بیاوریم': 'بیاوریم',
    'بیاورید': 'بیاورید',
    'بیاورند': 'بیاورند',
    'ببین': 'ببین',
    'ببیند': 'ببیند',
    'ببینم': 'ببینم',
    'ببینی': 'ببینی',
    'ببینیم': 'ببینیم',
    'ببینید': 'ببینید',
    'ببینند': 'ببینند',
    'برو': 'برو',
    'برود': 'برود',
    'بروم': 'بروم',
    'بروی': 'بروی',
    'برویم': 'برویم',
    'بروید': 'بروید',
    'بروند': 'بروند',
    'بکن': 'بکن',
    'بکند': 'بکند',
    'بکنم': 'بکنم',
    'بکنی': 'بکنی',
    'بکنیم': 'بکنیم',
    'بکنید': 'بکنید',
    'بکنند': 'بکنند',
};

// ─────────────────── توابع ویرایش ───────────────────
function spellCheck(text) {
    const corrections = [];
    let corrected = text;

    // بررسی غلط‌های املایی
    for (const [wrong, correct] of Object.entries(SPELLING_DICT)) {
        const regex = new RegExp(wrong.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g');
        const matches = corrected.match(regex);
        if (matches) {
            matches.forEach(() => {
                corrections.push({
                    type: 'spelling',
                    original: wrong,
                    corrected: correct,
                    description: `«${wrong}» ← «${correct}»`
                });
            });
            corrected = corrected.replace(regex, correct);
        }
    }

    // اصلاح فاصله قبل از علائم نگارشی
    const punctBefore = corrected.match(/ [.،؛:?!»)]/g);
    if (punctBefore) {
        punctBefore.forEach(m => {
            corrections.push({
                type: 'punctuation',
                original: m,
                corrected: m.trim(),
                description: `حذف فاصله قبل از «${m.trim()}»`
            });
        });
    }
    corrected = corrected.replace(/ ([.،؛:?!»\)])/g, '$1');

    // اصلاح فاصله بعد از علائم نگارشی
    corrected = corrected.replace(/([.،؛:?!«(])([^\s\d])/g, '$1 $2');

    // اصلاح نیم‌فاصله برای «می» و «نمی»
    corrected = corrected.replace(/می ([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])/g, 'می‌$1');
    corrected = corrected.replace(/نمی ([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])/g, 'نمی‌$1');

    return {
        original: text,
        corrected,
        corrections,
        has_errors: corrections.length > 0,
        error_count: corrections.length
    };
}

// ─────────────────── توابع تحلیل اصلی ───────────────────
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

    const readingEase = Math.max(0, Math.min(100, 100 - (basic.average_word_length * 2 + sentences.length * 1.5)));
    const readingTimeMinutes = Math.ceil(words.length / 200);

    return {
        analysis: basic,
        frequency: sortedFreq,
        unique_word_count: uniqueWords.size,
        text_type: textType,
        lexical_richness: { ttr: Math.round(ttr * 100) / 100 },
        sentiment: { label: sentiment, positive_words: positiveCount, negative_words: negativeCount },
        readability: { score: Math.round(readingEase), level: readingEase > 70 ? 'ساده' : readingEase > 50 ? 'متوسط' : 'دشوار' },
        reading_time_minutes: readingTimeMinutes,
        metadata: { version: '5.0.0', page: '218', processed_at: new Date().toISOString() }
    };
}

// ─────────────────── API Routes ───────────────────
app.get('/api', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '5.0.0',
        page: '218',
        status: 'فعال',
        features: ['chat', 'spell-check', 'deep-analysis'],
        endpoints: {
            health: '/api/health',
            chat: '/api/chat',
            spell: '/api/spell',
            process: '/api/process',
            deep: '/api/deep'
        }
    });
});

app.get('/api/health', (req, res) => {
    res.json({
        name: 'ناتیق اولتیمیت',
        version: '5.0.0',
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
        res.json({ success: true, analysis: analyzeText(text) });
    } catch (error) {
        res.status(500).json({ error: 'خطا در پردازش.' });
    }
});

app.post('/api/deep', (req, res) => {
    try {
        const { text } = req.body;
        if (!text || typeof text !== 'string' || text.trim().length === 0) {
            return res.status(400).json({ error: 'متن ورودی الزامی است.' });
        }
        res.json({ success: true, ...deepAnalyze(text) });
    } catch (error) {
        res.status(500).json({ error: 'خطا در تحلیل عمیق.' });
    }
});

// ✨ endpoint ویرایش املایی
app.post('/api/spell', (req, res) => {
    try {
        const { text } = req.body;
        if (!text || typeof text !== 'string' || text.trim().length === 0) {
            return res.status(400).json({ error: 'متن ورودی الزامی است.' });
        }
        const result = spellCheck(text);
        res.json({
            success: true,
            ...result,
            summary: result.has_errors
                ? `${result.error_count} مورد نیاز به اصلاح یافت شد.`
                : '✅ هیچ غلط املایی یافت نشد.',
            version: '5.0.0'
        });
    } catch (error) {
        res.status(500).json({ error: 'خطا در ویرایش متن.' });
    }
});

// ✨ endpoint چت با قابلیت ویرایش
app.post('/api/chat', (req, res) => {
    try {
        const { message } = req.body;
        if (!message || typeof message !== 'string' || message.trim().length === 0) {
            return res.status(400).json({ error: 'پیام نمی‌تواند خالی باشد.' });
        }

        const lowerMsg = message.trim().toLowerCase();

        // سلام
        if (lowerMsg === 'سلام' || lowerMsg === 'hi' || lowerMsg === 'hello') {
            return res.json({
                reply: 'سلام! 🌟 من ناتیق ۵.۰ هستم.\n\n✨ قابلیت‌های من:\n- تحلیل عمیق متن فارسی\n- ویرایش املایی و نگارشی\n- تشخیص احساس و خوانایی\n\n📝 متن بفرست تا تحلیل کنم.\n✍️ «ویرایش: ...» بفرست تا غلط‌ها رو پیدا کنم.',
                version: '5.0.0'
            });
        }

        // راهنما
        if (lowerMsg === 'راهنما' || lowerMsg === 'help' || lowerMsg === 'کمک') {
            return res.json({
                reply: '📘 **راهنمای ناتیق ۵.۰**:\n\n1️⃣ متن بفرست ← تحلیل عمیق\n2️⃣ «ویرایش: متن» ← اصلاح املایی\n3️⃣ «سلامت» ← وضعیت سیستم\n4️⃣ «پاک» ← پاک کردن گفتگو',
                version: '5.0.0'
            });
        }

        // سلامت
        if (lowerMsg === 'سلامت' || lowerMsg === 'health') {
            return res.json({
                reply: '✅ ناتیق ۵.۰ فعال است.\n📌 صفحه ۲۱۸\n✍️ ویرایشگر املایی: فعال\n☁️ آماده برای Vercel',
                version: '5.0.0'
            });
        }

        // ✨ درخواست ویرایش
        if (lowerMsg.startsWith('ویرایش:') || lowerMsg.startsWith('ویرایش ')) {
            const textToEdit = message.replace(/^ویرایش[:：]\s*/, '').replace(/^ویرایش\s+/, '').trim();
            if (!textToEdit) {
                return res.json({ reply: '⚠️ لطفاً متنی برای ویرایش وارد کنید.\nمثال: «ویرایش: سلام خوبی»', version: '5.0.0' });
            }
            const result = spellCheck(textToEdit);
            let reply = `✍️ **نتیجه ویرایش**:\n\n`;
            if (result.has_errors) {
                reply += `📊 **${result.error_count} مورد** یافت شد:\n`;
                result.corrections.forEach((c, i) => {
                    reply += `${i + 1}. ${c.description}\n`;
                });
                reply += `\n✅ **متن ویرایش‌شده**:\n${result.corrected}`;
            } else {
                reply += `✅ هیچ غلطی یافت نشد!\nمتن شما صحیح است.`;
            }
            return res.json({ reply, spell_result: result, version: '5.0.0' });
        }

        // تحلیل عمیق (پیش‌فرض)
        const analysis = deepAnalyze(message);
        const a = analysis.analysis;
        const s = analysis.sentiment;
        const r = analysis.readability;
        const topWords = analysis.frequency.slice(0, 5).map(([w, c]) => `${w}(${c})`).join('، ');

        const reply = [
            `📊 **تحلیل عمیق**:`,
            `▫️ کلمات: ${a.words} | کاراکتر: ${a.characters} | جمله: ${a.sentences}`,
            `▫️ نوع متن: ${analysis.text_type}`,
            `▫️ زمان مطالعه: ${analysis.reading_time_minutes} دقیقه`,
            `▫️ احساس: ${s.label} (${s.positive_words}+/${s.negative_words}-)`,
            `▫️ خوانایی: ${r.level} (${r.score}%)`,
            `▫️ واژگان یکتا: ${analysis.unique_word_count}`,
            `▫️ پرتکرار: ${topWords}`,
            `▫️ بلندترین: ${a.longest_word} | کوتاه‌ترین: ${a.shortest_word}`,
            ``,
            `💡 **راهنمایی**: برای ویرایش املایی، بنویسید: «ویرایش: متن شما»`
        ].join('\n');

        res.json({
            reply,
            analysis: {
                words: a.words,
                characters: a.characters,
                sentences: a.sentences,
                text_type: analysis.text_type,
                sentiment: s.label,
                readability: r.score,
                reading_time: analysis.reading_time_minutes
            },
            version: '5.0.0'
        });

    } catch (error) {
        res.status(500).json({ error: 'خطا در پردازش.' });
    }
});

module.exports = app;
