# -*- coding: utf-8 -*-

print("Program started!")

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as conn:
        # 【重要】一度テーブルを完全に削除して、新しい構造で作り直させる
        conn.execute("DROP TABLE IF EXISTS tasks") 
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT, 
                is_completed INTEGER DEFAULT 0,
                deadline TEXT
            )
        """)
    print("Database initialized.")
 
@app.route('/')
def index():
    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        #is_completed を取得
        #deadlineを取得
        #deadline IS NULL を使って、期限なしを後ろ(1)、期限ありを前(0)にする
        # 2. その後、期限があるもの同士を日付順(ASC)に並べる
        tasks = conn.execute("""
            SELECT id, title, deadline, is_completed FROM tasks 
           ORDER BY is_completed ASC, deadline IS NULL ASC, deadline ASC
        """).fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    deadline = request.form.get('deadline') # 日付を取得
    
    if title:
        with sqlite3.connect('database.db') as conn:
            conn.execute("INSERT INTO tasks (title, deadline) VALUES (?, ?)", (title, deadline))
            conn.commit()
    return redirect('/')

@app.route('/complete/<int:id>')
def complete(id):
    with sqlite3.connect('database.db') as conn:
        # 現在の状態を反転させる（0なら1に、1なら0にする）
        conn.execute("UPDATE tasks SET is_completed = 1 - is_completed WHERE id = ?", (id,))
        conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    with sqlite3.connect('database.db') as conn:
        # 指定されたIDのタスクを削除するSQL (Delete)
        conn.execute("DELETE FROM tasks WHERE id = ?", (id,))
        conn.commit()
    
    # 削除が終わったらトップページにリダイレクト
    return redirect('/')

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)