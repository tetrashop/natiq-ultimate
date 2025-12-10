// پیکربندی API
const API_CONFIG = {
    baseURL: window.location.origin,
    endpoints: {
        health: '/api/health',
        chat: '/api/chat',
        chatMemory: '/api/chat-memory',
        mathSolve: '/api/math/solve',
        mathDerive: '/api/math/derive',
        logicEvaluate: '/api/logic/evaluate',
        userStats: '/api/user/stats',
        tutor: '/api/tutor',
        exercises: '/api/exercises',
        plot: '/api/plot'
    },
    
    // متدهای کمکی
    async request(endpoint, method = 'GET', data = null) {
        const url = this.baseURL + endpoint;
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'User-ID': localStorage.getItem('user_id') || 'anonymous'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    // تست اتصال API
    async testConnection() {
        try {
            const response = await this.request(this.endpoints.health);
            return {
                connected: true,
                data: response
            };
        } catch (error) {
            return {
                connected: false,
                error: error.message
            };
        }
    },
    
    // حل معادله با پارامترهای پیشرفته
    async solveEquationAdvanced(equation, options = {}) {
        return await this.request(this.endpoints.mathSolve, 'POST', {
            equation,
            variable: options.variable || 'x',
            showSteps: options.showSteps || true,
            format: options.format || 'exact'
        });
    },
    
    // ارسال چت با context
    async sendChatWithContext(message, context = {}) {
        return await this.request(this.endpoints.chatMemory, 'POST', {
            message,
            session_id: context.sessionId || 'default',
            context: {
                userLevel: context.userLevel || 'intermediate',
                topic: context.topic || 'general',
                language: 'fa'
            }
        });
    },
    
    // دریافت تمرین‌های شخصی‌سازی شده
    async getPersonalizedExercises(topic, difficulty = 'medium', count = 5) {
        return await this.request(this.endpoints.exercises, 'POST', {
            topic,
            difficulty,
            count,
            userId: localStorage.getItem('user_id')
        });
    }
};

// صادر کردن برای استفاده در ماژول‌ها
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API_CONFIG;
}
