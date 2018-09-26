#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180924'
__version__ = '0.01'
__description__ = """Convert all words to lowercase and capitalizes letters at 
specified indexes. Can write output to a new file."""


import argparse
import os


def main():
    print('[*] Reading file: {}...'.format(filename))
    with open(filename, encoding="utf8", errors='ignore') as fh:
        words = fh.read().splitlines()
    print('[*] Processing {} words...'.format(len(words)))
    print('[*] Changing all words to lowercase...')
    words = [word.lower() for word in words]
    if args.index:
        print('[*] Capitalizing letters at specified indexes...')
        capitalized_words = []
        for word in words:
            if not word: continue
            list_word = list(word)
            for pos in args.index:
                try:
                    list_word[pos] = list_word[pos].capitalize()
                except IndexError as e:
                    continue
            capitalized_words.append(''.join(list_word))
    else:
        print('[*] Capitalizing first letter of each word...')
        capitalized_words = [word.title() for word in words]
    if args.outfile:
        print('[*] Writing to {}...'.format(args.outfile))
        with open(args.outfile, 'w', encoding="utf8", errors='ignore') as fh:
            for word in capitalized_words:
                fh.write(word + '\n')
    else:
        for word in capitalized_words:
            print(word)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        help="Specify a file containing words.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a specified file.")
    parser.add_argument("-i", "--index",
                        nargs='*',
                        type=int,
                        help="Specify one or more integers to be used as positions (zero index) to capitalize a letter or letters.")
    args = parser.parse_args()

    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify an input file containing words (-f).\n")
        exit()
    else:
        filename = args.filename
        if not os.path.exists(filename):
            print("\n[-] The file {} cannot be found or you do not have permission to open the file. Please check the path and try again\n".format(filename))
            exit()
    main()