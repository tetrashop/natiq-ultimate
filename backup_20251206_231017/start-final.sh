#!/bin/bash
echo "🚀 راه‌اندازی نهایی نطق مصطلح..."
cd ~/natiq-ultimate
pkill -f "node.*server" 2>/dev/null
sleep 1
node server.cjs > server.log 2>&1 &
sleep 2
echo "✅ سرور راه‌اندازی شد!"
echo "🌐 آدرس API: http://localhost:3001"
echo "🌐 آدرس وب: file://$(pwd)/index.html"
echo "📋 لاگ: tail -f server.log"
