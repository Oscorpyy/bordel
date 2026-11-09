from collections import deque
import heapq
from typing import Any


# =====================================================================
#                          RANK 06 - PYTHON
# =====================================================================

# ---------------------------------------------------------------------
# Level 1 : prefix_dictionary
# ---------------------------------------------------------------------
class PrefixDictionary:
    """Arbre préfixe (Trie) pour stocker et rechercher des mots."""

    def __init__(self):
        self.root: dict = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node['$'] = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node:
                return False
            node = node[ch]
        return '$' in node

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node:
                return False
            node = node[ch]
        return True


# ---------------------------------------------------------------------
# Level 1 : pack_strings
# ---------------------------------------------------------------------
def pack(strs: list[str]) -> str:
    """Encode une liste de chaînes en une seule chaîne.

    Utilise un encodage à longueur préfixée (ex: '5#hello').
    """
    res = []
    for s in strs:
        res.append(f"{len(s)}#{s}")
    return "".join(res)


def unpack(s: str) -> list[str]:
    """Décode la chaîne formatée pour retrouver la liste d'origine."""
    if not s:
        return []
    res = []
    i = 0
    n = len(s)
    while i < n:
        j = s.find('#', i)
        if j == -1:
            break
        length = int(s[i:j])
        start = j + 1
        end = start + length
        res.append(s[start:end])
        i = end
    return res


# ---------------------------------------------------------------------
# Level 1 : task_order
# ---------------------------------------------------------------------
def task_order(n: int, prereqs: list[list[int]]) -> list[int]:
    """Tri topologique (Kahn) avec choix lexicographique (min-heap).

    Retourne [] si un cycle est détecté.
    """
    adj = [[] for _ in range(n)]
    in_degree = [0] * n
    for dest, src in prereqs:
        adj[src].append(dest)
        in_degree[dest] += 1

    heap = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(heap)

    order = []
    while heap:
        u = heapq.heappop(heap)
        order.append(u)
        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                heapq.heappush(heap, v)

    return order if len(order) == n else []


# ---------------------------------------------------------------------
# Level 1 : redundant_link
# ---------------------------------------------------------------------
def redundant_link(edges: list[list[int]]) -> list[int]:
    """Trouve l'arête redondante formant un cycle dans un arbre.

    Retourne la dernière arête de la liste qui crée le cycle.
    """
    parent = {}

    def find(x: int) -> int:
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    for u, v in edges:
        if u not in parent:
            parent[u] = u
        if v not in parent:
            parent[v] = v

        ru = find(u)
        rv = find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv

    return []


# ---------------------------------------------------------------------
# Level 1 : trie_autocomplete
# ---------------------------------------------------------------------
def trie_autocomplete(words: list[str], prefix: str) -> list[str]:
    """Autocomplétion via un Trie.

    Retourne tous les mots uniques commençant par prefix dans l'ordre
    alphabétique.
    """
    root = {}
    for word in set(words):
        node = root
        for ch in word:
            if ch not in node:
                node[ch] = {}
            node = node[ch]
        node['$'] = word

    node = root
    for ch in prefix:
        if ch not in node:
            return []
        node = node[ch]

    results = []

    def dfs(curr: dict) -> None:
        if '$' in curr:
            results.append(curr['$'])
        for k in sorted(curr.keys()):
            if k != '$':
                dfs(curr[k])

    dfs(node)
    return results


# ---------------------------------------------------------------------
# Level 2 : union_find_system
# ---------------------------------------------------------------------
class UnionFind:
    """Ensembles disjoints (DSU) avec compression et union par rang."""

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)


# ---------------------------------------------------------------------
# Level 2 : cache_keeper
# ---------------------------------------------------------------------
class _LRUNode:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None


class CacheKeeper:
    """Cache LRU (Least Recently Used) de capacité fixe en O(1) moyen.

    Implémenté sans collections.OrderedDict via dictionnaire et
    liste doublement chaînée.
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, _LRUNode] = {}
        self.head = _LRUNode()
        self.tail = _LRUNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _LRUNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_tail(self, node: _LRUNode) -> None:
        node.prev = self.tail.prev
        node.next = self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_tail(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_tail(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.head.next
                self._remove(lru)
                del self.cache[lru.key]
            new_node = _LRUNode(key, value)
            self.cache[key] = new_node
            self._add_to_tail(new_node)


# ---------------------------------------------------------------------
# Level 2 : min_heap
# ---------------------------------------------------------------------
class MinHeap:
    """Tas binaire minimum (Min-Heap) stocké dans une liste Python.

    Implémenté sans le module heapq.
    """

    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)

    def pop(self) -> int | None:
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return min_val

    def peek(self) -> int | None:
        return self.heap[0] if self.heap else None

    def size(self) -> int:
        return len(self.heap)

    def _sift_up(self, idx: int) -> None:
        parent = (idx - 1) // 2
        while idx > 0 and self.heap[idx] < self.heap[parent]:
            self.heap[idx], self.heap[parent] = (
                self.heap[parent],
                self.heap[idx],
            )
            idx = parent
            parent = (idx - 1) // 2

    def _sift_down(self, idx: int) -> None:
        n = len(self.heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest != idx:
                self.heap[idx], self.heap[smallest] = (
                    self.heap[smallest],
                    self.heap[idx],
                )
                idx = smallest
            else:
                break


# ---------------------------------------------------------------------
# Level 2 : bridge_finder
# ---------------------------------------------------------------------
def bridge_finder(graph: dict[int, list[int]]) -> list[tuple[int, int]]:
    """Trouve tous les ponts (isthmes) dans un graphe non orienté via Tarjan.

    Retourne la liste des arêtes (u, v) avec u < v, triées.
    """
    if not graph:
        return []

    visited = set()
    tin = {}
    low = {}
    timer = 0
    bridges = []

    def dfs(node: int, parent: int | None = None) -> None:
        nonlocal timer
        visited.add(node)
        timer += 1
        tin[node] = low[node] = timer

        for neighbor in graph.get(node, []):
            if neighbor == parent:
                continue
            if neighbor in visited:
                low[node] = min(low[node], tin[neighbor])
            else:
                dfs(neighbor, node)
                low[node] = min(low[node], low[neighbor])
                if low[neighbor] > tin[node]:
                    u, v = min(node, neighbor), max(node, neighbor)
                    bridges.append((u, v))

    for node in graph:
        if node not in visited:
            dfs(node)

    return sorted(bridges)


# =====================================================================
#                          RANK 05 - PYTHON
# =====================================================================

def compress(s: str) -> str:
    """Compresse une chaîne de caractères (RLE limité à 9 répétitions)."""
    if len(s) == 0:
        return ""
    i = 1
    last = 0
    result = ""
    same = 1
    while i < len(s):
        if s[i] == s[last] and same < 9:
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
    return result


def decompress(s: str) -> str:
    """Décompresse une chaîne générée par compress."""
    result = ""
    if not s:
        return result
    i = 0
    while i < len(s) - 1:
        if s[i].isalpha() and s[i + 1].isdigit():
            result += str(int(s[i + 1]) * s[i])
        elif s[i].isalpha():
            result += str(s[i])
        i += 1
    if s[i].isalpha():
        result += str(s[i])
    return result


def generate_spiral(size: int) -> list[list[int]]:
    """Génère une matrice spirale carrée de dimension size x size."""
    if size < 1:
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

    return matrix


def py_graph_cycle_detector(graph: dict[int, list[int]]) -> bool:
    """Détecte si un graphe orienté contient un cycle."""
    visited = set()
    in_stack = set()

    def has_cycle(node: int) -> bool:
        visited.add(node)
        in_stack.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in in_stack:
                return True
        in_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if has_cycle(node):
                return True
    return False


def py_room_scheduler(meetings: list[list[int]]) -> dict[str, Any]:
    """Calcule le nombre minimal de salles requises et leur planning."""
    scheduler = {}
    meetings_sorted = sorted(meetings)
    for meet in meetings_sorted:
        start = meet[0]
        placed = False
        for _, sched in scheduler.items():
            if sched[-1][1] <= start:
                sched.append(meet)
                placed = True
                break
        if not placed:
            scheduler[len(scheduler)] = [meet]
    return {
        "rooms_necessary": len(scheduler),
        "room_scheduler": scheduler,
    }


def island_matrix_counter(matrix: list[list[str]]) -> int:
    """Compte le nombre total d'îles ('1') dans une grille 2D."""
    if not matrix or not matrix[0]:
        return 0

    visited: set[tuple[int, int]] = set()
    islands: int = 0

    def dfs(x: int, y: int) -> None:
        if (
            x < 0
            or x >= len(matrix)
            or y < 0
            or y >= len(matrix[0])
            or matrix[x][y] == "0"
            or (x, y) in visited
        ):
            return

        visited.add((x, y))
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


def prism_detector(
    grid: list[str], pattern: str
) -> list[tuple[int, int, str]]:
    """Recherche toutes les occurrences d'un mot dans une grille 2D."""
    if not grid or not pattern:
        return []

    rows: int = len(grid)
    cols: int = len(grid[0])
    results: list[tuple[int, int, str]] = []
    pattern_len: int = len(pattern)

    directions: dict[tuple[int, int], str] = {
        (0, 1): "H",
        (0, -1): "H_REV",
        (1, 0): "V",
        (-1, 0): "V_REV",
        (1, 1): "D",
        (-1, -1): "D_REV",
        (1, -1): "D_DL",
        (-1, 1): "D_UR",
    }

    for x in range(rows):
        for y in range(cols):
            if grid[x][y] != pattern[0]:
                continue

            for (dx, dy), code in directions.items():
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
    """Calcule la longueur de la plus courte chaîne de transformation."""
    if end not in sentence:
        return 0

    queue: deque[tuple[str, int]] = deque([(start, 1)])
    visited = {start}

    while queue:
        current_word, level = queue.popleft()

        if current_word == end:
            return level

        for i in range(len(current_word)):
            for char in "abcdefghijklmnopqrstuvwxyz":
                if char == current_word[i]:
                    continue

                next_word: str = (
                    current_word[:i] + char + current_word[i + 1:]
                )

                if next_word in sentence and next_word not in visited:
                    visited.add(next_word)
                    queue.append((next_word, level + 1))

    return 0
