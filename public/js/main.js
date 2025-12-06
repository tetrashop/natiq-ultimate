/**
 * 🎮 اسکریپت اصلی رابط کاربری
 */

class NatiqApp {
    constructor() {
        this.currentPage = 1;
        this.totalPages = 1;
        this.init();
    }
    
    init() {
        console.log('🚀 نطق مصطلف نسخه ۳.۰ راه‌اندازی شد');
        
        // بارگذاری اولیه
        this.loadArticles();
        this.loadStats();
        
        // راه‌اندازی event listeners
        this.setupEventListeners();
    }
    
    async loadArticles(page = 1) {
        try {
            const response = await fetch(`/api/articles?page=${page}&limit=12`);
            const data = await response.json();
            
            if (data.success) {
                this.renderArticles(data.data);
                this.renderPagination(data.pagination);
            }
        } catch (error) {
            console.error('❌ خطا در بارگذاری مقالات:', error);
            this.showError('خطا در بارگذاری مقالات');
        }
    }
    
    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const data = await response.json();
            
            if (data.success) {
                this.updateStats(data.data);
            }
        } catch (error) {
            console.error('❌ خطا در بارگذاری آمار:', error);
        }
    }
    
    renderArticles(articles) {
        const container = document.getElementById('articlesGrid');
        
        if (!articles || articles.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-journal-x"></i>
                    <h3>مقاله‌ای یافت نشد</h3>
                    <p>هیچ مقاله‌ای با معیارهای جستجوی شما مطابقت ندارد</p>
                </div>
            `;
            return;
        }
        
        const articlesHTML = articles.map(article => `
            <div class="article-card">
                <div class="article-content">
                    <div class="article-meta">
                        <span class="article-category">${article.category}</span>
                        <span class="article-date">
                            ${this.formatDate(article.created_at)}
                        </span>
                    </div>
                    
                    <h3 class="article-title">${article.title}</h3>
                    
                    <p class="article-excerpt">${article.excerpt}</p>
                    
                    <div class="article-footer">
                        <div class="article-stats">
                            <span title="بازدید">
                                <i class="bi bi-eye"></i>
                                ${this.formatNumber(article.views)}
                            </span>
                            <span title="پسندیده">
                                <i class="bi bi-heart"></i>
                                ${this.formatNumber(article.likes)}
                            </span>
                        </div>
                        
                        <button class="btn btn-sm btn-outline" onclick="app.viewArticle(${article.id})">
                            مشاهده مقاله
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = articlesHTML;
    }
    
    renderPagination(pagination) {
        const container = document.getElementById('pagination');
        
        if (!pagination || pagination.pages <= 1) {
            container.innerHTML = '';
            return;
        }
        
        this.currentPage = pagination.page;
        this.totalPages = pagination.pages;
        
        let paginationHTML = '';
        
        // دکمه قبلی
        if (pagination.page > 1) {
            paginationHTML += `
                <button class="pagination-btn" onclick="app.goToPage(${pagination.page - 1})">
                    <i class="bi bi-chevron-right"></i>
                    قبلی
                </button>
            `;
        }
        
        // صفحات
        for (let i = 1; i <= pagination.pages; i++) {
            if (i === pagination.page) {
                paginationHTML += `
                    <button class="pagination-btn active">${i}</button>
                `;
            } else {
                paginationHTML += `
                    <button class="pagination-btn" onclick="app.goToPage(${i})">${i}</button>
                `;
            }
        }
        
        // دکمه بعدی
        if (pagination.page < pagination.pages) {
            paginationHTML += `
                <button class="pagination-btn" onclick="app.goToPage(${pagination.page + 1})">
                    بعدی
                    <i class="bi bi-chevron-left"></i>
                </button>
            `;
        }
        
        container.innerHTML = paginationHTML;
    }
    
    updateStats(stats) {
        const totalViews = document.getElementById('totalViews');
        const totalLikes = document.getElementById('totalLikes');
        
        if (totalViews) totalViews.textContent = this.formatNumber(stats.total_views);
        if (totalLikes) totalLikes.textContent = this.formatNumber(stats.total_likes);
    }
    
    goToPage(page) {
        if (page < 1 || page > this.totalPages) return;
        this.loadArticles(page);
        
        // پیمایش به بخش مقالات
        document.getElementById('articles').scrollIntoView({ behavior: 'smooth' });
    }
    
    async viewArticle(id) {
        try {
            const response = await fetch(`/api/articles/${id}`);
            const data = await response.json();
            
            if (data.success) {
                this.showArticleModal(data.data);
            }
        } catch (error) {
            console.error('❌ خطا در بارگذاری مقاله:', error);
            this.showError('خطا در بارگذاری مقاله');
        }
    }
    
    showArticleModal(article) {
        const modalHTML = `
            <div class="modal" id="articleModal">
                <div class="modal-content">
                    <div class="modal-header">
                        <h2>${article.title}</h2>
                        <button class="modal-close" onclick="app.closeModal()">
                            <i class="bi bi-x-lg"></i>
                        </button>
                    </div>
                    
                    <div class="modal-body">
                        <div class="article-meta">
                            <span class="article-category">${article.category}</span>
                            <span>${this.formatDate(article.created_at)}</span>
                            <span>${article.author}</span>
                        </div>
                        
                        <div class="article-content">
                            ${article.content}
                        </div>
                        
                        <div class="article-footer">
                            <div class="article-stats">
                                <span>
                                    <i class="bi bi-eye"></i>
                                    ${this.formatNumber(article.views)} بازدید
                                </span>
                                <span>
                                    <i class="bi bi-heart"></i>
                                    ${this.formatNumber(article.likes)} پسندیده
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // نمایش modal
        setTimeout(() => {
            const modal = document.getElementById('articleModal');
            if (modal) modal.classList.add('show');
        }, 10);
    }
    
    closeModal() {
        const modal = document.getElementById('articleModal');
        if (modal) {
            modal.classList.remove('show');
            setTimeout(() => modal.remove(), 300);
        }
    }
    
    showError(message) {
        alert(`خطا: ${message}`);
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
    
    setupEventListeners() {
        // جستجو
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.searchArticles(e.target.value);
                }, 500);
            });
        }
    }
    
    async searchArticles(query) {
        if (!query || query.length < 2) {
            this.loadArticles();
            return;
        }
        
        try {
            const response = await fetch(`/api/articles/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.renderArticles(data.data);
                this.renderPagination(data.pagination);
            }
        } catch (error) {
            console.error('❌ خطا در جستجو:', error);
        }
    }
}

// راه‌اندازی اپلیکیشن
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new NatiqApp();
    window.app = app;
});
