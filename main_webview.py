import webview
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

html_path = resource_path('CoreProtectGenerator.html')

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Create a clean window wrapper
webview.create_window('CoreProtect Generator by bentianjia', html=html, width=900, height=750, background_color='#1c1c1e')
webview.start()
