# tests/conftest.py
import sys
import os

# Add project/src to sys.path so tests can import src packages
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
