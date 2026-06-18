import webview
import os
import sys

def get_resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

if __name__ == '__main__':
    html_path = get_resource_path('CoreProtectGenerator.html')
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    window = webview.create_window(
        'CoreProtect Command Generator', 
        html=html_content,
        width=900, 
        height=800,
        min_size=(600, 500)
    )
    webview.start()
