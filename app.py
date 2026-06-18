from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
DB_NAME = 'guestbook.db'

def get_db_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name, message, created_at FROM messages ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    messages = []
    for row in rows:
        messages.append({
            'name': row[0],
            'message': row[1],
            'created_at': row[2]
        })
    return messages

@app.route('/')
def index():
    messages = get_db_messages()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)