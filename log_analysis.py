#!/usr/bin/env python3

import psycopg2
from flask import Flask, request, redirect, url_for


DBNAME = 'news'


def get_popular3articles():
    """Return most popular three articles of all time"""
    db = psycopg2.connect(database=DBNAME)
    cur = db.cursor()
    query = """ SELECT a.title, count(l.path) as views
                    FROM articles a, log l
                    WHERE l.path like '/article/' || a.slug
                        AND l.status like '%200%'
                    GROUP BY a.title
                    ORDER BY views desc
                    LIMIT 3
    """
    cur.execute(query)
    results = cur.fetchall()
    db.close()
    return results


def get_popular_articles_authors():
    """Return the most popular article authors of all time"""
    db = psycopg2.connect(database=DBNAME)
    cur = db.cursor()
    query = """ SELECT au.name, count(l.path) as views
                FROM log l, articles a
                LEFT JOIN authors au
                    ON a.author = au.id
                WHERE l.path like '/article/' || a.slug
                    AND l.status like '%200%'
                GROUP BY au.name
                ORDER BY views desc
    """
    cur.execute(query)
    results = cur.fetchall()
    db.close()
    return results


def get_error_days():
    """Return days on which more than 1% of requests led to errors"""
    db = psycopg2.connect(database=DBNAME)
    cur = db.cursor()
    query = """ SELECT a.fdate, (a.failed*100.0/b.total) as percent
                FROM (SELECT date(time) as fdate, count(*) as failed
                        FROM log
                        WHERE status like '%404%'
                        GROUP BY date(time)) as a
                JOIN (SELECT date(time), count(*) as total
                        FROM log
                        GROUP BY date(time)) as b
                    ON a.fdate = b.date
                    AND (a.failed*100.0/b.total) > 1.0
    """
    cur.execute(query)
    results = cur.fetchall()
    db.close()
    return results


app = Flask(__name__)

# HTML template for the Log Analysis page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>Log Analysis</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
    <form>
        <h1>Log Analysis</h1>
        <div>
            <a href="/popolar_articles">
                <input type="button" value="Get 3 Popular Articles">
            </a>
            <a href="/popolar_authors">
                <input type="button" value="Get Popular Authors">
            </a>
            <a href="/error_days">
                <input type="button" value="Get Error Days">
            </a>
        </div>
    </form>
    <!-- post content will go here -->
%s
  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
    <div class=post><em class=date>%s</em><br>%s</div>
'''


@app.route('/', methods=['GET'])
def main():
    '''Main page for the Analysis.'''
    posts = ''
    html = HTML_WRAP % posts
    return html


@app.route('/popolar_articles')
def popolar_articles():
    """Fetche popular 3 Articles."""
    posts = "".join(
        POST % (title, views) for title, views in get_popular3articles())
    html = HTML_WRAP % posts
    return html


@app.route('/popolar_authors')
def popolar_authors():
    """Fetche Popular Authors."""
    posts = "".join(
        POST % (name, views) for name, views in get_popular_articles_authors())
    html = HTML_WRAP % posts
    return html


@app.route('/error_days')
def error_days():
    """Fetche days with more than 1% error."""
    posts = "".join(
        POST % (fdate, round(percent, 2))
        for fdate, percent in get_error_days())
    html = HTML_WRAP % posts
    return html


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
# Run as python log_analysis/log_analysis.py
