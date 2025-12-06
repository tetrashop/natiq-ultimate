const fs = require('fs');

const patch = `
    // API جستجوی واقعی
    if (pathname === '/api/search' && req.method === 'GET') {
        if (!searchAPI) {
            sendError(res, 503, 'سیستم جستجو در دسترس نیست');
            return;
        }
        
        try {
            const query = parsedUrl.query.q;
            
            if (!query || query.trim().length < 2) {
                sendError(res, 400, 'عبارت جستجو باید حداقل ۲ کاراکتر باشد');
                return;
            }
            
            // تشخیص نوع جستجو
            const mode = parsedUrl.query.mode || 'quick';
            
            let result;
            if (mode === 'advanced') {
                result = searchAPI.advancedSearch({
                    query: query,
                    category: parsedUrl.query.category,
                    minViews: parsedUrl.query.minViews,
                    minLikes: parsedUrl.query.minLikes,
                    dateFrom: parsedUrl.query.dateFrom,
                    dateTo: parsedUrl.query.dateTo,
                    featured: parsedUrl.query.featured,
                    sortBy: parsedUrl.query.sortBy,
                    limit: parsedUrl.query.limit || 20
                });
            } else {
                result = searchAPI.search(query, {
                    limit: parsedUrl.query.limit || 20,
                    category: parsedUrl.query.category,
                    sortBy: parsedUrl.query.sortBy || 'relevance'
                });
            }
            
            sendJSON(res, 200, result);
        } catch (error) {
            console.error('❌ خطا در پردازش جستجو:', error.message);
            console.error('جزئیات خطا:', error.stack);
            sendError(res, 500, 'خطا در پردازش جستجو: ' + error.message);
        }
        return;
    }
`;

// خواندن فایل اصلی
let content = fs.readFileSync('./src/server/final-server.js', 'utf8');

// حذف بخش قدیمی جستجو (از خط مربوطه تا یک بازه مشخص)
const lines = content.split('\n');
let newLines = [];
let inSearchSection = false;
let braceCount = 0;

for (let i = 0; i < lines.length; i++) {
    if (lines[i].includes("'/api/search'") && lines[i].includes('GET')) {
        // شروع بخش جستجو - جایگزین با patch
        newLines.push(patch);
        inSearchSection = true;
        braceCount = 0;
    }
    
    if (!inSearchSection) {
        newLines.push(lines[i]);
    } else {
        // شمردن آکولادها برای پیدا کردن پایان بخش
        if (lines[i].includes('{')) braceCount++;
        if (lines[i].includes('}')) braceCount--;
        
        if (braceCount === 0 && inSearchSection) {
            inSearchSection = false;
        }
    }
}

fs.writeFileSync('./src/server/final-server.js.patched', newLines.join('\n'));
console.log('✅ فایل اصلاح شده ایجاد شد: final-server.js.patched');
console.log('برای استفاده: cp src/server/final-server.js.patched src/server/final-server.js');
