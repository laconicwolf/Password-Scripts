#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20181227'
__version__ = '0.01'
__description__ = """Retrieves all idioms listed at https://www.theidioms.com
and writes to a file"""

import re
import requests

idioms = []
for num in range(1, 132):
    url = "https://www.theidioms.com/list/page/{}".format(num)
    contents = requests.get(url).text
    idioms += re.findall(
        r'<dt><a href="https://www.theidioms.com/.*?/">(.*?)</a></dt><dd>',
        contents
        )

with open('idioms.txt', 'w') as fh:
    for idiom in idioms:
        if '&#8217;' in idiom:
            idiom = idiom.replace('&#8217;', "'")
        print(idiom.lower())
        fh.write(idiom.lower() + '\n')

print('[*] File written to idioms.txt!')