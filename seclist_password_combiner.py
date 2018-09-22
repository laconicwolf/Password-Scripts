#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180921'
__version__ = '0.01'
__description__ = """Combines, sorts, and uniques the passwords contained in files located at 
https://github.com/danielmiessler/SecLists."""


import argparse
import os


def main():
    combined = []
    for root, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            if filepath.endswith('.txt') or filepath.endswith('.csv'):
                print("[*] Processing file: {}".format(filepath))
                with open(filepath, encoding="utf8", errors='ignore') as fh:
                    contents = fh.read().splitlines()

                    # This dir includes files containing username and password combos
                    # delimited usually by a colon, but some are csv files.
                    if os.sep + "Default-Credentials" in filepath:
                        if filepath.endswith('csv'):

                            # Annoying to parse so I'm not doing it.
                            if 'scada-pass.csv' in filepath:
                                pass
                            # This one is easier to parse.
                            if 'default-passwords.csv' in filepath:
                                passwords = [line.split(',')[2] for line in contents if line.split(',')[2] != "<BLANK>"]
                        else:
                            try:
                                passwords = [line.split(':')[1] for line in contents]
                            except IndexError:
                                passwords = contents
                        combined += passwords
                    else:
                        combined += contents
    print("[*] Sorting list and removing duplicates words...")
    combined.sort()
    unique_combined = list(set(combined))
    
    if args.outfile:
        print("[*] Writing to {}...".format(args.outfile))
        with open(args.outfile, 'w', encoding="utf8", errors='ignore') as fh:
            for word in unique_combined:
                fh.write(word + '\n')
    else:
        for word in unique_combined:
            print(word)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", 
                        nargs='?', 
                        const='.', 
                        help="Specify the directory. You'll want to run this in the Passwords folder.")
    parser.add_argument("-o", "--outfile",
                        help="Writes the output to a specified file.")
    args = parser.parse_args()

    if args.directory:
        root_dir = args.directory
    else:
        root_dir = '.'
    main()