import streamlit as st
import pandas as pd
import plotly.express as px

# Tải dữ liệu
df = pd.read_csv('education_career_success.csv')

# Lọc giá trị hợp lệ
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Nhóm dữ liệu
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)

# Tính phần trăm
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Đổi tên cột cho đẹp
df_grouped['Current_Job_Level'] = df_grouped['Current_Job_Level'].replace({
    'Entry': 'Entry',
    'Executive': 'Executive',
    'Mid': 'Mid',
    'Senior': 'Senior'
})

# Chọn các cấp bậc để hiển thị
job_levels = ['Entry', 'Executive', 'Mid', 'Senior']
selected_levels = st.multiselect("Select Job Levels", job_levels, default=job_levels)

# Lọc dữ liệu
filtered_df = df_grouped[df_grouped['Current_Job_Level'].isin(selected_levels)]

# Thiết lập màu giống ảnh mẫu
color_map = {'Yes': '#B7E084', 'No': '#6A0DAD'}  # Xanh lá nhạt và tím

# Vẽ biểu đồ
fig = px.bar(
    filtered_df,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    facet_col='Current_Job_Level',
    facet_col_wrap=2,
    color_discrete_map=color_map,
    category_orders={
        'Entrepreneurship': ['Yes', 'No'],
        'Current_Job_Level': job_levels
    },
    labels={'Percentage': 'Proportion', 'Age': 'Age'}
)

fig.update_layout(
    title="Stacked Bar Chart: Proportion of Entrepreneurship by Age and Job Level",
    height=600,
    legend_title_text='Entrepreneurship',
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

# Hiển thị biểu đồ
st.plotly_chart(fig, use_container_width=True)
