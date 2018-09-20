#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180914'
__version__ = '0.02'
__description__ = """Analyzes a password list to find frequency of characters per position."""


import argparse
import os
import string
import itertools


def get_freq(word):
    """docstring
    #https://stackoverflow.com/questions/43693018/python-position-frequency-dictionary-of-letters-in-words
    """
    l = len(word) - word.count(None)
    return {n: word.count(n)/l for n in charset}


def arrange_words_by_length(list_of_words):
    """Takes a list of words and returns a list arranged by the word length."""
    list_of_words.sort(key=len)
    return list_of_words


def sort_frequency_list(frequency_dict):
    """Returns a listed tuple of a frequencies, sorted by the key that occurs
    most.
    """
    sorted_frequencies = [(k, frequency_dict[k]) for k in sorted(frequency_dict, key=frequency_dict.get, reverse=True)]
    return sorted_frequencies

def group_words_by_length(word_list):
    d={}
    for word in word_list:
        d.setdefault(len(word), []).append(word)
    return [d[n] for n in sorted(d)] 


def main():
    for filename in args.filename:
        wordlist = open(filename, encoding="utf8", errors='ignore').read().splitlines()
        grouped_words = group_words_by_length(wordlist)
        for words in grouped_words:
            print("\n[*] {} letter words - Total words: {}\n".format(len(words[0]), len(words)))
            frequency_list = [get_freq(word) for word in itertools.zip_longest(*words)]
            pos_counter = 1
            for item in frequency_list:
                sorted_freq = sort_frequency_list(item)
                print('[*] Character position {}'.format(pos_counter))
                for k, v in sorted_freq:
                    if v:
                        print(k,v)
                pos_counter += 1


if __name__ == '__main__':                                
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        action='store_true',
                        help="Increase output verbosity.")
    parser.add_argument("-f", "--filename",
                        nargs='*',
                        help="Specify a file containing plain text passwords.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a specified file in the current directory.")
    args = parser.parse_args()
    
    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify one or more password files to analyze. For multiple input files, separate with a space.\n")
        exit()
    for filename in args.filename:
        if not os.path.exists(filename):
            parser.print_help()
            print("\n[-] The file {}, does not exist or you lack permissions to open it. Please try again.\n".format(filename))
            exit()  
    charset = string.ascii_letters + string.digits + string.punctuation + ' '
    main()