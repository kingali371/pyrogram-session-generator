#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات أمان مولد الجلسات
"""

import unittest
import re
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestSecurity(unittest.TestCase):
    """اختبارات الأمان"""
    
    def test_no_hardcoded_credentials(self):
        """التأكد من عدم وجود بيانات دخول مخزنة في الكود"""
        with open('../src/session_generator.py', 'r', encoding='utf-8') as file:
            content = file.read()
            
        # البحث عن بيانات API مخزنة
        suspicious_patterns = [
            r'api_id\s*=\s*["\'][0-9]+["\']',
            r'api_hash\s*=\s*["\'][a-f0-9]+["\']',
            r'session_string\s*=\s*["\'][A-Za-z0-9]+["\']',
            r'bot_token\s*=\s*["\'][0-9]+:[A-Za-z0-9]+["\']',
        ]
        
        for pattern in suspicious_patterns:
            matches = re.findall(pattern, content)
            self.assertEqual(len(matches), 0, f"تم العثور على بيانات حساسة: {matches}")
            
    def test_no_password_in_logs(self):
        """التأكد من عدم طباعة كلمات المرور"""
        with open('../src/session_generator.py', 'r', encoding='utf-8') as file:
            content = file.read()
            
        # البحث عن طباعة كلمات المرور
        password_print = re.findall(r'print.*password', content, re.IGNORECASE)
        self.assertEqual(len(password_print), 0, "تم العثور على طباعة لكلمة المرور!")
        
    def test_session_string_not_logged(self):
        """التأكد من عدم طباعة الجلسة بشكل غير آمن"""
        with open('../src/session_generator.py', 'r', encoding='utf-8') as file:
            content = file.read()
            
        # البحث عن طباعة الجلسة (باستثناء display_session)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'display_session' in line:
                continue
            if 'session_string' in line and 'print' in line:
                self.fail(f"سطر {i+1}: تم طباعة session_string بشكل غير آمن!")
                
    def test_no_eval_usage(self):
        """التأكد من عدم استخدام eval على مدخلات المستخدم"""
        with open('../src/session_generator.py', 'r', encoding='utf-8') as file:
            content = file.read()
            
        self.assertNotIn('eval(', content)
        self.assertNotIn('exec(', content)
        self.assertNotIn('__import__', content)

if __name__ == '__main__':
    unittest.main()
