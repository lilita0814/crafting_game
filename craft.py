import configs

def craft_item(grid):
    """
    根据 3x3 合成网格和所有配方列表，返回可合成物品的 ID（字符串）。
    如果没有匹配任何配方，则返回 None。
    """
    # 1) 把空字符串 '' 转成 None，表示空格子
    grid = [[None if i == '' else i for i in row] for row in grid]

    all_recipes = configs.ALL_RECIPES

    # 2) 依次检查每条配方
    for recipe in all_recipes:
        rtype = recipe.get("type")

        # 结果物品ID：可能写在 "id" 或 "item" 字段
        result_data = recipe.get("result", {})
        # 兼容 "id" 或 "item" 两种写法
        if isinstance(result_data, dict):
            result_id = result_data.get("id") or result_data.get("item")
        else:
            # 如果 result_data 不是 dict，可能是个字符串或其他格式
            result_id = result_data

        # ---- Shaped ----
        if rtype == "minecraft:crafting_shaped":
            if check_shaped_recipe(grid, recipe):
                return result_id

        # ---- Shapeless ----
        elif rtype == "minecraft:crafting_shapeless":
            if check_shapeless_recipe(grid, recipe):
                return result_id

        # 其它类型 (smelting, stonecutting, smithing...) 可按需加

    # 如果循环结束都没匹配到，就返回 None
    return None


def check_shaped_recipe(grid, recipe):
    """
    检查 grid 是否匹配 Shaped (有序) 配方。
    - 要求：pattern 指定的格子与 key 相符，其余格子必须为空。
    - recipe["pattern"] 是字符串数组，如: ["X", "#"] 或 ["###","###"]。
    - recipe["key"] 里每个符号可能是：
        1) 字符串 (如 "minecraft:stick")
        2) 字典 (如 {"item":"minecraft:stick"} 或 {"tag":"..."} )
        3) 列表 (如 ["minecraft:coal","minecraft:charcoal"]) -- 表示多选
    """
    pattern = recipe.get("pattern", [])
    key_map = recipe.get("key", {})

    pattern_height = len(pattern)
    pattern_width = max(len(row) for row in pattern) if pattern else 0

    # 在 3x3 网格上，逐个 offset 试图匹配 pattern
    for offset_y in range(3 - pattern_height + 1):
        for offset_x in range(3 - pattern_width + 1):
            if shaped_match_at_offset(grid, pattern, key_map, offset_x, offset_y):
                return True

    return False


def shaped_match_at_offset(grid, pattern, key_map, offset_x, offset_y):
    """
    判断在给定 offset 下，3x3 grid 是否与 Shaped pattern 完全吻合：
      - pattern 覆盖到的格子：
          若 symbol != ' '，则必须匹配 key_map 中对应物品(或列表)；
          若 symbol==' '，则必须为空
      - pattern 未覆盖的格子：必须为空
    """
    pattern_height = len(pattern)
    pattern_width = max(len(row) for row in pattern)

    for gy in range(3):
        for gx in range(3):
            pat_row = gy - offset_y
            pat_col = gx - offset_x

            # 判断是否在 pattern 范围内
            in_pattern = (
                0 <= pat_row < pattern_height and
                0 <= pat_col < len(pattern[pat_row])
            )

            actual_item = grid[gy][gx]

            if in_pattern:
                symbol = pattern[pat_row][pat_col]
                if symbol == ' ':
                    # 要求空
                    if actual_item is not None:
                        return False
                else:
                    # pattern 里有一个符号 (如 '#','X'...) => key_map 必须定义它
                    if symbol not in key_map:
                        return False
                    required_def = key_map[symbol]

                    # 判断 actual_item 是否匹配 required_def(可能是字符串/字典/数组)
                    if not matches_item_requirement(actual_item, required_def):
                        return False
            else:
                # 不在 pattern 范围 => 必须空
                if actual_item is not None:
                    return False

    return True


def check_shapeless_recipe(grid, recipe):
    """
    检查 grid 是否匹配 Shapeless (无序) 配方。
    - 只要放入的物品“总数量”和“种类”与 recipe["ingredients"] 相符，位置无关。
    - recipe["ingredients"] 里可能直接是字符串, dict, 或 列表(多选)。
      例: [
        "minecraft:stone",
        ["minecraft:coal","minecraft:charcoal"],
        {"item":"minecraft:stick"}
      ]
    """
    ingredients = recipe.get("ingredients", [])

    # 收集网格里所有非空物品
    placed_items = [slot for row in grid for slot in row if slot is not None]

    # 如果放置的物品数量 < 所需材料数量，直接不行
    if len(placed_items) < len(ingredients):
        return False

    # 我们需要“逐个 ingredient”地去匹配 placed_items 中的某一项
    placed_copy = placed_items[:]

    for ing in ingredients:
        matched_something = False
        # 试图从 placed_copy 里找到一个匹配 ing 的物品
        for i, placed in enumerate(placed_copy):
            if matches_item_requirement(placed, ing):
                # 找到了 => 移除并标记匹配成功
                placed_copy.pop(i)
                matched_something = True
                break

        if not matched_something:
            # 该 ingredient 找不到对应物品 => 失败
            return False

    # 全部 ingredients 都能匹配到
    return True


def matches_item_requirement(actual_item, required_def):
    """
    判断 "actual_item" (如 "minecraft:coal") 是否符合 "required_def" 的要求。

    required_def 可能是:
      1) 字符串:  "minecraft:stick"
      2) 字典:    {"item":"minecraft:stick"} 或 {"tag":"minecraft:planks"} 等
      3) 列表:    ["minecraft:coal","minecraft:charcoal"] (OR 逻辑: 只要匹配其中之一即可)

    如果匹配成功返回 True，否则 False。
    注: 如果要支持 tag，还需在这里额外对 tag 做解析判断。
    """
    # 1) 如果它是字符串，直接对比
    if isinstance(required_def, str):
        return (actual_item == required_def)

    # 2) 如果它是字典, 如 {"item":"minecraft:xxx"} 或 {"tag":"minecraft:xxx"}
    if isinstance(required_def, dict):
        if "item" in required_def:
            return (actual_item == required_def["item"])
        if "tag" in required_def:
            # 需要在这里做"tag包含哪些物品"的判断
            # 比如 if actual_item in TAGS[ required_def["tag"] ]: return True
            # 这里示例直接返回 False
            return False
        # 其它情况，未实现
        return False

    # 3) 如果它是列表, 表示多个可选物品 (OR 逻辑)
    if isinstance(required_def, list):
        # 只要 actual_item 匹配其中“任意一个”元素即可
        for sub_def in required_def:
            if matches_item_requirement(actual_item, sub_def):
                return True
        return False

    # 4) 其它未知格式，直接当不匹配
    return False
