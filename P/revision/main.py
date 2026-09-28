from typing import Any
from test import Test


def island_matrix_counter(matrix: list[list[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    
    nb_islands = 0
    visited: list[tuple(int, int)] = []
    def get_island(x, y):
        if (
            x < 0 or x >= len(matrix) or
            y < 0 or y >= len(matrix[0]) or
            matrix[x][y] == "0"  or 
            (x, y) in visited
        ):
            return

        visited.append((x, y))
        
        get_island(x + 1, y)
        get_island(x - 1, y)
        get_island(x, y + 1)
        get_island(x, y - 1)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if (matrix[i][j] == '1' and (i, j) not in visited):
                nb_islands += 1
                get_island(i, j)
    return nb_islands



if __name__ == "__main__":
    # matrix = [["1", "1", "1", "1", "0"],
    #           ["1", "1", "1", "0", "0"],
    #           ["1", "1", "0", "1", "0"],
    #           ["0", "0", "1", "0", "0"]]
    # print(island_matrix_counter(matrix))
    t= Test()
    t.island_matrix_counter()

