#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
اختبارات أداء مولد الجلسات
"""

import unittest
import time
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from session_generator import SessionGenerator

class TestPerformance(unittest.TestCase):
    """اختبارات الأداء"""
    
    def setUp(self):
        self.generator = SessionGenerator()
        
    def test_print_message_performance(self):
        """اختبار سرعة طباعة الرسائل"""
        start_time = time.time()
        
        for i in range(1000):
            self.generator.print_message("info", f"رسالة اختبار {i}")
            
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n⏱️ طباعة 1000 رسالة استغرقت: {duration:.4f} ثانية")
        self.assertLess(duration, 2.0, "طباعة 1000 رسالة بطيئة جداً!")
        
    def test_api_credentials_input_performance(self):
        """اختبار سرعة معالجة إدخال بيانات API"""
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["123456", "test_hash"]
            
            start_time = time.time()
            result = self.generator.get_api_credentials()
            end_time = time.time()
            
            duration = end_time - start_time
            self.assertTrue(result)
            print(f"\n⏱️ معالجة بيانات API استغرقت: {duration:.4f} ثانية")
            self.assertLess(duration, 0.1, "معالجة بيانات API بطيئة!")
            
    @patch('session_generator.Client')
    def test_session_generation_performance_mock(self, mock_client):
        """اختبار سرعة إنشاء الجلسة (محاكاة)"""
        self.generator.api_id = 123456
        self.generator.api_hash = "test_hash"
        
        mock_client_instance = MagicMock()
        mock_client.return_value.__enter__.return_value = mock_client_instance
        mock_client_instance.get_me.return_value = MagicMock(first_name="Test")
        mock_client_instance.export_session_string.return_value = "test_string"
        
        start_time = time.time()
        result = self.generator.generate_session()
        end_time = time.time()
        
        duration = end_time - start_time
        self.assertTrue(result)
        print(f"\n⏱️ إنشاء جلسة (محاكاة) استغرق: {duration:.4f} ثانية")
        self.assertLess(duration, 0.5, "إنشاء الجلسة بطيء!")

if __name__ == '__main__':
    unittest.main()
