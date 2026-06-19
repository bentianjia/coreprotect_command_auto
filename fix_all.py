import re

with open("CoreProtectGenerator.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove 'by bentianjia'
html = re.sub(r'<span style="font-size:0.8rem; color:var\(--text-muted\); font-weight:normal; margin-left:8px;">by bentianjia</span>', '', html)

# 3. Update VERSIONS JSON in the script
# We'll map majors to a display string like "v26.2 (1.20)"
html = html.replace(
    'const VERSIONS = {"majors": ["1.20", "1.19", "1.18", "1.17", "1.16", "1.15", "1.14", "1.13"]',
    'const CP_VERSIONS = {"1.20": "v26.2", "1.19": "v21.3", "1.18": "v20.4", "1.17": "v20.1", "1.16": "v19.5", "1.15": "v19.0", "1.14": "v2.17.5", "1.13": "v2.16.3"};\n        const VERSIONS = {"majors": ["1.20", "1.19", "1.18", "1.17", "1.16", "1.15", "1.14", "1.13"]'
)

# Update initVersionSelector to use CP_VERSIONS
html = html.replace(
    'majorSelect.innerHTML = VERSIONS.majors.map(m => `<option value="${m}">${m}</option>`).join(\'\');',
    'majorSelect.innerHTML = VERSIONS.majors.map(m => `<option value="${m}">${CP_VERSIONS[m] || \'\'} (${m})</option>`).join(\'\');'
)

# 2, 4, 5. Fix JS missing functions (Tabs, Lang Switch, DOM Listeners)
# We will inject the missing listeners right before `function updateCommand()`
missing_js = """
        // Tab Switching Logic
        const tabBtns = document.querySelectorAll('.tab-btn');
        const paginationGroup = document.getElementById('paginationGroup');
        const hashtagGroup = document.getElementById('hashtagGroup');
        
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentCommand = btn.dataset.cmd;
                
                if (currentCommand === 'lookup') {
                    paginationGroup.style.display = 'flex';
                } else {
                    paginationGroup.style.display = 'none';
                }
                
                initHashtags();
                updateCommand();
            });
        });

        // Language Switching Logic
        const langSwitchBtn = document.getElementById('langSwitch');
        function switchLang() {
            currentLang = currentLang === 'zh' ? 'en' : 'zh';
            langSwitchBtn.textContent = i18nData[currentLang].lang_switch;
            
            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.dataset.i18n;
                if (i18nData[currentLang][key]) {
                    el.textContent = i18nData[currentLang][key];
                }
            });
            
            document.querySelectorAll('[data-i18n-ph]').forEach(el => {
                const key = el.dataset.i18nPh;
                if (i18nData[currentLang][key]) {
                    el.placeholder = i18nData[currentLang][key];
                }
            });
            
            renderSelectedItems(state.include, includeItems);
            renderSelectedItems(state.exclude, excludeItems);
            renderSelectedItems(state.user, userItems, true);
        }
        
        if (langSwitchBtn) {
            langSwitchBtn.addEventListener('click', switchLang);
        }

        // Add event listeners to inputs to trigger updateCommand
        document.querySelectorAll('input, select').forEach(el => {
            if (el.id !== 'paramIncludeSearch' && el.id !== 'paramExcludeSearch' && el.id !== 'paramUser') {
                el.addEventListener('input', updateCommand);
                el.addEventListener('change', updateCommand);
            }
        });
        
        document.getElementById('paramUser').addEventListener('input', updateCommand);
        document.getElementById('paramUser').addEventListener('blur', updateCommand);

"""

# Insert missing_js before updateCommand()
html = html.replace('function updateCommand() {', missing_js + '\n        function updateCommand() {')

with open("CoreProtectGenerator.html", "w", encoding="utf-8") as f:
    f.write(html)

print("HTML logic fixed!")
