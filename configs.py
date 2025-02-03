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

ALL_RECIPES_DIR = os.path.join(ASSETS_DIR, "recipes")
ALL_RECIPES: List[dict] = [
    json.load(open(os.path.join(ALL_RECIPES_DIR, e), 'r', encoding='utf-8'))
    for e in os.listdir(ALL_RECIPES_DIR)
]

# 合成网格位置 (3x3)
GRID_POSITIONS = [
    (200, 150), (260, 150), (320, 150),
    (200, 210), (260, 210), (320, 210),
    (200, 270), (260, 270), (320, 270)
]

# 物品初始位置
ITEM_START_POSITIONS = [(50, 350), (100, 350), (150, 350)]
