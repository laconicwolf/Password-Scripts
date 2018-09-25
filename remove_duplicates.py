#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180921'
__version__ = '0.01'
__description__ = """Reads a file, removes duplicate lines, and writes to a new file."""


import argparse


def main():
    print('[*] Reading file: {}'.format(filename))
    with open(filename, encoding="utf8", errors='ignore') as fh:
        lines = fh.read().splitlines()
    print("[*] Processing {} words.".format(len(lines)))
    print('[*] Removing duplicate words...')
    unique_lines = list(set(lines))
    if args.outfile:
        print('[*] Writing to file: {}'.format(args.outfile))
        with open(args.outfile, 'w', encoding="utf8", errors='ignore') as fh:
            for line in unique_lines:
                fh.write(line + '\n')
    else:
        for line in unique_lines:
            print(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename')
    parser.add_argument('-o', '--outfile')
    args = parser.parse_args() 
    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify the filename of the wordlist.\n")
        exit()
    else:
        filename = args.filename
    main()