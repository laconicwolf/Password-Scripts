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
            elif char in string.punctuation or char == ' ':
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
            elif char in string.punctuation or char == ' ':
                mask += '?s'
            else:
                print('Encountered an non-standard character: {}. It will appear in a mask as ?X '.format(char))
                mask += '?X'
    return mask


def sort_char_masks(mask_list):
    """Returns a listed tuple of a character masks, where the mask is the first ([0]) element 
    and the number of times the mask occurs is the second element ([1]). For example:
    [('?l?l?l?l?l', 4)]
    """
    mask_dict = dict(Counter(mask_list))
    sorted_counted_mask = [(k, mask_dict[k]) for k in sorted(mask_dict, key=mask_dict.get, reverse=True)]
    return sorted_counted_mask


def arrange_words_by_length(list_of_words):
    """Takes a list of words and returns a list of multiple lists
    arranged by the word length.
    """
    list_of_words.sort(key=len)
    return list_of_words


def sort_dict_by_key_len(dict_obj):
    """Takes a dictionary and returns a list of tuples sorted by the length of
    the dictionary's keys.
    """
    return [(k, dict_obj[k]) for k in sorted(dict_obj, key=len)]


def sort_tuple_list_by_two_elements(tuple_list):
    """sorts a list of tuples that contain two values, first by the first value,
    then by the second value. The -x[1] sorts in reverse.
    #https://stackoverflow.com/questions/14466068/sort-a-list-of-tuples-by-second-value-reverse-true-and-then-by-key-reverse-fal
    """
    return sorted(tuple_list, key=lambda x: (len(x[0]), -x[1]))


def main():
    """Reads in a plain-text password lists to find the frequency 
    of password character masks. Will display all character masks found.
    """
    # Initialize variable to hold a list of all sorted mask dictionaries for a file
    file_mask_list = []
    for filename in args.filename:
        print("[*] Processing {}".format(filename))
        # Read the file into memory.
        words = open(filename).read().splitlines()

        # Sort the words by length.
        sorted_words = arrange_words_by_length(words)
        
        # Initialize a list per file to store lists of words sorted by length.
        file_word_list = []
        sorted_word_list = []

        # Probably can come back to the below code later and remove a lot of it.
        # I don't need to sort by length at this point because I do it later.

        # Starting point of the word length. A new list will be generated
        # for each increase in wordlength.
        base_word_length = len(sorted_words[0])
        for word in sorted_words:
            if len(word) == base_word_length:
                sorted_word_list.append(word)
            else:
                file_word_list.append(sorted_word_list)
                base_word_length += 1
                sorted_word_list = []

        # Loop through the list of lists.
        for group in file_word_list:

            # Continues if an empty list is encountered.
            if not group:
                continue

            # Generate the masks for each word and sort them by count.
            masks = [generate_char_mask(word) for word in group]
            sorted_masks = sort_char_masks(masks)
            file_mask_list.append(sorted_masks)

    # Converts tuples to a dictionary to combine values of the same mask
    # across the different input files
    file_mask_list = [dict(l) for l in file_mask_list]
    
    # Gets all the unique masks from the input files
    mask_keys = []
    for mask_dictionary in file_mask_list:
        dict_keys = list(mask_dictionary.keys())
        for k in dict_keys:
            mask_keys.append(k)
    mask_keys = list(set(mask_keys))
    
    # Adds the number of occurences of mask from each input file
    # by combining dictionary values of the same key
    results = {}
    for k in mask_keys:
        sums = []
        for item in file_mask_list:
            if item.get(k):
                sums.append(item.get(k))
        results[k] = sum(sums)

    # Sorts the result by mask length, converting it to a list of tuples
    sorted_results = sort_dict_by_key_len(results)

    # Sorts the tuples first by length, then by value
    sorted_results = sort_tuple_list_by_two_elements(sorted_results)

    # Output to terminal and file.
    if args.outfile:
        with open(args.outfile, 'a') as outfile:
            outfile.write('Processed files:\n')
            for f in args.filename:
                outfile.write(f + '\n')
            word_length = len(sorted_results[0][0])
            print("\n[+] Mask for {} letter words".format(word_length))
            outfile.write("\n[+] Mask for {} letter words\n".format(word_length))
            for k, v in sorted_results:
                new_word_length = len(k)
                if new_word_length != word_length:
                    print("\n[+] Mask for {} letter words".format(len(k)))
                    outfile.write("\n[+] Mask for {} letter words\n".format(len(k)))
                    word_length = new_word_length
                print("{} : {}".format(k, v))
                outfile.write("{} : {}\n".format(k, v))
    else:
        word_length = len(sorted_results[0][0])
        print("\n[+] Mask for {} letter words".format(word_length))
        for k, v in sorted_results:
            new_word_length = len(k)
            if new_word_length != word_length:
                print("\n[+] Mask for {} letter words".format(len(k)))
                word_length = new_word_length
            print("{} : {}".format(k, v))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        nargs='*',
                        help="Specify a file containing the output of an nmap scan in xml format.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a file, masks.txt, in the current directory.")
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