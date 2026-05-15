#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
سكريبت استخراج جلسة Pyrogram يعمل على GitHub Actions
يتلقى البيانات من متغيرات البيئة وليس من الإدخال المباشر
"""

import os
import sys
import time
from pyrogram import Client
from pyrogram.errors import FloodWait, PhoneNumberInvalid, PhoneCodeInvalid

# قراءة البيانات من متغيرات البيئة (GitHub Secrets)
API_ID = os.environ.get("API_ID")
API_HASH = os.environ.get("API_HASH")
PHONE_NUMBER = os.environ.get("PHONE_NUMBER")
PHONE_CODE = os.environ.get("PHONE_CODE", "")  # رمز التحقق (قد يكون فارغاً في البداية)
PASSWORD = os.environ.get("PASSWORD", "")      # كلمة المرور للتفعيل الثنائي (اختياري)

def print_colored(text, color="white"):
    """طباعة نص ملون في GitHub Actions logs"""
    colors = {
        "green": "\033[92m",
        "red": "\033[91m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "white": "\033[0m"
    }
    print(f"{colors.get(color, colors['white'])}{text}{colors['white']}")

def create_session():
    """إنشاء جلسة Pyrogram"""
    
    # التحقق من وجود البيانات الأساسية
    if not API_ID or not API_HASH or not PHONE_NUMBER:
        print_colored("❌ خطأ: API_ID, API_HASH, PHONE_NUMBER مطلوبة", "red")
        print_colored("تأكد من إضافتها في GitHub Secrets", "yellow")
        return None
    
    try:
        api_id_int = int(API_ID)
    except ValueError:
        print_colored("❌ خطأ: API_ID يجب أن يكون رقماً", "red")
        return None
    
    print_colored("🚀 بدء عملية استخراج الجلسة...", "blue")
    print_colored(f"📱 رقم الهاتف: {PHONE_NUMBER}", "yellow")
    
    # إنشاء العميل
    client = Client(
        name=":memory:",  # جلسة مؤقتة في الذاكرة
        api_id=api_id_int,
        api_hash=API_HASH,
        in_memory=True
    )
    
    try:
        with client:
            print_colored("✅ تم الاتصال بخوادم تلجرام", "green")
            
            # إرسال رمز التحقق
            try:
                sent_code = client.send_code(PHONE_NUMBER)
                print_colored("📲 تم إرسال رمز التحقق إلى هاتفك", "green")
                print_colored(f"📝 نوع الرمز: {sent_code.type}", "yellow")
                
                # انتظار رمز التحقق من المستخدم
                if not PHONE_CODE:
                    print_colored("⚠️ انتظر... هذا السكريبت يحتاج إلى رمز التحقق", "yellow")
                    print_colored("💡 قم بإعادة تشغيل workflow مع إضافة PHONE_CODE في Secrets", "blue")
                    return None
                
                # محاولة تسجيل الدخول بالرمز
                try:
                    signed_in = client.sign_in(PHONE_NUMBER, PHONE_CODE)
                    print_colored("✅ تم التحقق من الرمز بنجاح!", "green")
                except PhoneCodeInvalid:
                    print_colored("❌ رمز التحقق غير صحيح", "red")
                    return None
                    
            except PhoneNumberInvalid:
                print_colored("❌ رقم الهاتف غير صحيح", "red")
                return None
            
            # التحقق من الحاجة لكلمة مرور (2FA)
            try:
                # محاولة الحصول على معلومات المستخدم
                me = client.get_me()
                print_colored(f"👤 مرحباً {me.first_name} {me.last_name or ''}", "green")
                
            except Exception as e:
                if "SESSION_PASSWORD_NEEDED" in str(e) or "PASSWORD" in str(e):
                    print_colored("🔐 مطلوب كلمة مرور (التحقق بخطوتين)", "yellow")
                    
                    if not PASSWORD:
                        print_colored("⚠️ يلزم إضافة PASSWORD في Secrets", "yellow")
                        return None
                    
                    try:
                        client.check_password(PASSWORD)
                        me = client.get_me()
                        print_colored(f"👤 مرحباً {me.first_name}", "green")
                    except Exception as pwd_err:
                        print_colored(f"❌ كلمة المرور غير صحيحة: {pwd_err}", "red")
                        return None
                else:
                    print_colored(f"❌ خطأ غير متوقع: {e}", "red")
                    return None
            
            # استخراج الجلسة النصية
            session_string = client.export_session_string()
            
            print_colored("\n" + "="*60, "green")
            print_colored("🎉 تم استخراج الجلسة بنجاح! 🎉", "green")
            print_colored("="*60, "green")
            print_colored("\n📋 جلسة Pyrogram الخاصة بك:", "yellow")
            print_colored("─"*60, "blue")
            print_colored(session_string, "white")
            print_colored("─"*60, "blue")
            print_colored("\n⚠️ تحذير أمني: لا تشارك هذه الجلسة مع أي شخص!", "red")
            print_colored("💾 احفظها في مكان آمن", "yellow")
            
            # حفظ الجلسة في ملف (يمكن تحميله كـ Artifact)
            with open("session.txt", "w") as f:
                f.write(session_string)
            
            return session_string
            
    except FloodWait as e:
        print_colored(f"⏳ انتظر {e.value} ثانية قبل المحاولة مرة أخرى", "yellow")
        time.sleep(e.value)
        return create_session()
    except Exception as e:
        print_colored(f"❌ خطأ: {e}", "red")
        return None

def main():
    """الدالة الرئيسية"""
    print_colored("\n" + "🌟" * 20, "blue")
    print_colored("🌟 مولد جلسات Pyrogram على GitHub Actions 🌟", "blue")
    print_colored("🌟" * 20, "blue")
    
    session = create_session()
    
    if session:
        print_colored("\n✅ العملية كاملة بنجاح!", "green")
        print_colored("📁 تم حفظ الجلسة في ملف session.txt", "yellow")
        print_colored("💡 يمكنك تنزيل الملف من Artifacts أسفل هذه الصفحة", "blue")
        return 0
    else:
        print_colored("\n❌ فشل إنشاء الجلسة", "red")
        print_colored("📝 تأكد من صحة البيانات في Secrets", "yellow")
        return 1

if __name__ == "__main__":
    sys.exit(main())
