from typing import Any

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
    if not s:
        return result
    i = 0
    while (i < len(s) - 1):
        # print(f"s[i] = {s[i]}, i = {i}")
        if s[i].isalpha() and s[i + 1].isdigit():
            result += str(int(s[i + 1]) * s[i])
        elif s[i].isalpha():
            result += str(s[i])
        i += 1
    if s[i].isalpha():
        result += str(s[i])
    return (result)


def generate_spiral(size : int) -> list[list[int]]:
    if size < 1 :
        return []

    matrix = [[0] * size for _ in range(size)]
    y = x = direction = 0
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for nb in range(1, size * size + 1):
        matrix[x][y] = nb

        dx, dy = moves[direction]
        nx = x + dx
        ny = y + dy
        if not (0 <= nx < size and 0 <= ny < size) or matrix[nx][ny] != 0:
            direction = (direction + 1) % 4
            dx, dy = moves[direction]
            
        x += dx
        y += dy


    return (matrix)


def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:
    """
    Determine if a directed graph contains at least one cycle.
    Returns True if a cycle exists, False if acyclic or empty.
    btw this fonction is shit so i rewrote it in a better way (easier to reproduce):
    dankechun to the cocobussie wich helped me to find the cheat mode
    """
    def rec_check(graph, neighbors: list[int]):
        for i in neighbors:
            if not i in graph:
                continue
            rec_check(graph, graph[i])

    try:
        for i in graph:
            rec_check(graph, graph[i])
        return False
    except RecursionError:
        return True


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

    visited: set[tuple[int, int]] = set()
    islands: int = 0

    def dfs(x: int, y: int) -> None:
        if (
            x < 0 or x >= len(matrix) or 
            y < 0 or y >= len(matrix[0]) or 
            matrix[x][y] == "0" or 
            (x, y) in visited
        ):
            return
            
        visited.add((x, y))
        
        # Traverse horizontally and vertically
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)

    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] == "1" and (x, y) not in visited:
                islands += 1
                dfs(x, y)

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


from collections import deque


def word_ladder(start: str, end: str, sentence: list[str]) -> int:
    """
    Calculates the length of the shortest transformation sequence from a start word to an end word.
    Returns the number of words in the shortest ladder, or 0 if no transformation is possible.
    """
    
    if end not in sentence:
        return 0
        
    queue: deque[tuple[str, int]] = deque([(start, 1)])
    
    while queue:
        current_word, level = queue.popleft()
        
        if current_word == end:
            return level
            
        for i in range(len(current_word)):
            for char in "abcdefghijklmnopqrstuvwxyz":
                if char == current_word[i]:
                    continue
                    
                next_word: str = current_word[:i] + char + current_word[i+1:]
                
                if next_word in sentence:
                    # sentence.remove(next_word)
                    queue.append((next_word, level + 1))

    return 0
