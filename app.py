import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Tính toán Count và Percentage
df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Sidebar
st.sidebar.title("Filters")

# Job Levels
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Job Levels", job_levels, default=job_levels)

# Age slider
min_age = int(df_grouped['Age'].min())
max_age = int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))

# Entrepreneurship status
statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship", statuses, default=statuses)

# Count or Percentage
mode = st.sidebar.radio("Show as:", ["Percentage (%)", "Count"])

# Lọc dữ liệu
filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'] >= age_range[0]) &
    (df_grouped['Age'] <= age_range[1])
]

# Cài đặt biểu đồ
if mode == "Percentage (%)":
    y_col = 'Percentage'
    fmt = lambda x: f"{x:.0%}"
    y_axis_title = "Percentage"
    y_tick_format = ".0%"
else:
    y_col = 'Count'
    fmt = lambda x: str(x)
    y_axis_title = "Count"
    y_tick_format = None

# Màu sắc và thứ tự
colors = {'Yes': '#FFD700', 'No': '#004080'}
order_levels = ['Entry', 'Executive', 'Mid', 'Senior']
levels_to_show = [lvl for lvl in order_levels if lvl in selected_levels]

# Title
st.title("🚀 Education & Career Success Dashboard")

# Hiển thị biểu đồ
cols = st.columns(2)

for i, lvl in enumerate(levels_to_show):
    data_lvl = filtered[filtered['Current_Job_Level'] == lvl]
    if data_lvl.empty:
        with cols[i % 2]:
            st.write(f"### {lvl} — No data")
        continue

    fig = px.bar(
        data_lvl,
        x='Age',
        y=y_col,
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=colors,
        category_orders={
            'Entrepreneurship': ['No', 'Yes'],
            'Age': sorted(data_lvl['Age'].unique())
        },
        text=data_lvl[y_col].apply(fmt),
        labels={'Age': 'Age', y_col: y_axis_title},
        height=350,
        width=600,
        title=f"{lvl} Level"
    )

    # Text nằm bên ngoài cột, trình bày dọc
    fig.update_traces(textposition='outside')

    fig.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )

    fig.update_yaxes(title=y_axis_title)
    if y_tick_format:
        fig.update_yaxes(tickformat=y_tick_format)

    with cols[i % 2]:
        st.plotly_chart(fig, use_container_width=True)
