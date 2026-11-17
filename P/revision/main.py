from collections import deque
import heapq
from typing import Any
from runner import lancer_tests

def pack(strs: list[str]) -> str:
    s = ""
    nb_strs = len(strs)
    for j in range(nb_strs):
        for i in range(len(strs[j])):
            s += strs[j][i]
            if (j+1 < len(strs) and i+1 == len(strs[j])):
                s+="#"
    return s

def unpack(s: str) -> list[str]:
    strs = [[]]
    count = 0
    for i in range(len(s)):
        if s[i] == "#":
            count += 1
            strs.append([])
            continue
        strs[count] += s[i]
    return strs
 

if __name__ == "__main__":
    print(unpack(pack(['hello', 'world'])))
    print(unpack('5#hello5#world'))
    lancer_tests()