#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات وحدة لمولد جلسات Pyrogram
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# إضافة المجلد src للمسار
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from session_generator import SessionGenerator

class TestSessionGenerator(unittest.TestCase):
    """اختبارات كلاس SessionGenerator"""
    
    def setUp(self):
        """تهيئة قبل كل اختبار"""
        self.generator = SessionGenerator()
        
    def test_initialization(self):
        """اختبار تهيئة الكلاس"""
        self.assertIsNone(self.generator.api_id)
        self.assertIsNone(self.generator.api_hash)
        self.assertIsNone(self.generator.session_string)
        
    def test_clear_screen(self):
        """اختبار مسح الشاشة"""
        # فقط نتأكد أن الدالة لا ترمي خطأ
        try:
            self.generator.clear_screen()
            result = True
        except:
            result = False
        self.assertTrue(result)
        
    def test_print_message_types(self):
        """اختبار أنواع الرسائل"""
        message_types = ["success", "error", "info", "warning"]
        for msg_type in message_types:
            # نتأكد أن الدالة تعمل لكل الأنواع
            try:
                self.generator.print_message(msg_type, "رسالة اختبار")
                result = True
            except:
                result = False
            self.assertTrue(result)
            
    @patch('builtins.input')
    def test_get_api_credentials_valid(self, mock_input):
        """اختبار إدخال بيانات API صحيحة"""
        # محاكاة إدخال المستخدم
        mock_input.side_effect = ["123456", "test_hash_123"]
        
        result = self.generator.get_api_credentials()
        
        self.assertTrue(result)
        self.assertEqual(self.generator.api_id, 123456)
        self.assertEqual(self.generator.api_hash, "test_hash_123")
        
    @patch('builtins.input')
    def test_get_api_credentials_invalid_id(self, mock_input):
        """اختبار إدخال API ID غير صحيح"""
        mock_input.side_effect = ["invalid", "123456", "test_hash"]
        
        result = self.generator.get_api_credentials()
        
        self.assertTrue(result)
        self.assertEqual(self.generator.api_id, 123456)
        
    def test_generate_session_missing_credentials(self):
        """اختبار إنشاء جلسة بدون بيانات API"""
        result = self.generator.generate_session()
        self.assertFalse(result)
        
    @patch('session_generator.Client')
    def test_generate_session_success(self, mock_client):
        """اختبار إنشاء جلسة بنجاح"""
        # تجهيز البيانات المطلوبة
        self.generator.api_id = 123456
        self.generator.api_hash = "test_hash"
        
        # محاكاة عميل Pyrogram
        mock_client_instance = MagicMock()
        mock_client.return_value.__enter__.return_value = mock_client_instance
        mock_client_instance.get_me.return_value = MagicMock(first_name="Test User")
        mock_client_instance.export_session_string.return_value = "test_session_string_123"
        
        result = self.generator.generate_session()
        
        self.assertTrue(result)
        self.assertEqual(self.generator.session_string, "test_session_string_123")
        
    def test_save_session_no_session(self):
        """اختبار حفظ جلسة غير موجودة"""
        result = self.generator.save_session()
        self.assertFalse(result)
        
    def test_save_session_with_session(self):
        """اختبار حفظ جلسة موجودة"""
        self.generator.session_string = "test_session_string"
        self.generator.api_id = 123456
        
        with patch('builtins.open', unittest.mock.mock_open()) as mock_file:
            result = self.generator.save_session()
            self.assertTrue(result)
            mock_file.assert_called_once()
            
    def test_display_session(self):
        """اختبار عرض الجلسة"""
        self.generator.session_string = "test_session"
        
        with patch('builtins.print') as mock_print:
            self.generator.display_session()
            # نتأكد أن print تم استدعاؤه
            self.assertTrue(mock_print.called)
            
    @patch('builtins.input')
    @patch('session_generator.Client')
    def test_test_session_success(self, mock_client, mock_input):
        """اختبار اختبار جلسة صالحة"""
        mock_input.return_value = 'y'
        self.generator.api_id = 123456
        self.generator.api_hash = "test_hash"
        self.generator.session_string = "test_session"
        
        mock_client_instance = MagicMock()
        mock_client.return_value.__enter__.return_value = mock_client_instance
        mock_client_instance.get_me.return_value = MagicMock(first_name="Test")
        
        with patch('builtins.print') as mock_print:
            self.generator.test_session()
            self.assertTrue(mock_print.called)
            
    @patch('builtins.input')
    def test_test_session_skip(self, mock_input):
        """اختبار تخطي اختبار الجلسة"""
        mock_input.return_value = 'n'
        
        with patch('builtins.print') as mock_print:
            self.generator.test_session()
            # نتأكد أن رسالة النجاح لم تظهر
            calls = [str(call) for call in mock_print.call_args_list]
            self.assertNotIn("✅ الجلسة صالحة!", str(calls))

class TestMainFunction(unittest.TestCase):
    """اختبارات الدالة الرئيسية"""
    
    @patch('session_generator.SessionGenerator')
    def test_main_success(self, mock_generator_class):
        """اختبار تشغيل البرنامج بنجاح"""
        from session_generator import main
        
        mock_instance = MagicMock()
        mock_generator_class.return_value = mock_instance
        
        with patch('builtins.print'):
            main()
            
        mock_instance.run.assert_called_once()
        
    @patch('session_generator.SessionGenerator')
    def test_main_keyboard_interrupt(self, mock_generator_class):
        """اختبار مقاطعة المستخدم Ctrl+C"""
        from session_generator import main
        
        mock_instance = MagicMock()
        mock_instance.run.side_effect = KeyboardInterrupt()
        mock_generator_class.return_value = mock_instance
        
        with patch('builtins.print'):
            with self.assertRaises(SystemExit):
                main()
                
    @patch('session_generator.SessionGenerator')
    def test_main_general_exception(self, mock_generator_class):
        """اختبار خطأ عام"""
        from session_generator import main
        
        mock_instance = MagicMock()
        mock_instance.run.side_effect = Exception("Test error")
        mock_generator_class.return_value = mock_instance
        
        with patch('builtins.print'):
            with self.assertRaises(SystemExit):
                main()

if __name__ == '__main__':
    unittest.main()
