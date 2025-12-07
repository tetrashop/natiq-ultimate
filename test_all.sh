#!/bin/bash
echo "🧪 تست تمام نسخه‌های natiq"
echo "==============================="

echo "1. تست نسخه ارتقا یافته آفلاین..."
python src/enhanced_ai.py

echo -e "\n2. تست نسخه API رایگان..."
python src/free_api_ai.py

echo -e "\n3. برای اجرای سرور وب، دستور زیر را اجرا کنید:"
echo "   python src/natiq_server.py"
echo "   سپس در مرورگر: http://localhost:8080"
