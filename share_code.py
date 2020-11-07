from random import choice

words = []

def load():
    with open('words.txt', 'r') as word_file:
        return word_file.read().splitlines()

def generate_share_code(word_list):
    return choice(word_list) + "-" + choice(word_list) + "-" + choice(word_list)
    