#!/bin/bash
cd ~/natiq-ultimate
git add .
git commit -m "به‌روزرسانی: $(date '+%Y-%m-%d %H:%M')"
git push origin main
