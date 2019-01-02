#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190102'
__version__ = '0.01'
__description__ = """Retrieves words listed at https://raw.githubusercontent.com/alvations/Quotables/master/author-quote.txt,
parses, and writes to three files."""

import requests

url = "https://raw.githubusercontent.com/alvations/Quotables/master/author-quote.txt"
contents = requests.get(url).text

lines = [l.split('\t')[1] for l in contents]

with open('short_quotes.txt', 'w') as fh:
    s_lines = [l for l in lines if len(l) < 33]
    for line in s_lines:
        print(line.lower())
        fh.write(line.lower() + '\n')

print('[*] File written to short_quotes.txt!')

with open('medium_quotes.txt', 'w') as fh:
    m_lines = [l for l in lines if len(l) > 32 and len(l) < 128]
    for line in m_lines:
        print(line.lower())
        fh.write(line.lower() + '\n')

print('[*] File written to medium_quotes.txt!')

with open('long_quotes.txt', 'w') as fh:
    l_lines = [l for l in lines if len(l) < 127]
    for line in l_lines:
        print(line.lower())
        fh.write(line.lower() + '\n')

print('[*] File written to long_quotes.txt!')