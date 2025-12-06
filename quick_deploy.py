#!/usr/bin/env python3
"""
اسکریپت استقرار سریع با رابط کاربری
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
import questionary
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def check_dependencies():
    """بررسی وابستگی‌های سیستم"""
    deps = {
        "Git": ["git", "--version"],
        "Python": ["python3", "--version"],
        "Node.js": ["node", "--version"],
        "Vercel CLI": ["vercel", "--version"]
    }
    
    table = Table(title="بررسی وابستگی‌ها")
    table.add_column("ابزار", style="cyan")
    table.add_column("وضعیت", style="green")
    table.add_column("نسخه", style="yellow")
    
    for name, cmd in deps.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            if result.returncode == 0:
                version = result.stdout.strip()
                table.add_row(name, "✅ نصب شده", version)
            else:
                table.add_row(name, "❌ یافت نشد", "-")
        except:
            table.add_row(name, "❌ یافت نشد", "-")
    
    console.print(table)

def deploy_to_vercel():
    """استقرار روی Vercel"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("در حال استقرار روی Vercel...", total=None)
        
        # کپی فایل‌های مورد نیاز
        shutil.copy("vercel.json", "deploy/")
        shutil.copy("requirements-vercel.txt", "deploy/requirements.txt")
        shutil.copytree("api", "deploy/api", dirs_exist_ok=True)
        
        # اجرای دستور Vercel
        os.chdir("deploy")
        subprocess.run(["vercel", "--prod"], shell=False)
        os.chdir("..")
        
        progress.update(task, completed=100)
    
    console.print("[green]✅ استقرار Vercel تکمیل شد![/green]")

def deploy_to_github():
    """استقرار روی GitHub"""
    repo_url = questionary.text("آدرس ریپوی GitHub را وارد کنید:").ask()
    commit_msg = questionary.text("پیام commit را وارد کنید:").ask()
    
    if not commit_msg:
        commit_msg = "auto-deploy: استقرار خودکار"
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("در حال استقرار روی GitHub...", total=4)
        
        # 1. افزودن remote
        subprocess.run(["git", "remote", "add", "origin", repo_url], 
                      capture_output=True)
        progress.update(task, advance=1)
        
        # 2. افزودن فایل‌ها
        subprocess.run(["git", "add", "."])
        progress.update(task, advance=1)
        
        # 3. Commit
        subprocess.run(["git", "commit", "-m", commit_msg])
        progress.update(task, advance=1)
        
        # 4. Push
        subprocess.run(["git", "push", "-u", "origin", "main"])
        progress.update(task, advance=1)
    
    console.print(f"[green]✅ کد به {repo_url} پوش شد[/green]")

def main():
    """تابع اصلی"""
    console.print("[bold cyan]🚀 ابزار استقرار سریع natiq-ultimate[/bold cyan]")
    console.print("=" * 50)
    
    # بررسی وابستگی‌ها
    check_dependencies()
    
    # منوی اصلی
    choices = [
        "📦 استقرار روی Vercel",
        "🐙 استقرار روی GitHub", 
        "🐳 ساخت Docker Image",
        "📊 ایجاد گزارش",
        "🚪 خروج"
    ]
    
    while True:
        action = questionary.select(
            "چه کاری می‌خواهید انجام دهید؟",
            choices=choices
        ).ask()
        
        if action == choices[0]:  # Vercel
            if questionary.confirm("آیا مطمئنید؟").ask():
                deploy_to_vercel()
                
        elif action == choices[1]:  # GitHub
            if questionary.confirm("آیا مطمئنید؟").ask():
                deploy_to_github()
                
        elif action == choices[2]:  # Docker
            console.print("[yellow]در حال ساخت Docker Image...[/yellow]")
            subprocess.run(["docker", "build", "-t", "natiq-ultimate", "."])
            console.print("[green]✅ Docker Image ساخته شد[/green]")
            
        elif action == choices[3]:  # گزارش
            generate_report()
            
        elif action == choices[4]:  # خروج
            console.print("[cyan]خروج از برنامه...[/cyan]")
            break

def generate_report():
    """ایجاد گزارش استقرار"""
    report = {
        "project": "natiq-ultimate",
        "timestamp": subprocess.run(["date"], capture_output=True, text=True).stdout.strip(),
        "git_status": subprocess.run(["git", "status", "--short"], 
                                    capture_output=True, text=True).stdout,
        "file_count": len(list(Path(".").glob("**/*"))),
        "size_mb": sum(f.stat().st_size for f in Path(".").glob("**/*") if f.is_file()) / 1024 / 1024
    }
    
    # نمایش گزارش
    table = Table(title="گزارش استقرار")
    table.add_column("متریک", style="cyan")
    table.add_column("مقدار", style="green")
    
    for key, value in report.items():
        if key == "git_status":
            value = f"{len(value.splitlines())} فایل تغییر یافته"
        elif key == "size_mb":
            value = f"{value:.2f} MB"
        
        table.add_row(key.replace("_", " ").title(), str(value))
    
    console.print(table)

if __name__ == "__main__":
    main()

