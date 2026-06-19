const mcData = require('minecraft-data');
const fs = require('fs');

const versions = mcData.versions.pc.map(v => v.minecraftVersion).reverse(); 

const itemDataMap = {}; // id -> { version, type }

for (const v of versions) {
    try {
        const data = mcData(v);
        if (!data) continue;

        const recordItem = (id, type) => {
            if (id && !itemDataMap[id]) {
                itemDataMap[id] = { v, type };
            }
        };

        if (data.blocks) Object.values(data.blocks).forEach(b => recordItem(b.name, 'block'));
        if (data.items) Object.values(data.items).forEach(i => recordItem(i.name, 'item'));
        if (data.entities) Object.values(data.entities).forEach(e => recordItem(e.name, 'entity'));
    } catch (e) { }
}

const mcDataRaw = fs.readFileSync('mc_data.json', 'utf-8');
const translations = JSON.parse(mcDataRaw);

const finalData = [];

function versionToInt(v) {
    if (!v) return 0;
    const parts = v.split('.');
    const major = parseInt(parts[0]) || 1;
    const minor = parseInt(parts[1]) || 0;
    const patch = parseInt(parts[2]) || 0;
    return major * 100000 + minor * 1000 + patch;
}

for (const item of translations) {
    const id = item.id;
    const meta = itemDataMap[id];
    let added = meta ? meta.v : '1.20.4';
    let type = meta ? meta.type : 'block'; 

    finalData.push({
        id: id,
        en: item.en,
        zh: item.zh,
        s: item.s,
        t: type,
        v: added,
        vi: versionToInt(added)
    });
}

fs.writeFileSync('mc_data_with_versions.json', JSON.stringify(finalData), 'utf-8');

const majorVersions = new Set();
const minorVersions = {};

versions.forEach(v => {
    if (versionToInt(v) < 101300) return;
    const parts = v.split('.');
    const major = `${parts[0]}.${parts[1]}`;
    majorVersions.add(major);
    if (!minorVersions[major]) minorVersions[major] = [];
    if (!minorVersions[major].includes(v)) {
        minorVersions[major].push(v);
    }
});

fs.writeFileSync('versions.json', JSON.stringify({
    majors: Array.from(majorVersions).reverse(),
    minors: minorVersions
}), 'utf-8');
