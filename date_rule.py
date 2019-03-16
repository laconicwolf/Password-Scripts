#!/usr/bin/env python3

__author__ = 'Jake Miller (@LaconicWolf)'
__date__ = '20190316'
__version__ = '0.01'
__description__ = """Creates a rule file that will append digits that may 
map to dates in popular formats that may be appended to files."""

import pandas as pd
import numpy as np

def create_2_digit_year():
    """Returns a list of strings from 00-99."""
    string_year_range = []
    for i in range(0, 100):
        i = str(i)
        if len(i) < 2:
            i = '0' + i
        string_year_range.append(i)
    return string_year_range

def create_month_day():
    """Returns a list of from 0101-1231."""
    month_day_list = []
    times = pd.date_range('01-01-2020', '12-31-2021')
    for time in times:
        month_day_list.append(''.join(str(time).split(' ')[0].split('-')[1:]))
    return month_day_list

def create_month_day_2_dig_year():
    """Returns a list of from 010100-123199."""
    month_day_year = []
    times = pd.date_range('01-01-2000', '12-31-2099')
    for time in times:
        year = str(time).split('-')[0][-2:]
        month_day = ''.join(str(time).split(' ')[0].split('-')[1:])
        month_day_year.append(month_day + year)
    return month_day_year

def create_month_day_4_dig_year():
    """Returns a list of from 01011900-12312099."""
    month_day_year = []
    times = pd.date_range('01-01-1900', '12-31-2099')
    for time in times:
        year = ''.join(str(time).split('-')[0])
        month_day = ''.join(str(time).split(' ')[0].split('-')[1:])
        month_day_year.append(month_day + year)
    return month_day_year

def create_2_dig_year_month_day():
    """Returns a list of from 000101-991231."""
    year_month_day = []
    times = pd.date_range('01-01-2000', '12-31-2099')
    for time in times:
        year = str(time).split('-')[0][-2:]
        month_day = ''.join(str(time).split(' ')[0].split('-')[1:])
        year_month_day.append(year + month_day)
    return year_month_day

def create_4_dig_year_month_day():
    """Returns a list of from 19000101-20991231."""
    year_month_day = []
    times = pd.date_range('01-01-1970', '12-31-2099')
    for time in times:
        year_month_day.append(str(time).split(' ')[0].replace('-', ''))
    return year_month_day

def main():
    # 00-99
    two_dig_year = create_2_digit_year()

    # 0101-1231
    month_day = create_month_day()

    # 010100-123199
    month_day_2_dig_year = create_month_day_2_dig_year()

    # 01011900-12312099
    month_day_4_dig_year = create_month_day_4_dig_year()

    # 000101-991231
    two_dig_year_month_day = create_2_dig_year_month_day()

    # 19000101-20991231
    four_dig_year_month_day = create_4_dig_year_month_day()

    all_dates = two_dig_year + month_day + month_day_2_dig_year + month_day_4_dig_year + two_dig_year_month_day + four_dig_year_month_day
    
    special_chars = ['!', '!!', '!!!', '@', '@@', '@@@', '#', '##', '###',
                     '$', '$$', '$$$' '!@', '!@#', '!@#$']

    # Write to rule file
    with open('dates_rule.rule', 'w') as fh:
        for date in all_dates:
        	# Dates only
            fh.write('${}\n'.format('$'.join(list(date))))

            # Capitalizes first letter then dates
            fh.write('c${}\n'.format('$'.join(list(date))))

            # Capitalizes first letter, doubles, then dates
            fh.write('cd${}\n'.format('$'.join(list(date))))

            # Doubles, dates, then capitalizes first letter
            fh.write('d${}c\n'.format('$'.join(list(date))))

            for item in special_chars:
            	# Writes dates with special chars
                fh.write('${}${}\n'.format('$'.join(list(date)), '$'.join(list(item))))

                # Writes dates with special chars
                fh.write('c${}${}\n'.format('$'.join(list(date)), '$'.join(list(item))))

                # Capitalizes first letter, doubles, then dates with specials
                fh.write('cd${}${}\n'.format('$'.join(list(date)), '$'.join(list(item))))

                # Doubles, dates and specials, then capitalizes first letter
                fh.write('d${}${}c\n'.format('$'.join(list(date)), '$'.join(list(item))))



if __name__ == '__main__':
    main()
