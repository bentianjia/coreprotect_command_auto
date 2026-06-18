import json
import re

with open("mc_data_with_versions.json", "r", encoding="utf-8") as f:
    mc_data = f.read()

with open("versions.json", "r", encoding="utf-8") as f:
    versions = f.read()

with open("CoreProtectGenerator.html", "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(
    r"const MC_DATA = \[.*?\];",
    lambda m: f"const MC_DATA = {mc_data};\n        const VERSIONS = {versions};",
    html,
    flags=re.DOTALL
)

new_js_logic = r"""
        let currentVersionInt = 9999999;
        
        const majorSelect = document.getElementById('majorVersion');
        const minorSelect = document.getElementById('minorVersion');

        function initVersionSelector() {
            majorSelect.innerHTML = VERSIONS.majors.map(m => `<option value="${m}">${m}</option>`).join('');
            
            majorSelect.addEventListener('change', () => {
                const major = majorSelect.value;
                minorSelect.innerHTML = VERSIONS.minors[major].map(m => `<option value="${m}">${m}</option>`).join('');
                updateVersionInt();
            });

            minorSelect.addEventListener('change', updateVersionInt);

            majorSelect.dispatchEvent(new Event('change'));
        }

        function updateVersionInt() {
            const v = minorSelect.value;
            const parts = v.split('.');
            const major = parseInt(parts[0]) || 1;
            const minor = parseInt(parts[1]) || 0;
            const patch = parseInt(parts[2]) || 0;
            currentVersionInt = major * 100000 + minor * 1000 + patch;
            
            renderSelectedItems(state.include, includeItems);
            renderSelectedItems(state.exclude, excludeItems);
            renderSelectedItems(state.user, userItems, true);
            updateCommand();
        }

        const state = { include: new Set(), exclude: new Set(), user: new Set() };
        
        const includeSearch = document.getElementById('paramIncludeSearch');
        const excludeSearch = document.getElementById('paramExcludeSearch');
        const includeDropdown = document.getElementById('includeDropdown');
        const excludeDropdown = document.getElementById('excludeDropdown');
        const includeItems = document.getElementById('includeItems');
        const excludeItems = document.getElementById('excludeItems');
        
        const userSearch = document.getElementById('paramUser');
        const userDropdown = document.getElementById('userDropdown');
        const userItems = document.getElementById('userItems');

        function setupSearchable(searchInput, dropdown, set, itemsContainer, isUser = false) {
            searchInput.addEventListener('input', () => {
                const query = searchInput.value.toLowerCase().trim();
                if (!query) return dropdown.classList.remove('show');
                
                const queryParts = query.split(/\s+/);
                
                const filtered = MC_DATA.filter(item => {
                    if (item.vi > currentVersionInt) return false;
                    if (isUser && item.t !== 'entity') return false; 
                    return queryParts.every(part => item.s.includes(part));
                }).slice(0, 30);
                
                if (filtered.length > 0) {
                    dropdown.innerHTML = filtered.map(item => `
                        <div class="dropdown-item" data-id="${isUser ? '#' + item.id : item.id}">
                            <span class="zh-name">${currentLang === 'zh' ? item.zh : item.en}</span>
                            <span class="en-name">${isUser ? '#' + item.id : item.id}</span>
                        </div>
                    `).join('');
                } else {
                    dropdown.innerHTML = `<div class="dropdown-item" style="color:var(--text-muted); cursor:default;">${i18nData[currentLang].search_empty}</div>`;
                }
                dropdown.classList.add('show');
            });

            searchInput.addEventListener('keydown', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    let val = searchInput.value.trim().toLowerCase().replace(/ /g, '_');
                    if (val) {
                        if (isUser && !val.startsWith('#') && MC_DATA.some(d => d.id === val && d.t === 'entity')) {
                            val = '#' + val;
                        }
                        set.add(val);
                        renderSelectedItems(set, itemsContainer, isUser);
                        searchInput.value = '';
                        dropdown.classList.remove('show');
                        updateCommand();
                    }
                }
            });

            dropdown.addEventListener('mousedown', (e) => {
                const item = e.target.closest('.dropdown-item');
                if (item && item.dataset.id) {
                    set.add(item.dataset.id);
                    renderSelectedItems(set, itemsContainer, isUser);
                    searchInput.value = '';
                    dropdown.classList.remove('show');
                    updateCommand();
                }
            });

            searchInput.addEventListener('blur', () => {
                setTimeout(() => dropdown.classList.remove('show'), 150);
            });
            
            searchInput.addEventListener('focus', () => {
                if (searchInput.value.trim() !== '') {
                    dropdown.classList.add('show');
                }
            });
        }

        function renderSelectedItems(set, container, isUser = false) {
            container.innerHTML = Array.from(set).map(id => {
                const searchId = isUser && id.startsWith('#') ? id.substring(1) : id;
                const data = MC_DATA.find(d => d.id === searchId);
                let label = id;
                let isInvalid = false;
                
                if (data) {
                    label = `${currentLang === 'zh' ? data.zh : data.en} (${id})`;
                    if (data.vi > currentVersionInt) isInvalid = true;
                }
                
                const invalidStyle = isInvalid ? 'text-decoration: line-through; opacity: 0.5; color: red;' : '';
                return `<div class="selected-item" style="${invalidStyle}"><span title="${isInvalid ? '该版本不存在此物品' : ''}">${label}</span><span class="remove" data-id="${id}">×</span></div>`;
            }).join('');
            
            container.querySelectorAll('.remove').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    set.delete(e.target.dataset.id);
                    renderSelectedItems(set, container, isUser);
                    updateCommand();
                });
            });
        }

        setupSearchable(includeSearch, includeDropdown, state.include, includeItems);
        setupSearchable(excludeSearch, excludeDropdown, state.exclude, excludeItems);
        setupSearchable(userSearch, userDropdown, state.user, userItems, true);
        initVersionSelector();
"""

html = re.sub(
    r"const state =.*?setupSearchable\(excludeSearch, excludeDropdown, state\.exclude, excludeItems\);",
    lambda m: new_js_logic,
    html,
    flags=re.DOTALL
)

html = html.replace(
    """const user = document.getElementById('paramUser').value.trim();
            if (user) cmd += ` u:${user}`;""",
    """let users = Array.from(state.user);
            const textUser = document.getElementById('paramUser').value.trim();
            if (textUser) users.push(textUser);
            if (users.length > 0) cmd += ` u:${users.join(',')}`;"""
)

html = html.replace(
    """let currentVal = input.value.split(',').map(s => s.trim()).filter(Boolean);
                if (currentVal.includes(val)) {
                    currentVal = currentVal.filter(s => s !== val);
                    tag.classList.remove('active');
                } else {
                    currentVal.push(val);
                    tag.classList.add('active');
                }
                input.value = currentVal.join(',');""",
    """if (state.user.has(val)) {
                    state.user.delete(val);
                    tag.classList.remove('active');
                } else {
                    state.user.add(val);
                    tag.classList.add('active');
                }
                renderSelectedItems(state.user, userItems, true);"""
)

with open("CoreProtectGenerator.html", "w", encoding="utf-8") as f:
    f.write(html)

print("JS Logic injected.")
