#!/usr/bin/env python

import psycopg2
from datetime import datetime

DBNAME = "news"

print("hello")

# answers 3 questions based on data in the "news" database,
# found here:
# https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
#
# questions
#
# 1. What are the most popular three articles of all time?
#
#    Which articles have been accessed the most?
#    Present this information as a sorted list
#    with the most popular article at the top.
#    Example: "Princess Shellfish Marries Prince Handsome" - 1201 views


def get_most_popular_articles():
    print("\nThe three most popular articles of all time are...")
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
            SELECT a.title, count(*) as num
                FROM articles a
                JOIN log l on l.path like '%/article/' || a.slug || '%'
                WHERE l.path like '%/article/%'
                AND l.status like '2%'
                GROUP BY a.title
                ORDER BY num desc
                LIMIT 3
        """)
    articles = c.fetchall()
    db.close()
    for article in articles:
        title = article[0]
        count = article[1]
        print("\"{}\" - {} views".format(title, count))


# 2. Who are the most popular article authors of all time?
#
#    When you sum up all of the articles each author has written,
#    which authors get the most page views?
#    Present this as a sorted list with the most popular author at the top.
#    Example: Ursula La Multa - 2304 views


def get_most_popular_authors():
    print("\nThe most popular authors of all time are...")
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
        SELECT auth.name, count(*) as num
            FROM articles a
            JOIN authors auth on auth.id = a.author
            JOIN log l on l.path like '%/article/' || a.slug || '%'
            WHERE l.path like '%/article/%'
            AND l.status like '2%'
            GROUP BY auth.name
            ORDER BY num desc
        """)
    authors = c.fetchall()
    db.close()
    for author in authors:
        name = author[0]
        count = author[1]
        print("{} - {} views".format(name, count))

# 3. On which days did more than 1% of requests lead to errors?
#
#    The log table includes a column status that indicates the HTTP status code
#    that the news site sent to the user's browser.
#    Example: July 29, 2016 - 2.5% errors


def get_days_with_one_percent_errors():
    print("\nDays where more than 1 percent of requests led to errors are...")
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
            WITH total as (
                SELECT date_trunc('day', log.time) as day,
                    count(*) as totalrequests
                    FROM log
                    GROUP BY day
            )
                SELECT * from (
                    SELECT day, ROUND(
                        (
                            SELECT count(*) as failednum
                                FROM log
                                WHERE status like '5%' or status like '4%'
                                AND total.day = date_trunc('day', time)
                        )::numeric * 100 / totalrequests, 2
                    ) as failedpercent
                        FROM total
                ) results
                    WHERE results.failedpercent > 1
                    ORDER BY failedpercent desc
        """)
    days = c.fetchall()
    db.close()
    for day in days:
        date = day[0].strftime('%B %d, %Y')
        percent = day[1]
        print("{} - {}% errors".format(date, percent))


get_most_popular_articles()
get_most_popular_authors()
get_days_with_one_percent_errors()

print("\ngoodbye")
