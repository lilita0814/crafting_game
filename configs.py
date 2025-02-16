import json
import os
from typing import List

# 窗口大小
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# 资源文件路径
ASSETS_DIR = "assets"
CRAFTING_GUI = os.path.join(ASSETS_DIR, "Crafting_GUI.png")
BACKGROUND_IMAGE = os.path.join(ASSETS_DIR, "bg.png")

ITEM_TAGS_DIR = os.path.join(ASSETS_DIR, "item_tags")
ITEM_TAGS: dict[str, list[str]] = {
    f'#minecraft:{file_name.split('.')[0]}':
        json.load(open(os.path.join(ITEM_TAGS_DIR, file_name), 'r', encoding='utf-8')).get('values')
    for file_name in os.listdir(ITEM_TAGS_DIR)
}

ALL_RECIPES_DIR = os.path.join(ASSETS_DIR, "recipes")
ALL_RECIPES: List[dict] = []
for file_name in os.listdir(ALL_RECIPES_DIR):
    with open(os.path.join(ALL_RECIPES_DIR, file_name), 'r', encoding='utf-8') as file:
        recipe_json = json.load(file)
        # replace item tag
        if keys := recipe_json.get('key'):
            for key, value in keys.items():
                if isinstance(value, str) and value.startswith('#'):
                    recipe_json['key'][key] = ITEM_TAGS.get(value)
        # replace item tag
        if ingredients := recipe_json.get('ingredients'):
            recipe_json['ingredients'] = \
                [ITEM_TAGS.get(e) if isinstance(e, str) and e.startswith('#') else e for e in ingredients]
        ALL_RECIPES.append(recipe_json)

pass
