from collections import deque
import heapq
from typing import Any
from runner import lancer_tests

def pack(strs: list[str]) -> str:
    s = ""
    temp = ""
    nb_strs = len(strs)
    for j in range(nb_strs):
        for i in range(len(strs[j])):
            temp += strs[j][i]
            if (i+1 == len(strs[j])):
                s+=str(len(temp))
                s+="#"
                s+=temp
                temp = ""
    return s

def unpack(s: str) -> list[str]:
    strs = []
    count = 0
    temp = ''
    for i in range(len(s)):
        if s[i] == "#":
            count += 1
            if len(temp) > 0:
                strs.append(temp)
            temp = ''
            continue
        temp += s[i]
    if len(temp) > 0:
        strs.append(temp)
    return strs
 

if __name__ == "__main__":
    print(pack(['hello', 'world']))
    # print(unpack('5#hello5#world'))
    # print(unpack(pack("['', 'a', '', 'b', '']")))
    lancer_tests()