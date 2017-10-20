import sys
import re
from pathlib import Path

__author__ = 'Jake Miller'
__date__ = '20171013'
__version__ = '0.01'
__description__ = 'Analyzes a password list to find frequency of password character masks'

if len(sys.argv) != 2:
    print('Usage: mask_finder.py [filename]')
    exit()    

print('The bigger the file, the longer it will take...')    
    
infile = sys.argv[1]
outfile = 'masks_out.txt'

if not Path(infile).is_file():
    print('The file {} could not be found. Please try again'.format(infile))
    exit()

pattern_list = []

with open(infile) as file:
    for word in file:
        mask = ''
        for char in word:
            if char == '\n':
                continue
            elif re.search(r'[A-Z]', char):
                mask += 'u'
            elif re.search(r'[a-z]', char):
                mask += 'l'
            elif re.search(r'[0-9]', char):
                mask += 'd'
            elif re.search(r'\W', char):
                mask += 's' 
        pattern_list.append(mask)
            

pattern_dict = {i:pattern_list.count(i) for i in pattern_list}
sorted_pattern_dict = [(k, pattern_dict[k]) for k in sorted(pattern_dict, key=pattern_dict.get, reverse=True)]

with open(outfile, 'w') as file:
    for k, v in sorted_pattern_dict:
        print(k + " : " + str(v))
        file.write(k + " : " + str(v) + "\n")