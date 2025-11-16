"""Run bot once and exit (for PythonAnywhere scheduled tasks)."""
import subprocess
import sys
import os

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Run bot for 55 minutes then exit (to fit within PythonAnywhere task slots)
try:
    subprocess.run([sys.executable, "main.py"], timeout=3300)
except subprocess.TimeoutExpired:
    print("Bot timeout - scheduled task will restart automatically")
except KeyboardInterrupt:
    print("Bot stopped")
