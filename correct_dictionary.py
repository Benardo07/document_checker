import csv
import spacy
from collections import defaultdict

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Function to load and check the dataset
def load_and_check_dataset(filename):
    corrected_data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row if your CSV has one
        for row in reader:
            if len(row) < 3:  # Ensure the row has the expected number of columns
                continue
            word, original_pos = row[1], row[2].upper()  # Assume word is in second column and POS in third

            # Predict POS using spaCy
            doc = nlp(word)
            spacy_pos = doc[0].tag_  # Get POS tag of the first token
            print(spacy_pos)

            # Map spaCy tags to your dataset's tag format if necessary
            # mapped_pos = map_spacy_pos_to_dataset(spacy_pos)
            # Check if the original POS matches spaCy's prediction
            if original_pos != spacy_pos:
                corrected_data.append([row[0], word,spacy_pos])  # Assuming row[0] is an ID or similar
            else:
                corrected_data.append(row)
                
    return corrected_data

# Function to map spaCy POS tags to the dataset's POS format
def map_spacy_pos_to_dataset(spacy_pos):
    # Mapping of spaCy POS tags to your custom tags
    mapping = {
        'CCONJ': 'CC',  # Coordinating conjunction
        'CD': 'CD',     # Cardinal number, adding directly if spaCy had similar, which it does not; typically uses NUM
        'DET': 'DT',    # Determiner
        'EX': 'EX',     # Existential "there", same direct mapping
        'FW': 'FW',     # Foreign word
        'ADP': 'IN',    # Preposition or subordinating conjunction
        'JJ': 'JJ',     # Adjective
        'JJR': 'JJR',   # Adjective, comparative
        'JJS': 'JJS',   # Adjective, superlative
        'LS': 'LS',     # List item marker
        'MD': 'MD',     # Modal
        'NN': 'NN',     # Noun, singular or mass
        'NNS': 'NNS',   # Noun, plural
        'NNP': 'NNP',   # Proper noun, singular
        'NNPS': 'NNPS', # Proper noun, plural
        'PDT': 'PDT',   # Predeterminer
        'POS': 'POS',   # Possessive ending
        'PRP': 'PRP',   # Personal pronoun
        'PRP$': 'PRP$', # Possessive pronoun
        'RB': 'RB',     # Adverb
        'RBR': 'RBR',   # Adverb, comparative
        'RBS': 'RBS',   # Adverb, superlative
        'RP': 'RP',     # Particle
        'SYM': 'SYM',   # Symbol
        'TO': 'TO',     # "to" as preposition/infinitive marker
        'UH': 'UH',     # Interjection
        'VB': 'VB',     # Verb, base form
        'VBG': 'VBG',   # Verb, gerund or present participle
        'VBD': 'VBD',   # Verb, past tense
        'VBN': 'VBN',   # Verb, past participle
        'VBP': 'VBP',   # Verb, non-3rd person singular present
        'VBZ': 'VBZ',   # Verb, 3rd person singular present
        'WDT': 'WDT',   # Wh-determiner
        'WP': 'WP',     # Wh-pronoun
        'WP$': 'WP$',   # Possessive wh-pronoun
        'WRB': 'WRB'    # Wh-adverb
    }
    return mapping.get(spacy_pos, 'UNK')  # Return 'UNK' (Unknown) for unmapped tags


# Function to save the corrected data back to CSV
def save_corrected_data(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Word', 'POS'])  # Write header if needed
        writer.writerows(data)

# Main function
def main():
    input_filename = 'words_pos.csv'
    corrected_filename = 'corrected_words_pos.csv'
    corrected_data = load_and_check_dataset(input_filename)
    save_corrected_data(corrected_data, corrected_filename)

if __name__ == "__main__":
    main()
