import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Nhóm & tính phần trăm
df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Sidebar
st.sidebar.title("Filters")
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Job Levels", job_levels, default=job_levels)

min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship", statuses, default=statuses)

mode = st.sidebar.radio("Show as:", ["Percentage (%)", "Count"])

# Lọc dữ liệu
filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'] >= age_range[0]) &
    (df_grouped['Age'] <= age_range[1])
]

# Cấu hình
colors = {'Yes': '#FFD700', 'No': '#004080'}
order_levels = ['Entry', 'Executive', 'Mid', 'Senior']
levels_to_show = [lvl for lvl in order_levels if lvl in selected_levels]

st.title("🚀 Education & Career Success Dashboard")
cols = st.columns(2)

for i, lvl in enumerate(levels_to_show):
    data_lvl = filtered[filtered['Current_Job_Level'] == lvl]
    if data_lvl.empty:
        with cols[i % 2]:
            st.write(f"### {lvl} — No data")
        continue

    unique_ages = sorted(data_lvl['Age'].unique())
    num_bars = len(unique_ages)

    # Tính toán kích thước
    max_width = 1200
    min_width = 400
    bar_width_per_age = 60
    base_margin = 150
    chart_width = min(max(bar_width_per_age * num_bars + base_margin, min_width), max_width)

    # Tính font chữ dựa trên số cột
    font_size = max(6, min(18, int(chart_width / (num_bars * 3.5))))

    # Biểu đồ
    y_col = 'Percentage' if mode == "Percentage (%)" else 'Count'
    fmt = (lambda x: f"{x:.0%}") if mode == "Percentage (%)" else (lambda x: str(int(x)))
    y_axis_title = "Percentage" if mode == "Percentage (%)" else "Count"
    y_tick_format = ".0%" if mode == "Percentage (%)" else None

    fig = px.bar(
        data_lvl,
        x='Age',
        y=y_col,
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=colors,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': unique_ages},
        labels={'Age': 'Age', y_col: y_axis_title},
        height=400,
        width=chart_width,
        title=f"{lvl} Level"
    )

    # Gắn nhãn
    fig.update_traces(text='')  # Clear default labels
    bottoms = {age: 0 for age in unique_ages}
    stack_order = ['No', 'Yes']

    for status in stack_order:
        df_status = data_lvl[data_lvl['Entrepreneurship'] == status]
        for _, row in df_status.iterrows():
            age = row['Age']
            val = row[y_col]
            bottom = bottoms[age]
            if val == 0:
                continue

            y_pos = val * 0.5 if status == 'No' else bottom + val * 0.85
            fig.add_annotation(
                x=age,
                y=y_pos,
                text=fmt(val),
                showarrow=False,
                font=dict(color="white", size=font_size),
                xanchor="center",
                yanchor="middle"
            )
            bottoms[age] += val

    fig.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig.update_yaxes(title=y_axis_title)
    if y_tick_format:
        fig.update_yaxes(tickformat=y_tick_format)

    with cols[i % 2]:
        st.plotly_chart(fig, use_container_width=True)
