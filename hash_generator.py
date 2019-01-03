#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190102'
__version__ = '0.01'
__description__ = """Reads a plain text file and hashes each line. The hashes are written 
to a new file. The purpose of this tool is to generate sample hashes for testing password
cracking."""


import hashlib
import argparse
import os

def md5_hash(string_value):
    """Returns a md5 hash of the supplied string."""
    return hashlib.md5(string_value.encode()).hexdigest()

def ntlm_hash(string_value):
    """Returns an ntlm hash of the supplied string."""
    return hashlib.new('md4', string_value.encode('utf-16le')).hexdigest()

def main():
    with open(filename, encoding="utf8", errors='ignore') as fh:
        words = fh.read().splitlines()
    if algo == 'md5':
        hashes = [md5_hash(word) for word in words]
    elif algo == 'ntlm':
        hashes = [ntlm_hash(word) for word in words]
    else:
        hashes = ''
    with open(outfile, 'w', encoding="utf8", errors='ignore') as fh:
        for digest in hashes:
            print(digest)
            fh.write(digest + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename",
                        help="Specify a file containing words.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a specified file.")
    parser.add_argument("-a", "--algorithm",
                        choices=('md5', 'ntlm'),
                        help="Selects an algorithm to generate hashes.")
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
    if not args.algorithm:
        parser.print_help()
        print("\n[-] Please specify an algorithm (-a ntlm).\n")
        exit()
    else:
        algo = args.algorithm
    if args.outfile:
        outfile = args.outfile
    else:
        outfile = 'hashed_values.txt'
    main()