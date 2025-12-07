#!/bin/bash
# اسکریپت راه‌اندازی natiq-ultimate برای Termux

echo "🚀 راه‌اندازی natiq-ultimate v2.0 در Termux"
echo "=========================================="

# رنگ‌ها
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# توابع کمکی
log_info() { echo -e "${GREEN}✅ $1${NC}"; }
log_warn() { echo -e "${YELLOW}⚠️  $1${NC}"; }
log_error() { echo -e "${RED}❌ $1${NC}"; }
log_step() { echo -e "${BLUE}📦 $1${NC}"; }

# بررسی پایتون
log_step "بررسی پایتون..."
if ! command -v python3 &> /dev/null; then
    log_error "پایتون یافت نشد!"
    echo "لطفاً پایتون را نصب کنید:"
    echo "pkg install python"
    exit 1
fi

log_info "پایتون: $(python3 --version)"

# بررسی pip
log_step "بررسی pip..."
if ! command -v pip &> /dev/null; then
    log_warn "pip یافت نشد. در حال نصب..."
    pkg install python-pip
fi

# نصب/ارتقا pip
pip install --upgrade pip

# بررسی نیازمندی‌ها
cd backend
if [ -f "requirements.txt" ]; then
    log_step "نصب نیازمندی‌ها..."
    
    # نصب جداگانه بسته‌ها برای جلوگیری از خطا
    log_info "نصب fastapi..."
    pip install fastapi==0.104.1
    
    log_info "نصب uvicorn..."
    pip install "uvicorn[standard]"==0.24.0
    
    log_info "نصب websockets..."
    pip install websockets==12.0
    
    log_info "نصب python-multipart..."
    pip install python-multipart==0.0.6
    
    log_info "نصب pydantic (نسخه سازگار)..."
    pip install "pydantic<2"
    
    log_info "نصب python-dotenv..."
    pip install python-dotenv==1.0.0
    
    log_info "نصب asyncio..."
    pip install asyncio
else
    log_error "فایل requirements.txt یافت نشد"
    exit 1
fi

# بازگشت به دایرکتوری اصلی
cd ..

# ایجاد پوشه‌های ضروری
log_step "ایجاد پوشه‌های داده..."
mkdir -p data/knowledge data/conversations data/models logs

# بررسی natiq_smart.py
log_step "بررسی فایل natiq_smart.py..."
if [ ! -f "backend/natiq_smart.py" ]; then
    log_warn "فایل natiq_smart.py یافت نشد. ایجاد فایل پایه..."
    
    cat > backend/natiq_smart.py << 'PYTHON'
"""
فایل پایه natiq_smart برای Termux
"""

import json
import os
from datetime import datetime
from pathlib import Path
import re

class NatiqSmart:
    def __init__(self):
        self.user_name = "کاربر"
        self.stats = {
            "questions_asked": 0,
            "topics_covered": set(),
            "session_start": datetime.now().isoformat()
        }
        
        # ایجاد دایرکتوری‌ها
        self.data_dir = Path("data")
        self.knowledge_dir = self.data_dir / "knowledge"
        self.conv_dir = self.data_dir / "conversations"
        
        for dir_path in [self.data_dir, self.knowledge_dir, self.conv_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # بارگیری دانش پایه
        self.knowledge = self.load_knowledge()
        
        # الگوهای شناسایی
        self.patterns = {
            "greeting": [r"سلام", r"درود", r"علیک", r"hello", r"hi"],
            "name_query": [r"اسمت چیه", r"تو کیه", r"نام تو", r"کی هستی"],
            "name_set": [r"اسم من (\w+)", r"من (\w+) هستم", r"نام من (\w+)"],
            "learn": [r"یاد بگیر (.+)\|(.+)", r"آموزش بده (.+) جوابش (.+)"],
            "stats": [r"آمار", r"stat", r"تعداد سوال"],
            "topics": [r"موضوعات", r"topics", r"چه چیزهایی"]
        }
    
    def load_knowledge(self):
        """بارگیری دانش ذخیره شده"""
        knowledge_file = self.knowledge_dir / "base_knowledge.json"
        
        base_knowledge = {
            "هوش مصنوعی": "هوش مصنوعی شاخه‌ای از علوم کامپیوتر است که به ساخت ماشین‌های هوشمند می‌پردازد.",
            "پایتون": "پایتون یک زبان برنامه‌نویسی سطح بالا و همه‌منظوره است که برای توسعه وب، هوش مصنوعی و علم داده استفاده می‌شود.",
            "برنامه‌نویسی": "برنامه‌نویسی هنر نوشتن دستوراتی است که کامپیوتر آن‌ها را اجرا می‌کند.",
            "یادگیری ماشین": "یادگیری ماشین زیرشاخه‌ای از هوش مصنوعی است که به کامپیوترها توانایی یادگیری از داده را می‌دهد."
        }
        
        if knowledge_file.exists():
            try:
                with open(knowledge_file, 'r', encoding='utf-8') as f:
                    return {**base_knowledge, **json.load(f)}
            except:
                return base_knowledge
        
        # ذخیره دانش پایه
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(base_knowledge, f, ensure_ascii=False, indent=2)
        
        return base_knowledge
    
    def save_knowledge(self):
        """ذخیره دانش"""
        knowledge_file = self.knowledge_dir / "base_knowledge.json"
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge, f, ensure_ascii=False, indent=2)
    
    def analyze_question(self, question):
        """تحلیل سوال"""
        question_lower = question.lower()
        
        # بررسی الگوها
        for pattern_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, question_lower, re.IGNORECASE):
                    return {"type": pattern_type, "topic": pattern_type}
        
        # شناسایی موضوع
        for topic in self.knowledge.keys():
            if topic in question:
                return {"type": "knowledge_query", "topic": topic}
        
        return {"type": "general", "topic": "عمومی"}
    
    def generate_answer(self, question, analysis):
        """تولید پاسخ"""
        self.stats["questions_asked"] += 1
        
        # پردازش بر اساس نوع
        if analysis["type"] == "greeting":
            return f"سلام {self.user_name}! خوش آمدید. چطور می‌تونم کمک کنم؟"
        
        elif analysis["type"] == "name_query":
            return f"من natiq-ultimate هستم، دستیار هوشمند فارسی شما!"
        
        elif analysis["type"] == "name_set":
            match = re.search(r"اسم من (\w+)", question)
            if match:
                self.user_name = match.group(1)
                return f"سلام {self.user_name}! خوشحالم که شما را می‌شناسم."
        
        elif analysis["type"] == "learn":
            match = re.search(r"یاد بگیر (.+)\|(.+)", question)
            if match:
                key = match.group(1).strip()
                value = match.group(2).strip()
                self.knowledge[key] = value
                self.save_knowledge()
                self.stats["topics_covered"].add(key)
                return f"موفقیت! '{key}' را یاد گرفتم: {value}"
        
        elif analysis["type"] == "stats":
            return f"📊 آمار جلسه:\nسوالات: {self.stats['questions_asked']}\nموضوعات: {len(self.stats['topics_covered'])}\nکاربر: {self.user_name}"
        
        elif analysis["type"] == "topics":
            topics = list(self.knowledge.keys())[:10]
            return f"📚 موضوعات موجود:\n" + "\n".join([f"• {topic}" for topic in topics])
        
        elif analysis["type"] == "knowledge_query":
            topic = analysis["topic"]
            if topic in self.knowledge:
                self.stats["topics_covered"].add(topic)
                return self.knowledge[topic]
        
        # پاسخ پیش‌فرض
        responses = [
            "متأسفانه پاسخ این سوال را نمی‌دانم. می‌توانید با فرمت 'یاد بگیر سوال|پاسخ' به من آموزش دهید.",
            "این موضوع را به خوبی نمی‌شناسم. لطفاً با جملات ساده‌تر بپرسید.",
            "علاقه‌مندم در این مورد یاد بگیرم! می‌توانید اطلاعات بیشتری بدهید؟",
            f"در حال حاضر اطلاعات کافی درباره '{question}' ندارم. می‌توانید با دستور یادگیری به من آموزش دهید."
        ]
        
        return responses[self.stats["questions_asked"] % len(responses)]
    
    def save_conversation(self, question, answer):
        """ذخیره گفتگو"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        conv_file = self.conv_dir / f"conversation_{timestamp}.json"
        
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "user": self.user_name
        }
        
        with open(conv_file, 'w', encoding='utf-8') as f:
            json.dump(conversation, f, ensure_ascii=False, indent=2)

# ایجاد نمونه global برای تست
if __name__ == "__main__":
    natiq = NatiqSmart()
    print("🤖 natiq-ultimate فعال شد!")
    print("برای تست:")
    print("1. 'سلام'")
    print("2. 'اسم من علی'")
    print("3. 'یاد بگیر پایتون|زبان برنامه‌نویسی'")
    print("4. 'آمار'")
PYTHON
    
    log_info "فایل natiq_smart.py ایجاد شد"
else
    log_info "فایل natiq_smart.py یافت شد"
fi

# راه‌اندازی سرور
log_step "راه‌اندازی سرور..."
echo ""
echo "🌐 سرور در حال اجرا است:"
echo "   📍 آدرس محلی: http://localhost:8000"
echo "   📍 آدرس Termux: http://127.0.0.1:8000"
echo ""
echo "📱 برای دسترسی از مرورگر:"
echo "   1. مرورگر را باز کنید"
echo "   2. آدرس زیر را وارد کنید:"
echo "      http://localhost:8000"
echo ""
echo "🔧 برای توقف سرور: Ctrl+C"
echo "=========================================="

# اجرای سرور
cd backend
python3 server.py
