#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180921'
__version__ = '0.01'
__description__ = """Extracts the plain passwords from a hashcat pot file."""


import argparse


def main():
    with open(potfile) as fh:
        lines = fh.read().splitlines()
    try:
        pt_passwords = [line.split(':')[1] for line in lines]
    except IndexError as e:
        print('Error detected! Are you sure this is a hashcat pot file?')
        print(e)
    for password in pt_passwords:
        print(password)
    if args.outfile:
        with open(args.outfile, 'w') as fh:
            for password in pt_passwords:
                fh.write(password + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename')
    parser.add_argument('-o', '--outfile')
    args = parser.parse_args() 
    if not args.filename:
        parser.print_help()
        print("\n[-] Please specify the filename of the potfile\n")
        exit()
    else:
        potfile = args.filename
    main()