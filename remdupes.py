#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
remdupes.py: Reads lines from stdin and prints non-duplicated lines to stdout
"""

vers_date = '2015-05-13'
copyright = 'Copyright (c) 2015 Brian High'
license = 'MIT'
repos_url = 'https://github.com/brianhigh/amazon-search'

import sys

seen = set()
for line in sys.stdin:
    line = str(line.rstrip('\n'))
    if line not in seen:
        print line
        if line != '':
            # Only track non-blank lines
            seen.add(line)
