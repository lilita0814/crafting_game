import craft


def main():
    grid = [
        ['', 'minecraft:stone', 'minecraft:stone'],
        ['', '', ''],
        ['', '', '']
    ]
    result = craft.craft_item(grid)
    print(result)


if __name__ == "__main__":
    main()

