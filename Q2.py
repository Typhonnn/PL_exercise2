"""
Evyatar Menczer - 312278179
Tal Balelty - 312270291
"""


def g_load_word(flag, char):
    with open("words.txt", "r") as words:
        for line in words:
            for found_word in line.split(','):
                if flag.lower() == "include":
                    if char in found_word:
                        yield found_word
                elif flag.lower() == "exclude":
                    if char not in found_word:
                        yield found_word
                else:
                    return print("Nothing Found!")


if __name__ == '__main__':
    my_flag = input("Enter flag (Exclude/Include): ")
    letter = input("Enter letter: ")
    for word in g_load_word(my_flag, letter):
        print(word)
