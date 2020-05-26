"""
Evyatar Menczer - 312278179
Tal Balelty - 312270291
"""
import time


class Trie:

    def __init__(self):
        self.root = {}
        self.num_of_words = 0
        self.num_of_nodes = 0

    def add(self, word):
        cur = self.root
        for char in word:
            if char == '\n':
                break
            if char not in cur:
                cur[char] = {}
                self.num_of_nodes += 1
            cur = cur[char]
        cur['*'] = True
        self.num_of_words += 1

    def search(self, word):
        cur = self.root
        for letter in word:
            if letter not in cur:
                return False
            cur = cur[letter]
        if '*' in cur:
            return True
        else:
            return False

    def recursive_generator(self, root):
        my_list = []
        for k, v in root.items():
            if k != '*':
                for el in self.recursive_generator(v):
                    my_list.append(k + el)
                    yield k + el
            else:
                my_list.append('')
                yield my_list[-1]


class Patricia:

    def __init__(self):
        self.root = {}

    def add(self, word):
        current = self.root
        """this block is for check the matching key for the word. if not exists, word added to keys"""
        index = 0
        while index < len(word):
            key = find_key(current, word)
            """Finished going down the patricia and no more overlap found create mark new word"""
            if key is None:
                current[word] = {"*": True}
                return
            else:
                """New word overlaps with existing key"""
                index = find_common_key_length(key, word)
                main_key = word[0:index]
                if main_key == key:
                    """New substring of word matches whole key"""
                    current = current[main_key]
                    word = word[index:len(word)]
                    index = 0
                else:
                    """New substring of word is partially different than existing key, performs a split in node"""
                    small_key1 = key[index:len(key)]
                    small_key2 = word[index:len(word)]
                    self.split_node(current, main_key, small_key1, small_key2)
                    return

    def search(self, word):
        current = self.root
        key = ""
        for letter in word:
            key += letter
            if key in current.keys():
                current = current[key]
                key = ""
        if key == "" and "*" in current.keys():
            return True
        else:
            return False

    def find_num_nodes(self, my_dict):
        if my_dict is True:
            return 0
        length = len(my_dict)
        if '*' in my_dict.keys():
            length -= 1
        for node in my_dict.keys():
            length += self.find_num_nodes(my_dict[node])
        return length

    @staticmethod
    def split_node(current, main_key, small_key1, small_key2):
        """Given a node and new keys (after parsing) creates a new node with new children."""
        if small_key2 == "":
            """create one child for longer key"""
            prev_dict = current[main_key + small_key1]
            new_dict = {"*": True, small_key1: prev_dict}
            current.pop(main_key + small_key1)
        elif small_key1 == "":
            """create one child for longer new word"""
            prev_dict = current[main_key + small_key2]
            new_dict = {"*": True, small_key2: prev_dict}
        else:
            """create two children when both different"""
            prev_dict = current[main_key + small_key1]
            new_dict = {small_key2: {"*": True}, small_key1: prev_dict}
            current.pop(main_key + small_key1)
        current[main_key] = new_dict


def find_common_key_length(key, word):
    """Execute this function only when first char of key and word matches.
    return length of longest substring from start"""
    i = 0
    while i < len(word) and i < len(key) and key[i] == word[i]:
        i += 1
    return i


def find_key(patricia, word):
    """compare the first char of key and word.
    return key if found."""
    for key in patricia.keys():
        if key[0] == word[0]:
            return key
    return None


def timer(func):
    def run(trie):
        start_time = time.time() * 1000
        ret = func(trie)
        end_time = time.time() * 1000
        print('Time for {} = {}ms'.format(func.__name__, end_time - start_time))
        return ret

    return run


@timer
def build_patricia_from_file(filename):
    patricia = Patricia()
    with open(filename, "r") as words:
        for line in words:
            for word in line.split(','):
                word = word.lower()
                if patricia.search(word) is False:
                    patricia.add(word)
    return patricia


@timer
def build_trie_from_file(filename):
    trie = Trie()
    with open(filename, "r") as words:
        for line in words:
            for word in line.split(','):
                word = word.lower()
                if trie.search(word) is False:
                    trie.add(word)
    return trie


@timer
def loop_print(trie):
    """Sorted takes the words from generator function and sends them to word in reverse."""
    for word in sorted(trie.recursive_generator(trie.root), reverse=True):
        print(word)


if __name__ == '__main__':
    t = build_trie_from_file("words.txt")
    loop_print(t)
    print("Words in trie = {}".format(t.num_of_words))
    print("Number of nodes in Trie = {}".format(t.num_of_nodes))
    p = build_patricia_from_file("words.txt")
    print("Number of nodes in Patricia = {}".format(p.find_num_nodes(p.root)))
