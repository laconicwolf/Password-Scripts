#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180924'
__version__ = '0.01'
__description__ = """Removes case, digits, and special characters for a wordlist
and uniques it."""

import argparse
import re
import os


def main():
    """Passes a wordlist through a series of functions to generate
    a rule file.
    """
    global words
    print("[*] Processing {} words.".format(len(words)))
    print("[*] Changing all words to lowercase...")
    words = [word.lower() for word in words]
    print("[*] Removing numbers and special characters...")
    words = [re.sub(r'[^a-z]+', '', word) for word in words]
    print("[*] Removing duplicate words...")
    words = list(set(words))
    print("[*] Printing cleaned words to {}".format(outfile))
    with open(outfile, 'w') as fh:
        for word in words:
            fh.write(word + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",
                        help="Specify a file containing words.")
    parser.add_argument("-o", '--outfile',
                        help="Writes the words to a specified outfile name")
    args = parser.parse_args()

    if not args.file and not args.outfile:
        parser.print_help()
        print("\n[-] Please specify an input file containing words (-f) and the name of an output file to write to (-o out.txt).\n")
        exit()
    else:
        file = args.file
        outfile = args.outfile
        if not os.path.exists(file):
            print("\n[-] The file cannot be found or you do not have permission to open the file. Please check the path and try again\n")
            exit()
        print('[*] Reading file: {}'.format(file))
        with open(file, encoding="utf8", errors='ignore') as fh:
            words = fh.read().splitlines()

main()