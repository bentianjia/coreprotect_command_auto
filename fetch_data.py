import requests
import json
from pypinyin import pinyin, Style

ZH_URL = "https://ghproxy.net/https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.20.4/assets/minecraft/lang/zh_cn.json"
EN_URL = "https://ghproxy.net/https://raw.githubusercontent.com/InventivetalentDev/minecraft-assets/1.20.4/assets/minecraft/lang/en_us.json"

print("Fetching language files from proxy...")
try:
    zh_data = requests.get(ZH_URL, timeout=15).json()
    en_data = requests.get(EN_URL, timeout=15).json()
    print("Fetch successful.")
except Exception as e:
    print(f"Failed to fetch: {e}")
    exit(1)

# Large alias dictionary for slang
aliases = {
    "enderman": ["xh", "xiaohei", "末影人", "小黑"],
    "creeper": ["klp", "jjg", "苦力怕", "jj怪", "爬行者"],
    "zombie": ["zs", "僵尸"],
    "skeleton": ["xb", "小白", "骷髅"],
    "iron_golem": ["tkl", "tiekuilei", "铁傀儡", "保镖"],
    "villager": ["cm", "cunmin", "村民", "奸商"],
    "diamond": ["zs", "zuanshi", "钻石"],
    "diamond_block": ["zsk", "钻石块"],
    "netherite_ingot": ["xjhj", "下界合金"],
    "tnt": ["tnt", "炸药"],
    "wither": ["dl", "diaoling", "凋灵", "凋零"],
    "ender_dragon": ["myl", "末影龙", "黑龙", "龙"],
    "slime": ["slm", "史莱姆", "粘液怪"],
    "blaze": ["lyr", "烈焰人"],
    "ghast": ["eh", "恶魂", "水母"],
    "shulker": ["qyb", "潜影贝", "贝壳"],
    "phantom": ["hy", "幻翼"],
    "pillager": ["ldz", "掠夺者"],
    "vindicator": ["whz", "卫道士"],
    "evoker": ["hms", "唤魔者"],
    "ravager": ["js", "劫掠兽"],
    "warden": ["jss", "监守者", "瞎子"],
    "piglin": ["zlr", "猪灵"],
    "zombified_piglin": ["jszlr", "僵尸猪灵", "猪人"],
    "hoglin": ["ys", "疣猪兽"],
    "strider": ["czs", "炽足兽"],
    "snow_golem": ["xkl", "雪傀儡", "雪人"],
    "wandering_trader": ["lxsq", "流浪商人"],
    "zombie_villager": ["jscm", "僵尸村民"],
    "bedrock": ["jy", "基岩", "底岩"],
    "obsidian": ["hys", "黑曜石"],
    "ender_pearl": ["myzz", "末影珍珠"],
    "ender_eye": ["myzy", "末影之眼"],
    "elytra": ["qyc", "鞘翅", "翅膀"],
    "totem_of_undying": ["bstt", "不死图腾", "复活币"],
    "golden_apple": ["jgp", "金苹果"],
    "enchanted_golden_apple": ["fjgp", "附魔金苹果", "附魔苹果"],
    "experience_bottle": ["jyp", "经验瓶"],
    "command_block": ["mlfk", "命令方块", "指令方块"],
    "beacon": ["xb", "信标"],
    "nether_star": ["xjzx", "下界之星"]
}

items = {}

for key, zh_name in zh_data.items():
    if key.startswith("block.minecraft.") or key.startswith("entity.minecraft.") or key.startswith("item.minecraft."):
        item_id = key.split(".")[-1]
        
        if " " in item_id or item_id in items:
            continue
            
        en_name = en_data.get(key, item_id.replace("_", " ").title())
        
        pys = pinyin(zh_name, style=Style.FIRST_LETTER)
        py_initials = "".join([p[0] for p in pys if p[0].isalnum()]).lower()
        
        pys_full = pinyin(zh_name, style=Style.NORMAL)
        py_full = "".join([p[0] for p in pys_full if p[0].isalnum()]).lower()
        
        search_terms = [item_id, en_name.lower(), zh_name, py_initials, py_full]
        
        if item_id in aliases:
            search_terms.extend(aliases[item_id])
            
        search_str = " ".join(list(set(search_terms)))
        
        item_type = "block"
        if key.startswith("entity.minecraft."):
            item_type = "entity"
        elif key.startswith("item.minecraft."):
            item_type = "item"
            
        items[item_id] = {
            "id": item_id,
            "en": en_name,
            "zh": zh_name,
            "s": search_str,
            "t": item_type,
            "v": "1.13",  # Base version, everything starts visible
            "vi": 1013000
        }

# For simple offline version filtering, we approximate by looking at common blocks.
# In a real heavy app we'd map all 1600 items. Let's map a few prominent 1.16+ features to prove the filter works.
versions_map = {
    "1.14": ["bamboo", "campfire", "sweet_berry_bush", "barrel", "bell", "blast_furnace", "cartography_table", "composter", "grindstone", "lantern", "lectern", "loom", "smoker", "stonecutter", "fox", "panda", "pillager", "ravager"],
    "1.15": ["bee_nest", "beehive", "honey_block", "honeycomb_block", "bee"],
    "1.16": ["ancient_debris", "basalt", "blackstone", "crying_obsidian", "crimson_nylium", "warped_nylium", "netherite_block", "netherite_ingot", "piglin", "hoglin", "strider", "zoglin"],
    "1.17": ["amethyst_block", "calcite", "copper_ore", "deepslate", "dripstone_block", "moss_block", "powder_snow", "tuff", "axolotl", "goat", "glow_squid"],
    "1.18": ["music_disc_otherside"],
    "1.19": ["mangrove_log", "mud", "sculk", "sculk_catalyst", "sculk_shrieker", "sculk_vein", "frog", "tadpole", "warden", "allay"],
    "1.20": ["bamboo_block", "cherry_log", "cherry_leaves", "decorated_pot", "pink_petals", "sniffer", "camel", "brush"]
}

# Apply versions
for v, items_list in versions_map.items():
    vi = int(v.split(".")[0]) * 100000 + int(v.split(".")[1]) * 1000
    for i in items_list:
        if i in items:
            items[i]["v"] = v
            items[i]["vi"] = vi

output = list(items.values())
print(f"Total items extracted: {len(output)}")

with open("mc_data_with_versions.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False)
print("Data written to mc_data_with_versions.json")
