// Natiq Ultimate - Main Application Script

class NatiqApp {
    constructor() {
        this.apiBaseUrl = window.location.origin;
        this.currentSection = 'dashboard';
        this.api = new NatiqAPI(this.apiBaseUrl);
        this.charts = {};
        this.state = {
            connection: {
                status: 'disconnected',
                lastCheck: null,
                latency: null
            },
            stats: {
                requests: 0,
                success: 0,
                errors: 0
            },
            userPrefs: this.loadUserPreferences()
        };
        
        this.init();
    }
    
    init() {
        this.initTheme();
        this.initEventListeners();
        this.initCharts();
        this.checkConnection();
        this.loadDashboard();
        this.startHealthMonitor();
        
        // نمایش نسخه در فوتر
        document.getElementById('footerVersion').textContent = '1.0.0';
    }
    
    initTheme() {
        const theme = this.state.userPrefs.theme || 'light';
        document.documentElement.setAttribute('data-theme', theme);
        document.getElementById('themeSwitch').checked = theme === 'dark';
    }
    
    initEventListeners() {
        // تغییر تم
        document.getElementById('themeSwitch').addEventListener('change', (e) => {
            const theme = e.target.checked ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            this.saveUserPreference('theme', theme);
        });
        
        // ناوبری
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = link.getAttribute('href').substring(1);
                this.showSection(target);
                
                // بروزرسانی لینک فعال
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
        
        // دکمه اتصال
        document.getElementById('connectBtn').addEventListener('click', () => {
            this.showModal('connectionModal');
        });
        
        // ذخیره تنظیمات اتصال
        document.getElementById('saveConnectionBtn').addEventListener('click', () => {
            this.saveConnectionSettings();
        });
        
        // بستن مودال
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal');
                this.hideModal(modal.id);
            });
        });
        
        // کلیک خارج از مودال
        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.hideModal(modal.id);
                }
            });
        });
        
        // رفرش دشبورد
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadDashboard();
        });
        
        // تست API
        document.getElementById('testApiBtn').addEventListener('click', () => {
            this.testAllEndpoints();
        });
        
        // پردازش متن
        document.getElementById('processTextBtn').addEventListener('click', () => {
            this.processText();
        });
        
        // پاک کردن متن
        document.getElementById('clearTextBtn').addEventListener('click', () => {
            this.clearTextInput();
        });
        
        // نمونه متن
        document.getElementById('sampleTextBtn').addEventListener('click', () => {
            this.loadSampleText();
        });
        
        // شمارش کاراکترهای متن
        document.getElementById('textInput').addEventListener('input', (e) => {
            this.updateTextStats(e.target.value);
        });
        
        // اقدامات سریع
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const action = e.currentTarget.dataset.action;
                this.handleQuickAction(action);
            });
        });
        
        // گزارش مشکل
        document.getElementById('systemReportBtn').addEventListener('click', () => {
            this.reportIssue();
        });
    }
    
    initCharts() {
        // نمودار سیستم
        const ctx = document.getElementById('systemChart').getContext('2d');
        this.charts.system = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length: 10}, (_, i) => `${i * 5}ثانیه`),
                datasets: [{
                    label: 'درخواست‌ها',
                    data: Array(10).fill(0),
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    }
                }
            }
        });
        
        // نمودار لاگ‌ها
        const logCtx = document.getElementById('logsChart').getContext('2d');
        this.charts.logs = new Chart(logCtx, {
            type: 'bar',
            data: {
                labels: ['خطا', 'اخطار', 'اطلاعات', 'دیباگ'],
                datasets: [{
                    label: 'تعداد لاگ‌ها',
                    data: [0, 0, 0, 0],
                    backgroundColor: [
                        'rgba(231, 76, 60, 0.7)',
                        'rgba(243, 156, 18, 0.7)',
                        'rgba(52, 152, 219, 0.7)',
                        'rgba(155, 89, 182, 0.7)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
    
    showSection(sectionId) {
        // مخفی کردن همه بخش‌ها
        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
        
        // نمایش بخش انتخاب شده
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.classList.add('active');
            this.currentSection = sectionId;
            
            // بارگذاری داده‌های بخش
            switch(sectionId) {
                case 'dashboard':
                    this.loadDashboard();
                    break;
                case 'file-manager':
                    this.loadFileManager();
                    break;
                case 'logs':
                    this.loadLogs();
                    break;
                case 'api':
                    this.loadAPIDocs();
                    break;
            }
        }
    }
    
    showModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    }
    
    hideModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }
    }
    
    async checkConnection() {
        const startTime = Date.now();
        
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/health`);
            const data = await response.json();
            
            const latency = Date.now() - startTime;
            
            this.state.connection = {
                status: 'connected',
                lastCheck: new Date().toLocaleTimeString('fa-IR'),
                latency: latency,
                environment: data.environment || 'production'
            };
            
            this.updateConnectionStatus();
            this.showToast('اتصال به سرور برقرار شد', 'success');
            
        } catch (error) {
            this.state.connection.status = 'disconnected';
            this.updateConnectionStatus();
            this.showToast('خطا در اتصال به سرور', 'error');
        }
    }
    
    updateConnectionStatus() {
        const statusBar = document.getElementById('statusBar');
        const statusText = document.querySelector('.status-text');
        const statusDetail = document.querySelector('.status-detail');
        const statusIcon = document.querySelector('.status-icon');
        const healthStatus = document.getElementById('healthStatus');
        const footerApiStatus = document.getElementById('footerApiStatus');
        
        if (this.state.connection.status === 'connected') {
            statusBar.style.backgroundColor = 'rgba(46, 204, 113, 0.1)';
            statusText.textContent = 'اتصال برقرار';
            statusDetail.textContent = `تأخیر: ${this.state.connection.latency}ms`;
            statusIcon.className = 'fas fa-circle status-icon online';
            healthStatus.textContent = 'سالم';
            healthStatus.className = 'badge badge-success';
            footerApiStatus.textContent = 'آنلاین';
            footerApiStatus.className = 'status-value online';
            
            // بروزرسانی اطلاعات دشبورد
            document.getElementById('lastUpdate').textContent = this.state.connection.lastCheck;
            document.getElementById('responseTime').textContent = `${this.state.connection.latency}ms`;
            document.getElementById('environment').textContent = this.state.connection.environment;
            
            // آپدیت پروگرس بار
            const progress = Math.min(100, (this.state.connection.latency / 1000) * 100);
            document.querySelector('.progress-fill').style.width = `${100 - progress}%`;
            
        } else {
            statusBar.style.backgroundColor = 'rgba(231, 76, 60, 0.1)';
            statusText.textContent = 'اتصال قطع';
            statusDetail.textContent = 'در حال تلاش برای اتصال...';
            statusIcon.className = 'fas fa-circle status-icon offline';
            healthStatus.textContent = 'مشکل';
            healthStatus.className = 'badge badge-danger';
            footerApiStatus.textContent = 'آفلاین';
            footerApiStatus.className = 'status-value offline';
        }
        
        // بروزرسانی فوتر
        document.getElementById('footerLastUpdate').textContent = 
            this.state.connection.lastCheck || '--:--';
    }
    
    async loadDashboard() {
        this.showLoading();
        
        try {
            // دریافت اطلاعات سلامت
            const healthResponse = await this.api.getHealth();
            if (healthResponse.success) {
                this.state.connection.environment = healthResponse.data.environment;
                this.state.connection.lastCheck = new Date().toLocaleTimeString('fa-IR');
                this.updateConnectionStatus();
            }
            
            // دریافت اطلاعات اصلی API
            const rootResponse = await this.api.getRoot();
            if (rootResponse.success) {
                document.getElementById('apiName').textContent = 'Natiq Ultimate API';
                document.getElementById('apiVersion').textContent = rootResponse.data.version;
                document.getElementById('apiStatus').textContent = rootResponse.data.status === 'active' ? 'فعال' : 'غیرفعال';
            }
            
            // تست endpoint پردازش متن
            const testText = 'این یک متن تست برای بررسی عملکرد سیستم است.';
            const processResponse = await this.api.processText(testText);
            
            if (processResponse.success) {
                this.state.stats.success++;
                document.getElementById('successCount').textContent = this.state.stats.success;
            }
            
            // بروزرسانی نمودار
            this.updateSystemChart();
            
            this.showToast('داشبورد با موفقیت بارگذاری شد', 'success');
            
        } catch (error) {
            this.state.stats.errors++;
            document.getElementById('errorCount').textContent = this.state.stats.errors;
            this.showToast('خطا در بارگذاری داشبورد', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    async processText() {
        const textInput = document.getElementById('textInput');
        const text = textInput.value.trim();
        
        if (!text) {
            this.showToast('لطفا متن خود را وارد کنید', 'warning');
            return;
        }
        
        this.showLoading();
        
        try {
            const startTime = Date.now();
            const response = await this.api.processText(text);
            const processTime = Date.now() - startTime;
            
            if (response.success) {
                // نمایش نتیجه
                const outputContent = document.getElementById('outputContent');
                outputContent.innerHTML = `
                    <div class="output-result">
                        <div class="result-header">
                            <h4><i class="fas fa-check-circle"></i> پردازش موفق</h4>
                            <span class="badge badge-success">${processTime}ms</span>
                        </div>
                        <div class="result-body">
                            <div class="result-section">
                                <h5>متن پردازش شده:</h5>
                                <p class="processed-text">${response.data.processed_text}</p>
                            </div>
                            <div class="result-section">
                                <h5>اطلاعات آماری:</h5>
                                <div class="stats-grid">
                                    <div class="stat">
                                        <span class="stat-label">طول متن اصلی:</span>
                                        <span class="stat-value">${response.data.original_length} کاراکتر</span>
                                    </div>
                                    <div class="stat">
                                        <span class="stat-label">زمان پردازش:</span>
                                        <span class="stat-value">${processTime} میلی‌ثانیه</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                
                // بروزرسانی آمار
                document.getElementById('processTime').textContent = `${processTime}ms`;
                document.getElementById('outputCharCount').textContent = response.data.processed_text.length;
                
                const compression = Math.round((1 - (response.data.processed_text.length / text.length)) * 100);
                document.getElementById('compressionRate').textContent = 
                    compression > 0 ? `${compression}%` : '0%';
                
                this.state.stats.success++;
                document.getElementById('successCount').textContent = this.state.stats.success;
                
                this.showToast('متن با موفقیت پردازش شد', 'success');
                
            } else {
                throw new Error(response.message || 'خطا در پردازش متن');
            }
            
        } catch (error) {
            this.state.stats.errors++;
            document.getElementById('errorCount').textContent = this.state.stats.errors;
            
            const outputContent = document.getElementById('outputContent');
            outputContent.innerHTML = `
                <div class="output-error">
                    <i class="fas fa-exclamation-triangle"></i>
                    <h4>خطا در پردازش</h4>
                    <p>${error.message}</p>
                </div>
            `;
            
            this.showToast(error.message, 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    updateTextStats(text) {
        const charCount = text.length;
        const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;
        const lineCount = text.split('\n').length;
        
        document.getElementById('charCount').textContent = `${charCount} کاراکتر`;
        document.getElementById('wordCount').textContent = `${wordCount} کلمه`;
        document.getElementById('lineCount').textContent = `${lineCount} خط`;
    }
    
    clearTextInput() {
        document.getElementById('textInput').value = '';
        this.updateTextStats('');
        
        const outputContent = document.getElementById('outputContent');
        outputContent.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-robot"></i>
                <p>نتیجه پردازش اینجا نمایش داده می‌شود</p>
            </div>
        `;
        
        document.getElementById('processTime').textContent = '--';
        document.getElementById('outputCharCount').textContent = '0';
        document.getElementById('compressionRate').textContent = '0%';
        
        this.showToast('متن پاک شد', 'info');
    }
    
    loadSampleText() {
        const sampleText = `سلام! این یک نمونه متن فارسی است که می‌توانید برای تست سیستم پردازش متن از آن استفاده کنید.

ویژگی‌های سیستم پردازش متن Natiq Ultimate:
1. تحلیل آماری متن
2. خلاصه‌سازی خودکار
3. تشخیص زبان
4. تحلیل احساسات
5. پردازش هوشمند

این سیستم با استفاده از الگوریتم‌های پیشرفته هوش مصنوعی توسعه داده شده و می‌تواند نیازهای مختلف پردازش متنی شما را برآورده کند.

برای شروع پردازش، دکمه "شروع پردازش" را فشار دهید.`;
        
        document.getElementById('textInput').value = sampleText;
        this.updateTextStats(sampleText);
        this.showToast('متن نمونه بارگذاری شد', 'info');
    }
    
    async loadFileManager() {
        this.showLoading();
        
        try {
            // دریافت اطلاعات فایل
            const response = await this.api.getFileInfo('requirements.txt');
            
            if (response.success) {
                const fileInfo = document.getElementById('fileInfo');
                fileInfo.querySelector('#fileName').textContent = 'requirements.txt';
                fileInfo.querySelector('#filePath').textContent = response.data.file_path || '---';
                fileInfo.querySelector('#fileSize').textContent = response.data.content_preview ? 
                    `${response.data.content_preview.length} کاراکتر` : '---';
                
                const now = new Date();
                fileInfo.querySelector('#fileCreated').textContent = now.toLocaleDateString('fa-IR');
                fileInfo.querySelector('#fileModified').textContent = now.toLocaleDateString('fa-IR');
                
                // فعال کردن دکمه‌ها
                document.getElementById('viewFileBtn').disabled = false;
                document.getElementById('editFileBtn').disabled = false;
                document.getElementById('deleteFileBtn').disabled = false;
            }
            
            // بارگذاری ساختار درختی (شبیه‌سازی)
            this.loadFileTree();
            
            this.showToast('مدیریت فایل بارگذاری شد', 'success');
            
        } catch (error) {
            this.showToast('خطا در بارگذاری مدیریت فایل', 'error');
        } finally {
            this.hideLoading();
        }
    }
    
    loadFileTree() {
        const treeContent = document.getElementById('treeContent');
        const treeStructure = `
            <div class="tree-item">
                <div class="tree-node" data-path="/">
                    <i class="fas fa-folder"></i>
                    <span>root</span>
                </div>
                <div class="tree-children">
                    <div class="tree-item">
                        <div class="tree-node" data-path="/api">
                            <i class="fas fa-folder"></i>
                            <span>api</span>
                        </div>
                        <div class="tree-children">
                            <div class="tree-item">
                                <div class="tree-node" data-path="/api/app.py">
                                    <i class="fas fa-file-code"></i>
                                    <span>app.py</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tree-item">
                        <div class="tree-node" data-path="/public">
                            <i class="fas fa-folder"></i>
                            <span>public</span>
                        </div>
                        <div class="tree-children">
                            <div class="tree-item">
                                <div class="tree-node" data-path="/public/index.html">
                                    <i class="fas fa-file-code"></i>
                                    <span>index.html</span>
                                </div>
                            </div>
                            <div class="tree-item">
                                <div class="tree-node" data-path="/public/css">
                                    <i class="fas fa-folder"></i>
                                    <span>css</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tree-item">
                        <div class="tree-node" data-path="/requirements.txt">
                            <i class="fas fa-file"></i>
                            <span>requirements.txt</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        treeContent.innerHTML = treeStructure;
        
        // اضافه کردن event listener برای گره‌های درخت
        treeContent.querySelectorAll('.tree-node').forEach(node => {
            node.addEventListener('click', (e) => {
                e.stopPropagation();
                const path = node.dataset.path;
                this.selectFile(path);
            });
        });
    }
    
    selectFile(path) {
        const breadcrumb = document.getElementById('breadcrumb');
        const parts = path.split('/').filter(p => p);
        
        let breadcrumbHTML = '<a href="#" data-path="/">خانه</a>';
        let currentPath = '';
        
        parts.forEach((part, index) => {
            currentPath += `/${part}`;
            breadcrumbHTML += ` / <a href="#" data-path="${currentPath}">${part}</a>`;
        });
        
        breadcrumb.innerHTML = breadcrumbHTML;
        
        // بروزرسانی event listeners برای breadcrumb
        breadcrumb.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const path = e.target.dataset.path;
                this.selectFile(path);
            });
        });
        
        // نمایش اطلاعات فایل انتخاب شده
        if (path.endsWith('.py') || path.endsWith('.txt') || path.endsWith('.html') || path.endsWith('.css') || path.endsWith('.js')) {
            this.showFileInfo(path);
        }
    }
    
    async showFileInfo(path) {
        try {
            const response = await this.api.getFileInfo(path);
            
            if (response.success) {
                const fileName = path.split('/').pop();
                const fileInfo = document.getElementById('fileInfo');
                
                fileInfo.querySelector('#fileName').textContent = fileName;
                fileInfo.querySelector('#filePath').textContent = response.data.file_path || path;
                fileInfo.querySelector('#fileSize').textContent = response.data.content_preview ? 
                    `${response.data.content_preview.length} کاراکتر` : '---';
                
                const now = new Date();
                fileInfo.querySelector('#fileCreated').textContent = now.toLocaleDateString('fa-IR');
                fileInfo.querySelector('#fileModified').textContent = now.toLocaleDateString('fa-IR');
                
                // فعال کردن دکمه‌ها
                document.getElementById('viewFileBtn').disabled = false;
                document.getElementById('editFileBtn').disabled = false;
                document.getElementById('deleteFileBtn').disabled = false;
                
                // نمایش پیش‌نمایش محتوا
                const fileContent = document.getElementById('fileContent');
                fileContent.innerHTML = `
                    <div class="file-preview">
                        <div class="preview-header">
                            <h4><i class="fas fa-file-alt"></i> ${fileName}</h4>
                            <span class="badge">پیش‌نمایش</span>
                        </div>
                        <div class="preview-content">
                            <pre><code>${response.data.content_preview || 'بدون محتوا'}</code></pre>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            this.showToast('خطا در دریافت اطلاعات فایل', 'error');
        }
    }
    
    async loadLogs() {
        try {
            const response = await this.api.getLogs(25);
            
            if (response.success) {
                const logsBody = document.getElementById('logsBody');
                logsBody.innerHTML = '';
                
                response.data.recent_logs.forEach((log, index) => {
                    const row = document.createElement('tr');
                    
                    // تجزیه لاگ (فرضی)
                    const time = new Date().toLocaleTimeString('fa-IR');
                    const level = index % 3 === 0 ? 'error' : index % 3 === 1 ? 'warning' : 'info';
                    const source = ['API', 'File System', 'Database'][index % 3];
                    const message = log || `لاگ سیستم شماره ${index + 1}`;
                    
                    row.innerHTML = `
                        <td>${time}</td>
                        <td><span class="level-badge ${level}">${level.toUpperCase()}</span></td>
                        <td>${source}</td>
                        <td>${message.substring(0, 50)}${message.length > 50 ? '...' : ''}</td>
                        <td><button class="btn btn-sm" onclick="app.viewLogDetails(${index})">مشاهده</button></td>
                    `;
                    
                    logsBody.appendChild(row);
                });
                
                // بروزرسانی آمار
                document.getElementById('logCount').textContent = response.data.total_logs;
                document.getElementById('errorLogCount').textContent = Math.floor(response.data.total_logs * 0.3);
                document.getElementById('logSize').textContent = `${Math.round(response.data.total_logs * 0.1)}KB`;
                
                // بروزرسانی نمودار
                this.updateLogsChart();
                
                this.showToast('لاگ‌ها با موفقیت بارگذاری شدند', 'success');
            }
        } catch (error) {
            this.showToast('خطا در بارگذاری لاگ‌ها', 'error');
        }
    }
    
    updateLogsChart() {
        // داده‌های نمونه برای نمودار
        const data = [
            Math.floor(Math.random() * 50) + 10,  // خطاها
            Math.floor(Math.random() * 100) + 30, // اخطارها
            Math.floor(Math.random() * 200) + 50, // اطلاعات
            Math.floor(Math.random() * 30) + 5    // دیباگ
        ];
        
        this.charts.logs.data.datasets[0].data = data;
        this.charts.logs.update();
    }
    
    updateSystemChart() {
        const currentData = this.charts.system.data.datasets[0].data;
        const newValue = Math.floor(Math.random() * 50) + 10;
        
        // اضافه کردن مقدار جدید و حذف قدیمی‌ترین
        currentData.push(newValue);
        currentData.shift();
        
        this.charts.system.update();
        
        // بروزرسانی آمار
        this.state.stats.requests++;
        document.getElementById('requestCount').textContent = this.state.stats.requests;
    }
    
    async testAllEndpoints() {
        this.showLoading();
        
        const endpoints = [
            { name: 'ریشه API', method: 'GET', path: '/' },
            { name: 'سلامت API', method: 'GET', path: '/api/health' },
            { name: 'پردازش متن', method: 'POST', path: '/api/process' },
            { name: 'اطلاعات فایل', method: 'GET', path: '/api/file-info' }
        ];
        
        let successCount = 0;
        let errorCount = 0;
        
        for (const endpoint of endpoints) {
            try {
                let response;
                
                switch (endpoint.method) {
                    case 'GET':
                        response = await fetch(`${this.apiBaseUrl}${endpoint.path}`);
                        break;
                    case 'POST':
                        if (endpoint.path === '/api/process') {
                            response = await fetch(`${this.apiBaseUrl}${endpoint.path}`, {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify({
                                    text: 'تست API'
                                })
                            });
                        }
                        break;
                }
                
                if (response && response.ok) {
                    successCount++;
                } else {
                    errorCount++;
                }
                
            } catch (error) {
                errorCount++;
            }
        }
        
        this.hideLoading();
        
        this.showToast(
            `تست API کامل شد: ${successCount} موفق، ${errorCount} ناموفق`,
            errorCount === 0 ? 'success' : 'warning'
        );
    }
    
    handleQuickAction(action) {
        switch (action) {
            case 'text-processor':
                this.showSection('text-processor');
                break;
            case 'file-manager':
                this.showSection('file-manager');
                break;
            case 'check-logs':
                this.showSection('logs');
                this.loadLogs();
                break;
            case 'clear-cache':
                this.clearCache();
                break;
            case 'export-data':
                this.exportData();
                break;
            case 'settings':
                this.showModal('connectionModal');
                break;
        }
    }
    
    clearCache() {
        localStorage.removeItem('natiq_preferences');
        this.showToast('کش پاک شد', 'success');
    }
    
    exportData() {
        const data = {
            connection: this.state.connection,
            stats: this.state.stats,
            timestamp: new Date().toISOString()
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `natiq-export-${new Date().getTime()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showToast('داده‌ها با موفقیت دانلود شدند', 'success');
    }
    
    reportIssue() {
        const issueData = {
            url: window.location.href,
            userAgent: navigator.userAgent,
            connection: this.state.connection,
            timestamp: new Date().toISOString()
        };
        
        // در نسخه واقعی، این اطلاعات به سرور ارسال می‌شوند
        console.log('گزارش مشکل:', issueData);
        
        this.showToast('گزارش مشکل ثبت شد. با تشکر از بازخورد شما!', 'info');
    }
    
    saveConnectionSettings() {
        const apiUrl = document.getElementById('apiUrl').value;
        const apiKey = document.getElementById('apiKey').value;
        const autoConnect = document.getElementById('autoConnect').checked;
        
        // ذخیره تنظیمات
        const settings = {
            apiUrl,
            apiKey,
            autoConnect,
            savedAt: new Date().toISOString()
        };
        
        localStorage.setItem('natiq_connection', JSON.stringify(settings));
        
        // بروزرسانی URL پایه
        this.apiBaseUrl = apiUrl;
        this.api = new NatiqAPI(apiUrl);
        
        this.hideModal('connectionModal');
        this.checkConnection();
        
        this.showToast('تنظیمات اتصال ذخیره شد', 'success');
    }
    
    loadUserPreferences() {
        const prefs = localStorage.getItem('natiq_preferences');
        return prefs ? JSON.parse(prefs) : {
            theme: 'light',
            autoRefresh: true,
            notifications: true
        };
    }
    
    saveUserPreference(key, value) {
        this.state.userPrefs[key] = value;
        localStorage.setItem('natiq_preferences', JSON.stringify(this.state.userPrefs));
    }
    
    showLoading() {
        document.getElementById('loadingOverlay').classList.add('active');
    }
    
    hideLoading() {
        document.getElementById('loadingOverlay').classList.remove('active');
    }
    
    showToast(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer');
        const toastId = `toast-${Date.now()}`;
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.id = toastId;
        toast.innerHTML = `
            <i class="fas fa-${this.getToastIcon(type)}"></i>
            <div class="toast-content">
                <p>${message}</p>
            </div>
            <button class="toast-close" onclick="document.getElementById('${toastId}').remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        toastContainer.appendChild(toast);
        
        // حذف خودکار پس از 5 ثانیه
        setTimeout(() => {
            const toastElement = document.getElementById(toastId);
            if (toastElement) {
                toastElement.remove();
            }
        }, 5000);
    }
    
    getToastIcon(type) {
        switch (type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-circle';
            case 'warning': return 'exclamation-triangle';
            case 'info': return 'info-circle';
            default: return 'info-circle';
        }
    }
    
    startHealthMonitor() {
        // بررسی دوره‌ی سلامت هر 30 ثانیه
        setInterval(() => {
            this.checkConnection();
            this.updateSystemChart();
        }, 30000);
    }
}

// API Wrapper Class
class NatiqAPI {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        try {
            const response = await fetch(url, { ...defaultOptions, ...options });
            const data = await response.json();
            
            return {
                success: response.ok,
                status: response.status,
                data: data,
                message: response.ok ? 'درخواست موفق' : data.detail || 'خطا در درخواست'
            };
        } catch (error) {
            return {
                success: false,
                status: 0,
                data: null,
                message: error.message
            };
        }
    }
    
    async getHealth() {
        return this.request('/api/health');
    }
    
    async getRoot() {
        return this.request('/');
    }
    
    async processText(text) {
        return this.request('/api/process', {
            method: 'POST',
            body: JSON.stringify({ text })
        });
    }
    
    async getFileInfo(path = 'requirements.txt') {
        return this.request(`/api/file-info?path=${encodeURIComponent(path)}`);
    }
    
    async getLogs(limit = 25) {
        return this.request(`/api/logs?limit=${limit}`);
    }
}

// راه‌اندازی اپلیکیشن وقتی DOM لود شد
document.addEventListener('DOMContentLoaded', () => {
    window.app = new NatiqApp();
});
