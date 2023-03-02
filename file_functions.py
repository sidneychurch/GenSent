import random
import json
import pronouncing
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

ignore_chars = ['.', '?', '!', '(', ')', ',', ':', ';', ' ', '[', ']', '\n']

num_words_to_generate = 20  # the length in chars of the final output

ngrams = {}  # this will contain all of the found ngrams and their associations

files = []

loaded_dict = []


def load_file(file_list, status):
    # https://docs.python.org/3/library/dialog.html
    filename = askopenfilename(initialdir='./', filetypes=[('Text File', '.txt')], defaultextension='.txt',
                               multiple=True)  # show an "Open" dialog box and return the path to the selected file
    dict_list = ''

    if loaded_dict:
        dict_list = 'Files Loaded:\n'
        for dicts in loaded_dict:
            dict_list += dicts + '\n'

    for location in filename:
        if location != '':
            files.append(location)
            if not loaded_dict:
                updated_list = 'Files Loaded:\n'
            else:
                updated_list = dict_list

            i = 0
            for file in files:
                if '/' in file:
                    back = file.rfind('/')
                else:
                    back = file.rfind('\\')
                if i < len(files) - 1:
                    updated_list += file[back + 1:len(file)] + '\n'
                else:
                    updated_list += file[back + 1:len(file)]
                i += 1

            file_list.set(updated_list)
            status.set('Ready To Create Dictionary')


def load_dict(file_list, status):
    global ngrams
    file = askopenfilename(initialdir='./', filetypes=[('Generated Dictionary', '.gendict')],
                           defaultextension='.gendict')
    if file:
        with open(file) as to_load:
            ngrams = json.load(to_load)

        if '/' in file:
            back = file.rfind('/')
        else:
            back = file.rfind('\\')

        updated_list = 'Files Loaded:\n'
        file_name = file[back + 1:len(file)]
        updated_list += file_name
        loaded_dict.append(file_name)
        file_list.set(updated_list)
        status.set('Ready To Generate Text')


def save_dict():
    file = asksaveasfilename(initialdir='./', filetypes=[('Generated Dictionary','.gendict')], defaultextension='.gendict')
    if file:
        to_save = json.dumps(ngrams, indent=4)
        with open(file, mode='w') as save_file:
            save_file.write(to_save)


# extract single words from text in doc
def extract_words(status):
    for file in files:
        with open(file, errors='ignore', encoding="utf-8") as readFile:
            word_list = readFile.read()
            word_list = word_list.split()

        i = 0
        for word in word_list:
            # replace bad uni-chars
            if 'â€™' in word:
                word_list[i] = word.replace('â€™', '\'')
            elif 'â€”' in word:
                word_list[i] = word.replace('â€”', ',')
            elif 'Ã¢â‚¬â„¢' in word:
                word_list[i] = word.replace('Ã¢â‚¬â„¢', '\'')
            elif 'Ã¢â‚¬â€' in word:
                word_list[i] = word.replace('Ã¢â‚¬â€', ',')
            # remove unwanted chars
            for char in ignore_chars:
                if char in word:
                    word_list[i] = word.replace(char, '')
            i += 1

        i = 0
        for word in word_list:
            # populate ngram dictionary
            if word not in ngrams:
                ngrams[word] = {'before': [], 'after': []}
            if i != len(word_list) - 1:
                ngrams[word]['after'].append(word_list[i + 1])
            if i != 0:
                ngrams[word]['before'].append(word_list[i - 1])
            i += 1
    status.set('Ready To Generate Text')


# generate sentences based on the word that comes after the current word
def gen_after():
    # instead of word_list probably better to pull keys from ngrams dict.
    word_keys = list(ngrams.keys())
    current_gram = random.choice(word_keys)
    result = current_gram

    for _ in range(num_words_to_generate):
        if current_gram not in ngrams:
            break
        else:
            possible_next_word = ngrams[current_gram]['after']
        next_word = random.choice(possible_next_word)
        result += ' ' + next_word
        current_gram = next_word

    return result


# generate sentences based on the word that comes before the current word
def gen_before(end_word):
    result = end_word
    for _ in range(num_words_to_generate):
        if end_word not in ngrams:
            break
        else:
            possible_prev_word = ngrams[end_word]['before']
        prev_word = random.choice(possible_prev_word)
        result = prev_word + ' ' + result
        end_word = prev_word

    return result


def find_rhyme():
    # pull keys from ngrams dict.
    word_keys = list(ngrams.keys())
    first_word = ''
    rhyme_found = False
    found_rhymes = []
    while not rhyme_found:
        first_word = random.choice(word_keys)
        possible_rhymes = pronouncing.rhymes(first_word)
        for rhyme in possible_rhymes:
            if rhyme in ngrams and rhyme != first_word.lower():
                rhyme_found = True
                found_rhymes.append(rhyme)

    second_word = random.choice(found_rhymes)
    return [first_word, second_word]


def gen_rhyming_sentences(num_sentence):
    if num_sentence % 2 == 0:
        num_sentence /= 2
    else:
        num_sentence += 1
        num_sentence /= 2
    num_sentence = int(num_sentence)

    sentences = []
    for _ in range(num_sentence):
        end_words = find_rhyme()
        sentence_one = gen_before(end_words[0])
        sentence_two = gen_before(end_words[1])
        sentences.append(sentence_one)
        sentences.append(sentence_two)

    return sentences


def gen_sentences(num_sentence):
    sentences = []
    for _ in range(num_sentence):
        new_sentence = gen_after()
        sentences.append(new_sentence)

    return sentences
