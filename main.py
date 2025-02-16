import craft


def main():
    grid = [
        ['', '', ''],
        ['black_wool', 'black_wool', 'black_wool'],
        ['birch_planks', 'oak_planks', 'oak_planks']
    ]
    result = craft.craft_item(grid)
    print(result)


if __name__ == "__main__":
    main()

