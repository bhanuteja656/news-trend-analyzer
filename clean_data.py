import sqlite3
# Connect to same database
conn = sqlite3.connect('newsdb.sqlite')
cur = conn.cursor()
# Drop old cleaned table
cur.execute('DROP TABLE IF EXISTS CleanWords')
# Create cleaned words table
cur.execute('''
CREATE TABLE CleanWords(
    word TEXT PRIMARY KEY UNIQUE,
    count INTEGER
)
''')
# Stopwords to remove
stopwords = ['the','a','an','in','is','of','to','and','for',
             'on','at','by','with','this','that','are','was',
             'it','as','be','or','from','has','have','not','its',
             'he','she','they','we','i','but','after','over','new']

# Read raw headlines from RawArticles table
cur.execute('SELECT title FROM RawArticles')
rows = cur.fetchall()
print("Total headlines to clean:", len(rows))
for row in rows:
    title = row[0]
    # Clean and split
    words = title.lower().strip().split()
    for word in words:
        # Remove punctuation
        word = word.strip('.,!?:;\'"()-[]|')
        # Skip short words and stopwords
        if len(word) < 3 or word in stopwords:
            continue
        # Store into CleanWords
        cur.execute('INSERT OR IGNORE INTO CleanWords (word, count) VALUES (?, 0)', (word,))
        cur.execute('UPDATE CleanWords SET count = count + 1 WHERE word = ?', (word,))
conn.commit()
print("Cleaning done!")
# Preview top 10
cur.execute('SELECT word, count FROM CleanWords ORDER BY count DESC LIMIT 10')
rows = cur.fetchall()
print("\nTop 10 words:")
for row in rows:
    print(row[0], "-", row[1])
cur.close()