#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180921'
__version__ = '0.01'
__description__ = """Reads a plain text file and hashes each line. The hashes are written 
to a new file. The purpose of this tool is to generate sample hashes for testing password
cracking."""


import hashlib
import sys

def md5(string):
    """Returns a md5 hash of the supplied parameter"""
    return hashlib.md5(string.encode()).hexdigest()

def main():
    hashes = [md5(word) for word in words]
    with open(outfile, 'w', encoding="utf8", errors='ignore') as fh:
        for hash in hashes:
            print(hash)
            fh.write(hash + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("\n[*] Usage: python3 {} <plaintext_word_infile> <outfile_to_write_hashes>\n".format(sys.argv[0]))
        exit()
    filename = sys.argv[1]
    outfile = sys.argv[2]
    with open(filename, encoding="utf8", errors='ignore') as fh:
        words = fh.read().splitlines()
    main()