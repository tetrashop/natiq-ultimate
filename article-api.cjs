// اضافه کردن به ultimate-server.cjs
if (req.url.startsWith('/api/article/')) {
    const id = parseInt(req.url.split('/').pop());
    const article = articles.find(a => a.id === id);
    
    if (article) {
        res.end(JSON.stringify({
            success: true,
            article: {
                ...article,
                related: getRelatedArticles(article.id)
            }
        }, null, 2));
    } else {
        res.end(JSON.stringify({
            success: false,
            error: 'مقاله یافت نشد'
        }, null, 2));
    }
    return;
}
