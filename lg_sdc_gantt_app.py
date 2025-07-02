
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from datetime import datetime, timedelta

# Define initial task data
tasks = [
    {"Task": "키비주얼(KV), 키컬러(KC) 선정", "Start": "2025-06-18", "Finish": "2025-07-04", "Resource": "김영삼"},
    {"Task": "키노트 발표 주제 선정", "Start": "2025-06-23", "Finish": "2025-07-11", "Resource": "김영삼"},
    {"Task": "데모 부스 주제 선정", "Start": "2025-06-23", "Finish": "2025-07-11", "Resource": "김영삼"},
    {"Task": "세션 및 이그나잇 발표자 모집", "Start": "2025-07-14", "Finish": "2025-08-01", "Resource": "김영삼"},
    {"Task": "세션 및 이그나잇 발표자 선정", "Start": "2025-08-04", "Finish": "2025-08-08", "Resource": "김영삼"},
    {"Task": "LGCPC 참가자 모집", "Start": "2025-07-25", "Finish": "2025-08-22", "Resource": "정진우"},
    {"Task": "키노트, 세션 발표 자료 제출", "Start": "2025-08-11", "Finish": "2025-09-12", "Resource": "김영삼"},
    {"Task": "참가자 사전 등록", "Start": "2025-08-25", "Finish": "2025-09-19", "Resource": "김영삼"},
    {"Task": "언론 보도 의뢰", "Start": "2025-08-25", "Finish": "2025-09-19", "Resource": "나명지"},
    {"Task": "LGCPC 2025 예선 대회", "Start": "2025-09-06", "Finish": "2025-09-06", "Resource": "정진우"},
    {"Task": "LGCPC 2025 본선 대회", "Start": "2025-09-20", "Finish": "2025-09-20", "Resource": "정진우"},
    {"Task": "LG SDC 2025", "Start": "2025-09-23", "Finish": "2025-09-25", "Resource": "김영삼"},
    {"Task": "커피챗 지원자 모집", "Start": "2025-07-25", "Finish": "2025-08-22", "Resource": "김영삼"},
    {"Task": "키노트 연사 프로필 사진 취합", "Start": "2025-06-23", "Finish": "2025-07-11", "Resource": "김영삼"},
]

# Initialize session state for task statuses
if "statuses" not in st.session_state:
    st.session_state.statuses = {}
    today = datetime.today()
    for task in tasks:
        finish_date = datetime.strptime(task["Finish"], "%Y-%m-%d")
        if finish_date < today:
            status = "Overdue"
        elif (finish_date - today).days <= 7:
            status = "Due Soon"
        else:
            status = "Planned"
        st.session_state.statuses[task["Task"]] = status

# Sidebar for task selection and status update
st.sidebar.header("작업 상태 변경")
selected_task = st.sidebar.selectbox("작업 선택", [task["Task"] for task in tasks])
new_status = st.sidebar.selectbox("새 상태 선택", ["Planned", "Due Soon", "Overdue", "Completed"])
if st.sidebar.button("상태 업데이트"):
    st.session_state.statuses[selected_task] = new_status
    st.sidebar.success(f"'{selected_task}' 상태가 '{new_status}'로 변경되었습니다.")

# Apply status to tasks and calculate duration
for task in tasks:
    task["Status"] = st.session_state.statuses[task["Task"]]
    start_date = datetime.strptime(task["Start"], "%Y-%m-%d")
    end_date = datetime.strptime(task["Finish"], "%Y-%m-%d")
    duration_days = (end_date - start_date).days + 1
    if duration_days >= 7:
        weeks = duration_days // 7
        task["Task"] += f" ({weeks}주)"
    else:
        task["Task"] += f" ({duration_days}일)"

# Sort tasks by start date
tasks_sorted = sorted(tasks, key=lambda x: datetime.strptime(x["Start"], "%Y-%m-%d"), reverse=True)

# Create Gantt chart
fig = ff.create_gantt(
    tasks_sorted,
    index_col="Status",
    show_colorbar=True,
    group_tasks=True,
    title="LG SDC 2025 Gantt Chart with Status and Duration",
    hover_data=["Resource", "Status"]
)

# Add vertical lines for deadlines
for task in tasks_sorted:
    finish_date = datetime.strptime(task["Finish"], "%Y-%m-%d")
    fig.add_shape(
        dict(
            type="line",
            x0=finish_date,
            x1=finish_date,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            line=dict(color="red", width=1, dash="dot")
        )
    )

# Display chart
st.plotly_chart(fig, use_container_width=True)
