from itertools import chain
from typing import Optional, Any

import configs


def craft_item(grid) -> Optional[str]:
    # turn None to empty str
    cur_pattern = [['' if i is None else
                    'minecraft:' + i if ('minecraft:' not in i and i) else i
                    for i in row] for row in grid]

    # empty
    if all(all(cell == '' for cell in row) for row in cur_pattern):
        return None

    # remove empty row
    cur_pattern = [i for i in cur_pattern if i != ['' for _ in range(3)]]

    # row empty col
    transposed = list(zip(*cur_pattern))  # 转置，使列变成行
    filtered = [col for col in transposed if any(cell != '' for cell in col)]  # 只保留非空列
    cur_pattern = [list(row) for row in zip(*filtered)]  # 还原回原来的行结构

    all_recipes = filter(lambda e:
                         e.get("type") in ('minecraft:crafting_shapeless', 'minecraft:crafting_shaped'),
                         configs.ALL_RECIPES)

    for recipe in all_recipes:
        # if recipe.get('result', {}).get('id') != 'minecraft:torch':
        #     continue
        # replace key
        recipe_keys = recipe.get('key', {})
        keyed_pattern = cur_pattern[:]
        for k, v in recipe_keys.items():
            keyed_pattern = [[k if (i == v if isinstance(v, str) else i in v) else i for i in row]
                             for row in keyed_pattern]
        keyed_pattern = [''.join(row) for row in keyed_pattern]

        # check got pattern
        if pattern := recipe.get("pattern"):
            if pattern == keyed_pattern:
                # return if result is str
                return result if isinstance(result := recipe.get("result"), str) else result.get('id')
        else:
            # no pattern
            recipe_ingredients: list[Any] = recipe.get("ingredients")
            cur_pattern_item: list[str] = list(chain.from_iterable(cur_pattern))
            # check len
            if len(recipe_ingredients) == len(cur_pattern_item):
                # check item match
                if check_ingredients(recipe_ingredients, cur_pattern_item):
                    return result if isinstance(result := recipe.get("result"), str) else result.get('id')

    return None


def check_ingredients(recipe_ingredients: list[Any], cur_pattern_item: list[str]) -> bool:
    return all(
        # is list
        any([i in r for i in cur_pattern_item])
        if isinstance(r, list) else
        # not list
        r in cur_pattern_item
        for r in recipe_ingredients
    )
