# Task_Manager_App

## Overview
Streamlitによるタスク管理アプリケーション

## Requirement
Python==3.11
- streamlit
- pandas
- streamlit_calendar

## Main function
以下の4画面の遷移をst.sidebar.selectboxによって実装
ユーザは各画面でタスクの登録、閲覧、編集、削除が可能
タスクデータはsqliteを用いて簡易的なデータベースを構築し、実装においてはSQLでデータベースへのインタラクションを実現

### タスク登録画面
ユーザはTask Name, Status=['ToDo(未着手)', 'Doing(稼働中)', 'Done(完了)'], Due Date　を入力し、
'Add Task'ボタンで追加

### タスク表示画面
登録されているタスクデータをデータフレーム形式で表示。各カラム名をクリックすることでその列ごとに昇順、降順のソートが可能
また、df.style.applyによってデータフレームの各セルに関数を割り当てることで、以下のようにタスクデータを装飾した。

- Due Dateが現在の日付より一週間後以内であれば、背景を黄色にハイライト
- タスクのステータスによってテキストの色を変える：　Todo：red, Doing: blue, Done: green

streamlit_calendarによって、カレンダーを表示しタスク状況を俯瞰することが可能

### タスク編集画面
編集したいタスク名を選択し、Task Name, Status, Due Dateを編集する

### タスク削除画面
削除したいタスクを選択し、Deleteボタンを押し削除