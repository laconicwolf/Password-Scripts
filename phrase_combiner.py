#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190102'
__version__ = '0.01'
__description__ = """Combines files containing phrases. Can capitalize, manipulate the phrases, etc."""

import argparse
import os

def main():
    all_lines = []
    for filename in files:
        print('[*] Reading file: {}...'.format(filename))
        with open(filename, encoding="utf8", errors='ignore') as fh:
            lines = fh.read().splitlines()
        print('[*] Processing {} lines...'.format(len(lines)))
        for line in lines:
            line = line.strip('.')
            line = line.strip(',')
            line = line.strip('\'')
            words = line.split(' ')
            base_words = [word.lower() for word in words]

            all_lines.append(''.join(base_words))
            all_lines.append(' '.join(base_words))
            all_lines.append('-'.join(base_words))
            all_lines.append('_'.join(base_words))

            words = [word.title() for word in base_words]
            all_lines.append(''.join(words))
            all_lines.append(' '.join(words))
            all_lines.append('-'.join(words))
            all_lines.append('_'.join(words))

            words = [word for word in base_words]
            all_lines.append(''.join(words).title())
            all_lines.append(' '.join(words).title())
            all_lines.append('-'.join(words).title())
            all_lines.append('_'.join(words).title())

    if args.outfile:
        print('[*] Writing to {}...'.format(args.outfile))
        with open(args.outfile, 'w', encoding="utf8", errors='ignore') as fh:
            for line in all_lines:
                fh.write(line + '\n')
    else:
        for line in all_lines:
            print(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        nargs='*',
                        help="Specify a file containing phrases.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a specified file.")
    args = parser.parse_args()
    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify an input file containing words (-f).\n")
        exit()
    else:
        files = args.filename
        for filename in files:
            if not os.path.exists(filename):
                print("\n[-] The file {} cannot be found or you do not have permission to open the file. Please check the path and try again\n".format(filename))
                exit()
    main()