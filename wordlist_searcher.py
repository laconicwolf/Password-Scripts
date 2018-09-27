#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180921'
__version__ = '0.01'
__description__ = """Searches for specified words in a dictionary."""


import argparse
import os


def main():
    global words
    dict_words = {}
    print('[*] Reading dictionary file: {}'.format(filename))
    dict_file =  open(filename, encoding="utf8", errors='ignore')
    for line in dict_file.read().split('\n'):
        dict_words[line] = True
    dict_file.close()
    print('[*] Searching...')
    words = [word for word in words]
    unique_words = []
    for word in words:
        if not dict_words.get(word):
            unique_words.append(word)
    if unique_words:
        if args.outfile:
            print("[*] Writing words that do not appear in {} to {}...".format(filename, args.outfile))
            with open(args.outfile, 'w', encoding="utf8", errors='ignore') as fh:
                for word in unique_words:
                    fh.write(word + '\n')
        else:
            for word in unique_words:
                print("[*] {} does not appear in {}".format(word, filename))
    else:
        print("[*] All words from {} appeared in {}".format(args.wordlist, filename))
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dictionary',
                        help="Specify the dictionary you would like to search in.")
    parser.add_argument('-w', '--word',
                        nargs="*",
                        help="Specify the word or words you'd like to search for.")
    parser.add_argument('-wl', '--wordlist',
                        help="Specify the filename containing the list of words you'd like to search for.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a specified file.")
    args = parser.parse_args() 
    if not args.dictionary:
        parser.print_help()
        print("\n[-] Please specify the filename of the dictionary you would like to search in.\n")
        exit()
    else:
        filename = args.dictionary
    if not args.word and not args.wordlist:
        parser.print_help()
        print("\n[-] Please specify a word you would like to search for (-w) or specify a filename containing a list of words you'd like to search for (-wl).\n")
        exit()
    if args.word and args.wordlist:
        parser.print_help()
        print("\n[-] Please specify a word (-w) or specify a filename containing a list of words (-wl). Not both.\n")
        exit()
    if args.word:
        words = args.word
    if args.wordlist:
        if not os.path.exists(args.wordlist):
            print("\n[-] The file cannot be found or you do not have permission to open the file. Please check the path and try again\n")
            exit()
        with open(args.wordlist, encoding="utf8", errors='ignore') as fh:
            words = fh.read().splitlines() 
    main()
