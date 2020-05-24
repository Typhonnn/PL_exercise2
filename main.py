import time


class Trie:
    root = {}

    def _init_(self):
        self.count = 0
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
        self.count += 1

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

    def recursive_generator(self, trie):
        my_list = []
        for k, v in trie.items():
            if k != '*':
                for el in self.recursive_generator(v):
                    my_list.append(k + el)
                    yield k + el
            else:
                my_list.append('')
                yield my_list[-1]


def timer(func):
    def run(trie):
        start_time = time.time() * 1000
        ret = func(trie)
        end_time = time.time() * 1000
        print('Time for {} = {}ms'.format(func.__name__, end_time - start_time))
        return ret

    return run


def find_common_key_length(key, word):
    i = 0
    while i < len(word) and i < len(key) and key[i] == word[i]:
        i += 1
    return i


def find_key(patricia, word):
    for key in patricia.keys():
        if key[0] == word[0]:
            return key
    return None


def split_root(current, main_key, small_key1, small_key2):
    if small_key2 == "":
        prev_dict = current[main_key + small_key1]
        new_dict = {"*": True, small_key1: prev_dict}
        current.pop(main_key + small_key1)
    elif small_key1 == "":
        prev_dict = current[main_key + small_key2]
        new_dict = {"*": True, small_key2: prev_dict}
    else:
        prev_dict = current[main_key + small_key1]
        new_dict = {small_key2: {"*": True}, small_key1: prev_dict}
        current.pop(main_key + small_key1)
    current[main_key] = new_dict


class Patricia:
    root = {}

    def __init__(self):
        self.num_of_nodes = 0

    def add(self, word):
        current = self.root
        """this block is for check the matching key for the word. if not exists, word added to keys"""
        index = 0
        while index < len(word):
            key = find_key(current, word)
            if key is None:
                current[word] = {"*": True}
                return
            else:
                index = find_common_key_length(key, word)
                main_key = word[0:index]
                if main_key == key:
                    current = current[main_key]
                    word = word[index:len(word)]
                    index = 0
                else:
                    small_key1 = key[index:len(key)]
                    small_key2 = word[index:len(word)]
                    split_root(current, main_key, small_key1, small_key2)
                    return

    def search(self, word):
        pass


@timer
def build_patricia_from_file(filename):
    patricia = Patricia()
    with open(filename, "r") as words:
        for line in words:
            for word in line.split(','):
                # if patricia.search(word) is False:
                patricia.add(word.lower())
    return patricia


@timer
def build_trie_from_file(filename):
    trie = Trie()
    with open(filename, "r") as words:
        for line in words:
            for word in line.split(','):
                if trie.search(word) is False:
                    trie.add(word.lower())
    return trie


@timer
def loop_print(root):
    for word in sorted(Trie.recursive_generator(root), reverse=True):
        print(word)


if __name__ == '__main__':
    # t = build_trie_from_file("words.txt")
    # loop_print(t.root)
    # print("Words in trie = {}".format(t.count))
    # print("Number of nodes = {}".format(t.num_of_nodes))
    p = build_patricia_from_file("test.txt")
    print(p.root)
