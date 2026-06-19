import re

with open("CoreProtectGenerator.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the search logic robustly
old_search_logic = r"const filtered = MC_DATA\.filter\(item =>[\s\S]*?\.slice\(0, 10\);"
new_search_logic = """const queryParts = query.toLowerCase().split(/\\s+/);
                const filtered = MC_DATA.filter(item => 
                    queryParts.every(part => item.s.includes(part))
                ).slice(0, 30);"""

html = re.sub(old_search_logic, new_search_logic, html)

# If it didn't match because my previous script successfully replaced it to slice(0, 30), let's fix that
old_search_logic2 = r"const filtered = MC_DATA\.filter\(item =>[\s\S]*?\.slice\(0, 30\);"
html = re.sub(old_search_logic2, new_search_logic, html)

# Ensure bentianjia is in the title
if "bentianjia" not in html:
    html = html.replace('<h1 data-i18n="title">CoreProtect</h1>', '<h1 data-i18n="title">CoreProtect</h1>\\n<span style="font-size:0.8rem; color:var(--text-muted); font-weight:normal; margin-left:8px;">by bentianjia</span>')

with open("CoreProtectGenerator.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Logic fixed!")
