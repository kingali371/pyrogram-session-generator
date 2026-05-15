#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
برنامج عربي لاستخراج جلسات Pyrogram
النسخة المحسنة للمشروع على GitHub
"""

from pyrogram import Client
from pyrogram.errors import (
    PhoneCodeInvalid, 
    SessionPasswordNeeded, 
    PhoneNumberInvalid,
    FloodWait
)
import os
import sys
import time
from colorama import init, Fore, Style

# تهيئة colorama للنوافذ
init()

class SessionGenerator:
    """الكلاس الرئيسي لتوليد الجلسات"""
    
    def __init__(self):
        self.api_id = None
        self.api_hash = None
        self.session_string = None
        
    def clear_screen(self):
        """مسح الشاشة"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_banner(self):
        """عرض الشعار"""
        print(f"{Fore.CYAN}{Style.BRIGHT}")
        print("╔══════════════════════════════════════════════════════╗")
        print("║     🌟 مولد جلسات Pyrogram - الإصدار 1.0.0 🌟       ║")
        print("║          برمجة عربية احترافية بالكامل               ║")
        print("║        GitHub: github.com/YourUsername               ║")
        print("╚══════════════════════════════════════════════════════╝")
        print(f"{Style.RESET_ALL}")
    
    def print_message(self, msg_type, text):
        """طباعة رسائل ملونة"""
        colors = {
            "success": f"{Fore.GREEN}✅ {text}{Style.RESET_ALL}",
            "error": f"{Fore.RED}❌ {text}{Style.RESET_ALL}",
            "info": f"{Fore.BLUE}ℹ️ {text}{Style.RESET_ALL}",
            "warning": f"{Fore.YELLOW}⚠️ {text}{Style.RESET_ALL}"
        }
        print(colors.get(msg_type, text))
    
    def get_api_credentials(self):
        """الحصول على بيانات API"""
        self.print_message("info", "أدخل بيانات API من my.telegram.org")
        
        while True:
            try:
                self.api_id = int(input(f"{Fore.YELLOW}🔢 API ID: {Style.RESET_ALL}"))
                if self.api_id <= 0:
                    self.print_message("error", "API ID يجب أن يكون رقماً موجباً")
                    continue
                break
            except ValueError:
                self.print_message("error", "API ID يجب أن يكون رقماً")
        
        self.api_hash = input(f"{Fore.YELLOW}🔑 API HASH: {Style.RESET_ALL}").strip()
        if not self.api_hash:
            self.print_message("error", "API HASH لا يمكن أن يكون فارغاً")
            return self.get_api_credentials()
        
        return True
    
    def generate_session(self):
        """إنشاء الجلسة"""
        self.print_message("info", "جاري الاتصال بخوادم تلجرام...")
        
        client = Client(
            name=":memory:",
            api_id=self.api_id,
            api_hash=self.api_hash,
            in_memory=True
        )
        
        try:
            with client:
                self.print_message("success", "تم الاتصال بنجاح!")
                
                # الحصول على معلومات المستخدم
                me = client.get_me()
                self.print_message("success", f"مرحباً {me.first_name}!")
                
                # تصدير الجلسة
                self.session_string = client.export_session_string()
                
                return True
                
        except FloodWait as e:
            self.print_message("warning", f"الانتظار {e.value} ثانية...")
            time.sleep(e.value)
            return self.generate_session()
        except Exception as e:
            self.print_message("error", f"خطأ: {str(e)}")
            return False
    
    def save_session(self):
        """حفظ الجلسة في ملف"""
        if not self.session_string:
            return False
        
        filename = f"session_{self.api_id}_{int(time.time())}.txt"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# جلسة Pyrogram\n")
            f.write(f"# تاريخ الإنشاء: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# API ID: {self.api_id}\n")
            f.write(f"{'='*50}\n\n")
            f.write(self.session_string)
        
        self.print_message("success", f"تم حفظ الجلسة في: {filename}")
        return filename
    
    def display_session(self):
        """عرض الجلسة على الشاشة"""
        print(f"\n{Fore.GREEN}{Style.BRIGHT}{'='*60}")
        print("جلسة Pyrogram الخاصة بك:")
        print(f"{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{self.session_string}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}\n")
    
    def test_session(self):
        """اختبار الجلسة"""
        self.print_message("info", "هل تريد اختبار الجلسة؟ (y/n): ", end="")
        if input().lower() == 'y':
            try:
                client = Client(
                    "test_session",
                    api_id=self.api_id,
                    api_hash=self.api_hash,
                    session_string=self.session_string
                )
                
                with client:
                    me = client.get_me()
                    self.print_message("success", f"✅ الجلسة صالحة! مرحباً {me.first_name}")
                    
            except Exception as e:
                self.print_message("error", f"❌ فشل الاختبار: {str(e)}")
    
    def run(self):
        """تشغيل البرنامج"""
        self.clear_screen()
        self.print_banner()
        
        self.print_message("info", "مرحباً بك في مولد جلسات Pyrogram!")
        self.print_message("warning", "تأكد من أن لديك اتصالاً بالإنترنت")
        
        # الحصول على بيانات API
        if not self.get_api_credentials():
            return
        
        # إنشاء الجلسة
        if self.generate_session():
            self.display_session()
            self.save_session()
            self.test_session()
            
            self.print_message("success", "\n✨ تمت العملية بنجاح! ✨")
            self.print_message("info", "شكراً لاستخدام البرنامج! 👋")
        else:
            self.print_message("error", "فشل إنشاء الجلسة. حاول مرة أخرى")

def main():
    """الدالة الرئيسية"""
    try:
        generator = SessionGenerator()
        generator.run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️ تم إلغاء العملية{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ خطأ غير متوقع: {str(e)}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
