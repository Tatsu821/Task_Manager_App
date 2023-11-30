import streamlit as st
import pandas as pd 
from db_func import * 
import streamlit_calendar as st_calendar
import datetime

#表示タスクデータのハイライト
def decorate_df(x):
	print(highlight_duedate(x))
	print(status_color(x))
	return highlight_duedate(x) + status_color(x)

#1週間前になるとハイライト
def highlight_duedate(x):
	print(x)
	if isinstance(x['Date'], str):
		return ['background-color: yellow'] if datetime.datetime.strptime(str(x['Date']), '%Y-%m-%d')-datetime.timedelta(days=7) < datetime.datetime.now() else ['']
	else:
		print(x)
		return ['']

#ステータスごとに色付け
def status_color(x):
	if x['Status'] == 'ToDo':
		return ['color: red']
	elif x['Status'] == 'Doing':
		return ['color: blue']
	else:
		return ['color: green']
    

def main():
	menu = ["Create","Task_List","Update","Delete"]
	choice = st.sidebar.selectbox("Menu",menu)
	create_table()
	
	st.title("Task Manager")

    #タスク登録画面
	if choice == "Create":
		st.subheader("Add Item")
		col1,col2 = st.columns(2)
		
		with col1:
			task = st.text_area("Task Name")

		with col2:
			task_status = st.selectbox("Status",["ToDo","Doing","Done"])
			task_due_date = st.date_input("Due Date")

		if st.button("Add Task"):
			add_data(task,task_status,task_due_date)
			st.success("Added ---{}--- To Task".format(task))

    #タスクリスト表示
	elif choice == "Task_List":
		result = view_all_data()
		clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
		st.dataframe(clean_df.style.apply(decorate_df, subset=['Date', 'Status'], axis=1), use_container_width=True, hide_index=True)
	
		eventList = []
		for indx, row in clean_df.iterrows():
			bgcolor = 'red' if row['Status']=='ToDo' else 'green' if row['Status']=='Done' else 'blue'
			event = {
				'id': indx,
                'title': row['Task'],
                'start': row['Date'],
				'backgroundColor': bgcolor,
				'borderColor': bgcolor
            }
			eventList.append(event)
			
		with st.expander("Task Status"):
			task_df = clean_df['Status'].value_counts().to_frame()
			# st.dataframe(task_df)
			task_df = task_df.reset_index()
			st.dataframe(task_df.style.apply(status_color, subset=['Status'], axis=1), use_container_width=True, hide_index=True)
			
		st_calendar.calendar(events=eventList)

    #タスク更新画面
	elif choice == "Update":
		st.subheader("Edit Items")
		with st.expander("Current Data"):
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df.style.apply(decorate_df, subset=['Date', 'Status'], axis=1), use_container_width=True, hide_index=True)

		list_of_tasks = [i[0] for i in view_all_task_names()]
		selected_task = st.selectbox("Task",list_of_tasks)
		task_result = get_task(selected_task)

		if task_result:
			task = task_result[0][0]
			task_status = task_result[0][1]
			task_due_date = task_result[0][2]

			col1,col2 = st.columns(2)
			
			with col1:
				new_task = st.text_area("Task Name",task)

			with col2:
				new_task_status = st.selectbox(f'Status',["ToDo","Doing","Done"])
				new_task_due_date = st.date_input(f'Due Date', datetime.datetime.strptime(task_due_date, '%Y-%m-%d'))

			if st.button("Update Task"):
				edit_task_data(new_task,new_task_status,new_task_due_date,task,task_status,task_due_date)
				st.success("Updated {} ➡️ {}".format(task,new_task))
				#編集後のタスクデータ表示
				result = view_all_data()
				clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
				st.dataframe(clean_df, use_container_width=True, hide_index=True)

    #タスク削除画面
	elif choice == "Delete":
		st.subheader("Delete")
		with st.expander("View Data"):
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df.style.apply(decorate_df, subset=['Date', 'Status'], axis=1), use_container_width=True, hide_index=True)

		unique_list = [i[0] for i in view_all_task_names()]
		delete_by_task_name =  st.selectbox("Select Task",unique_list)
		if st.button("Delete"):
			delete_data(delete_by_task_name)
			st.warning("Deleted: '{}'".format(delete_by_task_name))
			result = view_all_data()
			clean_df = pd.DataFrame(result,columns=["Task","Status","Date"])
			st.dataframe(clean_df, use_container_width=True, hide_index=True)


if __name__ == '__main__':
	main()