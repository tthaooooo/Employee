import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('education_career_success.csv')

# Kiểm tra cột bắt buộc
required_columns = ['Current_Job_Level', 'Gender', 'Entrepreneurship']
if not all(col in df.columns for col in required_columns):
    st.error("Dataset missing required columns!")
    st.stop()

# Drop missing data ở các cột cần dùng
df = df.dropna(subset=required_columns)

# Chỉ lấy các giá trị cần cho biểu đồ
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar: chọn Job Level
st.sidebar.title("Filters")
job_levels = sorted(df['Current_Job_Level'].unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Lọc theo Job Level
df_filtered = df[df['Current_Job_Level'] == selected_level]

# Kiểm tra nếu không có dữ liệu
if df_filtered.empty:
    st.warning(f"No data available for job level: {selected_level}")
    st.stop()

# Gom nhóm theo Entrepreneurship + Gender
pie_data = df_filtered.groupby(['Entrepreneurship', 'Gender']).size().reset_index(name='Count')

# Vẽ pie chart
fig = px.pie(
    pie_data,
    names='Entrepreneurship',
    values='Count',
    color='Entrepreneurship',
    title=f"Entrepreneurship by Gender – {selected_level} Level",
    hole=0.4,
    color_discrete_map={'Yes': '#FFD700', 'No': '#004080'}
)

fig.update_traces(textinfo='percent+label')

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
