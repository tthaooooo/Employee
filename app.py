import streamlit as st
import pandas as pd
import plotly.express as px

# Tải dữ liệu
df = pd.read_csv('education_career_success.csv')

# Tiền xử lý
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Tính phần trăm theo nhóm
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)

# Tính phần trăm trong mỗi nhóm Age + Job_Level
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Đổi tên để xóa tiền tố "Current_Job_Level=" trong tiêu đề cột phụ
df_grouped['Current_Job_Level'] = df_grouped['Current_Job_Level'].replace({
    'Entry': 'Entry',
    'Executive': 'Executive',
    'Mid': 'Mid',
    'Senior': 'Senior'
})

# Bộ lọc tương tác
job_levels = df_grouped['Current_Job_Level'].unique()
selected_levels = st.multiselect("Select Job Levels", job_levels, default=list(job_levels))

filtered_df = df_grouped[df_grouped['Current_Job_Level'].isin(selected_levels)]

# Vẽ biểu đồ
fig = px.bar(
    filtered_df,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    facet_col='Current_Job_Level',
    category_orders={'Entrepreneurship': ['No', 'Yes']},
    labels={'Percentage': 'Percentage (%)'},
    height=600
)

fig.update_layout(title_text="Percentage of People Doing Entrepreneurship by Age and Job Level")

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
