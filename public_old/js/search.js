/**
 * 🔍 ماژول جستجوی هوشمند نطق مصطلح
 */

class NatiqSearch {
    constructor() {
        this.baseUrl = window.location.origin;
        this.searchTimeout = null;
        this.currentSearchId = null;
        this.searchHistory = JSON.parse(localStorage.getItem('natiq_search_history') || '[]');
        this.searchStats = {
            totalSearches: 0,
            lastQuery: null,
            popularQueries: []
        };
        
        this.init();
    }
    
    init() {
        console.log('🔍 ماژول جستجوی هوشمند راه‌اندازی شد');
        this.setupSearchUI();
        this.loadSearchHistory();
        this.updateSearchStats();
    }
    
    setupSearchUI() {
        const searchInput = document.getElementById('search-input');
        if (!searchInput) return;
        
        // ایجاد container برای پیشنهادات
        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.id = 'search-suggestions';
        suggestionsContainer.className = 'search-suggestions';
        searchInput.parentNode.appendChild(suggestionsContainer);
        
        // رویداد input برای پیشنهادات
        searchInput.addEventListener('input', (e) => {
            this.handleInput(e.target.value);
        });
        
        // رویداد focus
        searchInput.addEventListener('focus', () => {
            if (searchInput.value.length >= 2) {
                this.showSuggestions(searchInput.value);
            }
        });
        
        // رویداد keypress برای Enter
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch(searchInput.value);
            }
        });
        
        // اضافه کردن دکمه جستجوی پیشرفته
        const advancedBtn = document.createElement('button');
        advancedBtn.innerHTML = '<i class="fas fa-sliders-h"></i>';
        advancedBtn.className = 'search-advanced-btn';
        advancedBtn.title = 'جستجوی پیشرفته';
        advancedBtn.onclick = () => this.showAdvancedSearch();
        searchInput.parentNode.appendChild(advancedBtn);
        
        // اضافه کردن استایل‌ها
        this.addSearchStyles();
    }
    
    addSearchStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .search-suggestions {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                max-height: 300px;
                overflow-y: auto;
                z-index: 1000;
                display: none;
            }
            
            .search-suggestions.show {
                display: block;
            }
            
            .suggestion-item {
                padding: 12px 16px;
                cursor: pointer;
                border-bottom: 1px solid #f0f0f0;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            
            .suggestion-item:hover {
                background: #f8f9fa;
            }
            
            .suggestion-text {
                flex: 1;
            }
            
            .suggestion-type {
                font-size: 0.8rem;
                color: #666;
                background: #e9ecef;
                padding: 2px 8px;
                border-radius: 4px;
                margin-right: 8px;
            }
            
            .search-advanced-btn {
                position: absolute;
                left: 10px;
                top: 50%;
                transform: translateY(-50%);
                background: none;
                border: none;
                color: #666;
                cursor: pointer;
                padding: 8px;
                border-radius: 4px;
            }
            
            .search-advanced-btn:hover {
                background: #f0f0f0;
                color: #333;
            }
            
            .search-results-summary {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
            }
            
            .search-inference {
                background: #e8f4fd;
                border-right: 4px solid #2196f3;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }
            
            .search-reasoning {
                background: #f0f8ff;
                padding: 12px;
                border-radius: 6px;
                margin: 10px 0;
                font-size: 0.9rem;
            }
            
            .search-reason {
                margin: 5px 0;
                padding-right: 20px;
                position: relative;
            }
            
            .search-reason:before {
                content: "•";
                position: absolute;
                right: 0;
                color: #2196f3;
            }
            
            .search-stats {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
                margin: 15px 0;
            }
            
            .search-stat {
                background: white;
                padding: 10px 15px;
                border-radius: 6px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            .search-mode-badge {
                display: inline-block;
                background: #4361ee;
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.8rem;
                margin-right: 5px;
            }
        `;
        document.head.appendChild(style);
    }
    
    async handleInput(query) {
        clearTimeout(this.searchTimeout);
        
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        this.searchTimeout = setTimeout(async () => {
            await this.showSuggestions(query);
        }, 300);
    }
    
    async showSuggestions(query) {
        try {
            const response = await fetch(`${this.baseUrl}/api/search/suggest?q=${encodeURIComponent(query)}`);
            const data = await response.json();
            
            if (data.success) {
                this.displaySuggestions(data, query);
            }
        } catch (error) {
            console.error('خطا در دریافت پیشنهادات:', error);
        }
    }
    
    displaySuggestions(data, query) {
        const container = document.getElementById('search-suggestions');
        if (!container) return;
        
        let html = '';
        
        // پیشنهادات جستجو
        if (data.suggestions && data.suggestions.length > 0) {
            html += '<div class="suggestion-section">';
            data.suggestions.forEach(suggestion => {
                html += `
                    <div class="suggestion-item" onclick="searchModule.selectSuggestion('${suggestion}')">
                        <span class="suggestion-text">${suggestion}</span>
                        <span class="suggestion-type">پیشنهاد</span>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        // جستجوهای پرطرفدار
        if (data.popular && data.popular.length > 0) {
            html += '<div class="suggestion-section">';
            html += '<div style="padding: 10px 16px; color: #666; font-size: 0.9rem; border-top: 1px solid #eee;">جستجوهای پرطرفدار</div>';
            data.popular.forEach(item => {
                html += `
                    <div class="suggestion-item" onclick="searchModule.selectSuggestion('${item.query}')">
                        <span class="suggestion-text">${item.query}</span>
                        <span class="suggestion-type">${item.count} بار</span>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        // جستجوهای اخیر از تاریخچه
        const recentSearches = this.searchHistory
            .filter(s => s.query.toLowerCase().includes(query.toLowerCase()))
            .slice(0, 3);
        
        if (recentSearches.length > 0) {
            html += '<div class="suggestion-section">';
            html += '<div style="padding: 10px 16px; color: #666; font-size: 0.9rem; border-top: 1px solid #eee;">جستجوهای اخیر</div>';
            recentSearches.forEach(item => {
                html += `
                    <div class="suggestion-item" onclick="searchModule.selectSuggestion('${item.query}')">
                        <span class="suggestion-text">${item.query}</span>
                        <span class="suggestion-type">اخیر</span>
                    </div>
                `;
            });
            html += '</div>';
        }
        
        container.innerHTML = html || '<div class="suggestion-item">پیشنهادی یافت نشد</div>';
        container.classList.add('show');
    }
    
    hideSuggestions() {
        const container = document.getElementById('search-suggestions');
        if (container) {
            container.classList.remove('show');
        }
    }
    
    selectSuggestion(query) {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = query;
            searchInput.focus();
            this.performSearch(query);
        }
        this.hideSuggestions();
    }
    
    async performSearch(query, options = {}) {
        if (!query || query.trim().length < 2) {
            this.showMessage('لطفا عبارت جستجو را وارد کنید (حداقل ۲ کاراکتر)', 'warning');
            return;
        }
        
        // ذخیره در تاریخچه
        this.addToHistory(query);
        
        // نمایش حالت بارگذاری
        this.showLoading();
        
        try {
            const mode = options.advanced ? 'advanced' : 'quick';
            let url = `${this.baseUrl}/api/search?q=${encodeURIComponent(query)}&mode=${mode}`;
            
            // اضافه کردن پارامترهای پیشرفته
            if (options.advanced) {
                const params = new URLSearchParams();
                if (options.category) params.append('category', options.category);
                if (options.minViews) params.append('minViews', options.minViews);
                if (options.minLikes) params.append('minLikes', options.minLikes);
                if (options.dateFrom) params.append('dateFrom', options.dateFrom);
                if (options.dateTo) params.append('dateTo', options.dateTo);
                if (options.featured) params.append('featured', 'true');
                if (options.sortBy) params.append('sortBy', options.sortBy);
                
                url += '&' + params.toString();
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.success) {
                this.displaySearchResults(data);
                this.currentSearchId = data.metadata?.searchId;
                this.updateSearchStats();
            } else {
                this.showMessage(data.error || 'خطا در جستجو', 'error');
            }
        } catch (error) {
            console.error('❌ خطا در جستجو:', error);
            this.showMessage('خطا در ارتباط با سرور', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    displaySearchResults(data) {
        // پنهان کردن لیست مقالات معمولی
        const articlesContainer = document.getElementById('articles-container');
        const pagination = document.getElementById('pagination');
        
        if (articlesContainer) articlesContainer.style.display = 'none';
        if (pagination) pagination.style.display = 'none';
        
        // ایجاد container نتایج جستجو
        let resultsContainer = document.getElementById('search-results-container');
        if (!resultsContainer) {
            resultsContainer = document.createElement('div');
            resultsContainer.id = 'search-results-container';
            const articlesSection = document.querySelector('.articles-section');
            if (articlesSection) {
                const articleGrid = articlesSection.querySelector('.article-grid');
                if (articleGrid) {
                    articleGrid.parentNode.insertBefore(resultsContainer, articleGrid);
                }
            }
        }
        
        // نمایش خلاصه جستجو
        let html = `
            <div class="search-results-summary">
                <h3>
                    <i class="fas fa-search"></i>
                    نتایج جستجو برای: "${data.query}"
                    <span class="search-mode-badge">${data.metadata?.optionsUsed ? 'پیشرفته' : 'سریع'}</span>
                </h3>
                
                <div class="search-stats">
                    <div class="search-stat">
                        <i class="fas fa-file-alt"></i>
                        ${data.totalResults} مقاله یافت شد
                    </div>
                    <div class="search-stat">
                        <i class="fas fa-clock"></i>
                        ${data.metadata?.searchTime || 'کمتر از 1s'}
                    </div>
                    <div class="search-stat">
                        <i class="fas fa-brain"></i>
                        ${data.metadata?.queryComplexity?.level || 'ساده'}
                    </div>
                </div>
                
                ${data.inference ? `
                    <div class="search-inference">
                        <h4><i class="fas fa-lightbulb"></i> استنتاج سیستم:</h4>
                        <p>${data.inference.summary}</p>
                        
                        ${data.inference.insights ? `
                            <div style="margin-top: 10px;">
                                ${data.inference.insights.map(insight => `
                                    <div style="margin: 5px 0; padding-right: 15px; position: relative;">
                                        <i class="fas fa-chevron-left" style="position: absolute; right: 0; top: 5px; color: #2196f3;"></i>
                                        ${insight}
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                        
                        ${data.inference.recommendations ? `
                            <div style="margin-top: 10px; padding: 10px; background: rgba(33, 150, 243, 0.1); border-radius: 6px;">
                                <strong>توصیه‌ها:</strong>
                                ${data.inference.recommendations.map(rec => `
                                    <div style="margin: 5px 0;">${rec}</div>
                                `).join('')}
                            </div>
                        ` : ''}
                    </div>
                ` : ''}
            </div>
        `;
        
        // نمایش نتایج
        if (data.results && data.results.length > 0) {
            html += '<div class="search-results-list">';
            
            data.results.forEach((result, index) => {
                const article = result.article;
                
                html += `
                    <div class="article-card search-result-card">
                        <div class="article-content">
                            <div class="article-meta">
                                <span class="article-category">${article.category}</span>
                                <span class="article-date">${this.formatDate(article.created_at)}</span>
                                <span class="article-score" style="background: #4caf50; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">
                                    ${(parseFloat(result.score) * 100).toFixed(0)}% مرتبط
                                </span>
                            </div>
                            
                            <h3 class="article-title">
                                ${index + 1}. ${article.title}
                            </h3>
                            
                            <p class="article-excerpt">${article.excerpt}</p>
                            
                            ${result.reasons && result.reasons.length > 0 ? `
                                <div class="search-reasoning">
                                    <strong><i class="fas fa-check-circle"></i> دلایل مرتبط بودن:</strong>
                                    ${result.reasons.map(reason => `
                                        <div class="search-reason">${reason}</div>
                                    `).join('')}
                                </div>
                            ` : ''}
                            
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
                `;
            });
            
            html += '</div>';
            
            // دکمه بازگشت به مقالات
            html += `
                <div style="text-align: center; margin: 30px 0;">
                    <button class="btn btn-secondary" onclick="searchModule.clearSearchResults()">
                        <i class="fas fa-arrow-right"></i>
                        بازگشت به همه مقالات
                    </button>
                </div>
            `;
        } else {
            html += `
                <div class="empty-state">
                    <i class="fas fa-search-minus"></i>
                    <h3>مقاله‌ای یافت نشد</h3>
                    <p>${data.inference?.summary || 'هیچ مقاله‌ای با جستجوی شما مطابقت نداشت.'}</p>
                    
                    ${data.inference?.suggestions ? `
                        <div style="margin-top: 20px;">
                            <h4>پیشنهادها:</h4>
                            ${data.inference.suggestions.map(suggestion => `
                                <div style="margin: 5px 0;">${suggestion}</div>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    ${data.inference?.relatedTopics ? `
                        <div style="margin-top: 20px;">
                            <h4>موضوعات مرتبط:</h4>
                            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                                ${data.inference.relatedTopics.map(topic => `
                                    <button class="btn btn-sm btn-outline" onclick="searchModule.performSearch('${topic}')">
                                        ${topic}
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        resultsContainer.innerHTML = html;
        resultsContainer.style.display = 'block';
        
        // اسکرول به نتایج
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    clearSearchResults() {
        const resultsContainer = document.getElementById('search-results-container');
        const articlesContainer = document.getElementById('articles-container');
        const pagination = document.getElementById('pagination');
        
        if (resultsContainer) {
            resultsContainer.style.display = 'none';
            resultsContainer.innerHTML = '';
        }
        
        if (articlesContainer) {
            articlesContainer.style.display = 'grid';
            articlesContainer.scrollIntoView({ behavior: 'smooth' });
        }
        
        if (pagination) {
            pagination.style.display = 'flex';
        }
        
        // پاک کردن فیلد جستجو
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = '';
        }
    }
    
    showAdvancedSearch() {
        // ایجاد مدال جستجوی پیشرفته
        const modalHTML = `
            <div class="modal-overlay" id="advanced-search-modal">
                <div class="modal-content" style="max-width: 500px;">
                    <div class="modal-header">
                        <h3><i class="fas fa-sliders-h"></i> جستجوی پیشرفته</h3>
                        <button class="modal-close" onclick="searchModule.closeAdvancedSearch()">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                    
                    <div class="modal-body">
                        <form id="advanced-search-form">
                            <div style="margin-bottom: 15px;">
                                <label>عبارت جستجو:</label>
                                <input type="text" 
                                       id="advanced-query" 
                                       class="search-input" 
                                       placeholder="موضوع مورد نظر..."
                                       required>
                            </div>
                            
                            <div style="margin-bottom: 15px;">
                                <label>دسته‌بندی:</label>
                                <select id="advanced-category" class="category-select">
                                    <option value="">همه دسته‌بندی‌ها</option>
                                    <option value="آموزش">آموزش</option>
                                    <option value="پروژه">پروژه</option>
                                    <option value="تحلیل">تحلیل</option>
                                    <option value="اخبار">اخبار</option>
                                    <option value="کتابخانه">کتابخانه</option>
                                    <option value="توسعه">توسعه</option>
                                </select>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                                <div>
                                    <label>حداقل بازدید:</label>
                                    <input type="number" 
                                           id="advanced-min-views" 
                                           class="search-input" 
                                           placeholder="مثلاً 100"
                                           min="0">
                                </div>
                                
                                <div>
                                    <label>حداقل لایک:</label>
                                    <input type="number" 
                                           id="advanced-min-likes" 
                                           class="search-input" 
                                           placeholder="مثلاً 10"
                                           min="0">
                                </div>
                            </div>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 15px;">
                                <div>
                                    <label>از تاریخ:</label>
                                    <input type="date" 
                                           id="advanced-date-from" 
                                           class="search-input">
                                </div>
                                
                                <div>
                                    <label>تا تاریخ:</label>
                                    <input type="date" 
                                           id="advanced-date-to" 
                                           class="search-input">
                                </div>
                            </div>
                            
                            <div style="margin-bottom: 15px;">
                                <label>
                                    <input type="checkbox" id="advanced-featured">
                                    فقط مقالات ویژه
                                </label>
                            </div>
                            
                            <div style="margin-bottom: 20px;">
                                <label>مرتب‌سازی بر اساس:</label>
                                <select id="advanced-sort-by" class="category-select">
                                    <option value="relevance">مرتبط‌ترین</option>
                                    <option value="views">پر بازدیدترین</option>
                                    <option value="likes">پر لایک‌ترین</option>
                                    <option value="date">جدیدترین</option>
                                </select>
                            </div>
                        </form>
                    </div>
                    
                    <div class="modal-footer">
                        <button class="btn btn-secondary" onclick="searchModule.closeAdvancedSearch()">
                            انصراف
                        </button>
                        <button class="btn btn-primary" onclick="searchModule.submitAdvancedSearch()">
                            <i class="fas fa-search"></i>
                            جستجوی پیشرفته
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        // حذف مدال قبلی
        const existingModal = document.getElementById('advanced-search-modal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // اضافه کردن مدال جدید
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // تنظیم تاریخ‌های پیش‌فرض
        const today = new Date().toISOString().split('T')[0];
        const threeMonthsAgo = new Date();
        threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
        const threeMonthsAgoStr = threeMonthsAgo.toISOString().split('T')[0];
        
        const dateFromInput = document.getElementById('advanced-date-from');
        const dateToInput = document.getElementById('advanced-date-to');
        
        if (dateFromInput) dateFromInput.value = threeMonthsAgoStr;
        if (dateToInput) dateToInput.value = today;
        
        // پر کردن فیلد جستجو با مقدار فعلی
        const searchInput = document.getElementById('search-input');
        const advancedQueryInput = document.getElementById('advanced-query');
        if (searchInput && advancedQueryInput && searchInput.value) {
            advancedQueryInput.value = searchInput.value;
        }
    }
    
    closeAdvancedSearch() {
        const modal = document.getElementById('advanced-search-modal');
        if (modal) {
            modal.remove();
        }
    }
    
    submitAdvancedSearch() {
        const query = document.getElementById('advanced-query')?.value;
        const category = document.getElementById('advanced-category')?.value;
        const minViews = document.getElementById('advanced-min-views')?.value;
        const minLikes = document.getElementById('advanced-min-likes')?.value;
        const dateFrom = document.getElementById('advanced-date-from')?.value;
        const dateTo = document.getElementById('advanced-date-to')?.value;
        const featured = document.getElementById('advanced-featured')?.checked;
        const sortBy = document.getElementById('advanced-sort-by')?.value;
        
        if (!query || query.length < 2) {
            this.showMessage('لطفا عبارت جستجو را وارد کنید (حداقل ۲ کاراکتر)', 'warning');
            return;
        }
        
        const options = {
            advanced: true,
            category: category || null,
            minViews: minViews ? parseInt(minViews) : null,
            minLikes: minLikes ? parseInt(minLikes) : null,
            dateFrom: dateFrom || null,
            dateTo: dateTo || null,
            featured: featured || false,
            sortBy: sortBy || 'relevance'
        };
        
        this.performSearch(query, options);
        this.closeAdvancedSearch();
    }
    
    addToHistory(query) {
        const timestamp = new Date().toISOString();
        const searchItem = { query, timestamp };
        
        // حذف اگر قبلا وجود دارد
        this.searchHistory = this.searchHistory.filter(item => item.query !== query);
        
        // اضافه کردن به ابتدای لیست
        this.searchHistory.unshift(searchItem);
        
        // محدود کردن به 50 آیتم
        this.searchHistory = this.searchHistory.slice(0, 50);
        
        // ذخیره در localStorage
        localStorage.setItem('natiq_search_history', JSON.stringify(this.searchHistory));
        
        // به‌روزرسانی آمار
        this.searchStats.totalSearches++;
        this.searchStats.lastQuery = query;
    }
    
    loadSearchHistory() {
        try {
            this.searchHistory = JSON.parse(localStorage.getItem('natiq_search_history') || '[]');
        } catch (error) {
            this.searchHistory = [];
        }
    }
    
    async updateSearchStats() {
        try {
            const response = await fetch(`${this.baseUrl}/api/search/stats`);
            const data = await response.json();
            
            if (data.success) {
                this.searchStats = {
                    ...this.searchStats,
                    ...data.stats
                };
            }
        } catch (error) {
            // ignore
        }
    }
    
    showLoading() {
        // ایجاد overlay بارگذاری
        let loadingOverlay = document.getElementById('search-loading');
        if (!loadingOverlay) {
            loadingOverlay = document.createElement('div');
            loadingOverlay.id = 'search-loading';
            loadingOverlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.8);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                flex-direction: column;
            `;
            loadingOverlay.innerHTML = `
                <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                    <span class="visually-hidden">در حال جستجو...</span>
                </div>
                <div style="margin-top: 20px; font-size: 1.1rem; color: #333;">
                    <i class="fas fa-search"></i>
                    در حال جستجوی هوشمند...
                </div>
                <div style="margin-top: 10px; color: #666; font-size: 0.9rem;">
                    سیستم در حال تحلیل معنایی و استنتاج است
                </div>
            `;
            document.body.appendChild(loadingOverlay);
            
            // اضافه کردن استایل spinner
            if (!document.querySelector('#spinner-styles')) {
                const style = document.createElement('style');
                style.id = 'spinner-styles';
                style.textContent = `
                    @keyframes spinner-border {
                        to { transform: rotate(360deg); }
                    }
                    
                    .spinner-border {
                        display: inline-block;
                        width: 2rem;
                        height: 2rem;
                        vertical-align: text-bottom;
                        border: 0.25em solid currentColor;
                        border-right-color: transparent;
                        border-radius: 50%;
                        animation: spinner-border .75s linear infinite;
                    }
                    
                    .spinner-border.text-primary {
                        color: #4361ee;
                    }
                `;
                document.head.appendChild(style);
            }
        }
    }
    
    hideLoading() {
        const loadingOverlay = document.getElementById('search-loading');
        if (loadingOverlay) {
            loadingOverlay.remove();
        }
    }
    
    showMessage(text, type = 'info') {
        // ایجاد پیام
        const message = document.createElement('div');
        message.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: ${type === 'error' ? '#f8d7da' : type === 'warning' ? '#fff3cd' : '#d1ecf1'};
            color: ${type === 'error' ? '#721c24' : type === 'warning' ? '#856404' : '#0c5460'};
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            border: 1px solid ${type === 'error' ? '#f5c6cb' : type === 'warning' ? '#ffeaa7' : '#bee5eb'};
            display: flex;
            align-items: center;
            gap: 10px;
            animation: slideDown 0.3s ease;
        `;
        
        const icon = type === 'error' ? 'exclamation-circle' : 
                    type === 'warning' ? 'exclamation-triangle' : 'info-circle';
        
        message.innerHTML = `
            <i class="fas fa-${icon}"></i>
            <span>${text}</span>
            <button onclick="this.parentElement.remove()" style="background: none; border: none; color: inherit; cursor: pointer; margin-right: auto;">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        document.body.appendChild(message);
        
        // حذف خودکار پس از 5 ثانیه
        setTimeout(() => {
            if (message.parentElement) {
                message.remove();
            }
        }, 5000);
        
        // اضافه کردن انیمیشن
        if (!document.querySelector('#message-animation')) {
            const style = document.createElement('style');
            style.id = 'message-animation';
            style.textContent = `
                @keyframes slideDown {
                    from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
                    to { transform: translateX(-50%) translateY(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
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
}

// ایجاد نمونه جستجو
let searchModule;
document.addEventListener('DOMContentLoaded', () => {
    searchModule = new NatiqSearch();
    window.searchModule = searchModule;
    
    // اضافه کردن به app اصلی
    if (window.app) {
        window.app.search = searchModule;
    }
});
