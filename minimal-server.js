const http = require('http');
console.log('سرور مینیمال...');
const server = http.createServer((req, res) => {
    res.end(JSON.stringify({status: 'ok'}));
});
server.listen(3005, () => console.log('✅ سرور روی پورت 3005'));
