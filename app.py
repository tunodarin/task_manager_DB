# -*- coding: utf-8 -*-

print("Program started!")

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# データベースを初期化する関数
def init_db():
    with sqlite3.connect('database.db') as conn:
        # 'is_completed' カラムを追加（0: 未完了, 1: 完了）
        conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, is_completed INTEGER DEFAULT 0)")
    print("Database initialized.")
    
@app.route('/')
def index():
    # DBからデータを取得して表示する
    with sqlite3.connect('database.db') as conn:
        # 取得したデータを辞書形式で扱いやすくする設定
        conn.row_factory = sqlite3.Row
        tasks = conn.execute("SELECT id, title FROM tasks").fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    # フォームから送信された「title」を取得
    title = request.form.get('title')
    
    if title:
        with sqlite3.connect('database.db') as conn:
            # SQLのINSERT文を実行してデータを保存 (Create)
            conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,)) 
            conn.commit()
        # 保存が終わったらトップページに戻る
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
        app.run(debug=True)