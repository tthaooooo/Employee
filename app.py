import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc dữ liệu CSV
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Gom nhóm và tính phần trăm
df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Sidebar filters
st.sidebar.title("Filters")
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Job Levels", job_levels, default=job_levels)

min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship", statuses, default=statuses)

mode = st.sidebar.radio("Show as:", ["Percentage (%)", "Count"])

# Lọc dữ liệu theo filter
filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'] >= age_range[0]) &
    (df_grouped['Age'] <= age_range[1])
]

# Hàm xác định cỡ chữ theo số cột
def determine_font_size(num_bars):
    if num_bars <= 1: return 20
    elif num_bars == 2: return 18
    elif num_bars == 3: return 16
    elif num_bars == 4: return 14
    elif num_bars == 5: return 12
    elif num_bars == 6: return 11
    elif num_bars == 7: return 10
    elif num_bars == 8: return 9
    elif num_bars == 9: return 8
    elif num_bars == 10: return 7
    else:  # num_bars == 11
        return 6

# Cấu hình hiển thị
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

    # Cỡ chữ và width theo số cột
    font_size = determine_font_size(num_bars)
    chart_width = max(400, min(1200, 50 * num_bars + 100))

    # Chế độ hiển thị
    y_col = 'Percentage' if mode == "Percentage (%)" else 'Count'
    fmt = (lambda x: f"{x:.0%}") if mode == "Percentage (%)" else (lambda x: str(int(x)))
    y_axis_title = "Percentage" if mode == "Percentage (%)" else "Count"
    y_tick_format = ".0%" if mode == "Percentage (%)" else None

    # Tạo biểu đồ
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

    # Xóa label mặc định
    fig.update_traces(text='')

    # Gắn text tùy theo stack
    bottoms = {age: 0 for age in unique_ages}
    for status in ['No', 'Yes']:
        df_status = data_lvl[data_lvl['Entrepreneurship'] == status]
        for _, row in df_status.iterrows():
            age = row['Age']
            val = row[y_col]
            if val == 0:
                continue
            y_pos = val * 0.5 if status == 'No' else bottoms[age] + val * 0.85
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

    # Cập nhật layout
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
