import sqlite3
conn = sqlite3.connect('newsdb.sqlite')
cur = conn.cursor()
# Add this at the bottom of analyze.py
print("\nTop 5 Trending Words:")
print("-" * 35)
cur.execute('SELECT word, count FROM CleanWords ORDER BY count DESC LIMIT 5')
rows = cur.fetchall()
for row in rows:
    bar = "»"*row[1]
    print(f"{row[0]:<15} {bar} {row[1]}")