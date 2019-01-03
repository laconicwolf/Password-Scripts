#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190102'
__version__ = '0.01'
__description__ = """Retrieves data listed at https://gist.githubusercontent.com/signed0/d70780518341e1396e11/raw/2a7f4af8d181a714f9d49105ed57fafb3f450960/quotes.json,
parses, and writes to a file."""

import requests
import ast

url = "https://gist.githubusercontent.com/signed0/d70780518341e1396e11/raw/2a7f4af8d181a714f9d49105ed57fafb3f450960/quotes.json"
contents = requests.get(url).text.split('\n')

lines = []
for line in contents:
    try:
        line = ast.literal_eval(line)
    except SyntaxError:
        input(line)
        continue
    lines.append(line[0])

with open('short_quotes.txt', 'a') as fh:
    s_lines = [l for l in lines if len(l) < 33]
    for line in s_lines:
        print(line.lower())
        fh.write(line.lower() + '\n')

print('[*] File written to short_quotes.txt!')

with open('medium_quotes.txt', 'a') as fh:
    m_lines = [l for l in lines if len(l) > 32 and len(l) < 128]
    for line in m_lines:
        print(line.lower())
        fh.write(line.lower() + '\n')

print('[*] File written to medium_quotes.txt!')

with open('long_quotes.txt', 'a') as fh:
    l_lines = [l for l in lines if len(l) < 127]
    for line in l_lines:
        print(line.lower())
        fh.write(line.lower() + '\n')

print('[*] File written to long_quotes.txt!')