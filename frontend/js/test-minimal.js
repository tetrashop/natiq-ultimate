const http = require('http');
console.log('تست سرور مینیمال...');

const server = http.createServer((req, res) => {
    console.log('درخواست: ' + req.url);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('سرور کار می‌کند!\n');
});

server.listen(3002, () => {
    console.log('✅ سرور تست روی پورت 3002');
    
    // تست خودکار
    const req = require('http').get('http://localhost:3002', (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
            console.log('✅ پاسخ: ' + data.trim());
            server.close();
        });
    });
});
