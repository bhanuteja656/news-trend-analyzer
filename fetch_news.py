import urllib.request
import json
import ssl
import sqlite3
# Database connection
conn = sqlite3.connect('newsdb.sqlite')
cur = conn.cursor()
# Drop old table
cur.execute('DROP TABLE IF EXISTS RawArticles')
# Create raw storage table
cur.execute('''
CREATE TABLE RawArticles(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT UNIQUE
)
''')
# API URL
url = "https://newsapi.org/v2/everything?q=india&apiKey=aplkey"
# SSL context
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Fetch data
data = urllib.request.urlopen(url, context=ctx).read()
json_data = json.loads(data.decode())

# Store raw headlines only — no cleaning
articles = json_data.get('articles', [])
for article in articles:
    title = article.get('title', '')
    if not title:
        continue
    cur.execute('INSERT OR IGNORE INTO RawArticles (title) VALUES (?)', (title,))
conn.commit()
print("Raw headlines stored:", len(articles))
cur.close()
