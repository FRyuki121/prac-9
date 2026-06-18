from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'guestbook.db'

MONTHS = {
    '01': 'января', '02': 'февраля', '03': 'марта', '04': 'апреля',
    '05': 'мая', '06': 'июня', '07': 'июля', '08': 'августа',
    '09': 'сентября', '10': 'октября', '11': 'ноября', '12': 'декабря'
}

def format_russian_date(date_str):
    try:
        parts = date_str.split('-')
        year = parts[0]
        month = MONTHS.get(parts[1], parts[1])
        day = str(int(parts[2]))
        return f"{day} {month} {year}"
    except:
        return date_str

def get_db_messages():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, message, created_at FROM messages ORDER BY id DESC')
    rows = cursor.fetchall()
    conn.close()
    
    messages = []
    for row in rows:
        messages.append({
            'id': row[0],
            'name': row[1],
            'message': row[2],
            'created_at': format_russian_date(row[3])
        })
    return messages

@app.route('/')
def index():
    from database import get_message_count
    messages = get_db_messages()
    count = get_message_count()
    return render_template('index.html', messages=messages, count=count)

@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()
    
    if not name or not message:
        from database import get_message_count
        messages = get_db_messages()
        count = get_message_count()
        return render_template('index.html', messages=messages, count=count, error='Заполните все поля', name=name, message=message)
        
    from database import add_message
    add_message(name, message)
    return redirect('/')

@app.route('/delete/<int:message_id>')
def delete(message_id):
    from database import delete_message
    delete_message(message_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)