const http = require('http');
const fs = require('fs');
const url = require('url');

console.log('🧠 راه‌اندازی سرور پرسش و پاسخ نطق مصطلح (نسخه اصلاح شده)...');

// بارگذاری مقالات
const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
console.log(`✅ ${articles.length} مقاله بارگذاری شد`);

// بارگذاری الگوریتم‌های ساده
const SimpleKeyword = require('./algorithms/simple_keyword');
const SimpleSemantic = require('./algorithms/simple_semantic');
const SimpleNLP = require('./algorithms/simple_nlp');

// ایجاد نمونه‌های الگوریتم
const keywordEngine = new SimpleKeyword(articles);
const semanticEngine = new SimpleSemantic(articles);
const nlpEngine = new SimpleNLP(articles);

// پایگاه داده سوالات
const faqDatabase = [];

// تابع پردازش سوالات
async function processQuestion(question, algorithm = 'auto') {
    console.log(`🤔 سوال: "${question}" - الگوریتم: ${algorithm}`);
    
    let result;
    const startTime = Date.now();
    
    try {
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
                // اجرای همه الگوریتم‌ها
                const [keywordResult, semanticResult, nlpResult] = await Promise.all([
                    keywordEngine.answerQuestion(question).catch(e => ({ 
                        success: false, 
                        error: e.message,
                        confidence: 0 
                    })),
                    semanticEngine.processQuestion(question).catch(e => ({ 
                        success: false, 
                        error: e.message,
                        confidence: 0 
                    })),
                    nlpEngine.processQuestion(question, articles).catch(e => ({ 
                        success: false, 
                        error: e.message,
                        confidence: 0 
                    }))
                ]);
                
                // انتخاب بهترین نتیجه
                const validResults = [keywordResult, semanticResult, nlpResult]
                    .filter(r => r.success)
                    .sort((a, b) => (b.confidence || 0) - (a.confidence || 0));
                
                if (validResults.length > 0) {
                    result = validResults[0];
                    result.usedAlgorithm = 'auto-selection';
                    result.allConfidences = {
                        keyword: keywordResult.confidence || 0,
                        semantic: semanticResult.confidence || 0,
                        nlp: nlpResult.confidence || 0
                    };
                } else {
                    result = {
                        success: false,
                        answer: 'هیچ یک از الگوریتم‌ها نتوانستند پاسخ مناسبی تولید کنند.',
                        errors: {
                            keyword: keywordResult.error,
                            semantic: semanticResult.error,
                            nlp: nlpResult.error
                        }
                    };
                }
                break;
        }
        
        // اضافه کردن زمان پردازش
        const processingTime = Date.now() - startTime;
        result.processingTime = processingTime;
        
        // ذخیره در پایگاه داده
        if (result.success) {
            faqDatabase.push({
                question,
                answer: result.answer.substring(0, 500),
                algorithm: result.algorithm || algorithm,
                confidence: result.confidence || 0,
                timestamp: new Date().toISOString(),
                processingTime: processingTime
            });
            
            // محدود کردن اندازه
            if (faqDatabase.length > 100) {
                faqDatabase.shift();
            }
        }
        
    } catch (error) {
        console.error('❌ خطا در پردازش سوال:', error);
        result = {
            success: false,
            answer: `خطا در پردازش سوال: ${error.message}`,
            error: error.message,
            algorithm: algorithm
        };
    }
    
    return result;
}

// تابع جستجوی سوالات مشابه
function findSimilarQuestions(question) {
    const keywords = question
        .toLowerCase()
        .replace(/[^\u0600-\u06FF\s]/g, '')
        .split(/\s+/)
        .filter(word => word.length > 2);
    
    const results = [];
    
    for (const faq of faqDatabase) {
        let score = 0;
        const faqText = (faq.question + ' ' + faq.answer).toLowerCase();
        
        for (const keyword of keywords) {
            if (faqText.includes(keyword)) {
                score++;
            }
        }
        
        if (score > 0) {
            results.push({
                question: faq.question,
                answer: faq.answer.substring(0, 100) + '...',
                score: score,
                date: faq.timestamp,
                algorithm: faq.algorithm
            });
        }
    }
    
    return results.sort((a, b) => b.score - a.score).slice(0, 5);
}

// ایجاد سرور HTTP
const server = http.createServer((req, res) => {
    // هدرهای CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    
    console.log(`📨 ${req.method} ${req.url}`);
    
    // مدیریت OPTIONS
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
            version: '2.0.0',
            timestamp: new Date().toISOString(),
            lastQuestions: faqDatabase.slice(-3).map(q => ({
                question: q.question.substring(0, 30) + '...',
                algorithm: q.algorithm
            }))
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
                            res.end(JSON.stringify(result, null, 2));
                        })
                        .catch(error => {
                            res.end(JSON.stringify({
                                success: false,
                                error: error.message
                            }, null, 2));
                        });
                        
                } catch (error) {
                    res.end(JSON.stringify({
                        success: false,
                        error: 'خطا در پردازش JSON'
                    }, null, 2));
                }
            });
            
        } else {
            res.statusCode = 405;
            res.end(JSON.stringify({
                success: false,
                error: 'متد غیرمجاز'
            }, null, 2));
        }
        return;
    }
    
    // سوالات مشابه
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
            totalFound: similar.length
        }, null, 2));
        return;
    }
    
    // آمار
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
            avgConfidence: faqDatabase.length > 0 ? 
                Math.round(faqDatabase.reduce((sum, q) => sum + q.confidence, 0) / faqDatabase.length) : 0,
            avgProcessingTime: faqDatabase.length > 0 ? 
                Math.round(faqDatabase.reduce((sum, q) => sum + q.processingTime, 0) / faqDatabase.length) : 0
        }, null, 2));
        return;
    }
    
    // آموزش
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
                        error: 'question و answer الزامی هستند'
                    }, null, 2));
                    return;
                }
                
                faqDatabase.push({
                    question: data.question,
                    answer: data.answer,
                    algorithm: 'human',
                    confidence: 100,
                    timestamp: new Date().toISOString(),
                    processingTime: 0
                });
                
                res.end(JSON.stringify({
                    success: true,
                    message: 'آموزش با موفقیت ثبت شد',
                    question: data.question.substring(0, 50) + '...',
                    databaseSize: faqDatabase.length
                }, null, 2));
                
            } catch (error) {
                res.end(JSON.stringify({
                    success: false,
                    error: 'خطا در پردازش درخواست'
                }, null, 2));
            }
        });
        return;
    }
    
    // صفحه اصلی
    if (pathname === '/') {
        res.setHeader('Content-Type', 'text/html; charset=utf-8');
        res.end(`
            <!DOCTYPE html>
            <html dir="rtl">
            <head><meta charset="UTF-8"><title>پرسش و پاسخ نطق مصطلح</title></head>
            <body>
                <h1>🧠 سیستم پرسش و پاسخ نطق مصطلح</h1>
                <p>نسخه 2.0.0 - الگوریتم‌های ساده و پایدار</p>
                <p><a href="/api/qna/health">سلامت سیستم</a></p>
                <p><a href="/api/qna/stats">آمار</a></p>
                <p>مثال: <code>/api/qna/ask?q=پردازش زبان طبیعی چیست؟</code></p>
            </body>
            </html>
        `);
        return;
    }
    
    // 404
    res.statusCode = 404;
    res.end(JSON.stringify({
        success: false,
        error: 'Endpoint یافت نشد',
        available: [
            'GET /api/qna/health',
            'GET /api/qna/ask?q=سوال',
            'GET /api/qna/similar?q=سوال',
            'GET /api/qna/stats',
            'POST /api/qna/teach'
        ]
    }, null, 2));
});

// راه‌اندازی سرور
const PORT = 3002;
server.listen(PORT, () => {
    console.log('\n' + '='.repeat(60));
    console.log('   🧠 سرور پرسش و پاسخ نطق مصطلح (نسخه اصلاح شده)');
    console.log('='.repeat(60));
    console.log(`   آدرس: http://localhost:${PORT}`);
    console.log(`   مقالات: ${articles.length} مقاله`);
    console.log(`   الگوریتم‌ها: keyword, semantic, nlp, auto`);
    console.log('='.repeat(60));
});

server.on('error', (err) => {
    console.error('❌ خطای سرور:', err.message);
});
