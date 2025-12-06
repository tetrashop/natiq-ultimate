#!/bin/bash
cd ~/natiq-ultimate

# ایجاد backup
cp super-simple-server.js super-simple-server.js.backup

# اصلاح کد جستجو
sed -i '/function simpleSearch(query) {/,/^}/ {
    /function simpleSearch(query) {/ {
        a\
    console.log("🔍 جستجو برای: " + query);
    }
}' super-simple-server.js

# اضافه کردن log به handler جستجو
sed -i '/if (parsedUrl.pathname === .api.search.*GET/) {
    a\
        console.log("📥 درخواست جستجو دریافت شد: " + query);
}' super-simple-server.js

echo "✅ کد جستجو اصلاح شد"
