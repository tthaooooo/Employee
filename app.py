import streamlit as st
import pandas as pd
import plotly.express as px

# Load and filter data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Group and calculate percentages
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

mode = st.sidebar.radio("Display Mode:", ["Percentage (%)", "Count"])

# Filter data
filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'] >= age_range[0]) &
    (df_grouped['Age'] <= age_range[1])
]

# Determine dynamic font size based on number of bars
def get_font_size(num_bars):
    size_map = {
        1: 20, 2: 18, 3: 16, 4: 14, 5: 12,
        6: 11, 7: 10, 8: 9, 9: 8, 10: 7, 11: 6
    }
    return size_map.get(num_bars, 6)

# Display setup
color_map = {'Yes': '#FFD700', 'No': '#004080'}
level_order = ['Entry', 'Executive', 'Mid', 'Senior']
visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

st.title("🚀 Education & Career Success Dashboard")
cols = st.columns(2)

for i, level in enumerate(visible_levels):
    data = filtered[filtered['Current_Job_Level'] == level]
    if data.empty:
        with cols[i % 2]:
            st.write(f"### {level} — No data available")
        continue

    ages = sorted(data['Age'].unique())
    num_bars = len(ages)
    font_size = get_font_size(num_bars)

    chart_width = max(400, min(1200, 50 * num_bars + 100))

    y_col = 'Percentage' if mode == "Percentage (%)" else 'Count'
    value_format = (lambda x: f"{x:.0%}") if mode == "Percentage (%)" else (lambda x: str(int(x)))
    y_title = "Percentage" if mode == "Percentage (%)" else "Count"
    tick_format = ".0%" if mode == "Percentage (%)" else None

    fig = px.bar(
        data,
        x='Age',
        y=y_col,
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', y_col: y_title},
        height=400,
        width=chart_width,
        title=f"{level} Level"
    )

    fig.update_traces(text='')

    # Align labels horizontally for each color
    for status in ['No', 'Yes']:
        subset = data[data['Entrepreneurship'] == status]

        if mode == "Percentage (%)":
    y_pos = 0.20 if status == 'No' else 0.90  # tăng nhẹ vị trí
else:
    max_val = data[y_col].max()
    y_pos = max_val * (0.20 if status == 'No' else 0.90)

        for _, row in subset.iterrows():
            if row[y_col] == 0:
                continue
            fig.add_annotation(
                x=row['Age'],
                y=y_pos,
                text=value_format(row[y_col]),
                showarrow=False,
                font=dict(color="white", size=font_size),
                xanchor="center",
                yanchor="middle"
            )

    fig.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig.update_yaxes(title=y_title)
    if tick_format:
        fig.update_yaxes(tickformat=tick_format)

    with cols[i % 2]:
        st.plotly_chart(fig, use_container_width=True)
