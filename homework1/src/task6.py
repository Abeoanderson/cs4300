import string

def main():
    with open("task6_read_me.txt","r") as f:
        text = f.read()

    for p in string.punctuation:
        text = text.replace(p," ")

    f.close()

    return len(text.split())

if __name__ == "__main__":
    main()