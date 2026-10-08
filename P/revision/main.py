from typing import Any
from test import Test
from collections import deque

def compress(s: str) -> str:
    if len(s) < 1: 
        return ""
    i = 1
    last = 0
    result = ""
    same = 1
    while (i < len(s)):
        if s[i] == s[last]:
            same +=1
            i+=1
        else :
            if same > 1:
                result = result + ((s[last] + "9") * (same//9)) + (s[last] + str(same % 9))
            else :
                result = result + s[last]
            last = i
            i +=1
            same = 1
    if same > 1 and (same % 9 != 1):
        result = result + ((s[last] + "9") * (same//9)) + (s[last] + str(same % 9))
    elif same > 1 and (same % 9 == 1):
        result = result + ((s[last] + "9") * (same//9)) + (s[last])
    else :
        result = result + s[last]
    return result

def decompress(s: str) -> str:
    res = ""
    if not s:
        return res
    i = 0
    while (i < len(s) - 1):
        if s[i].isalpha():
            if s[i + 1].isdigit():
                res += (s[i] * int(s[i +1]))
            else :
                res += (s[i])
        i+=1
    if s[i].isalpha():
        res += (s[i])
    return res


if __name__ == "__main__":
    # print(decompress("a2bc5a3"))
    t= Test()
    # t.compress()
    t.decompress()
