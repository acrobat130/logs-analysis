### Installation
- download this repo
- download the supporting db setup files here: https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
- run `psql -d news -f newsdata.sql` to set up the db

### How to run
- after setting up the db, run `python analyze-logs.py` to see the output (see `example-output.txt` for an example)

### What it does
- `analyze-logs.py` runs a series of queries to answer these 3 questions:

  - What are the most popular three articles of all time?
  - Who are the most popular article authors of all time?
  - On which days did more than 1% of requests lead to errors?

 ### Views created
 - none
