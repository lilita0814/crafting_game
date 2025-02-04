import craft


def main():
    grid = [
        ['', '', ''],
        ['white_wool', 'white_wool', 'white_wool'],
        ['oak_planks', 'oak_planks', 'oak_planks']
    ]
    result = craft.craft_item(grid)
    print(result)


if __name__ == "__main__":
    main()

