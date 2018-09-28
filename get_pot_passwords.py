#!/usr/bin/env python3


__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20180921'
__version__ = '0.01'
__description__ = """Extracts the plain passwords from a hashcat or jtr pot file."""


import argparse


def decode_hashcat_hexstring(hexstring):
    """Parses a hex encoded password string ($HEX[476f6f646669676874343a37])
    and returns the decodes the hex.
    """
    index_1 = hexstring.index("[")+1
    index_2 = len(hexstring)-1
    hexdata = hexstring[index_1:index_2]
    return bytes.fromhex(hexdata).decode()


def decode_hashcat_hex(data):
    """Calls the decoded_hashcat_hexstring on an encoded hex represented password
    ($HEX[476f6f646669676874343a37]). Occasionally the string will be encoded
    multiple times, so a loop is used until the $HEX prefix no longer remains.
    Returns the decodes the hexstring.
    """
    while data.startswith('$HEX['):
        data = decode_hashcat_hexstring(data)
    return data


def main():

    # Reads in the potfile
    with open(potfile) as fh:
        lines = fh.read().splitlines()
    try:
        # Both JTR and Hashcat potfiles are colon delimited. In JTR pot files, 
        # a colon in the password will mess up the split, so it must be split
        # from the first colon until the end of line.
        pt_passwords = [line.split(':')[1:] for line in lines]
        fixed_passwords = []
        for line in pt_passwords:
            if len(line) > 1:
                fixed_passwords.append(':'.join(line))
            else:
                fixed_passwords.append(''.join(line))
    except IndexError as e:
        print('Error detected:')
        print(e)
    passwords = []
    for password in fixed_passwords:

        # Hashcat will encode passwords containing colons or non-ascii characters.
        # This will decode those passwords if they are there.
        if password.startswith('$HEX['):
            passwords.append(decode_hashcat_hex(password))
        else:
            passwords.append(password)

    # Output to file or print to terminal
    if args.outfile:
        with open(args.outfile, 'w') as fh:
            for password in passwords:
                fh.write(password + '\n')
    else:
        for password in passwords:
            print(password)


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
