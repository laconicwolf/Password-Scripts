#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180914'
__version__ = '0.02'
__description__ = """Reads in one or more plain-text password lists to find the frequency 
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


def main():
    for filename in args.filename:
        words = open(filename).read().splitlines()
        masks = [generate_char_mask(word) for word in words]
        sorted_masks = sort_char_masks(masks)
        if args.outfile:
            with open('masks.txt', 'w') as outfile:
                for k, v in sorted_masks:
                    print("{} : {}".format(k, v))
                    outfile.write("{} : {}\n".format(k, v))
        else:
            for k, v in sorted_masks:
                print("{} : {}".format(k, v))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        nargs='*',
                        help="Specify a file containing the output of an nmap scan in xml format.")
    parser.add_argument("-o", "--outfile",
                        action="store_true",
                        help="Writes the output to a file in the current directory.")
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
    main()