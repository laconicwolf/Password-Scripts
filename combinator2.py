#!/usr/bin/env python

__author__ = "Jake Miller (@LaconicWolf)"
__date__ = "20181216"
__version__ = "0.01"
__description__ = """Combines two wordlists."""

import os
import argparse
from collections import OrderedDict

def create_separate_wordlists(word_dict):
    separate_wordlists = []
    for key, value in word_dict.items():
        separate_wordlists.append(value)
    return separate_wordlists

def combine_words(wordlists):
    combined_words = []
    d1 = wordlists[0]
    d2 = wordlists[1] 
    for h in range(len(d1)):
        w1 = d1[h]
        for i in range(len(d2)):
            w2 = d2[i]
            combined_words.append(w1 + w2)
    return combined_words

def main():
    wordlists = create_separate_wordlists(dictionaries)
    combined_words = combine_words(wordlists)
    if args.outfile:
        with open(args.outfile, 'w', encoding="utf8", errors='ignore') as fh:
            for word in combined_words:
                fh.write(word + '\n')
    else:
        for word in combined_words:
            print(word)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dictionaries",
                        nargs="*",
                        help="Specify a file or files containing words.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a specified file.")
    args = parser.parse_args()
    if not args.dictionaries:
        parser.print_help()
        print("\n[-] Please specify 2 dictionaries (-d dict1.txt dict2.txt).\n")
        exit()
    if len(args.dictionaries) != 2:
        parser.print_help()
        print("\n[-] You must specify 2 dictionaries (-d dict1.txt dict2.txt). No more, no less.\n")
        exit()
    dictionaries = OrderedDict()
    for file in args.dictionaries:
        if not os.path.exists(file):
            print("\n[-] The file cannot be found or you do not have permission to open the file. Please check the path and try again\n")
            exit()
        with open(file, encoding="utf8", errors='ignore') as fh:
            words = fh.read().splitlines()
            dictionaries[file] = words
    main()