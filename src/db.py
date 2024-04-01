import sqlite3

# SQLite 연결 설정
conn = sqlite3.connect('url_shortener.db')
cursor = conn.cursor()

# URL 테이블 생성
cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, original_url TEXT, short_slug TEXT, short_url TEXT)''')
conn.commit()
