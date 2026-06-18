import sqlite3
from datetime import datetime

DB_NAME = 'guestbook.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    
    cursor.execute('SELECT COUNT(*) FROM messages')
    if cursor.fetchone()[0] == 0:
        sample_messages = [
            ('Алексей', 'Отличный сайт! Всё работает супер.', '2026-06-17'),
            ('Мария', 'Привет всем! Классная гостевая книга.', '2026-06-18')
        ]
        cursor.executemany('INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)', sample_messages)
        conn.commit()
        
    conn.close()

def add_message(name, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO messages (name, message, created_at) VALUES (?, ?, ?)', (name, message, current_date))
    conn.commit()
    conn.close()

def delete_message(message_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
    conn.commit()
    conn.close()

def get_message_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM messages')
    count = cursor.fetchone()[0]
    conn.close()
    return count

if __name__ == '__main__':
    init_db()