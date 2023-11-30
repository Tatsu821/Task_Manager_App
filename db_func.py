import sqlite3
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()

#テーブル作成
def create_table():
	c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,task_status TEXT,task_due_date DATE)')

#タスクを登録
def add_data(task: str, task_status: str, task_due_date: str):
	c.execute('INSERT INTO taskstable(task,task_status,task_due_date) VALUES (?,?,?)',(task,task_status,task_due_date))
	conn.commit()

#全タスク情報を取得
def view_all_data():
	c.execute('SELECT * FROM taskstable')
	data = c.fetchall()
	return data

def view_all_task_names():
	c.execute('SELECT DISTINCT task FROM taskstable')
	data = c.fetchall()
	return data

#タスク名から該当するタスクを取得
def get_task(task: str):
	c.execute('SELECT * FROM taskstable WHERE task="{}"'.format(task))
	data = c.fetchall()
	return data

#ステータスから該当するタスクを取得
def get_task_by_status(task_status):
	c.execute('SELECT * FROM taskstable WHERE task_status="{}"'.format(task_status))
	data = c.fetchall()

#タスクを更新
def edit_task_data(new_task: str, new_task_status: str, new_task_date: str , task: str, task_status: str, task_due_date: str):
	c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",(new_task,new_task_status,new_task_date,task,task_status,task_due_date))
	conn.commit()
	data = c.fetchall()
	return data

#タスク名から該当するタスクを削除
def delete_data(task):
	c.execute('DELETE FROM taskstable WHERE task="{}"'.format(task))
	conn.commit()
