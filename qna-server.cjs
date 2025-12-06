const http = require('http');
const fs = require('fs');
const url = require('url');
const KeywordQnA = require('./algorithms/keyword_qna');
const SemanticQnA = require('./algorithms/semantic_qna');
const SimpleNLP = require('./algorithms/simple_nlp');

console.log('🧠 راه‌اندازی سرور پرسش و پاسخ نطق مصطلح...');

// بارگذاری مقالات
const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
console.log(`✅ ${articles.length} مقاله بارگذاری شد`);

// ایجاد نمونه‌های الگوریتم
const keywordEngine = new KeywordQnA(articles);
const semanticEngine = new SemanticQnA(articles);
const nlpEngine = new SimpleNLP();

// ذخیره‌سازی سوالات متداول
const faqDatabase = [];

// تابع برای پردازش سوالات
async function processQuestion(question, algorithm = 'auto') {
    console.log(`🤔 سوال: "${question}" - الگوریتم: ${algorithm}`);
    
    let result;
    
    switch (algorithm) {
        case 'keyword':
            result = await keywordEngine.answerQuestion(question);
            break;
        case 'semantic':
            result = await semanticEngine.processQuestion(question);
            break;
        case 'nlp':
            result = await nlpEngine.processQuestion(question, articles);
            break;
        case 'auto':
        default:
            // اجرای همه الگوریتم‌ها و انتخاب بهترین
            const results = await Promise.all([
                keywordEngine.answerQuestion(question),
                semanticEngine.processQuestion(question),
                nlpEngine.processQuestion(question, articles)
            ]);
            
            // انتخاب نتیجه با بیشترین اطمینان
            result = results.reduce((best, current) => {
                if (current.success && current.confidence > (best.confidence || 0)) {
                    return current;
                }
                return best;
            }, { success: false, confidence: 0 });
            
            // اگر هیچکدام موفق نبودند، از اولین نتیجه استفاده کن
            if (!result.success) {
                result = results.find(r => r.success) || {
                    success: false,
                    answer: 'متاسفانه هیچ یک از الگوریتم‌ها نتوانستند پاسخ مناسبی پیدا کنند.'
                };
            }
            
            result.usedAlgorithm = 'auto-selection';
            break;
    }
    
    // ذخیره سوال و پاسخ در پایگاه داده
    if (result.success) {
        faqDatabase.push({
            question,
            answer: result.answer,
            algorithm: result.algorithm || algorithm,
            timestamp: new Date().toISOString(),
            confidence: result.confidence || 0
        });
        
        // محدود کردن اندازه پایگاه داده
        if (faqDatabase.length > 1000) {
            faqDatabase.shift();
        }
    }
    
    return result;
}

// تابع برای یافتن سوالات مشابه
function findSimilarQuestions(question, limit = 5) {
    const keywords = question
        .toLowerCase()
        .replace(/[^\u0600-\u06FF\s]/g, '')
        .split(/\s+/)
        .filter(word => word.length > 2);
    
    const scoredQuestions = [];
    
    for (const faq of faqDatabase) {
        let score = 0;
        const faqLower = faq.question.toLowerCase();
        
        for (const keyword of keywords) {
            if (faqLower.includes(keyword)) {
                score++;
            }
        }
        
        if (score > 0) {
            scoredQuestions.push({
                question: faq.question,
                answer: faq.answer.substring(0, 100) + '...',
                score,
                date: faq.timestamp
            });
        }
    }
    
    return scoredQuestions
        .sort((a, b) => b.score - a.score)
        .slice(0, limit);
}

// ایجاد سرور HTTP
const server = http.createServer((req, res) => {
    // هدرهای CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    // گرفتن مسیر
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    console.log(`📨 ${req.method} ${req.url}`);
    
    // مدیریت OPTIONS برای CORS
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // سلامت سیستم
    if (pathname === '/api/qna/health') {
        res.end(JSON.stringify({
            status: 'فعال',
            articles: articles.length,
            faqCount: faqDatabase.length,
            algorithms: ['keyword', 'semantic', 'nlp', 'auto'],
            version: '1.0.0',
            timestamp: new Date().toISOString()
        }, null, 2));
        return;
    }
    
    // پرسش و پاسخ
    if (pathname === '/api/qna/ask') {
        if (req.method === 'GET') {
            const question = parsedUrl.query.q;
            const algorithm = parsedUrl.query.algorithm || 'auto';
            
            if (!question || question.trim().length < 2) {
                res.end(JSON.stringify({
                    success: false,
                    error: 'سوال باید حداقل ۲ کاراکتر داشته باشد',
                    example: 'پردازش زبان طبیعی چیست؟'
                }, null, 2));
                return;
            }
            
            processQuestion(question.trim(), algorithm)
                .then(result => {
                    res.end(JSON.stringify(result, null, 2));
                })
                .catch(error => {
                    res.end(JSON.stringify({
                        success: false,
                        error: error.message,
                        answer: 'خطا در پردازش سوال'
                    }, null, 2));
                });
            
        } else if (req.method === 'POST') {
            let body = '';
            
            req.on('data', chunk => {
                body += chunk.toString();
            });
            
            req.on('end', () => {
                try {
                    const data = JSON.parse(body);
                    const question = data.question;
                    const algorithm = data.algorithm || 'auto';
                    
                    if (!question || question.trim().length < 2) {
                        res.end(JSON.stringify({
                            success: false,
                            error: 'سوال باید حداقل ۲ کاراکتر داشته باشد'
                        }, null, 2));
                        return;
                    }
                    
                    processQuestion(question.trim(), algorithm)
                        .then(result => {
                            // اضافه کردن بازخورد اگر وجود داشته باشد
                            if (data.feedback) {
                                console.log(`📝 بازخورد دریافت شد: ${data.feedback}`);
                            }
                            
                            res.end(JSON.stringify(result, null, 2));
                        })
                        .catch(error => {
                            res.end(JSON.stringify({
                                success: false,
                                error: error.message,
                                answer: 'خطا در پردازش سوال'
                            }, null, 2));
                        });
                        
                } catch (error) {
                    res.end(JSON.stringify({
                        success: false,
                        error: 'خطا در پردازش درخواست JSON',
                        details: error.message
                    }, null, 2));
                }
            });
            
        } else {
            res.statusCode = 405;
            res.end(JSON.stringify({
                success: false,
                error: 'متد غیرمجاز. فقط GET و POST مجاز هستند.'
            }, null, 2));
        }
        return;
    }
    
    // جستجوی سوالات مشابه
    if (pathname === '/api/qna/similar') {
        const question = parsedUrl.query.q;
        
        if (!question) {
            res.end(JSON.stringify({
                success: false,
                error: 'پارامتر q الزامی است'
            }, null, 2));
            return;
        }
        
        const similar = findSimilarQuestions(question.trim());
        
        res.end(JSON.stringify({
            success: true,
            question: question,
            similarQuestions: similar,
            totalFound: similar.length,
            totalInDatabase: faqDatabase.length
        }, null, 2));
        return;
    }
    
    // آموزش سیستم با سوال و پاسخ جدید
    if (pathname === '/api/qna/teach' && req.method === 'POST') {
        let body = '';
        
        req.on('data', chunk => {
            body += chunk.toString();
        });
        
        req.on('end', () => {
            try {
                const data = JSON.parse(body);
                
                if (!data.question || !data.answer) {
                    res.end(JSON.stringify({
                        success: false,
                        error: 'پارامترهای question و answer الزامی هستند'
                    }, null, 2));
                    return;
                }
                
                faqDatabase.push({
                    question: data.question,
                    answer: data.answer,
                    algorithm: 'human-taught',
                    timestamp: new Date().toISOString(),
                    confidence: 100,
                    teacher: data.teacher || 'anonymous'
                });
                
                console.log(`🎓 سیستم آموزش داده شد: "${data.question.substring(0, 50)}..."`);
                
                res.end(JSON.stringify({
                    success: true,
                    message: 'سوال و پاسخ با موفقیت ذخیره شد',
                    question: data.question,
                    databaseSize: faqDatabase.length
                }, null, 2));
                
            } catch (error) {
                res.end(JSON.stringify({
                    success: false,
                    error: 'خطا در پردازش درخواست آموزش'
                }, null, 2));
            }
        });
        return;
    }
    
    // آمار سیستم
    if (pathname === '/api/qna/stats') {
        const today = new Date().toISOString().split('T')[0];
        const todayQuestions = faqDatabase.filter(q => 
            q.timestamp.startsWith(today)
        );
        
        const algorithmStats = {};
        faqDatabase.forEach(q => {
            algorithmStats[q.algorithm] = (algorithmStats[q.algorithm] || 0) + 1;
        });
        
        res.end(JSON.stringify({
            success: true,
            totalQuestions: faqDatabase.length,
            questionsToday: todayQuestions.length,
            algorithmsUsed: algorithmStats,
            mostCommonQuestions: faqDatabase
                .slice(-20) // آخرین ۲۰ سوال
                .map(q => ({
                    question: q.question.substring(0, 50) + '...',
                    algorithm: q.algorithm,
                    confidence: q.confidence
                }))
        }, null, 2));
        return;
    }
    
    // صفحه‌ی تست پرسش و پاسخ
    if (pathname === '/api/qna/test') {
        const testQuestions = [
            'پردازش زبان طبیعی چیست؟',
            'چگونه با پایتون برنامه نویسی کنیم؟',
            'تفاوت هوش مصنوعی و یادگیری ماشین چیست؟',
            'آیا مقاله 203 موجود است؟',
            'کاربردهای NLP در زندگی روزمره چیست؟'
        ];
        
        res.end(JSON.stringify({
            success: true,
            message: 'سوالات تستی برای آزمایش سیستم',
            testQuestions,
            instructions: 'می‌توانید هر یک از این سوالات را به /api/qna/ask ارسال کنید',
            example: 'GET /api/qna/ask?q=پردازش زبان طبیعی چیست؟'
        }, null, 2));
        return;
    }
    
    // صفحه‌ی اصلی
    if (pathname === '/') {
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.end(`
            <!DOCTYPE html>
            <html dir="rtl" lang="fa">
            <head>
                <meta charset="UTF-8">
                <title>سیستم پرسش و پاسخ نطق مصطلح</title>
                <style>
                    body { font-family: Tahoma, sans-serif; padding: 20px; background: #f5f5f5; }
                    .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
                    h1 { color: #2c3e50; }
                    .api-box { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
                    code { background: #eee; padding: 2px 5px; border-radius: 3px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🧠 سیستم پرسش و پاسخ نطق مصطلح</h1>
                    <p>این سیستم از الگوریتم‌های مختلفی برای پاسخ به سوالات شما استفاده می‌کند.</p>
                    
                    <h2>📡 API های موجود:</h2>
                    
                    <div class="api-box">
                        <h3>GET /api/qna/ask?q=سوال شما</h3>
                        <p>پاسخ به سوال شما را می‌دهد.</p>
                        <code>http://localhost:3001/api/qna/ask?q=پردازش زبان طبیعی چیست؟</code>
                    </div>
                    
                    <div class="api-box">
                        <h3>GET /api/qna/similar?q=سوال شما</h3>
                        <p>سوالات مشابه با سوال شما را پیدا می‌کند.</p>
                    </div>
                    
                    <div class="api-box">
                        <h3>GET /api/qna/stats</h3>
                        <p>آمار سیستم را نمایش می‌دهد.</p>
                    </div>
                    
                    <div class="api-box">
                        <h3>GET /api/qna/health</h3>
                        <p>سلامت سیستم را بررسی می‌کند.</p>
                    </div>
                    
                    <div class="api-box">
                        <h3>POST /api/qna/teach</h3>
                        <p>سیستم را با سوال و پاسخ جدید آموزش می‌دهد.</p>
                        <pre>
{
    "question": "سوال جدید",
    "answer": "پاسخ صحیح"
}
                        </pre>
                    </div>
                    
                    <h2>🔧 پارامتر algorithm:</h2>
                    <p>می‌توانید نوع الگوریتم را مشخص کنید:</p>
                    <ul>
                        <li><code>algorithm=keyword</code> - الگوریتم مبتنی بر کلیدواژه</li>
                        <li><code>algorithm=semantic</code> - الگوریتم معنایی</li>
                        <li><code>algorithm=nlp</code> - الگوریتم NLP ساده</li>
                        <li><code>algorithm=auto</code> - انتخاب خودکار بهترین الگوریتم (پیش‌فرض)</li>
                    </ul>
                </div>
            </body>
            </html>
        `);
        return;
    }
    
    // اگر endpoint یافت نشد
    res.statusCode = 404;
    res.end(JSON.stringify({
        success: false,
        error: 'Endpoint یافت نشد',
        availableEndpoints: [
            'GET /api/qna/ask?q=سوال',
            'GET /api/qna/similar?q=سوال',
            'GET /api/qna/stats',
            'GET /api/qna/health',
            'GET /api/qna/test',
            'POST /api/qna/teach'
        ]
    }, null, 2));
});

// راه‌اندازی سرور
const PORT = 3002;
server.listen(PORT, () => {
    console.log('\n' + '='.repeat(60));
    console.log('   🧠 سرور پرسش و پاسخ نطق مصطلح');
    console.log('='.repeat(60));
    console.log(`   آدرس: http://localhost:${PORT}`);
    console.log(`   مقالات: ${articles.length} مقاله`);
    console.log('');
    console.log('   📌 API های فعال:');
    console.log('      • GET  /api/qna/ask?q=سوال شما');
    console.log('      • GET  /api/qna/similar?q=سوال');
    console.log('      • GET  /api/qna/stats');
    console.log('      • GET  /api/qna/health');
    console.log('      • GET  /api/qna/test');
    console.log('      • POST /api/qna/teach');
    console.log('');
    console.log('   ⚙️  الگوریتم‌های پشتیبانی شده:');
    console.log('      • keyword   - مبتنی بر کلیدواژه');
    console.log('      • semantic  - مبتنی بر معناشناسی');
    console.log('      • nlp       - پردازش زبان طبیعی ساده');
    console.log('      • auto      - انتخاب خودکار (پیش‌فرض)');
    console.log('='.repeat(60));
});

// مدیریت خطا
server.on('error', (err) => {
    console.error('❌ خطای سرور:', err.message);
});
