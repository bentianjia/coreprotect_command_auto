import json
import re

with open("mc_data.json", "r", encoding="utf-8") as f:
    mc_data = json.load(f)

json_str = json.dumps(mc_data, ensure_ascii=False)

with open("CoreProtectGenerator.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace MC_DATA array
html = re.sub(
    r"const MC_DATA = \[.*?\];",
    f"const MC_DATA = {json_str};",
    html,
    flags=re.DOTALL
)

# Update search logic to use the new 's' property which contains pinyin and aliases
html = html.replace(
    """const filtered = MC_DATA.filter(item => 
                    item.id.toLowerCase().includes(query) || 
                    item.en.toLowerCase().includes(query) || 
                    item.zh.includes(query)
                ).slice(0, 10);""",
    """const filtered = MC_DATA.filter(item => 
                    item.s.includes(query)
                ).slice(0, 30);"""
)

# Update the header to include author credit
html = html.replace(
    '<h1 data-i18n="title">CoreProtect</h1>',
    '<h1 data-i18n="title">CoreProtect</h1>\n                <span style="font-size:0.75rem; color:var(--text-muted); font-weight:normal; margin-left:8px;">by bentianjia</span>'
)

with open("CoreProtectGenerator.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML updated successfully.")
