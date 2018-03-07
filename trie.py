
class Trie(object):
    def __init__(self):
        self.tree = {}

    def add(self, word, freq):
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                tree[char] = {}
                tree = tree[char]
        tree['exist'] = True  # leaf node
        tree['freq'] = freq

    def find(self, word):
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                return False

        if "exist" in tree:  # and tree["exist"] == True:
            return True
        else:
            return False

    def get_freq(self, word):
        tree = self.tree
        for char in word:
            if char in tree:
                tree = tree[char]
            else:
                return 0
        if "exist" in tree:
            return tree['freq']
        else:
            return 0