def g_show_word(file_name):
    """Generator the search for next word that includes a char"""
    next_choice = yield
    with open(file_name, "r") as file:
        for line in file:
            for word in line.split(','):
                if next_choice[0]:
                    """includes the char"""
                    if word.__contains__(next_choice[1]):
                        next_choice = (yield word)
                else:
                    """doesn't include the char"""
                    if not word.__contains__(next_choice[1]):
                        next_choice = (yield word)


def get_choice():
    """Ask the user to include or exclude, and a char to search for."""
    ch = input("Choose Char: ")
    include = input("Include {} in Word (y/n)? ".format(ch))
    if include == "y":
        include = True
    else:
        include = False
    return [include, ch]


def show_word(file_name):
    gen = g_show_word(file_name)
    next(gen)
    while True:
        try:
            next_choice = get_choice()
            word = gen.send(next_choice)
            print(word)
        except StopIteration:
            del gen
            return


if __name__ == '__main__':
    show_word("words.txt")
