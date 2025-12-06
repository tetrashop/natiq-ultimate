async function search() {
    const query = document.getElementById('searchInput').value;
    
    if (query.length < 2) {
        showError('عبارت جستجو باید حداقل ۲ کاراکتر باشد');
        return;
    }
    
    showLoading();
    
    try {
        // استفاده از encodeURIComponent برای فارسی
        const encodedQuery = encodeURIComponent(query);
        const response = await fetch(`http://localhost:3000/api/search?q=${encodedQuery}`);
        
        if (!response.ok) {
            throw new Error(`خطای HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.results);
            updateStats(data.totalResults, query);
        } else {
            showError(data.error || 'خطا در جستجو');
        }
    } catch (error) {
        showError('خطا در ارتباط با سرور: ' + error.message);
    }
}
