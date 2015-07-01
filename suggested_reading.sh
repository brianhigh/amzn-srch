#!/bin/bash

OUT="suggested_reading.md"
HTMLOUT="suggested_reading.html"

echo '# Suggested Reading
Brian High  
07/01/2015
' > $OUT

echo -e "This list was automatically generated from the Amazon API. It includes
the top-5 search results for each search term, based on customer reviews.
Duplicates have been removed. An Internet search will reveal additional 
resources, often freely available and of high quailty.\n" >> $OUT

echo -e "## Information Systems\n" >> $OUT
python amznsrch.py 'Computer Hardware' 'Computer Software' >> $OUT
python amznsrch.py 'Systems Analysis' 'Project Management' >> $OUT
python amznsrch.py 'Computer Networking' >> $OUT
python amznsrch.py 'Information Security' 'Computer Security' >> $OUT

echo -e "## Data Management\n" >> $OUT
python amznsrch.py 'Data Management' 'Database' 'SQL' >> $OUT
python amznsrch.py 'Data Wrangling' 'Bad Data' >> $OUT
python amznsrch.py 'R Web Scraping' 'Python Web Scraping' >> $OUT

echo -e "## Programming\n" >> $OUT
python amznsrch.py 'R Programming' 'RStudio' >> $OUT
python amznsrch.py 'Python Programming' 'IPython' >> $OUT
python amznsrch.py 'Regular Expressions' >> $OUT

echo -e "## Version Control\n" >> $OUT
python amznsrch.py 'Version Control' 'GitHub' >> $OUT

echo -e "## Data Analysis and Visualization\n" >> $OUT
python amznsrch.py 'Data Analysis' >> $OUT
python amznsrch.py 'R Visualization' 'Python Visualization' >> $OUT

echo -e "## Bioinformatics\n" >> $OUT
python amznsrch.py 'R Bioinformatics' 'Python Bioinformatics' >> $OUT
python amznsrch.py 'Computational Biology' >> $OUT

echo -e "## Buzzwords\n" >> $OUT
python amznsrch.py 'Big Data' >> $OUT
python amznsrch.py 'Cloud Computing' >> $OUT
python amznsrch.py 'Data Science' 'R Data Science' 'Python Data Science' >> $OUT
python amznsrch.py 'Data Mining' >> $OUT
python amznsrch.py 'R Machine Learning' 'Python Machine Learning' >> $OUT

cat $OUT | ./remdupes.py | pandoc -f markdown -s -o $HTMLOUT 
