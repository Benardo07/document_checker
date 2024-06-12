import csv
import re
import time
import os
from collections import defaultdict
from Levenshtein import distance as levenshtein_distance

# Load words from CSV and create a dictionary of sets based on parts of speech
def load_words(filename):
    words_pos = defaultdict(set)
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')  
        next(reader)  
        for row in reader:
            if len(row) < 2: 
                continue
            word, pos = row[1], row[2]
            words_pos[pos.strip()].add(word.lower().strip()) 
    return words_pos

# KMP algorithm helper functions
def border_function(pattern):
    table = [0] * len(pattern)
    j = 0
    for i in range(1, len(pattern)):
        if pattern[i] == pattern[j]:
            j += 1
            table[i] = j
        else:
            j = table[j - 1] if j > 0 else 0
    return table

def kmp_search(text, pattern, table):
    m, i = 0, 0  
    while m + i < len(text):
        if pattern[i] == text[m + i]:
            if i == len(pattern) - 1:
                return True  
            i += 1
        else:
            if table[i] > 0:
                m += i - table[i]
                i = table[i]
            else:
                i = 0
                m += 1
    return False  

def check_noun_verb_presence(sentence, nouns, verbs, algorithm):
    words = re.findall(r'\b\w+\b', sentence)
    if(algorithm == "KMP"):
        noun_found = any(kmp_search(words, [noun], border_function([noun])) for noun in nouns)
        verb_found = any(kmp_search(words, [verb], border_function([verb])) for verb in verbs)
    else:
        noun_found = any(boyer_moore_search(words, [noun]) for noun in nouns)
        verb_found = any(boyer_moore_search(words, [verb]) for verb in verbs)
    
    if not noun_found or not verb_found:
        return f"Sentence '{sentence}' lacks {'a noun' if not noun_found else ''}{' and ' if not noun_found and not verb_found else ''}{'a verb' if not verb_found else ''}."
    return None





def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1  
            deletions = current_row[j] + 1       
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_closest_word(word, words_pos):
    closest_words = []
    min_distance = float('inf')
    for pos in words_pos:
        for w in words_pos[pos]:
            dist = levenshtein_distance(word, w)
            if dist < min_distance:
                min_distance = dist
                closest_words = [w]
            elif dist == min_distance:
                closest_words.append(w)
    return closest_words,min_distance

def validate_words(doc, words_pos):
    found_words = set()
    for pos in words_pos:
        found_words.update(words_pos[pos])

    words_in_doc = re.findall(r'\b\w+\b', doc)
    not_found = []
    suggestions = {}
    
    for word in words_in_doc:
        word_lower = word.lower()
        if word_lower not in found_words:
            if word.isdigit(): 
                continue
            not_found.append(word)
            closest_word,_ = find_closest_word(word_lower, words_pos)
            suggestions[word] = closest_word
    
    return not_found, suggestions

def preprocess_text(text):
    # Replace periods in abbreviations with a placeholder
    abbreviations = {
        "Mr.": "Mr<prd>",
        "Mrs.": "Mrs<prd>",
        "Ms.": "Ms<prd>",
        "Dr.": "Dr<prd>"
    }
    for abbr, replacement in abbreviations.items():
        text = text.replace(abbr, replacement)
    return text

def postprocess_text(text):
    # Revert placeholders to original abbreviations
    return text.replace("<prd>", ".")

def check_sentence_rules(document, words_pos, algorithm):
    noun_tags = {'NN', 'NNS', 'NNP', 'NNPS','PRP','PRP$'}
    verb_tags = {'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ', 'NNS'}
    nouns = {word for tag in noun_tags for word in words_pos[tag]}
    verbs = {word for tag in verb_tags for word in words_pos[tag]}
    
    document = preprocess_text(document)
    sentences = re.split(r'(?<=[.!?])\s+|\n+', document)

    sentences = [postprocess_text(sentence) for sentence in sentences]

    sentence_errors = []
    
    for sentence in sentences:
        if not re.match(r'^"?\s?[A-Z]', sentence.strip()):
            sentence_errors.append(f"Capitalization error at: {sentence}")
        
        if re.search(r'\s{2,}', sentence):
            sentence_errors.append(f"Multiple spaces: {sentence}")

        if not re.match('.*[.?!]$', sentence.strip()):
            sentence_errors.append(
            f"No ending mark at : {sentence}")


        punctuation_errors = re.findall(r'\.([A-Za-z])', sentence)  
        punctuation_errors += re.findall(r',([^ \n\"])', sentence)  
        for error in punctuation_errors:
            sentence_errors.append(
                f"Punctuation spacing error at: '{error}' in '{sentence}'")

        error_verbNoun = check_noun_verb_presence(sentence, nouns, verbs, algorithm)
        if error_verbNoun:
            sentence_errors.append(error_verbNoun)

    return sentence_errors

def last_occurrence_function(pattern):
    last_occurrence = {}
    for index, char in enumerate(pattern):
        last_occurrence[char] = index
    return last_occurrence

def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    last_occurrence = last_occurrence_function(pattern)

    s = 0 
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1

        if j < 0:
            return True  
        else:
            char_shift = last_occurrence.get(text[s + j], -1)
            s += max(1, j - char_shift)
    
    return False  

def main():
    words_pos = load_words('dictionary/corrected_words_pos.csv')
    print()
    text_file = input("Enter the document name: ")
    if not os.path.isfile(text_file):
        print("The specified text file does not exist.")
        return
    with open(text_file, 'r', encoding='utf-8') as file:
        document = file.read()

    algorithm = input("Select Algorithm: ")

    start_time = time.time()
    not_found, suggestions = validate_words(document, words_pos)
    sentence_mistake = check_sentence_rules(document,words_pos, algorithm)

    print()
    print("Words not found:", not_found)
    print()
    print("Suggestions:")
    if suggestions:
        for word, suggestion_list in suggestions.items():
            print(f"{word}: {', '.join(suggestion_list)}")


    print()
    print("Sentence errors:")
    i = 1
    if sentence_mistake:
        for mistake in sentence_mistake:
            print(str(i) + ". " + mistake)
            i += 1
    else:
        print("No Sentences Error")

    end_time = time.time()
    execution_time = end_time - start_time
    print()
    print(f"Execution time: {execution_time:.2f} seconds")
    print()
main()