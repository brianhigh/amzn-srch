#!/bin/sh

OUT="suggested_reading.md"
HTMLOUT="suggested_reading.html"

echo '# Suggested Reading
Brian High  
06/30/2015
' > $OUT

echo "## Information Systems" >> $OUT
python amznsrch.py 'Computer Hardware' 'Computer Software' >> $OUT
python amznsrch.py 'Systems Analysis' 'Project Management' >> $OUT
python amznsrch.py 'Computer Networking' >> $OUT
python amznsrch.py 'Information Security' 'Computer Security' >> $OUT

echo "## Data Management" >> $OUT
python amznsrch.py 'Data Management' 'Database' 'SQL' >> $OUT
python amznsrch.py 'Data Wrangling' 'Bad Data' >> $OUT
python amznsrch.py 'R Web Scraping' 'Python Web Scraping' >> $OUT

echo "## Programming" >> $OUT
python amznsrch.py 'R Programming' 'RStudio' >> $OUT
python amznsrch.py 'Python Programming' 'IPython' >> $OUT
python amznsrch.py 'Regular Expressions' >> $OUT

echo "## Version Control" >> $OUT
python amznsrch.py 'Version Control' 'GitHub' >> $OUT

echo "## Data Analysis and Visualization" >> $OUT
python amznsrch.py 'Data Analysis' >> $OUT
python amznsrch.py 'R Visualization' 'Python Visualization' >> $OUT

echo "## Bioinformatics" >> $OUT
python amznsrch.py 'R Bioinformatics' 'Python Bioinformatics' >> $OUT
python amznsrch.py 'Computational Biology' >> $OUT

echo "## Buzzwords" >> $OUT
python amznsrch.py 'Big Data' >> $OUT
python amznsrch.py 'Cloud Computing' >> $OUT
python amznsrch.py 'Data Science' 'R Data Science' 'Python Data Science' >> $OUT
python amznsrch.py 'Data Mining' >> $OUT
python amznsrch.py 'R Machine Learning' 'Python Machine Learning' >> $OUT

cat $OUT | pandoc -f markdown -s -o $HTMLOUT 
