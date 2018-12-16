#!/usr/bin/env python

__author__ = "Jake Miller (@LaconicWolf)"
__date__ = "20181216"
__version__ = "0.01"
__description__ = """Combines four wordlists."""

import os
import argparse

def combine_words(wordlists):
    combined_words = []
    d1 = wordlists[0]
    d2 = wordlists[1]
    d3 = wordlists[2]
    d4 = wordlists[3]  
    for h in range(len(d1)):
        w1 = d1[h].title() if args.title_case else d1[h]
        for i in range(len(d2)):
            w2 = d2[i].title() if args.title_case else d2[i]
            for j in range(len(d3)):
                w3 = d3[j].title() if args.title_case else d3[j]
                for k in range(len(d4)):
                    w4 = d4[k].title() if args.title_case else d4[k]
                    combined_words.append(w1 + w2 + w3 + w4)
    return combined_words

def main():
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
    parser.add_argument("-t", "--title_case",
                        action="store_true",
                        help="Capitalizes the first letter and lowercases the remaining letters of a word.")
    args = parser.parse_args()
    if not args.dictionaries:
        parser.print_help()
        print("\n[-] Please specify 4 dictionaries (-d dict1.txt dict2.txt dict3.txt dict4.txt).\n")
        exit()
    if len(args.dictionaries) != 4:
        parser.print_help()
        print("\n[-] You must specify 4 dictionaries (-d dict1.txt dict2.txt dict3.txt dict4.txt). No more, no less.\n")
        exit()
    wordlists = []
    for file in args.dictionaries:
        if not os.path.exists(file):
            print("\n[-] The file {} cannot be found or you do not have permission to open the file. Please check the path and try again\n".format(file))
            exit()
        with open(file, encoding="utf8", errors='ignore') as fh:
            words = fh.read().splitlines()
            wordlists.append(words)
    main()