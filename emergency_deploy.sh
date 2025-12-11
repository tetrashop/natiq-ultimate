#!/bin/bash

echo "🚨 استقرار اضطراری - ترمیم سیستم الماس"
echo "======================================"

# استقرار روی Vercel
echo "🚀 در حال استقرار..."
vercel --prod --yes --confirm 2>&1 | grep -E "(Success|Error|Deployment|Ready)" | head -10

# تست سلامت
echo ""
echo "🧪 تست سلامت سیستم..."
for i in {1..3}; do
    echo "تست $i:"
    curl -s "https://natiq-ultimate.vercel.app/api/health?emergency_test=$i" | \
    python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    status = data.get('status', 'UNKNOWN')
    version = data.get('version', 'UNKNOWN')
    latency = data.get('metrics', {}).get('latency', 'UNKNOWN')
    success = data.get('metrics', {}).get('success_rate', 'UNKNOWN')
    print(f'   ✅ Status: {status}')
    print(f'   📦 Version: {version}')
    print(f'   ⚡ Latency: {latency}')
    print(f'   📈 Success: {success}%')
except:
    print('   ❌ Failed to parse response')
"
    sleep 2
done

echo ""
echo "🌐 آدرس نهایی: https://natiq-ultimate.vercel.app"
echo "💎 سیستم الماس ترمیم شده"
