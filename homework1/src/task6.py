import string

def count_num_words():
    """opens task6_read_me and counts number of words"""
    with open("task6_read_me.txt","r") as f:
        text = f.read()
    #it was counting the puncuation as words so we map " " to all found punctuation
    for p in string.punctuation:
        text = text.replace(p," ")

    f.close()
    #split into strings based on " " as a defualt val and get length of list
    count = len(text.split())
    return count

if __name__ == "__main__":
    count_num_words()