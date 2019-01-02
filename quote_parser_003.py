#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190102'
__version__ = '0.01'
__description__ = """Retrieves words listed at https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html,
parses, and writes to a file."""

import requests
import re

url = "https://www.phrases.org.uk/meanings/phrases-and-sayings-list.html"
contents = requests.get(url).text

lines = re.findall(r'<p class="phrase-list"><a href=".*?">(.*?)</a></p>', contents)

with open('phrases_and_sayings.txt', 'w') as fh:
    for line in lines:
        print(line.lower())
        fh.write(line.lower() + '\n')

print('[*] File written to phrases_and_sayings.txt!')