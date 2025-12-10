"""
ماژول قابلیت‌های پیشرفته چت
"""

# دیکشنری برای ذخیره حافظه مکالمه (در حافظه سرور - موقت)
conversation_memory = {}

def get_memory(session_id="default"):
    """دریافت حافظه مکالمه یک session"""
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    return conversation_memory[session_id]

def add_to_memory(session_id, role, content):
    """افزودن پیام به حافظه"""
    memory = get_memory(session_id)
    memory.append({"role": role, "content": content})
    
    # محدود کردن تاریخچه به ۵ پیام آخر (برای جلوگیری از overload)
    if len(memory) > 5:
        conversation_memory[session_id] = memory[-5:]
    
    return len(memory)

def clear_memory(session_id="default"):
    """پاکسازی حافظه یک session"""
    if session_id in conversation_memory:
        del conversation_memory[session_id]
        return True
    return False

def generate_smart_response_with_memory(message, session_id="default"):
    """تولید پاسخ هوشمند با توجه به تاریخچه مکالمه"""
    memory = get_memory(session_id)
    
    # اگر حافظه خالی است، پاسخ معمولی بده
    if not memory:
        return "سلام! اولین پیام شما رو دریافت کردم. از این به بعد مکالممون رو به خاطر می‌سپارم. 😊"
    
    # بررسی آخرین پیام‌ها
    last_messages = memory[-3:] if len(memory) >= 3 else memory
    
    # پاسخ‌های هوشمند بر اساس تاریخچه
    message_lower = message.lower()
    
    if "قبلا" in message_lower or "یادت هست" in message_lower:
        last_user_msg = ""
        for msg in reversed(last_messages):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break
        
        if last_user_msg:
            return f"بله یادمه! قبلاً گفتی: '{last_user_msg[:30]}...' 😊"
    
    if "حافظه" in message_lower and ("چنده" in message_lower or "چند" in message_lower):
        return f"حافظه ما {len(memory)} پیام داره. می‌تونم تا ۵ پیام آخر رو به خاطر بسپارم."
    
    if "پاک کن" in message_lower and "حافظه" in message_lower:
        clear_memory(session_id)
        return "حافظه مکالمه پاک شد! از نو شروع می‌کنیم. 🔄"
    
    # پاسخ پیش‌فرض
    return f"پیامت رو با توجه به {len(memory)} پیام قبلی دریافت کردم. در حال پردازش..."
