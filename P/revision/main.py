from typing import Any
from test import Test

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
            for char in "abcdefghijklmnopqrstuvwxyz":
                if char == current_word[i]:
                    continue
                    
                next_word: str = current_word[:i] + char + current_word[i+1:]
                
                if next_word in word_set:
                    word_set.remove(next_word)
                    queue.append((next_word, level + 1))
                    
    return 0

if __name__ == "__main__":
    # print(prism_detector(["CAT", "A..", "T.."], "CAT"))
    t= Test()
    t.word_ladder()

