import streamlit as st
import pandas as pd
import plotly.express as px

# --- (Phần load và xử lý dữ liệu giữ nguyên) ---

df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)

df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

st.sidebar.title("🔍 Data Filters")

job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Select Job Levels", job_levels, default=job_levels)

ages = sorted(df_grouped['Age'].unique())
ages_with_all = ['ALL'] + [str(age) for age in ages]
selected_ages = st.sidebar.multiselect("Select Ages", ages_with_all, default=['ALL'])

statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship Status", statuses, default=statuses)

st.sidebar.title("📊 Display Options")
mode = st.sidebar.radio("Show data as:", ["Percentage (%)", "Count"])

if 'ALL' in selected_ages:
    filtered_df = df_grouped[
        (df_grouped['Current_Job_Level'].isin(selected_levels)) &
        (df_grouped['Entrepreneurship'].isin(selected_statuses))
    ]
else:
    selected_ages_int = [int(age) for age in selected_ages]
    filtered_df = df_grouped[
        (df_grouped['Current_Job_Level'].isin(selected_levels)) &
        (df_grouped['Age'].isin(selected_ages_int)) &
        (df_grouped['Entrepreneurship'].isin(selected_statuses))
    ]

if mode == "Percentage (%)":
    y_col = "Percentage"
    y_label = "Percentage"
    def fmt_text(x): return f"{x:.0%}"
    y_format = ".0%"
else:
    y_col = "Count"
    y_label = "Count"
    def fmt_text(x): return str(x)
    y_format = None

color_map = {'Yes': '#FFD700', 'No': '#004080'}
job_levels_order = ['Entry', 'Executive', 'Mid', 'Senior']
job_levels_to_show = [lvl for lvl in job_levels_order if lvl in selected_levels]

st.title("🚀 Education & Career Success Dashboard")

# --- Tạo 2 cột ---
cols = st.columns(2)

# Chia 4 charts cho 2 cột, mỗi cột tối đa 2 chart
for i, lvl in enumerate(job_levels_to_show):
    df_lvl = filtered_df[filtered_df['Current_Job_Level'] == lvl]
    if df_lvl.empty:
        with cols[i % 2]:
            st.write(f"### {lvl} — No data to display.")
        continue

    fig = px.bar(
        df_lvl,
        x='Age',
        y=y_col,
        color='Entrepreneurship',
        barmode='stack',
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': sorted(df_lvl['Age'].unique())},
        color_discrete_map=color_map,
        text=df_lvl[y_col].apply(fmt_text),
        labels={'Age': 'Age', y_col: y_label},
        height=350,
        width=600,
        title=f"{lvl} Level"
    )
    fig.update_traces(textposition='inside', textangle=90)  # xoay text label phần trăm dọc theo thanh bar

    fig.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
    )

    fig.update_yaxes(title=y_label)
    if y_format:
        fig.update_yaxes(tickformat=y_format)

    with cols[i % 2]:
        st.plotly_chart(fig, use_container_width=True)
