#!/usr/bin/env python

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190316'
__version__ = '0.01'
__description__ = """Creates a rule file that will append digits that may 
map to dates in popular formats that may be appended to files."""

import argparse
import time
try:
	import pandas as pd
	import numpy as np
except ImportError:
	print("This script requires Pandas and Numpy. Try 'pip install pandas', or 'python -m pip install pandas', or do an Internet search for installation instructions.")
	exit()

def create_2_digit_year():
    """Returns a list of strings from 00-99."""
    string_year_range = []
    for i in range(0, 100):
        i = str(i)
        if len(i) < 2:
            i = '0' + i
        string_year_range.append(i)
    return string_year_range

def create_month_day(start_year, end_year):
    """Returns a list of from 0101-1231."""
    month_day_list = []
    times = pd.date_range('01-01-{}'.format(start_year), '12-31-{}'.format(end_year))
    for time in times:
        month_day_list.append(''.join(str(time).split(' ')[0].split('-')[1:]))
    return list(set(month_day_list))

def create_month_day_2_dig_year(start_year, end_year):
    """Returns a list of from 010100-123199."""
    month_day_year = []
    times = pd.date_range('01-01-{}'.format(start_year), '12-31-{}'.format(end_year))
    for time in times:
        year = str(time).split('-')[0][-2:]
        month_day = ''.join(str(time).split(' ')[0].split('-')[1:])
        month_day_year.append(month_day + year)
    return list(set(month_day_year))

def create_month_day_4_dig_year(start_year, end_year):
    """Returns a list of from 01011900-12312099."""
    month_day_year = []
    times = pd.date_range('01-01-{}'.format(start_year), '12-31-{}'.format(end_year))
    for time in times:
        year = ''.join(str(time).split('-')[0])
        month_day = ''.join(str(time).split(' ')[0].split('-')[1:])
        month_day_year.append(month_day + year)
    return list(set(month_day_year))

def create_2_dig_year_month_day(start_year, end_year):
    """Returns a list of from 000101-991231."""
    year_month_day = []
    times = pd.date_range('01-01-2000', '12-31-2099')
    for time in times:
        year = str(time).split('-')[0][-2:]
        month_day = ''.join(str(time).split(' ')[0].split('-')[1:])
        year_month_day.append(year + month_day)
    return list(set(year_month_day))

def create_4_dig_year_month_day(start_year, end_year):
    """Returns a list of from 19000101-20991231."""
    year_month_day = []
    times = pd.date_range('01-01-{}'.format(start_year), '12-31-{}'.format(end_year))
    for time in times:
        year_month_day.append(str(time).split(' ')[0].replace('-', ''))
    return list(set(year_month_day))

def main():
    print("[*] Generating dates...")

    # 00-99
    two_dig_year = create_2_digit_year()

    # 0101-1231
    month_day = create_month_day(start_year, end_year)

    # 010100-123199
    month_day_2_dig_year = create_month_day_2_dig_year(start_year, end_year)

    # 01011900-12312099
    month_day_4_dig_year = create_month_day_4_dig_year(start_year, end_year)

    # 000101-991231
    two_dig_year_month_day = create_2_dig_year_month_day(start_year, end_year)

    # 19000101-20991231
    four_dig_year_month_day = create_4_dig_year_month_day(start_year, end_year)

    all_dates = two_dig_year + month_day + month_day_2_dig_year + month_day_4_dig_year + two_dig_year_month_day + four_dig_year_month_day

    # Write to rule file
    print("[*] Writing rules...")
    with open(filename, 'w') as fh:
        for date in all_dates:
        	# Dates only
            fh.write('${}\n'.format('$'.join(list(date))))

            if args.title:
            	# Capitalizes first letter then dates
                fh.write('c${}\n'.format('$'.join(list(date))))

            if args.title and args.double:
            	# Capitalizes first letter, doubles, then dates
                fh.write('cd${}\n'.format('$'.join(list(date))))

            	# Doubles, dates, then capitalizes first letter
                fh.write('d${}c\n'.format('$'.join(list(date))))

            if not special_chars: continue
            for item in special_chars:
                # Writes dates with special chars
                fh.write('${}${}\n'.format('$'.join(list(date)), '$'.join(list(item))))

                if args.title:
                    # Capitalizes, dates, and writes with special chars
                    fh.write('c${}${}\n'.format('$'.join(list(date)), '$'.join(list(item))))

                if args.double:
                    # Capitalizes first letter, doubles, then dates with specials
                    fh.write('cd${}${}\n'.format('$'.join(list(date)), '$'.join(list(item))))

                if args.title and args.double:
                    # Capitalizes first letter, then doubles, dates and specials
                    fh.write('cd${}${}\n'.format('$'.join(list(date)), '$'.join(list(item))))

                    # Doubles, dates and specials, then capitalizes first letter
                    fh.write('d${}${}c\n'.format('$'.join(list(date)), '$'.join(list(item))))

    print("[+] Complete! Rule file written to {}".format(filename))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--double",
                        help="Double word before appending date",
                        action="store_true")
    parser.add_argument("-t", "--title",
                        help="title case word",
                        action="store_true")
    parser.add_argument("-a", "--append_chars",
                        nargs="*",
                        help="Specify characters to add to end of dates, separated by spaces. (-a ! !! !!! !@#$")
    parser.add_argument("-s", "--start_year",
                        help="Specify 4 digit year as a starting date range. Default is 1970.")
    parser.add_argument("-e", "--end_year",
                        help="Specify 4 digit year as a starting date range. Default is current year + 1.")
    parser.add_argument("-o", "--filename",
                        help="Specify a filename to write to. Default is date_rule.rule")
    args = parser.parse_args()
    if args.start_year:
    	if not args.start_year.isdigit() or len(args.start_year) != 4:
    		print('[-] Start year must be a 4 digit year (-s 2005). Default is 1970')
    		exit()
    start_year = args.start_year if args.start_year else '1970'
    if args.end_year:
    	if not args.end_year.isdigit() or len(args.end_year) != 4:
    		print('[-] End year must be a 4 digit year (-e 2019). Default is current year + 1')
    		exit()
    end_year = args.end_year if args.end_year else str(time.localtime().tm_year + 1)
    special_chars = args.append_chars if args.append_chars else None
    filename = args.filename if args.filename else 'date_rule.rule'

    main()
