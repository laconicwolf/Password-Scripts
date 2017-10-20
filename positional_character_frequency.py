import argparse
import sys
from itertools import zip_longest
from string import printable
from pathlib import Path

__author__ = 'Jake Miller'
__date__ = '20171014'
__version__ = '0.01'
__description__ = 'Analyzes a password list to find frequency of characters per position.'   



#https://stackoverflow.com/questions/43693018/python-position-frequency-dictionary-of-letters-in-words
def freq(code):
    l = len(code) - code.count(None)
    return {n: code.count(n)/l for n in chars}

    
def process_results(results):
    pos = 1
    with open(outfile, 'w') as file:
        for res in results:
            sorted_freq = [(k, res[k]) for k in sorted(res, key=res.get, reverse=True)]
            print("\nCharacter frequency for position {}.".format(str(pos)))
            file.write("Character frequency for position {}.\n".format(str(pos)))
            for k, v in sorted_freq:
                print(k + " : " + str(v))
                file.write(k + " : " + str(v) + "\n")
            file.write('\n')
            pos += 1
        
if __name__ == '__main__':                                
    parser = argparse.ArgumentParser()
    parser.add_argument("-pl", "--passwordlist", help="provide one or more password files seperated by commas. Example: ./script.py -pl list1.txt,list2.txt") 
    parser.add_argument("-o", "--outfile", help="specify the file name to record the results. By default a file freq.txt will be created in the current directory.")
    args = parser.parse_args()
	
    if not args.passwordlist:
        parser.print_help()
        exit()
    
    if ',' in args.passwordlist:
        infile = args.passwordlist.split(',')
    else:
        infile = args.passwordlist
    
    for i in infile:
        if not Path(i).is_file():
            print('The file {} could not be found. Please try again'.format(i))
            exit()
    
    print('The bigger the file, the longer it will take...')    
    if args.outfile:
        outfile = args.outfile
    else:    
        outfile = 'freq.txt'
    chars = printable    
    
    for i in infile:
        word_list = open(i).read().splitlines()
        results = [ freq(code) for code in zip_longest(*word_list) ]
        process_results(results)