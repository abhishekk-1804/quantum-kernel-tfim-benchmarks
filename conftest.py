"""
conftest.py — adds src/ to sys.path for pytest runs from project root.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
