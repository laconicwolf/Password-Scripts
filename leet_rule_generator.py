#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf). Inspired by work from Adam Willard (@aswsec)'
__date__ = '20190323'
__version__ = '0.01'
__description__ = """Generates leet word rules"""

import argparse
import itertools

small_leet_dict = {
    'a': ['4', '@'],
    'b': ['8', '6'],
    'c': ['(', '<', '{', 'k'],
    'e': ['3'],
    'g': ['9', '6'],
    'h': ['#'],
    'i': ['l','1','|','!'],
    'l': ['|','1'],
    'o': ['0'],
    'q': ['9'],
    's': ['5','$'],
    't': ['+','7'],
    'x': ['%'],
    'z': ['2']
}

# Uppercase letters omitted due to memory error when 
# creating the combined list of dictionaries.
large_leet_dict = {
    'a': ['a', '4', '@'],
    'b': ['b', '8', '6'],
    'c': ['c', '(', '<', '{'],
    'd': ['d'],
    'e': ['e','3'],
    'f': ['f'],
    'g': ['g', '9', '6'],
    'h': ['h','#'],
    'i': ['i','l','1','|','!'],
    'j': ['j'],
    'k': ['k'],
    'l': ['l','|','1'],
    'm': ['m'],
    'n': ['n'],
    'o': ['o','0'],
    'p': ['p'],
    'q': ['q','9'],
    'r': ['r'],
    's': ['s','5','$'],
    't': ['t','+','7'],
    'u': ['u'],
    'v': ['v'],
    'w': ['w'],
    'x': ['x','%'],
    'z': ['2']
}


def main():
    """Permutates a dictionary to write hashcat rules."""
    if args.size == 'large':
        leet_mappings = large_leet_dict
    else:
        leet_mappings = small_leet_dict
    print('[*] Generating rules...')

    # https://codereview.stackexchange.com/questions/171173/list-all-possible-permutations-from-a-python-dictionary-of-lists
    keys, values = zip(*leet_mappings.items())
    leet_dict_list = [dict(zip(keys, v)) for v in itertools.product(*values)]
    
    all_lines = []
    for leet_dict in leet_dict_list:
        subruleline = []
        for key in leet_dict:
            subruleline.append('s{}{}'.format(key,leet_dict.get(key)))
        all_lines.append(subruleline)

    print('[*] Writing rules...')

    with open(outfilename, 'w') as fh:
        for line in all_lines:
            fh.write('{}\n'.format(' '.join(line)))
            
            if args.title:
                fh.write('l {} c\n'.format(' '.join(line)))

            if args.double and not args.title:
                fh.write('d {}\n'.format(' '.join(line)))

            if args.double and args.title:
                fh.write('d {} c\n'.format(' '.join(line)))
                fh.write('c d {}\n'.format(' '.join(line)))

            if appensions:
                for item in appensions:
                    fh.write('{}${}\n'.format(' '.join(line), '$'.join(list(item))))

                    if args.title:
                        fh.write('l {} ${} c\n'.format(' '.join(line), '$'.join(list(item))))

                    if args.double and not args.title:
                        fh.write('{} ${} d\n'.format(' '.join(line), '$'.join(list(item))))

                    if args.double and args.title:
                        fh.write('l d {} ${} c\n'.format(' '.join(line), '$'.join(list(item))))
                        fh.write('l c d {} ${}\n'.format(' '.join(line), '$'.join(list(item))))

            if prepensions:
                for item in prepensions:
                    fh.write('^{}{}\n'.format('^'.join(list(item)[::-1]), ' '.join(line)))

                    if args.title:
                        fh.write('l ^{} {} c\n'.format('^'.join(list(item)[::-1]), ' '.join(line)))

                    if args.double and not args.title:
                        fh.write('^{} {} d\n'.format('^'.join(list(item)[::-1]), ' '.join(line)))

                    if args.double and args.title:
                        fh.write('l d ^{} {} c\n'.format('^'.join(list(item)[::-1]), ' '.join(line)))
                        fh.write('l c d ^{} {}\n'.format('^'.join(list(item)[::-1]), ' '.join(line)))

    print('[+] Complete! Rules written to {}'.format(outfilename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outfile",
                        help="Output file name")
    parser.add_argument("-s", "--size",
                        nargs='?',
                        choices=["small", "large"],
                        const="small",
                        default="small",
                        help="'small' uses a dictionary of only leet mappings. 'large' uses the lowercase character, and the leet mappings, which results in a MUCH larger rule file. ")
    parser.add_argument("-d", "--double",
                        action="store_true",
                        help="Double word and leet")
    parser.add_argument("-t", "--title",
                        action="store_true",
                        help="title case word")
    parser.add_argument("-a", "--append",
                        nargs="*",
                        help="Specify characters or words to add to end of the word, separated by spaces. (-a ! !! !!! !@#$")
    parser.add_argument("-p", "--prepend",
                        nargs="*",
                        help="Specify characters or words to add to the beginning of the word, separated by spaces. (-p ! !! !!! !@#$")
    args = parser.parse_args()
    
    appensions = args.append if args.append else None
    prepensions = args.prepend if args.prepend else None
    outfilename = args.outfile if args.outfile else "5UP3R_1337.rule"
        
    main()
