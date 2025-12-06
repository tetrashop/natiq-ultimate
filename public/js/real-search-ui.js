/**
 * 🎨 رابط کاربری جستجوی واقعی نطق مصطلح
 */

class RealSearchUI {
    constructor() {
        this.baseUrl = window.location.origin;
        this.isSearching = false;
        this.currentSearch = null;
        this.searchHistory = [];
        this.init();
    }
    
    init() {
        console.log('🎨 رابط کاربری جستجوی واقعی راه‌اندازی شد');
        this.setupSearchInterface();
        this.loadSearchHistory();
        this.setupEventListeners();
    }
    
    setupSearchInterface() {
        // بهبود فیلد جستجو
        const searchInput = document.getElementById('search-input');
        if (!searchInput) return;
        
        // ایجاد container جستجو
        const searchContainer = document.createElement('div');
        searchContainer.className = 'real-search-container';
        searchInput.parentNode.insertBefore(searchContainer, searchInput);
        searchContainer.appendChild(searchInput);
        
        // اضافه کردن دکمه جستجو
        const searchButton = document.createElement('button');
        searchButton.className = 'real-search-button';
        searchButton.innerHTML = '<i class="fas fa-search"></i>';
        searchButton.onclick = () => this.executeSearch(searchInput.value);
        searchContainer.appendChild(searchButton);
        
        // اضافه کردن دکمه جستجوی پیشرفته
        const advancedButton = document.createElement('button');
        advancedButton.className = 'real-search-advanced-button';
        advancedButton.innerHTML = '<i class="fas fa-sliders-h"></i>';
        advancedButton.title = 'جستجوی پیشرفته';
        advancedButton.onclick = () => this.showAdvancedSearchPanel();
        searchContainer.appendChild(advancedButton);
        
        // ایجاد container پیشنهادات
        const suggestionsContainer = document.createElement('div');
        suggestionsContainer.className = 'real-search-suggestions';
        suggestionsContainer.id = 'real-search-suggestions';
        searchContainer.appendChild(suggestionsContainer);
        
        // اضافه کردن استایل‌ها
        this.addSearchStyles();
        
        // اضافه کردن container نتایج جستجو
        const resultsContainer = document.createElement('div');
        resultsContainer.className = 'real-search-results';
        resultsContainer.id = 'real-search-results';
        const mainContent = document.querySelector('main') || document.body;
        mainContent.insertBefore(resultsContainer, mainContent.firstChild);
    }
    
    addSearchStyles() {
        const style = document.createElement('style');
        style.textContent = `
            /* استایل‌های جستجوی واقعی */
            .real-search-container {
                position: relative;
                display: flex;
                align-items: center;
                background: white;
                border: 2px solid #4361ee;
                border-radius: 50px;
                padding: 5px;
                box-shadow: 0 4px 12px rgba(67, 97, 238, 0.15);
                transition: all 0.3s ease;
                max-width: 800px;
                margin: 0 auto;
            }
            
            .real-search-container:focus-within {
                box-shadow: 0 6px 20px rgba(67, 97, 238, 0.25);
                border-color: #3a0ca3;
            }
            
            #search-input {
                flex: 1;
                border: none;
                padding: 12px 20px;
                font-size: 1.1rem;
                background: transparent;
                outline: none;
                width: 100%;
            }
            
            .real-search-button {
                background: #4361ee;
                color: white;
                border: none;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
                transition: all 0.3s ease;
                margin-left: 5px;
            }
            
            .real-search-button:hover {
                background: #3a0ca3;
                transform: scale(1.05);
            }
            
            .real-search-advanced-button {
                background: transparent;
                color: #666;
                border: none;
                width: 40px;
                height: 40px;
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1rem;
                transition: all 0.3s ease;
                margin-right: 5px;
            }
            
            .real-search-advanced-button:hover {
                background: #f0f0f0;
                color: #333;
            }
            
            .real-search-suggestions {
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: white;
                border: 1px solid #ddd;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.15);
                max-height: 400px;
                overflow-y: auto;
                z-index: 1000;
                display: none;
                margin-top: 10px;
            }
            
            .real-search-suggestions.show {
                display: block;
                animation: slideDown 0.3s ease;
            }
            
            @keyframes slideDown {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .suggestion-item {
                padding: 12px 20px;
                cursor: pointer;
                border-bottom: 1px solid #f5f5f5;
                display: flex;
                align-items: center;
                transition: all 0.2s ease;
            }
            
            .suggestion-item:hover {
                background: #f8f9fa;
                padding-right: 25px;
            }
            
            .suggestion-icon {
                width: 30px;
                height: 30px;
                background: #e9ecef;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-left: 10px;
                color: #4361ee;
            }
            
            .suggestion-content {
                flex: 1;
            }
            
            .suggestion-title {
                font-weight: 600;
                color: #333;
                margin-bottom: 3px;
            }
            
            .suggestion-meta {
                font-size: 0.85rem;
                color: #666;
                display: flex;
                gap: 10px;
            }
            
            .suggestion-type {
                background: #e0e7ff;
                color: #3730a3;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.75rem;
            }
            
            .real-search-results {
                display: none;
                animation: fadeIn 0.5s ease;
            }
            
            .real-search-results.show {
                display: block;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            /* استایل‌های نتایج جستجو */
            .search-results-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                margin-bottom: 30px;
                text-align: center;
            }
            
            .search-results-stats {
                display: flex;
                justify-content: center;
                gap: 30px;
                flex-wrap: wrap;
                margin-top: 20px;
            }
            
            .search-stat {
                background: rgba(255, 255, 255, 0.2);
                padding: 10px 20px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            
            .search-inference-card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 30px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                border-right: 5px solid #4361ee;
            }
            
            .search-result-card {
                background: white;
                border-radius: 15px;
                padding: 25px;
                margin-bottom: 20px;
                box-shadow: 0 3px 10px rgba(0,0,0,0.08);
                transition: all 0.3s ease;
                border: 1px solid #eee;
            }
            
            .search-result-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                border-color: #4361ee;
            }
            
            .result-score {
                position: absolute;
                top: 20px;
                left: 20px;
                background: #4caf50;
                color: white;
                width: 50px;
                height: 50px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 1.1rem;
                box-shadow: 0 3px 10px rgba(76, 175, 80, 0.3);
            }
            
            .highlight {
                background: #fff3cd;
                padding: 2px 4px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            .match-details {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 15px 0;
            }
            
            .match-badge {
                background: #e0e7ff;
                color: #3730a3;
                padding: 5px 12px;
                border-radius: 20px;
                font-size: 0.85rem;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            /* پنل جستجوی پیشرفته */
            .advanced-search-panel {
                position: fixed;
                top: 0;
                right: -400px;
                width: 380px;
                height: 100vh;
                background: white;
                box-shadow: -5px 0 25px rgba(0,0,0,0.1);
                z-index: 10000;
                transition: right 0.3s ease;
                overflow-y: auto;
                padding: 20px;
            }
            
            .advanced-search-panel.show {
                right: 0;
            }
            
            .advanced-search-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0,0,0,0.5);
                z-index: 9999;
                display: none;
            }
            
            .advanced-search-overlay.show {
                display: block;
                animation: fadeIn 0.3s ease;
            }
            
            /* انیمیشن‌ها */
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            
            .pulse {
                animation: pulse 2s infinite;
            }
            
            /* رسپانسیو */
            @media (max-width: 768px) {
                .real-search-container {
                    border-radius: 25px;
                    padding: 3px;
                }
                
                #search-input {
                    padding: 10px 15px;
                    font-size: 1rem;
                }
                
                .real-search-button {
                    width: 45px;
                    height: 45px;
                }
                
                .advanced-search-panel {
                    width: 100%;
                    right: -100%;
                }
                
                .search-results-stats {
                    gap: 15px;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    setupEventListeners() {
        // رویدادهای جستجو
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            // Input برای پیشنهادات
            searchInput.addEventListener('input', (e) => {
                this.handleSearchInput(e.target.value);
            });
            
            // Enter برای جستجو
            searchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.executeSearch(searchInput.value);
                }
            });
            
            // Focus برای نمایش تاریخچه
            searchInput.addEventListener('focus', () => {
                if (searchInput.value.length >= 2) {
                    this.showQuickSuggestions(searchInput.value);
                } else {
                    this.showSearchHistory();
                }
            });
        }
        
        // کلیک خارج از پیشنهادات برای پنهان کردن
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.real-search-container')) {
                this.hideSuggestions();
            }
        });
    }
    
    handleSearchInput(query) {
        clearTimeout(this.inputTimeout);
        
        if (query.length < 2) {
            this.hideSuggestions();
            return;
        }
        
        this.inputTimeout = setTimeout(() => {
            this.showQuickSuggestions(query);
        }, 300);
    }
    
    async showQuickSuggestions(query) {
        if (this.isSearching) return;
        
        try {
            const response = await fetch(`${this.baseUrl}/api/search/quick?q=${encodeURIComponent(query)}&limit=6`);
            const data = await response.json();
            
            if (data.success) {
                this.displaySuggestions(data);
            }
        } catch (error) {
            console.error('خطا در دریافت پیشنهادات:', error);
        }
    }
    
    displaySuggestions(data) {
        const container = document.getElementById('real-search-suggestions');
        if (!container) return;
        
        let html = '';
        
        // مقالات پیشنهادی
        if (data.suggestions && data.suggestions.length > 0) {
            data.suggestions.forEach(suggestion => {
                const icon = suggestion.type === 'عنوان' ? 'fa-heading' : 'fa-file-alt';
                
                html += `
                    <div class="suggestion-item" onclick="realSearchUI.selectSuggestion('${suggestion.text}')">
                        <div class="suggestion-icon">
                            <i class="fas ${icon}"></i>
                        </div>
                        <div class="suggestion-content">
                            <div class="suggestion-title">${suggestion.text}</div>
                            <div class="suggestion-meta">
                                <span>${suggestion.category}</span>
                                <span class="suggestion-type">${suggestion.type}</span>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        
        // کلمات کلیدی مرتبط
        if (data.relatedKeywords && data.relatedKeywords.length > 0) {
            html += '<div style="padding: 15px 20px; color: #666; font-weight: 600; border-top: 1px solid #eee;">کلمات کلیدی مرتبط</div>';
            data.relatedKeywords.forEach(keyword => {
                html += `
                    <div class="suggestion-item" onclick="realSearchUI.selectSuggestion('${keyword}')">
                        <div class="suggestion-icon">
                            <i class="fas fa-hashtag"></i>
                        </div>
                        <div class="suggestion-content">
                            <div class="suggestion-title">${keyword}</div>
                        </div>
                    </div>
                `;
            });
        }
        
        // جستجوهای پرطرفدار
        if (data.popular && data.popular.length > 0) {
            html += '<div style="padding: 15px 20px; color: #666; font-weight: 600; border-top: 1px solid #eee;">جستجوهای پرطرفدار</div>';
            data.popular.forEach(item => {
                html += `
                    <div class="suggestion-item" onclick="realSearchUI.selectSuggestion('${item.query}')">
                        <div class="suggestion-icon">
                            <i class="fas fa-fire"></i>
                        </div>
                        <div class="suggestion-content">
                            <div class="suggestion-title">${item.query}</div>
                            <div class="suggestion-meta">
                                <span>${item.count} بار جستجو شده</span>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        
        container.innerHTML = html || '<div style="padding: 20px; text-align: center; color: #666;">پیشنهادی یافت نشد</div>';
        container.classList.add('show');
    }
    
    showSearchHistory() {
        const container = document.getElementById('real-search-suggestions');
        if (!container) return;
        
        if (this.searchHistory.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        let html = '<div style="padding: 15px 20px; color: #666; font-weight: 600;">جستجوهای اخیر</div>';
        
        this.searchHistory.slice(0, 8).forEach(item => {
            const timeAgo = this.getTimeAgo(item.timestamp);
            
            html += `
                <div class="suggestion-item" onclick="realSearchUI.selectSuggestion('${item.query}')">
                    <div class="suggestion-icon">
                        <i class="fas fa-history"></i>
                    </div>
                    <div class="suggestion-content">
                        <div class="suggestion-title">${item.query}</div>
                        <div class="suggestion-meta">
                            <span>${timeAgo}</span>
                        </div>
                    </div>
                    <button onclick="event.stopPropagation(); realSearchUI.removeFromHistory('${item.query}')" 
                            style="background: none; border: none; color: #999; cursor: pointer; padding: 5px;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
        });
        
        html += `
            <div style="padding: 10px 20px; border-top: 1px solid #eee;">
                <button onclick="realSearchUI.clearHistory()" 
                        style="background: none; border: none; color: #666; cursor: pointer; width: 100%; text-align: center; padding: 10px;">
                    <i class="fas fa-trash"></i> پاک کردن تاریخچه
                </button>
            </div>
        `;
        
        container.innerHTML = html;
        container.classList.add('show');
    }
    
    hideSuggestions() {
        const container = document.getElementById('real-search-suggestions');
        if (container) {
            container.classList.remove('show');
        }
    }
    
    selectSuggestion(query) {
        const searchInput = document.getElementById('search-input');
        if (searchInput) {
            searchInput.value = query;
            searchInput.focus();
            this.executeSearch(query);
        }
        this.hideSuggestions();
    }
    
    async executeSearch(query, options = {}) {
        if (!query || query.trim().length < 2) {
            this.showMessage('لطفاً عبارت جستجو را وارد کنید (حداقل ۲ کاراکتر)', 'warning');
            return;
        }
        
        if (this.isSearching) return;
        
        this.isSearching = true;
        this.currentSearch = query;
        
        // افزودن به تاریخچه
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
                if (options.limit) params.append('limit', options.limit);
                
                url += '&' + params.toString();
            }
            
            const response = await fetch(url);
            const data = await response.json();
            
            if (data.success) {
                this.displaySearchResults(data);
            } else {
                this.showMessage(data.error || 'خطا در جستجو', 'error');
            }
        } catch (error) {
            console.error('❌ خطا در جستجو:', error);
            this.showMessage('خطا در ارتباط با سرور', 'error');
        } finally {
            this.isSearching = false;
            this.hideLoading();
            this.hideSuggestions();
        }
    }
    
    displaySearchResults(data) {
        // پنهان کردن مقالات اصلی
        const articlesContainer = document.getElementById('articles-container');
        const pagination = document.getElementById('pagination');
        const heroSection = document.querySelector('.hero');
        
        if (articlesContainer) articlesContainer.style.display = 'none';
        if (pagination) pagination.style.display = 'none';
        if (heroSection) heroSection.style.display = 'none';
        
        // نمایش container نتایج جستجو
        const resultsContainer = document.getElementById('real-search-results');
        if (!resultsContainer) return;
        
        // ساخت HTML نتایج
        let html = `
            <div class="search-results-header">
                <h2>
                    <i class="fas fa-search"></i>
                    نتایج جستجو برای: "${data.query}"
                </h2>
                
                <div class="search-results-stats">
                    <div class="search-stat">
                        <i class="fas fa-file-alt"></i>
                        ${data.totalResults} مقاله یافت شد
                    </div>
                    <div class="search-stat">
                        <i class="fas fa-clock"></i>
                        ${data.searchTime} میلی‌ثانیه
                    </div>
                    <div class="search-stat">
                        <i class="fas fa-microchip"></i>
                        ${data.metadata?.engine || 'سیستم جستجو'}
                    </div>
                </div>
            </div>
        `;
        
        // نمایش استنتاج
        if (data.inference) {
            html += `
                <div class="search-inference-card">
                    <h3><i class="fas fa-lightbulb"></i> تحلیل جستجو:</h3>
                    <p>${data.inference.summary}</p>
                    
                    ${data.inference.insights ? `
                        <div style="margin-top: 15px;">
                            ${data.inference.insights.map(insight => `
                                <div style="margin: 8px 0; padding-right: 15px; position: relative;">
                                    <i class="fas fa-chevron-left" style="position: absolute; right: 0; top: 5px; color: #4361ee;"></i>
                                    ${insight}
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    ${data.inference.recommendations ? `
                        <div style="margin-top: 15px; padding: 15px; background: #f8f9fa; border-radius: 10px;">
                            <strong>توصیه‌های سیستم:</strong>
                            ${data.inference.recommendations.map(rec => `
                                <div style="margin: 8px 0;">${rec}</div>
                            `).join('')}
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        // نمایش نتایج
        if (data.results && data.results.length > 0) {
            data.results.forEach((result, index) => {
                const article = result.article;
                const score = result.score || 0;
                const relevance = result.relevance || 'متوسط';
                
                // highlight کردن کلمات کلیدی
                let highlightedExcerpt = article.excerpt;
                if (article.highlights && article.highlights.content) {
                    article.highlights.content.forEach(highlight => {
                        if (highlight.context) {
                            highlightedExcerpt = highlight.context;
                        }
                    });
                }
                
                html += `
                    <div class="search-result-card">
                        <div class="result-score">
                            ${Math.round(score)}
                        </div>
                        
                        <div style="margin-right: 60px;">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
                                <h3 style="margin: 0; flex: 1;">
                                    ${index + 1}. ${article.title}
                                </h3>
                                <span style="background: ${this.getRelevanceColor(relevance)}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;">
                                    ${relevance}
                                </span>
                            </div>
                            
                            <div style="color: #666; margin-bottom: 10px;">
                                <i class="fas fa-folder"></i> ${article.category} 
                                • <i class="far fa-calendar"></i> ${this.formatDate(article.created_at)}
                                • <i class="fas fa-eye"></i> ${this.formatNumber(article.views || 0)}
                                • <i class="fas fa-heart"></i> ${this.formatNumber(article.likes || 0)}
                            </div>
                            
                            <p style="color: #555; line-height: 1.6; margin-bottom: 15px;">
                                ${highlightedExcerpt}
                            </p>
                            
                            ${result.matchDetails && result.matchDetails.length > 0 ? `
                                <div class="match-details">
                                    ${result.matchDetails.map(detail => `
                                        <span class="match-badge">
                                            <i class="fas fa-${this.getMatchIcon(detail.type)}"></i>
                                            ${detail.description}
                                        </span>
                                    `).join('')}
                                </div>
                            ` : ''}
                            
                            ${article.tags && article.tags.length > 0 ? `
                                <div style="margin: 15px 0;">
                                    <strong>برچسب‌ها:</strong>
                                    ${article.tags.map(tag => `
                                        <span style="background: #e0e7ff; color: #3730a3; padding: 4px 10px; border-radius: 15px; font-size: 0.85rem; margin-right: 5px;">
                                            ${tag}
                                        </span>
                                    `).join('')}
                                </div>
                            ` : ''}
                            
                            <div style="display: flex; justify-content: flex-end; margin-top: 20px;">
                                <button class="real-search-button" style="width: auto; padding: 10px 25px; border-radius: 25px;" 
                                        onclick="app.viewArticle(${article.id})">
                                    <i class="fas fa-book-reader"></i>
                                    مطالعه کامل مقاله
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            // دکمه بازگشت
            html += `
                <div style="text-align: center; margin: 40px 0;">
                    <button class="real-search-button" style="width: auto; padding: 12px 30px; border-radius: 25px;" 
                            onclick="realSearchUI.clearSearchResults()">
                        <i class="fas fa-arrow-right"></i>
                        بازگشت به همه مقالات
                    </button>
                </div>
            `;
        } else {
            html += `
                <div class="search-inference-card" style="text-align: center;">
                    <i class="fas fa-search-minus" style="font-size: 4rem; color: #ddd; margin-bottom: 20px;"></i>
                    <h3>مقاله‌ای یافت نشد</h3>
                    <p>${data.inference?.summary || 'هیچ مقاله‌ای با جستجوی شما مطابقت نداشت.'}</p>
                    
                    ${data.inference?.suggestions ? `
                        <div style="margin-top: 25px;">
                            <h4>پیشنهادهای جستجو:</h4>
                            ${data.inference.suggestions.map(suggestion => `
                                <div style="margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 10px;">
                                    ${suggestion}
                                </div>
                            `).join('')}
                        </div>
                    ` : ''}
                    
                    ${data.inference?.relatedTerms && data.inference.relatedTerms.length > 0 ? `
                        <div style="margin-top: 25px;">
                            <h4>کلمات کلیدی مرتبط:</h4>
                            <div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 15px;">
                                ${data.inference.relatedTerms.map(term => `
                                    <button class="real-search-button" style="width: auto; padding: 8px 20px; border-radius: 20px; background: #6c757d;" 
                                            onclick="realSearchUI.executeSearch('${term}')">
                                        ${term}
                                    </button>
                                `).join('')}
                            </div>
                        </div>
                    ` : ''}
                </div>
            `;
        }
        
        resultsContainer.innerHTML = html;
        resultsContainer.classList.add('show');
        
        // اسکرول به نتایج
        resultsContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    clearSearchResults() {
        const resultsContainer = document.getElementById('real-search-results');
        const articlesContainer = document.getElementById('articles-container');
        const pagination = document.getElementById('pagination');
        const heroSection = document.querySelector('.hero');
        const searchInput = document.getElementById('search-input');
        
        if (resultsContainer) {
            resultsContainer.classList.remove('show');
            resultsContainer.innerHTML = '';
        }
        
        if (articlesContainer) {
            articlesContainer.style.display = 'grid';
            articlesContainer.scrollIntoView({ behavior: 'smooth' });
        }
        
        if (pagination) pagination.style.display = 'flex';
        if (heroSection) heroSection.style.display = 'block';
        if (searchInput) searchInput.value = '';
    }
    
    showAdvancedSearchPanel() {
        // ایجاد overlay
        let overlay = document.getElementById('advanced-search-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'advanced-search-overlay';
            overlay.className = 'advanced-search-overlay';
            overlay.onclick = () => this.hideAdvancedSearchPanel();
            document.body.appendChild(overlay);
        }
        
        // ایجاد پنل
        let panel = document.getElementById('advanced-search-panel');
        if (!panel) {
            panel = document.createElement('div');
            panel.id = 'advanced-search-panel';
            panel.className = 'advanced-search-panel';
            document.body.appendChild(panel);
            
            // محتوای پنل
            panel.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                    <h3 style="margin: 0;">
                        <i class="fas fa-sliders-h"></i>
                        جستجوی پیشرفته
                    </h3>
                    <button onclick="realSearchUI.hideAdvancedSearchPanel()" 
                            style="background: none; border: none; color: #666; cursor: pointer; font-size: 1.5rem;">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                
                <form id="advanced-search-form">
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">عبارت جستجو:</label>
                        <input type="text" 
                               id="advanced-query" 
                               class="search-input" 
                               placeholder="موضوع مورد نظر..."
                               required
                               style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem;">
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">دسته‌بندی:</label>
                        <select id="advanced-category" style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem; background: white;">
                            <option value="">همه دسته‌بندی‌ها</option>
                            <option value="آموزش">آموزش</option>
                            <option value="پروژه">پروژه</option>
                            <option value="تحلیل">تحلیل</option>
                            <option value="اخبار">اخبار</option>
                            <option value="کتابخانه">کتابخانه</option>
                            <option value="توسعه">توسعه</option>
                        </select>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">حداقل بازدید:</label>
                            <input type="number" 
                                   id="advanced-min-views" 
                                   placeholder="100"
                                   min="0"
                                   style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem;">
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">حداقل لایک:</label>
                            <input type="number" 
                                   id="advanced-min-likes" 
                                   placeholder="10"
                                   min="0"
                                   style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem;">
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">از تاریخ:</label>
                            <input type="date" 
                                   id="advanced-date-from" 
                                   style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem;">
                        </div>
                        
                        <div>
                            <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">تا تاریخ:</label>
                            <input type="date" 
                                   id="advanced-date-to" 
                                   style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem;">
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: flex; align-items: center; gap: 10px; cursor: pointer;">
                            <input type="checkbox" id="advanced-featured" style="width: 18px; height: 18px;">
                            فقط مقالات ویژه
                        </label>
                    </div>
                    
                    <div style="margin-bottom: 25px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">مرتب‌سازی بر اساس:</label>
                        <select id="advanced-sort-by" style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem; background: white;">
                            <option value="relevance">مرتبط‌ترین</option>
                            <option value="views">پر بازدیدترین</option>
                            <option value="likes">پر لایک‌ترین</option>
                            <option value="date">جدیدترین</option>
                        </select>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <label style="display: block; margin-bottom: 8px; font-weight: 600; color: #333;">تعداد نتایج:</label>
                        <input type="number" 
                               id="advanced-limit" 
                               value="20"
                               min="5" 
                               max="100"
                               style="width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 10px; font-size: 1rem;">
                    </div>
                </form>
                
                <div style="position: sticky; bottom: 0; background: white; padding-top: 20px; border-top: 1px solid #eee;">
                    <button onclick="realSearchUI.submitAdvancedSearch()" 
                            style="width: 100%; padding: 15px; background: #4361ee; color: white; border: none; border-radius: 10px; font-size: 1.1rem; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 10px;">
                        <i class="fas fa-search"></i>
                        جستجوی پیشرفته
                    </button>
                </div>
            `;
            
            // تنظیم تاریخ‌های پیش‌فرض
            const today = new Date().toISOString().split('T')[0];
            const threeMonthsAgo = new Date();
            threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
            const threeMonthsAgoStr = threeMonthsAgo.toISOString().split('T')[0];
            
            const dateFromInput = document.getElementById('advanced-date-from');
            const dateToInput = document.getElementById('advanced-date-to');
            
            if (dateFromInput) dateFromInput.value = threeMonthsAgoStr;
            if (dateToInput) dateToInput.value = today;
        }
        
        // نمایش overlay و panel
        overlay.classList.add('show');
        panel.classList.add('show');
        
        // پر کردن فیلد جستجو با مقدار فعلی
        const searchInput = document.getElementById('search-input');
        const advancedQueryInput = document.getElementById('advanced-query');
        if (searchInput && advancedQueryInput && searchInput.value) {
            advancedQueryInput.value = searchInput.value;
        }
    }
    
    hideAdvancedSearchPanel() {
        const overlay = document.getElementById('advanced-search-overlay');
        const panel = document.getElementById('advanced-search-panel');
        
        if (overlay) overlay.classList.remove('show');
        if (panel) panel.classList.remove('show');
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
        const limit = document.getElementById('advanced-limit')?.value || 20;
        
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
            sortBy: sortBy || 'relevance',
            limit: parseInt(limit)
        };
        
        this.executeSearch(query, options);
        this.hideAdvancedSearchPanel();
    }
    
    // Helper Methods
    
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
    }
    
    removeFromHistory(query) {
        this.searchHistory = this.searchHistory.filter(item => item.query !== query);
        localStorage.setItem('natiq_search_history', JSON.stringify(this.searchHistory));
        this.showSearchHistory();
    }
    
    clearHistory() {
        this.searchHistory = [];
        localStorage.setItem('natiq_search_history', JSON.stringify([]));
        this.hideSuggestions();
        this.showMessage('تاریخچه جستجو پاک شد', 'success');
    }
    
    loadSearchHistory() {
        try {
            const history = localStorage.getItem('natiq_search_history');
            this.searchHistory = history ? JSON.parse(history) : [];
        } catch (error) {
            this.searchHistory = [];
        }
    }
    
    getTimeAgo(timestamp) {
        const now = new Date();
        const past = new Date(timestamp);
        const diffMs = now - past;
        const diffMins = Math.floor(diffMs / 60000);
        const diffHours = Math.floor(diffMs / 3600000);
        const diffDays = Math.floor(diffMs / 86400000);
        
        if (diffMins < 1) return 'همین الآن';
        if (diffMins < 60) return `${diffMins} دقیقه قبل`;
        if (diffHours < 24) return `${diffHours} ساعت قبل`;
        if (diffDays < 30) return `${diffDays} روز قبل`;
        return 'مدتی قبل';
    }
    
    getRelevanceColor(relevance) {
        switch (relevance) {
            case 'خیلی زیاد': return '#28a745';
            case 'زیاد': return '#20c997';
            case 'متوسط': return '#ffc107';
            case 'کم': return '#fd7e14';
            case 'خیلی کم': return '#dc3545';
            default: return '#6c757d';
        }
    }
    
    getMatchIcon(type) {
        switch (type) {
            case 'title': return 'heading';
            case 'content': return 'file-alt';
            case 'tags': return 'tags';
            case 'category': return 'folder';
            default: return 'check-circle';
        }
    }
    
    formatDate(dateString) {
        try {
            const date = new Date(dateString);
            return new Intl.DateTimeFormat('fa-IR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            }).format(date);
        } catch (error) {
            return 'تاریخ نامعلوم';
        }
    }
    
    formatNumber(num) {
        return new Intl.NumberFormat('fa-IR').format(num);
    }
    
    showLoading() {
        // ایجاد overlay بارگذاری
        let overlay = document.getElementById('search-loading-overlay');
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'search-loading-overlay';
            overlay.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.9);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 99999;
                flex-direction: column;
                backdrop-filter: blur(5px);
            `;
            overlay.innerHTML = `
                <div style="width: 60px; height: 60px; border: 5px solid #f3f3f3; border-top: 5px solid #4361ee; border-radius: 50%; animation: spin 1s linear infinite;"></div>
                <div style="margin-top: 20px; font-size: 1.2rem; color: #333; text-align: center;">
                    <i class="fas fa-search"></i>
                    در حال جستجوی هوشمند...
                </div>
                <div style="margin-top: 10px; color: #666; font-size: 0.9rem; text-align: center;">
                    سیستم در حال بررسی ${this.currentSearch ? `"${this.currentSearch}"` : 'عبارت جستجو'}
                </div>
            `;
            document.body.appendChild(overlay);
            
            // اضافه کردن استایل spinner
            const style = document.createElement('style');
            style.textContent = `
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    hideLoading() {
        const overlay = document.getElementById('search-loading-overlay');
        if (overlay) {
            overlay.remove();
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
            background: ${type === 'error' ? '#dc3545' : 
                        type === 'warning' ? '#ffc107' : 
                        type === 'success' ? '#28a745' : '#17a2b8'};
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 12px;
            animation: slideDown 0.3s ease;
            min-width: 300px;
            max-width: 500px;
        `;
        
        const icon = type === 'error' ? 'exclamation-circle' : 
                    type === 'warning' ? 'exclamation-triangle' : 
                    type === 'success' ? 'check-circle' : 'info-circle';
        
        message.innerHTML = `
            <i class="fas fa-${icon}" style="font-size: 1.2rem;"></i>
            <span style="flex: 1;">${text}</span>
            <button onclick="this.parentElement.remove()" 
                    style="background: none; border: none; color: white; cursor: pointer; opacity: 0.8; transition: opacity 0.3s;">
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
    }
}

// راه‌اندازی رابط کاربری جستجو
let realSearchUI;
document.addEventListener('DOMContentLoaded', () => {
    realSearchUI = new RealSearchUI();
    window.realSearchUI = realSearchUI;
    
    // اضافه کردن به app اصلی
    if (window.app) {
        window.app.searchUI = realSearchUI;
    }
});
