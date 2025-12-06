/**
 * 🚀 اسکریپت اصلی نطق مصطلح
 */

class NatiqApp {
    constructor() {
        this.baseUrl = window.location.origin;
        this.currentPage = 1;
        this.totalPages = 1;
        this.totalArticles = 0;
        this.isLoading = false;
        
        this.init();
    }
    
    init() {
        console.log('🚀 نطق مصطلح نسخه ۳.۰ راه‌اندازی شد');
        
        this.loadArticles();
        this.setupEventListeners();
        this.updateStats();
    }
    
    async loadArticles(page = 1, searchQuery = '') {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.currentPage = page;
        
        const container = document.getElementById('articles-container');
        if (container) {
            container.innerHTML = '<div class="loading">در حال بارگذاری مقالات...</div>';
        }
        
        try {
            let url = `${this.baseUrl}/api/articles?page=${page}&limit=12`;
            if (searchQuery) {
                // اگر جستجو فعال باشد
                const allArticles = await this.searchArticles(searchQuery);
                this.renderArticles(allArticles);
                this.renderPagination({ page: 1, total: allArticles.length, pages: 1 });
                this.isLoading = false;
                return;
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.success) {
                this.totalArticles = data.pagination.total;
                this.totalPages = data.pagination.pages;
                
                this.renderArticles(data.data);
                this.renderPagination(data.pagination);
                this.updateStats();
            } else {
                this.showError('خطا در بارگذاری مقالات');
            }
        } catch (error) {
            console.error('❌ خطا در بارگذاری مقالات:', error);
            this.showError('خطا در بارگذاری مقالات');
        } finally {
            this.isLoading = false;
        }
    }
    
    async searchArticles(query) {
        if (!query || query.trim().length < 2) {
            return [];
        }
        
        try {
            const response = await fetch(`${this.baseUrl}/api/articles`);
            const data = await response.json();
            
            if (data.success) {
                const searchTerm = query.toLowerCase();
                return data.data.filter(article => 
                    article.title.toLowerCase().includes(searchTerm) ||
                    article.content.toLowerCase().includes(searchTerm) ||
                    article.excerpt.toLowerCase().includes(searchTerm) ||
                    article.category.toLowerCase().includes(searchTerm)
                );
            }
        } catch (error) {
            console.error('❌ خطا در جستجو:', error);
        }
        
        return [];
    }
    
    renderArticles(articles) {
        const container = document.getElementById('articles-container');
        if (!container) return;
        
        if (!articles || articles.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>مقاله‌ای یافت نشد</h3>
                    <p>هیچ مقاله‌ای با معیارهای جستجوی شما مطابقت ندارد</p>
                </div>
            `;
            return;
        }
        
        const articlesHTML = articles.map(article => `
            <div class="article-card fade-in">
                <div class="article-image">
                    <i class="fas fa-book-open"></i>
                </div>
                <div class="article-content">
                    <div class="article-meta">
                        <span class="article-category">${article.category}</span>
                        <span class="article-date">${this.formatDate(article.created_at)}</span>
                    </div>
                    
                    <h3 class="article-title">${article.title}</h3>
                    
                    <p class="article-excerpt">${article.excerpt}</p>
                    
                    <div class="article-footer">
                        <div class="article-stats">
                            <span title="بازدید">
                                <i class="fas fa-eye"></i>
                                ${this.formatNumber(article.views)}
                            </span>
                            <span title="پسندیده">
                                <i class="fas fa-heart"></i>
                                ${this.formatNumber(article.likes)}
                            </span>
                            <span title="اشتراک‌گذاری">
                                <i class="fas fa-share"></i>
                                ${this.formatNumber(article.shares)}
                            </span>
                        </div>
                        
                        <button class="read-more" onclick="app.viewArticle(${article.id})">
                            <i class="fas fa-book-reader"></i>
                            مطالعه مقاله
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = articlesHTML;
    }
    
    renderPagination(pagination) {
        const container = document.getElementById('pagination');
        if (!container) return;
        
        if (!pagination || pagination.pages <= 1) {
            container.innerHTML = '';
            return;
        }
        
        let paginationHTML = '';
        
        // دکمه قبلی
        if (pagination.page > 1) {
            paginationHTML += `
                <button class="pagination-btn" onclick="app.loadArticles(${pagination.page - 1})">
                    <i class="fas fa-chevron-right"></i>
                    قبلی
                </button>
            `;
        }
        
        // صفحات
        const maxPagesToShow = 5;
        let startPage = Math.max(1, pagination.page - Math.floor(maxPagesToShow / 2));
        let endPage = Math.min(pagination.pages, startPage + maxPagesToShow - 1);
        
        if (endPage - startPage + 1 < maxPagesToShow) {
            startPage = Math.max(1, endPage - maxPagesToShow + 1);
        }
        
        for (let i = startPage; i <= endPage; i++) {
            if (i === pagination.page) {
                paginationHTML += `<button class="pagination-btn active">${i}</button>`;
            } else {
                paginationHTML += `<button class="pagination-btn" onclick="app.loadArticles(${i})">${i}</button>`;
            }
        }
        
        // دکمه بعدی
        if (pagination.page < pagination.pages) {
            paginationHTML += `
                <button class="pagination-btn" onclick="app.loadArticles(${pagination.page + 1})">
                    بعدی
                    <i class="fas fa-chevron-left"></i>
                </button>
            `;
        }
        
        container.innerHTML = paginationHTML;
    }
    
    async viewArticle(id) {
        try {
            const response = await fetch(`${this.baseUrl}/api/articles/${id}`);
            const data = await response.json();
            
            if (data.success) {
                this.showArticleModal(data.data);
            } else {
                this.showError('مقاله یافت نشد');
            }
        } catch (error) {
            console.error('❌ خطا در بارگذاری مقاله:', error);
            this.showError('خطا در بارگذاری مقاله');
        }
    }
    
    showArticleModal(article) {
        const modalHTML = `
            <div class="modal-overlay" id="articleModal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>${article.title}</h2>
                        <button class="modal-close" onclick="app.closeModal()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="modal-body">
                        <div class="article-meta">
                            <span class="article-category">${article.category}</span>
                            <span>${this.formatDate(article.created_at)}</span>
                            <span>نویسنده: ${article.author}</span>
                        </div>
                        
                        <div class="article-content-full">
                            ${article.content.split('\n').map(p => `<p>${p}</p>`).join('')}
                        </div>
                        
                        <div class="article-tags">
                            ${article.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                        
                        <div class="article-stats">
                            <div class="stat">
                                <i class="fas fa-eye"></i>
                                <span>${this.formatNumber(article.views)} بازدید</span>
                            </div>
                            <div class="stat">
                                <i class="fas fa-heart"></i>
                                <span>${this.formatNumber(article.likes)} پسندیده</span>
                            </div>
                            <div class="stat">
                                <i class="fas fa-share"></i>
                                <span>${this.formatNumber(article.shares)} اشتراک‌گذاری</span>
                            </div>
                        </div>
                    </div>
                    
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="app.closeModal()">
                            بستن
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // اضافه کردن استایل modal
        if (!document.getElementById('modal-styles')) {
            const style = document.createElement('style');
            style.id = 'modal-styles';
            style.textContent = `
                .modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    background-color: rgba(0, 0, 0, 0.7);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    z-index: 10000;
                    animation: fadeIn 0.3s ease;
                }
                
                .modal-content {
                    background: white;
                    border-radius: 12px;
                    width: 90%;
                    max-width: 800px;
                    max-height: 90vh;
                    overflow-y: auto;
                    animation: slideUp 0.3s ease;
                }
                
                .modal-header {
                    padding: 1.5rem;
                    border-bottom: 1px solid #eee;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .modal-close {
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    cursor: pointer;
                    color: #666;
                }
                
                .modal-body {
                    padding: 1.5rem;
                }
                
                .modal-footer {
                    padding: 1rem 1.5rem;
                    border-top: 1px solid #eee;
                    text-align: left;
                }
                
                .article-content-full {
                    line-height: 1.8;
                    margin: 1.5rem 0;
                }
                
                .article-tags {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.5rem;
                    margin: 1rem 0;
                }
                
                .tag {
                    background: #e0e7ff;
                    color: #3730a3;
                    padding: 0.25rem 0.75rem;
                    border-radius: 4px;
                    font-size: 0.875rem;
                }
                
                @keyframes slideUp {
                    from { transform: translateY(50px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
        
        // حذف modal قبلی اگر وجود دارد
        const existingModal = document.getElementById('articleModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // اضافه کردن modal جدید
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // جلوگیری از اسکرول پشت modal
        document.body.style.overflow = 'hidden';
    }
    
    closeModal() {
        const modal = document.getElementById('articleModal');
        if (modal) {
            modal.remove();
            document.body.style.overflow = 'auto';
        }
    }
    
    updateStats() {
        // به‌روزرسانی آمار در صفحه
        const totalElement = document.getElementById('total-articles');
        if (totalElement) {
            totalElement.textContent = this.formatNumber(this.totalArticles);
        }
    }
    
    setupEventListeners() {
        // جستجو
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    const query = e.target.value.trim();
                    if (query.length >= 2 || query.length === 0) {
                        this.loadArticles(1, query);
                    }
                }, 500);
            });
        }
        
        // فیلتر دسته‌بندی
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                // بعداً پیاده‌سازی می‌شود
                console.log('فیلتر دسته‌بندی:', e.target.value);
            });
        }
    }
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('fa-IR', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        }).format(date);
    }
    
    formatNumber(num) {
        return new Intl.NumberFormat('fa-IR').format(num);
    }
    
    showError(message) {
        const container = document.getElementById('articles-container');
        if (container) {
            container.innerHTML = `
                <div class="error-state">
                    <i class="fas fa-exclamation-circle"></i>
                    <h3>خطا</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="app.loadArticles(1)">
                        تلاش مجدد
                    </button>
                </div>
            `;
        }
    }
}

// راه‌اندازی اپلیکیشن
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new NatiqApp();
    window.app = app;
    
    // اضافه کردن Font Awesome اگر وجود ندارد
    if (!document.querySelector('link[href*="font-awesome"]')) {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css';
        document.head.appendChild(link);
    }
});

// اضافه کردن ماژول جستجو به کلاس اصلی
// در انتهای کلاس NatiqApp اضافه می‌کنیم:

    // اضافه کردن جستجو
    setupSearch() {
        // اگر ماژول جستجو وجود دارد، آن را به app متصل کن
        if (window.searchModule) {
            this.search = window.searchModule;
            console.log('🔍 ماژول جستجو به اپلیکیشن متصل شد');
        }
    }

// و در init() بعد از loadArticles() اضافه کنیم:
    init() {
        console.log('🚀 نطق مصطلح نسخه ۳.۰ راه‌اندازی شد');
        
        this.loadArticles();
        this.setupEventListeners();
        this.updateStats();
        this.setupSearch(); // این خط اضافه شد
    }

// همچنین در setupEventListeners() اضافه کنیم:
    setupEventListeners() {
        // جستجو (اگر توسط ماژول جداگانه مدیریت نمی‌شود)
        const searchInput = document.getElementById('search-input');
        if (searchInput && !window.searchModule) {
            // پیاده‌سازی ساده جستجو
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                const query = e.target.value.trim();
                if (query.length >= 2 || query.length === 0) {
                    searchTimeout = setTimeout(() => {
                        this.loadArticles(1, query);
                    }, 500);
                }
            });
        }
        
        // بقیه event listeners...
    }

// اضافه کردن اتصال به سیستم جستجوی واقعی
// در انتهای کلاس NatiqApp اضافه می‌کنیم:

    // تنظیم جستجوی واقعی
    setupRealSearch() {
        // اگر رابط کاربری جستجوی واقعی وجود دارد
        if (window.realSearchUI) {
            this.searchUI = window.realSearchUI;
            console.log('🔍 رابط کاربری جستجوی واقعی متصل شد');
            
            // غیرفعال کردن جستجوی ساده قبلی
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.removeEventListener('input', this.searchHandler);
                searchInput.removeEventListener('keypress', this.enterHandler);
            }
        }
    }

// و در init() بعد از setupSearch() اضافه کنیم:
    init() {
        console.log('🚀 نطق مصطلح نسخه ۳.۰ راه‌اندازی شد');
        
        this.loadArticles();
        this.setupEventListeners();
        this.updateStats();
        this.setupSearch();
        this.setupRealSearch(); // این خط اضافه شد
    }
