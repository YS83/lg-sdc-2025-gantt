import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# Initial task data
initial_tasks = [
    {"Task": "콘셉트 디자인 확정", "Start": "2025-06-18", "Finish": "2025-07-07", "Resource": "Kim", "Status": "Completed"},
    {"Task": "키노트 발표 주제 확정", "Start": "2025-06-23", "Finish": "2025-07-11", "Resource": "Kim", "Status": "In progress"},
    {"Task": "데모 부스 주제 확정", "Start": "2025-06-23", "Finish": "2025-07-11", "Resource": "Kim", "Status": "In progress"},
    {"Task": "발표자 모집", "Start": "2025-07-14", "Finish": "2025-08-01", "Resource": "Kim", "Status": "Planned"},
    {"Task": "발표자 선정", "Start": "2025-08-04", "Finish": "2025-08-08", "Resource": "Kim", "Status": "Planned"},
    {"Task": "발표자 선정 결과 안내", "Start": "2025-08-11", "Finish": "2025-08-11", "Resource": "Kim", "Status": "Planned"},
    {"Task": "CPC 참가자 모집", "Start": "2025-07-25", "Finish": "2025-08-22", "Resource": "Jung", "Status": "Planned"},
    {"Task": "키노트, 세션 발표 자료 제출", "Start": "2025-08-11", "Finish": "2025-09-12", "Resource": "Kim", "Status": "Planned"},
    {"Task": "참가자 사전 등록", "Start": "2025-08-25", "Finish": "2025-09-19", "Resource": "Kim", "Status": "Planned"},
    {"Task": "언론 보도 의뢰", "Start": "2025-08-25", "Finish": "2025-09-19", "Resource": "Na", "Status": "Planned"},
    {"Task": "CPC 2025 예선 대회", "Start": "2025-09-06", "Finish": "2025-09-06", "Resource": "Jung", "Status": "Planned"},
    {"Task": "CPC 2025 본선 대회", "Start": "2025-09-20", "Finish": "2025-09-20", "Resource": "Jung", "Status": "Planned"},
    {"Task": "SDC 2025", "Start": "2025-09-23", "Finish": "2025-09-25", "Resource": "Kim", "Status": "Planned"},
    {"Task": "커피챗 지원자 모집", "Start": "2025-07-25", "Finish": "2025-08-22", "Resource": "Kim", "Status": "Planned"},
    {"Task": "키노트 연사 프로필 사진 취합", "Start": "2025-06-23", "Finish": "2025-07-11", "Resource": "Kim", "Status": "In progress"},
    {"Task": "컨퍼런스 주제/슬로건 확정", "Start": "2025-06-30", "Finish": "2025-07-01", "Resource": "Kim", "Status": "Completed"},
    {"Task": "홈페이지 오픈 준비", "Start": "2025-07-03", "Finish": "2025-07-10", "Resource": "Kim", "Status": "Planned"},
]

# Convert to DataFrame
df = pd.DataFrame(initial_tasks)

# Sidebar: Add new task
st.sidebar.header("➕ Add New Task")
new_task_name = st.sidebar.text_input("Task Name")
new_start_date = st.sidebar.date_input("Start Date", value=datetime(2025, 6, 18))
new_finish_date = st.sidebar.date_input("Finish Date", value=datetime(2025, 6, 25))
new_resource = st.sidebar.text_input("Resource")
new_status = st.sidebar.selectbox("Status", ["Planned", "In progress", "Due Soon", "Overdue", "Completed"])
if st.sidebar.button("Add Task"):
    if new_task_name and new_resource:
        new_task = {
            "Task": new_task_name,
            "Start": new_start_date.strftime("%Y-%m-%d"),
            "Finish": new_finish_date.strftime("%Y-%m-%d"),
            "Resource": new_resource,
            "Status": new_status
        }
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)

# Sidebar: Manual status update
st.sidebar.header("✏️ Update Task Status")
selected_task = st.sidebar.selectbox("Select Task to Update", df["Task"])
new_status_for_task = st.sidebar.selectbox("New Status", ["Planned", "In progress", "Due Soon", "Overdue", "Completed"])
if st.sidebar.button("Update Status"):
    df.loc[df["Task"] == selected_task, "Status"] = new_status_for_task

# Automatically update status based on today's date
today = datetime.today().date()
for i, row in df.iterrows():
    finish_date = datetime.strptime(row['Finish'], "%Y-%m-%d").date()
    days_left = (finish_date - today).days
    if row['Status'] not in ["Completed"]:
        if days_left < 0:
            df.at[i, 'Status'] = 'Overdue'
        elif days_left <= 7:
            df.at[i, 'Status'] = 'Due Soon'

# Sort tasks by start date descending
df['Start_dt'] = pd.to_datetime(df['Start'])
df = df.sort_values(by='Start_dt', ascending=False)

# Add duration to task name
def add_duration_label(row):
    start = datetime.strptime(row['Start'], "%Y-%m-%d")
    end = datetime.strptime(row['Finish'], "%Y-%m-%d")
    duration = (end - start).days + 1
    if duration >= 7:
        return f"{row['Task']} ({duration // 7}주)"
    else:
        return f"{row['Task']} ({duration}일)"

df['Task'] = df.apply(add_duration_label, axis=1)

# Create Gantt chart using Status for color
fig = ff.create_gantt(
    df.to_dict('records'),
    index_col='Status',
    show_colorbar=True,
    group_tasks=True,
    title="SDC 2025 Gantt Chart with Status and Duration"
)

# Display in Streamlit
st.title("SDC 2025 Gantt Chart")
st.plotly_chart(fig, use_container_width=True)

