import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
df = df[df['Gender'].notna()]  # loại bỏ dòng thiếu giới tính nếu có

# Sidebar filter for Job Level
st.sidebar.title("Filters")
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Filter theo Job Level
df_filtered = df[df['Current_Job_Level'] == selected_level]

# Tính số lượng theo Entrepreneurship + Gender
pie_df = df_filtered.groupby(['Entrepreneurship', 'Gender']).size().reset_index(name='Count')

# Vẽ biểu đồ tròn
fig_pie = px.pie(
    pie_df,
    names='Entrepreneurship',
    values='Count',
    color='Entrepreneurship',
    title=f"Entrepreneurship Distribution by Gender – {selected_level} Level",
    hole=0.4,
    color_discrete_map={'Yes': '#FFD700', 'No': '#004080'},
)

# Phân tách thêm bằng legend Gender (optional)
fig_pie.update_traces(textinfo='percent+label', pull=[0.05 if e == 'Yes' else 0 for e in pie_df['Entrepreneurship']])

# Hiển thị biểu đồ
st.plotly_chart(fig_pie, use_container_width=True)
