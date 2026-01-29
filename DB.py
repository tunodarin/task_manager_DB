import sqlite3

class TaskManager:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name
        self._create_table()

    def _create_table(self):
        /*タスクを保存するテーブルを作成*/
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            """)

    def add_task(self, title):
        /*新しいタスクをデータベースに保存*/
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
            print(f"Added task: {title}")

    def show_tasks(self):
        /*データベースから全てのタスクを取得して表示*/
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute("SELECT id, title, status FROM tasks")
            tasks = cursor.fetchall()
            print("\n--- Current Tasks ---")
            for t in tasks:
                print(f"[{t[0]}] {t[1]} - {t[2]}")

    def delete_task(self, task_id):
        /*指定したIDのタスクを削除*/
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            print(f"Deleted task ID: {task_id}")

/*実行コード*/
if __name__ == "__main__":
    app = TaskManager()
    
    /*タスクを追加してみる*/
    app.add_task("Pythonの勉強をする")
    app.add_task("買い物に行く")
    
    /*一覧を表示*/
    app.show_tasks()
    
    /*削除のテスト（例としてID 1を削除）*/
    app.delete_task(1)