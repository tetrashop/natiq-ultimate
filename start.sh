#!/bin/bash
echo "🚀 راه‌اندازی نطق مصطلح..."
pkill -f "node.*natiq" 2>/dev/null
cd ~/natiq-ultimate
node natiq-server.cjs > natiq.log 2>&1 &
sleep 2
echo "✅ سیستم راه‌اندازی شد!"
echo "🌐 آدرس: http://localhost:3001"
echo "📋 لاگ: tail -f natiq.log"
