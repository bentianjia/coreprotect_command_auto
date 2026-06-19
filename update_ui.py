import re

with open("CoreProtectGenerator.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Insert Version Selector
version_selector_html = """
        <div class="version-selector" style="margin-bottom: 2rem; display: flex; gap: 0.5rem; align-items: center; background: var(--bg-card); padding: 0.8rem 1rem; border-radius: var(--radius-md); border: 1px solid var(--border-color); box-shadow: var(--shadow-sm);">
            <label style="font-size: 0.85rem; font-weight: 500; margin-right: 0.5rem;" data-i18n="version">Minecraft 版本</label>
            <select id="majorVersion" style="width: auto; flex: 1; padding: 0.4rem; cursor: pointer;"></select>
            <select id="minorVersion" style="width: auto; flex: 1; padding: 0.4rem; cursor: pointer;"></select>
        </div>
        <div class="grid-layout">
"""
html = html.replace('<div class="grid-layout">', version_selector_html)

# 2. Update User Field HTML
old_user_html = """<!-- User -->
                <div class="form-group">
                    <label><span data-i18n="user">玩家</span> <span class="param-badge">u:</span></label>
                    <input type="text" id="paramUser" data-i18n-ph="user_ph" placeholder="例如 Notch, Jeb_">
                    <div class="tag-container">
                        <span class="tag" data-target="paramUser" data-val="#fire">#fire</span>
                        <span class="tag" data-target="paramUser" data-val="#tnt">#tnt</span>
                        <span class="tag" data-target="paramUser" data-val="#creeper">#creeper</span>
                        <span class="tag" data-target="paramUser" data-val="#explosion">#explosion</span>
                    </div>
                </div>"""

new_user_html = """<!-- User -->
                <div class="form-group searchable-select" id="userGroup">
                    <label><span data-i18n="user">玩家/实体</span> <span class="param-badge">u:</span></label>
                    <input type="text" id="paramUser" data-i18n-ph="user_ph" placeholder="例如 Notch 或输入实体名称..." autocomplete="off">
                    <div class="search-dropdown" id="userDropdown"></div>
                    <div class="selected-items" id="userItems"></div>
                    <div class="tag-container" style="margin-top:0.4rem;">
                        <span class="tag" data-target="paramUser" data-val="#fire">#fire</span>
                        <span class="tag" data-target="paramUser" data-val="#tnt">#tnt</span>
                        <span class="tag" data-target="paramUser" data-val="#explosion">#explosion</span>
                    </div>
                </div>"""

html = html.replace(old_user_html, new_user_html)

# Add "version" and "user" to i18n
html = html.replace('title: "CoreProtect",', 'title: "CoreProtect",\n                version: "游戏版本 (Version)",\n                user: "玩家/实体",\n                user_ph: "输入玩家名或搜索实体...",')
html = html.replace('title: "CoreProtect",\n                lookup: "Lookup"', 'title: "CoreProtect",\n                version: "Game Version",\n                user: "User / Entity",\n                user_ph: "Type name or search entity...",\n                lookup: "Lookup"')

with open("CoreProtectGenerator.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML DOM updated successfully.")
