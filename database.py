import sqlite3

DB_NAME = 'guestbook.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    cursor.execute('SELECT COUNT(*) FROM messages')
    if cursor.fetchone()[0] == 0:
        sample_messages = [
            ('Алексей', 'Отличный сайт! Всё работает супер.'),
            ('Мария', 'Привет всем! Классная гостевая книга.')
        ]
        cursor.executemany('INSERT INTO messages (name, message) VALUES (?, ?)', sample_messages)
        conn.commit()
        
    conn.close()

if __name__ == '__main__':
    init_db()