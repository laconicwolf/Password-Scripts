#!/usr/bin/env python

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190401'
__version__ = '0.01'
__description__ = """Reads a file containing plain text words, accepts user input
specifying the number of charsets present, and prints to new file words that meet
the charset requirement."""

import argparse
import string
import os

def get_complexity(word):
    """Analyzes a word and returns a tuple containing the 
    word, along with a complexity number of the number of
    charsets present."""
    complexity = 0
    lowercase = False
    uppercase = False
    special = False
    digits = False

    string.punctuation += ' '

    for char in string.ascii_lowercase:
        if char in word:
            lowercase = True

    for char in string.ascii_uppercase:
        if char in word:
            uppercase = True

    for char in string.punctuation:
        if char in word:
            special = True

    for char in string.digits:
        if char in word:
            digits = True
    if lowercase:
        complexity += 1
    if uppercase:
        complexity += 1
    if special:
        complexity += 1
    if digits:
        complexity += 1
    return (word,complexity)


def main():
    sorted_words = []
    print('[*] Reading file: {}...',format(filename))
    with open(filename) as fh:
        words = fh.read().splitlines()
    print('[*] Getting word complexity...')
    word_tuple = [get_complexity(word) for word in words]
    for item in word_tuple:
        word = item[0]
        complexity = item[1]
        if complexity in [int(number) for number in args.complexity]:
            sorted_words.append(word)
    print('[+] Writing words to {}...'.format(outfile))
    with open(outfile, 'w') as fh:
        for word in sorted_words:
            fh.write(word + '\n')
    print('[+] Complete!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        help="Specify a file containing plain text passwords.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a file, masks.txt, in the current directory.")
    parser.add_argument("-c", "--complexity",
                        nargs='*',
                        default=['1','2','3','4'],
                        choices=['1','2','3','4'],
                        help="Specify the the number of charsets the must be present.")
    parser.add_argument("-i", "--include_less_complex",
                        help="Specify a file containing plain text passwords.")
    args = parser.parse_args()

    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify a file containing plaintext passwords.\n")
        exit()
    filename = args.filename
    if not os.path.exists(filename):
        parser.print_help()
        print("\n[-] The file {}, does not exist or you lack permissions to open it. Please try again.\n".format(filename))
        exit()

    outfile = args.outfile if args.outfile else "complexity_sorter_outfile.txt"
    main()