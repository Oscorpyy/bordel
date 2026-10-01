from typing import Any
from test import Test
from collections import deque

def generate_spiral(size: int) -> list[list[int]]:

    if size <= 0:
        return []

    max_nb = size * size
    matrix = [[max_nb] * size for _ in range(size)]

    top = 0
    bottom = size - 1
    left = 0
    right = size - 1

    nb = 1

    while nb < max_nb:
        for i in range(left, right + 1, + 1):
            matrix[top][i] = nb
            nb += 1
        top += 1

        for i in range(top, bottom + 1, + 1):
            matrix[i][right] = nb
            nb += 1
        right -= 1

        for i in range(right, left - 1, -1):
            matrix[bottom][i] = nb
            nb += 1
        bottom -= 1

        for i in range(bottom, top - 1, -1):
            matrix[i][left] = nb
            nb += 1
        left += 1

    return matrix

def generate_spiral(n: int) -> list[list[int]]:
    matrix = [[0] * n for _ in range(n)]
    x = y = direction = 0
    moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    for num in range(1, n * n + 1):
        matrix[y][x] = num

        dx, dy = moves[direction]
        nx, ny = x + dx, y + dy

        if not (0 <= nx < n and 0 <= ny < n) or matrix[ny][nx]:
            direction = (direction + 1) % 4
            dx, dy = moves[direction]

        x += dx
        y += dy

    return matrix

if __name__ == "__main__":
    print(generate_spiral(4))
    t= Test()
    # t.generate_spiral()
