#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
مشغل برنامج استخراج جلسات Pyrogram
"""

import sys
import os

# إضافة المجلد src للمسار
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from session_generator import الرئيسي

if __name__ == "__main__":
    الرئيسي()
