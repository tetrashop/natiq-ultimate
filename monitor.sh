#!/bin/bash
echo "📊 مانیتورینگ سیستم ناطق اولتیمیت"
echo "================================="

while true; do
    echo -n "$(date '+%H:%M:%S') - "
    
    # چک سلامت API
    if curl -s https://natiq-ultimate.vercel.app/api/health | grep -q '"status":"healthy"'; then
        echo "✅ سیستم سالم"
    else
        echo "❌ مشکل در سیستم"
    fi
    
    sleep 30
done
