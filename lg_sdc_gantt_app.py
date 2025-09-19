import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# Initial task data
initial_tasks = [
    {"Task": "콘셉트 디자인 확정", "Start": "2025-06-18", "Finish": "2025-07-07", "Resource": "Kim", "Status": "Completed"},
    {"Task": "키노트 발표 주제 확정", "Start": "2025-06-23", "Finish": "2025-07-14", "Resource": "Kim", "Status": "Completed"},
    {"Task": "데모 부스 주제 확정", "Start": "2025-06-23", "Finish": "2025-09-05", "Resource": "Kim", "Status": "Completed"},
    {"Task": "워크숍 주제 및 일정 확정", "Start": "2025-06-23", "Finish": "2025-08-11", "Resource": "Kim", "Status": "Completed"},
    {"Task": "발표자 모집", "Start": "2025-08-04", "Finish": "2025-08-15", "Resource": "Kim", "Status": "Completed"},
    {"Task": "발표자 선정", "Start": "2025-08-18", "Finish": "2025-08-20", "Resource": "Kim", "Status": "Completed"},
    {"Task": "발표자 선정 결과 안내", "Start": "2025-08-20", "Finish": "2025-08-20", "Resource": "Kim", "Status": "Completed"},
    {"Task": "CPC 참가자 모집", "Start": "2025-07-25", "Finish": "2025-08-22", "Resource": "Jeong", "Status": "Completed"},
    {"Task": "발표 자료 취합", "Start": "2025-08-20", "Finish": "2025-09-19", "Resource": "Kim", "Status": "In progress"},
    {"Task": "사전 참가자 등록", "Start": "2025-08-25", "Finish": "2025-09-19", "Resource": "Kim", "Status": "In progress"},
    {"Task": "언론 보도 준비", "Start": "2025-08-25", "Finish": "2025-09-19", "Resource": "Na", "Status": "Completed"},
    {"Task": "CPC 2025 예선", "Start": "2025-09-06", "Finish": "2025-09-06", "Resource": "Jeong", "Status": "Completed"},
    {"Task": "CPC 2025 본선", "Start": "2025-09-20", "Finish": "2025-09-20", "Resource": "Jeong", "Status": "Planned"},
    {"Task": "SDC 2025 개최", "Start": "2025-09-23", "Finish": "2025-09-25", "Resource": "Kim", "Status": "Planned"},
    {"Task": "오픈멘토링 멘토 지원자 모집", "Start": "2025-08-05", "Finish": "2025-08-19", "Resource": "Kim", "Status": "Completed"},
    {"Task": "디스커버리투어 멘토 모집", "Start": "2025-07-18", "Finish": "2025-07-25", "Resource": "Kim", "Status": "Completed"},
    {"Task": "키노트 연사 프로필 자료 취합", "Start": "2025-06-23", "Finish": "2025-07-17", "Resource": "Kim", "Status": "Completed"},
    {"Task": "컨퍼런스 주제/슬로건 확정", "Start": "2025-06-30", "Finish": "2025-07-01", "Resource": "Kim", "Status": "Completed"},
    {"Task": "홈페이지 가오픈 준비", "Start": "2025-07-03", "Finish": "2025-07-10", "Resource": "Kim", "Status": "Completed"},
    {"Task": "홈페이지 오픈", "Start": "2025-08-04", "Finish": "2025-08-04", "Resource": "Kim", "Status": "Completed"},
    {"Task": "이용약관 검토", "Start": "2025-07-10", "Finish": "2025-07-31", "Resource": "Kim", "Status": "Completed"},
    {"Task": "SDC 굿즈 선정", "Start": "2025-07-02", "Finish": "2025-07-22", "Resource": "Kim", "Status": "Completed"},
    {"Task": "개발자 모임 통합 브랜딩 굿즈 검토", "Start": "2025-06-25", "Finish": "2025-07-23", "Resource": "Kim", "Status": "Completed"},
    {"Task": "프로그램별 안내페이지 제작", "Start": "2025-07-22", "Finish": "2025-08-25", "Resource": "Kim", "Status": "Completed"},
    {"Task": "글로벌라운지 시설 예약", "Start": "2025-07-25", "Finish": "2025-07-27", "Resource": "Kim", "Status": "Completed"},
    {"Task": "공용시설 운영 협조 요청", "Start": "2025-08-05", "Finish": "2025-09-15", "Resource": "Kim", "Status": "Completed"},
    {"Task": "안전작업계획서 작성", "Start": "2025-08-01", "Finish": "2025-09-09", "Resource": "Kim", "Status": "Completed"},
    {"Task": "추가 발표자 모집", "Start": "2025-08-25", "Finish": "2025-08-29", "Resource": "Kim", "Status": "Completed"},
    {"Task": "오찬 참석자 명단 확정", "Start": "2025-08-25", "Finish": "2025-08-29", "Resource": "Kim", "Status": "Completed"},
    {"Task": "오픈멘토링 준비 사항 안내", "Start": "2025-08-27", "Finish": "2025-08-27", "Resource": "Kim", "Status": "Completed"},
    {"Task": "VIP 참석자 확인", "Start": "2025-08-25", "Finish": "2025-09-19", "Resource": "Kim", "Status": "Completed"},
    {"Task": "키노트 오찬 안내", "Start": "2025-08-25", "Finish": "2025-09-08", "Resource": "Kim", "Status": "Completed"},
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
    title="SDC 2025 Gantt Chart"
)

# Add vertical line for today's date
fig.add_shape(
    dict(
        type="line",
        x0=today.strftime("%Y-%m-%d"),
        x1=today.strftime("%Y-%m-%d"),
        y0=0,
        y1=1,
        xref='x',
        yref='paper',
        line=dict(color="red", width=2, dash="dot")
    )
)

# Display in Streamlit
st.title("SDC 2025")
st.plotly_chart(fig, use_container_width=True)
