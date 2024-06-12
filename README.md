# Document Checker

## Overview

The Document Checker application is designed to help users verify the correctness of their documents using various string matching algorithms and regular expressions. This tool checks for common errors such as missing capitalization, improper punctuation, multiple spaces, and ensures that each sentence contains at least one noun and one verb. It also provides suggestions for misspelled words using the Levenshtein distance algorithm.

## Algorithms Used

### Knuth-Morris-Pratt (KMP) Algorithm

The KMP algorithm is used for pattern matching in this application. It preprocesses the pattern to create a partial match table (also known as the "border function") which helps to determine the next positions of the pattern to match against the text, thereby avoiding redundant comparisons. This makes it efficient for checking the presence of nouns and verbs in sentences.

### Boyer-Moore (BM) Algorithm

The BM algorithm is another string matching algorithm used in this application. It preprocesses the pattern to create a last occurrence table, which helps in determining the shift distance when a mismatch occurs, making the algorithm efficient for long texts. However, in our use case, KMP is generally more efficient due to the shorter length of patterns (words).

### Levenshtein Distance

The Levenshtein distance algorithm is used to provide suggestions for misspelled words. It calculates the minimum number of single-character edits (insertions, deletions, or substitutions) required to change one word into another, providing a measure of similarity between two words.

### Regular Expressions (Regex)

Regex is used to perform various checks on the sentences, including:
- Ensuring proper capitalization at the beginning of sentences.
- Detecting multiple consecutive spaces.
- Checking for the presence of ending punctuation marks (periods, exclamation marks, question marks).
- Ensuring proper spacing around punctuation marks.

## How to Use

To use the Stack Overflow Search Enhancer, you will need to have Python installed on your machine. Follow these steps to get started:

1. Clone the repository to your local machine using:
```
git clone https://github.com/Benardo07/document_checker.git
```
2. Navigate to the directory containing the project files.
```
cd document_checker
```
3. Run the program by executing:
```
python main.py
```

## Author
This application was developed by Benardo (13522055).
