#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180921'
__version__ = '0.01'
__description__ = """Extracts the plain passwords from a hashcat or jtr pot file."""


import argparse


def main():
    with open(potfile) as fh:
        lines = fh.read().splitlines()
    try:
        pt_passwords = [line.split(':')[1:] for line in lines]
        fixed_passwords = []
        for line in pt_passwords:
            if len(line) > 1:
                fixed_passwords.append(':'.join(line))
            else:
                fixed_passwords.append(''.join(line))
    except IndexError as e:
        print('Error detected! Check the line where the error occurred?')
        print(e)
    for password in fixed_passwords:
        print(password)
    if args.outfile:
        with open(args.outfile, 'w') as fh:
            for password in fixed_passwords:
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