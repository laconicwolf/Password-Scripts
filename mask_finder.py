#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180914'
__version__ = '0.02'
__description__ = """Reads in a plain-text password lists to find the frequency 
of password character masks. Will display all character masks found"""


import argparse
import string
import os
from collections import Counter


def generate_char_mask(word):
    """Analyzes the characters of a word and generates a mask per character.
    Returns the mask of a word as a string."""
    mask = ''
    for char in word:
        try:
            if char in string.uppercase:
                mask += '?u'
            elif char in string.lowercase:
                mask += '?l'
            elif char in string.digits:
                mask += '?d'
            elif char in string.punctuation:
                mask += '?s'
            else:
                print('Encountered an non-standard character: {}. It will appear in a mask as ?X '.format(char))
                mask += '?X'
        except AttributeError:
            if char in string.ascii_uppercase:
                mask += '?u'
            elif char in string.ascii_lowercase:
                mask += '?l'
            elif char in string.digits:
                mask += '?d'
            elif char in string.punctuation:
                mask += '?s'
            else:
                print('Encountered an non-standard character: {}. It will appear in a mask as ?X '.format(char))
                mask += '?X'
    return mask


def sort_char_masks(mask_list):
    """Returns a dictionary of character masks, where the mask is the key and the 
    value is the number of times the mask occurs
    """
    mask_dict = dict(Counter(mask_list))
    sorted_mask_dict = [(k, mask_dict[k]) for k in sorted(mask_dict, key=mask_dict.get, reverse=True)]
    return sorted_mask_dict


def arrange_words_by_length(list_of_words):
    """Takes a list of words and returns a list of multiple lists
    arranged by the word length.
    """
    list_of_words.sort(key=len)
    return list_of_words


def main():
    """Reads in a plain-text password lists to find the frequency 
    of password character masks. Will display all character masks found.
    """
    # Read the file into memory.
    words = open(filename).read().splitlines()

    # Sort the words by length.
    sorted_words = arrange_words_by_length(words)
    
    # Initialize a main list to store lists of words sorted by length.
    main_word_list = []
    sorted_word_list = []

    # Starting point of the word length. A new list will be generated
    # for each increase in wordlength.
    base_word_length = len(sorted_words[0])
    for word in sorted_words:
        if len(word) == base_word_length:
            sorted_word_list.append(word)
        else:
            main_word_list.append(sorted_word_list)
            base_word_length += 1
            sorted_word_list = []

    # Loop through the list of lists.
    for group in main_word_list:

        # Continues if an empty list is encountered.
        if not group:
            continue
        print("\n[+] Mask for {} letter words".format(len(group[0])))

        # Generate the masks for each word and sort them by count.
        masks = [generate_char_mask(word) for word in group]
        sorted_masks = sort_char_masks(masks)

        # Output to terminal and file.
        if args.outfile:
            with open('masks.txt', 'a') as outfile:
                for k, v in sorted_masks:
                    print("{} : {}".format(k, v))
                    outfile.write("{} : {}\n".format(k, v))
        else:
            for k, v in sorted_masks:
                print("{} : {}".format(k, v))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        help="Specify a file containing plain text passwords.")
    parser.add_argument("-o", "--outfile",
                        action="store_true",
                        help="Writes the output to a file, masks.txt, in the current directory.")
    args = parser.parse_args()

    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify a password file to analyze.\n")
        exit()
    filename = args.filename

    if not os.path.exists(filename):
        parser.print_help()
        print("\n[-] The file {}, does not exist or you lack permissions to open it. Please try again.\n".format(filename))
        exit()

    main()