import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Tải dữ liệu ---
df = pd.read_csv('education_career_success.csv')

# --- 2. Tiền xử lý ---
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Tính toán tỉ lệ theo nhóm Job + Age + Entrepreneurship
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# --- 3. Sidebar lọc tương tác ---
st.sidebar.title("🔍 Filter Options")

job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Select Job Levels", job_levels, default=job_levels)

ages = sorted(df_grouped['Age'].unique())
selected_ages = st.sidebar.multiselect("Select Age(s)", ages, default=ages)

statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship Status", statuses, default=statuses)

# --- 4. Lọc dữ liệu theo lựa chọn ---
filtered_df = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Age'].isin(selected_ages)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses))
]

# --- 5. Vẽ biểu đồ ---
fig = px.bar(
    filtered_df,
    x='Age',
    y='Percentage',
    color='Entrepreneurship',
    barmode='stack',
    facet_col='Current_Job_Level',
    category_orders={'Entrepreneurship': ['No', 'Yes']},
    color_discrete_map={'Yes': '#ff7f0e', 'No': '#d62728'},
    text=filtered_df['Percentage'].apply(lambda x: f"{x:.0%}"),
    height=600,
)

# --- 6. Tuỳ chỉnh biểu đồ ---
fig.update_layout(
    title=dict(
        text="📊 Entrepreneurship Rate by Age and Job Level",
        x=0.5,
        font=dict(size=20, color='black')
    ),
    legend_title_text='Entrepreneurship Status',
    bargap=0.1,
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    margin=dict(t=80, l=30, r=30, b=40),
)

fig.update_yaxes(tickformat=".0%", title="Percentage")
fig.update_traces(textposition='inside')

fig.update_traces(
    hovertemplate=
        '<b>Job Level:</b> %{facet_col}<br>' +
        '<b>Age:</b> %{x}<br>' +
        '<b>Status:</b> %{legendgroup}<br>' +
        '<b>Percentage:</b> %{y:.0%}<extra></extra>'
)

# --- 7. Hiển thị ---
st.title("💼 Education & Career Analysis Dashboard")
st.plotly_chart(fig, use_container_width=True)
