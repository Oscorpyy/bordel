from typing import Any
from collections import deque


def compress(s: str) -> str:
    if (len(s) == 0):
        return ""
    i = 1
    last = 0
    result = ""
    same = 1
    while (i < len(s)):
        # print(f"s[i] = {s[i]}, i = {i}, last = {last}, same = {same}")
        if (s[i] == s[last] and same < 9):
            same += 1
            i += 1
        else:
            result += str(s[last])
            if same > 1:
                result += str(same)
            last = i
            same = 1
            i += 1
    result += str(s[last])
    if same > 1:
        result += str(same)
    return (result)


def decompress(s: str) -> str:
    result = ""
    i = 0
    while (i < len(s)):
        # print(f"s[i] = {s[i]}, i = {i}")
        if s[i].isalpha() and s[i + 1].isdigit():
            result += str(int(s[i + 1]) * s[i])
        elif s[i].isalpha():
            result += str(s[i])
        i += 1
    return (result)


def generate_spiral(n: int) -> list[list[int]]:
    """
    Generate an n x n matrix filled with elements from 1 to n^2 in spiral order.
    """
    if n <= 0:
        return []

    matrix: list[list[int]] = [[0] * n for _ in range(n)]

    top: int = 0
    bottom: int = n - 1
    left: int = 0
    right: int = n - 1

    current_num: int = 1
    total_elements: int = n * n

    while current_num <= total_elements:
        for i in range(left, right + 1):
            matrix[top][i] = current_num
            current_num += 1
        top += 1

        for i in range(top, bottom + 1):
            matrix[i][right] = current_num
            current_num += 1
        right -= 1

        if top <= bottom:
            for i in range(right, left - 1, -1):
                matrix[bottom][i] = current_num
                current_num += 1
            bottom -= 1

        if left <= right:
            for i in range(bottom, top - 1, -1):
                matrix[i][left] = current_num
                current_num += 1
            left += 1

    return matrix


def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:
    """
    Determine if a directed graph contains at least one cycle.
    Returns True if a cycle exists, False if acyclic or empty.
    """
    visiting: set[int] = set()
    visited: set[int] = set()

    def dfs(node: int) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False

        visiting.add(node)

        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True

        visiting.remove(node)
        visited.add(node)
        return False

    for node in graph:
        if node not in visited:
            if dfs(node):
                return True

    return False


def py_room_scheduler(meetings: list[list[int]]) -> dict[str, Any]:
    """
    Determines the minimum number of meeting rooms required and assigns slots.
    Returns a dictionary mapping the room count and a dictionary of room IDs to schedules.
    """
    scheduler = {}
    meetings.sort()
    for meet in meetings:
        start = meet[0]
        placed = False
        for nb_room, sched in scheduler.items():
            if sched[-1][1] <= start:
                sched.append(meet)
                placed = True
                break
        if not placed :
            scheduler[len(scheduler)] = [meet]
    return {
        "rooms_necessary": len(scheduler),
        "room_scheduler": scheduler
    }


def island_matrix_counter(matrix: list[list[str]]) -> int:
    """
    Counts the total number of islands in a 2D matrix of "1"s and "0"s.
    """
    if not matrix or not matrix[0]:
        return 0

    rows: int = len(matrix)
    cols: int = len(matrix[0])
    visited: set[tuple[int, int]] = set()
    islands: int = 0

    def dfs(r: int, c: int) -> None:
        if (
            r < 0 or r >= rows or 
            c < 0 or c >= cols or 
            matrix[r][c] == "0" or 
            (r, c) in visited
        ):
            return
            
        visited.add((r, c))
        
        # Traverse horizontally and vertically
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == "1" and (r, c) not in visited:
                islands += 1
                dfs(r, c)

    return islands


def prism_detector(grid: list[str], pattern: str) -> list[tuple[int, int, str]]:
    """
    Searches for all occurrences of a target word in a 2D grid across all 8 directions.
    Returns a list of tuples (x, y, direction_code).
    """
    if not grid or not pattern:
        return []

    rows: int = len(grid)
    cols: int = len(grid[0])
    results: list[tuple[int, int, str]] = []
    pattern_len: int = len(pattern)

    directions: dict[tuple[int, int], str] = {
        (0, 1): "H",        # Horizontal Right
        (0, -1): "H_REV",   # Horizontal Left
        (1, 0): "V",        # Vertical Down
        (-1, 0): "V_REV",   # Vertical Up
        (1, 1): "D",        # Diagonal Down-Right
        (-1, -1): "D_REV",  # Diagonal Up-Left
        (1, -1): "D_DL",    # Diagonal Down-Left
        (-1, 1): "D_UR"     # Diagonal Up-Right
    }

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] != pattern[0]:
                continue

            for (dx, dy), code in directions.items():
                # Calculate end coordinates to check boundaries early
                end_x: int = x + dx * (pattern_len - 1)
                end_y: int = y + dy * (pattern_len - 1)

                if 0 <= end_x < rows and 0 <= end_y < cols:
                    match: bool = True
                    for i in range(1, pattern_len):
                        if grid[x + dx * i][y + dy * i] != pattern[i]:
                            match = False
                            break
                    
                    if match:
                        results.append((x, y, code))

    return results


def word_ladder(start: str, end: str, sentence: list[str]) -> int:
    """
    Calculates the length of the shortest transformation sequence from a start word to an end word.
    Returns the number of words in the shortest ladder, or 0 if no transformation is possible.
    """
    word_set: set[str] = set(sentence)
    
    if end not in word_set:
        return 0
        
    queue: deque[tuple[str, int]] = deque([(start, 1)])
    
    while queue:
        current_word, level = queue.popleft()
        
        if current_word == end:
            return level
            
        for i in range(len(current_word)):
            for char_code in range(97, 123):
                char: str = chr(char_code)
                if char == current_word[i]:
                    continue
                    
                next_word: str = current_word[:i] + char + current_word[i+1:]
                
                if next_word in word_set:
                    word_set.remove(next_word)
                    queue.append((next_word, level + 1))
                    
    return 0
