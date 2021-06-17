import emoji
from typing import List, Tuple


def create(n: int, m: int) -> List[List[tuple]]:
    grid = []
    for _ in range(n):
        line = []
        for _ in range(m):
            line.append((0,0))
            """print('\033[;42m  \033[0m', end = '')
            print("\n")
            print('\033[;44m  \033[0m', end = '')
            print("\n")
            print(emoji.emojize('Python is :tiger:'))
            print(emoji.emojize('Python is :shark:'))
            print(emoji.emojize('Python is :crocodile:'))"""
        grid.append(line)
    return grid

def affichage(grid: List[List[tuple]]):
    for i in range(len(grid)):
        line = []
        for _ in range(len(grid[i])):
            line.append((0,0))
            """print('\033[;41m   \033[0m', end = '')
            print("\n")
            print("\n")
            print(emoji.emojize('Python is :tiger:'))
            print(emoji.emojize('Python is :shark:'))
            print(emoji.emojize('Python is :crocodile:'))"""
            print('\033[;44m  \033[0m', end = '')
        print('')



def main():
    n = 10
    m = 10
    grid=create(n,m)

    affichage(grid)

if __name__ == "__main__":
    main()