class PrefixDictionary:
    def __init__(self):
        self.dct = {}

    def insert(self, word: str) -> None:
        self.dct[len(self.dct.values()) + 1] = word

    def search(self, word: str) -> bool:
        found = False
        for words in self.dct.values():
            if words == word:
                found = True
        return found

    def starts_with(self, prefix: str) -> bool:
        found = False
        for words in self.dct.values():
            if prefix in words:
                found = True
        return found

"""
    d = PrefixDictionary(); d.insert("apple"); 
    print(d.search("apple"))
    print(d.search("app"))
    print(d.starts_with("app"))
    d.insert("app")
    print(d.search("app"))
"""

