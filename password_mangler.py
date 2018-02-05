#!/usr/bin/env python3

import argparse

__author__ = 'Jake Miller'
__date__ = '20171013'
__version__ = '0.01'
__description__ = 'Mangles a wordlist in various ways specified by the user.'

def make_leet(words):
    """Runs each word through a leet translate function.
    
    Args:
        words: A list object containing words to be transformed.
        
    Returns:
        A list object containing the transformed words.
    """
    intab  = "oilest" 
    outtab = "011357"
    trantab = str.maketrans(intab, outtab)
    leet_list = []
    for word in words:
        leet_list.append(word.lower().translate(trantab))
        leet_list.append(word.title().translate(trantab))
    return leet_list
        
  
def half_leet(words):
    """Runs each word through a minimal leet translate function
    """
    #TODO
    pass

def add_suffix(words, suff):
    """Adds a user specified suffix to each word
    Args:
        words: A list object containing words to be appended to.
        suff: A suffix to append to the word.
    Returns:
        A list object containing the suffix-appended words.
    """
    suffix_list = []
    for word in words:
        suffix_list.append(word + suff)   
    return suffix_list
        
def add_prefix(words, pref):
    """Adds a user specified prefix to each word
    Args:
        words: A list object containing words to be prepended to.
        pref: A prefix to prepend to the word.
    Returns:
        A list object containing the prefix-prepended words.
    """
    prefix_list = []
    for word in words:
        prefix_list.append(pref + word)   
    return prefix_list
    
def duplicate(words):
    """Duplicates each word.
    
    Args:
        words: A list object containing words to be duplicated.
        
    Returns:
        A list object containing the duplicated words.
    """
    double_list = []
    for word in words:
        double_list.append(word + word)   
    return double_list
    pass
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-d", "--duplicate", help="duplicates each word", action="store_true")
    parser.add_argument("-wl", "--word_list", help="specify word list to mangle")
    parser.add_argument("-l", "--leet", help="produces multiple leet variations of provided words", action='store_true')
    parser.add_argument("-s", "--suffix", help="add a suffix to a word")
    parser.add_argument("-p", "--prefix", help="add a prefix to a word")

    args = parser.parse_args()

    if not args.word_list:
        print('Please specify a word list to be mangled.\n')
        parser.print_help()
        exit()
    if args.verbose:
        print("Verbosity turned on")
    
    word_list = open(args.word_list).read().splitlines()
    outfile = args.word_list + '_mangled.txt'
    mangled_list = []
    all_words = []
    
    for word in word_list:
        mangled_list.append(word)
        mangled_list.append(word.title())
        all_words.append(word)
        all_words.append(word.title())
        
    if args.duplicate:
        mangled_list += duplicate(all_words)
        all_words += duplicate(all_words)
    
    if args.leet:
        mangled_list += make_leet(all_words)
        all_words += make_leet(all_words)
        
    if args.suffix:
        suffix = args.suffix
        mangled_list += add_suffix(all_words, suffix)
        all_words += add_suffix(all_words, suffix)
        
    if args.suffix:
        prefix = args.prefix
        mangled_list += add_prefix(all_words, prefix)
        all_words += add_prefix(all_words, prefix)
    
    for word in sorted(set(mangled_list)):
        if args.verbose:
            print(word)
        with open("mangled_" + args.word_list, "a") as outfile:
            outfile.write(word + "\n")
            
    print('\nCompleted creating a wordlist of {} words from an initial {} words.'.format(len(set(mangled_list)), len(word_list)))