import subprocess
import webview
import time
import sys

import ctypes
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

process = subprocess.Popen([
    "streamlit", 
    "run",
    "app/main.py"
    ])

time.sleep(3)

webview.create_window("AgroBoard [Client]", "http://localhost:8510", resizable=True, maximized=True, min_size=(screen_width, screen_height))
webview.start()
process.terminate()

