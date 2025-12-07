const fs = require('fs');

// خواندن مقالات فعلی
const articles = JSON.parse(fs.readFileSync('./data/articles.json', 'utf8'));
console.log(`مقالات فعلی: ${articles.length}`);

// پیدا کردن بزرگترین ID
const maxId = Math.max(...articles.map(a => a.id));
console.log(`بزرگترین ID فعلی: ${maxId}`);

// اضافه کردن مقالات جدید اگر نیاز باشد
if (maxId < 203) {
    const newArticles = [];
    
    for (let i = maxId + 1; i <= 203; i++) {
        const categories = ['NLP', 'آموزش', 'تکنولوژی', 'هوش مصنوعی', 'برنامه‌نویسی'];
        const tagsList = [
            ['NLP', 'پردازش زبان'],
            ['Python', 'برنامه‌نویسی'],
            ['هوش مصنوعی', 'یادگیری ماشین'],
            ['داده', 'تحلیل'],
            ['شبکه عصبی', 'Deep Learning']
        ];
        
        const category = categories[Math.floor(Math.random() * categories.length)];
        const tags = tagsList[Math.floor(Math.random() * tagsList.length)];
        
        newArticles.push({
            id: i,
            title: `مقاله شماره ${i} در مورد ${category}`,
            content: `این محتوای کامل مقاله شماره ${i} است که در مورد ${category} نوشته شده است. این مقاله به بررسی جنبه‌های مختلف این موضوع می‌پردازد.\n\n## بخش اول\nمتن تستی برای بخش اول مقاله.\n\n## بخش دوم\nادامه محتوای مقاله برای نمایش کامل.`,
            excerpt: `خلاصه مقاله شماره ${i} در زمینه ${category}`,
            author: i % 3 === 0 ? 'دکتر محمدی' : 
                   i % 3 === 1 ? 'مهندس کریمی' : 'تیم نطق مصطلح',
            category: category,
            tags: tags,
            views: Math.floor(Math.random() * 500) + 100,
            likes: Math.floor(Math.random() * 200) + 50,
            created_at: new Date(Date.now() - Math.random() * 31536000000).toISOString()
        });
    }
    
    // اضافه کردن به مقالات موجود
    const allArticles = [...articles, ...newArticles];
    
    // ذخیره فایل جدید
    fs.writeFileSync('./data/articles.json', JSON.stringify(allArticles, null, 2), 'utf8');
    console.log(`✅ ${newArticles.length} مقاله جدید اضافه شد`);
    console.log(`📚 مجموع مقالات: ${allArticles.length}`);
    console.log(`🎯 مقاله 203 اضافه شد: ${allArticles.find(a => a.id === 203).title}`);
} else {
    console.log('✅ مقاله 203 از قبل وجود دارد');
}
