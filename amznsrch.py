#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Search Amazon books and return results as a Markdown list.
"""

vers_date = '2015-06-30'
copyright = 'Copyright (c) 2015 Brian High'
license = 'MIT'
repos_url = 'https://github.com/brianhigh/amazon-search'

"""
Searches Amazon API by subject to produce a list of matching books in
Markdown's bullet-list format, with links to each book's Amazon page,
and also links to title searches at other sources (e.g. Google Books).

See code help messages for script usage and required API key file format.
Or, simply run script as: python amznsrch.py -h

Usage Examples:

  python amznsrch.py "Data Mining"
  python amznsrch.py -n 3 "Data Mining" > mining.md
  python amznsrch.py -l 0 "R Programming" "Python Programming" > programming.md
  python amznsrch.py "Data Mining" | pandoc -f markdown -s -o > mining.html

Install dependencies (as an "administrator" if necessary):
  easy_install pip
  pip install requests
  pip install BeautifulSoup4
  pip install amazon_scraper
  pip install python-amazon-simple-product-api
  pip install xmltodict

References:
  https://pypi.python.org/pypi/amazon_scraper/0.1.2
  https://pypi.python.org/pypi/python-amazon-simple-product-api/
  https://affiliate-program.amazon.com/gp/advertising/api/detail/main.html
"""

keyhelp = """
The Amazon API key file must contain exactly three lines in this order:
   your access key (20 alphanumeric characters)
   your secret key (40 alphanumeric+slash+plus characters)
   your associate tag (12 digits with dashes: ####-####-####)

Example:
   GNS9FJNB89S78DGSDG9B
   A8g78sh+G68nS/9VBsJfqR+z1tdy39sMW/oH5yr4
   7910-6883-4207
"""

import argparse
import os
import sys
import re
import textwrap
from amazon_scraper import AmazonScraper
import itertools
import urllib

def get_api_config(apikeyfile):
    """Check configuration file and return contents"""
    
    # Define regular expressions for data validation of API config parameters
    access_key_re = '^[A-Za-z0-9]{20}$'
    secret_key_re = '^[A-Za-z0-9/+]{40}$'
    associate_tag_re = '^\d{4}-\d{4}-\d{4}$'
    
    # Check validity of API key file before returning contents as a list
    if os.path.isfile(apikeyfile) and os.access(apikeyfile, os.R_OK):
        try:
            with open(apikeyfile) as filehandle:
                # Read API key file into list and check for valid data
                apikey = [str(line.strip()) for line in filehandle]
                if len(apikey) != 3:
                    raise ValueError
                if (not re.match(access_key_re, apikey[0])):
                    raise ValueError
                if (not re.match(secret_key_re, apikey[1])):
                    raise ValueError
                if (not re.match(associate_tag_re, apikey[2])):
                    raise ValueError
        except ValueError:
            print(keyhelp)
            sys.exit(1)
        return apikey
    else:
        print("Can't find or read Amazon API key file named: " + apikeyfile)
        sys.exit(1)
    
def main(num_items, heading_level, args):
    """Main routine"""
        
    # Retrieve the contents of the API key file
    apikey = get_api_config('.amznrc')
        
    # Create AmazonScraper object using API key
    amznscpr = AmazonScraper(*apikey)
    
    # Check keyword list entered on the command line
    if len(args) < 1:
        print('Missing search terms. For usage help: python amznsrch.py -h')
        sys.exit(1)
    
    # Loop through quoted lists of search terms from command line arguments
    for arg in args:
    
        # Print search terms as a markdown heading
        srch_terms = str(arg)
        if heading_level > 0 and heading_level < 7:
            print '\n' + '#' * heading_level + ' ' + srch_terms + '\n'
        
        # Fetch and return results
        for item in itertools.islice(amznscpr.search(
            Keywords = srch_terms, SearchIndex='Books'), num_items):
            
            # Skip if no title, else encode, remove parenthetical text, & quote
            if not item.title:
                continue
            else:
                bktitle = item.title.encode('utf8')
                bktitle = re.sub('\s*[(\[].*[)\]]', '', bktitle)
                bktitlesrch = urllib.quote_plus('"' + bktitle + '"')
            
            # Encode author, if present, and format for printing
            if not item.author:
                bkauthor = ''
            else:
                bkauthor = 'by ' + item.author.encode('utf8')
            
            # Add associate tag to item URL
            bkurl = str(item.url) + '/?tag=' + apikey[2]
            
            # Construct links as desired
            amzn = '[AMZN](' + bkurl + ')'
            goog = ('[GOOG]' + '(https://www.google.com/' + 
                    'search?tbo=p&tbm=bks&q=intitle:' + 
                    bktitlesrch + '&num=10&gws_rd=ssl)')
            spl = ('[SPL](https://seattle.bibliocommons.com/search?' + 
                   't=title&search_category=title&q=' + bktitlesrch + 
                   '&commit=Search)')
            uwl = ('[UW](http://uwashington.worldcat.org' + 
                   '/search?q=ti%3A' + bktitlesrch + '&qt=advanced)')
            
            # Print markdown for title, author, and links as bulleted list item
            print('- _' + bktitle + '_ ' + bkauthor + 
                 ' ( ' + goog + ' | ' + amzn + ' | ' + spl + ' | ' + uwl + ' )')

def get_parser():
    """Parse command line arguments"""
    
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    parser = ArgumentParser(description=__doc__,
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-n', '--num-items',
        dest = 'num_items',
        type=int, 
        default = 5,
        help="Number of items to return, default: 5" )
    
    parser.add_argument('-l', '--heading-level', 
        dest = 'heading_level',
        type=int, 
        default = 3,
        help="Markdown heading level, default: 3, no heading: 0" )
        
    parser.add_argument('-v', '--version', 
        action='version', 
        version='%(prog)s ' + vers_date + ' ' + repos_url)
    
    parser.add_argument('args', 
        help="Quoted list(s) of search terms, space-delimited", 
        nargs=argparse.REMAINDER)
        
    return parser
    
if __name__ == "__main__":
    """Get command-line arguments and hand them off to main()"""
    args = get_parser().parse_args()
    main(args.num_items, args.heading_level, args.args)
