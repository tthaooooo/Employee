import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load and preprocess data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Sidebar filters
st.sidebar.title("Filters")
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Select Job Levels", job_levels, default=job_levels)

min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# Filter data
filtered = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

# Font size adjustment based on bar count
def get_font_size(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

# Chart colors
color_map = {'Yes': '#FFD700', 'No': '#004080'}
level_order = ['Entry', 'Executive', 'Mid', 'Senior']
visible_levels = [lvl for lvl in level_order if lvl in selected_levels]

# Page title
st.title("🚀 Education & Career Success Dashboard")

# Display each level's charts
for level in visible_levels:
    data = filtered[filtered['Current_Job_Level'] == level]
    if data.empty:
        st.write(f"### {level} – No data available")
        continue

    ages = sorted(data['Age'].unique())
    font_size = get_font_size(len(ages))
    chart_width = max(400, min(1200, 50 * len(ages) + 100))

    # Stacked Bar Chart (Percentage) - only % text annotation
    fig_bar = px.bar(
        data,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=400,
        width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (%)"
    )

    # Add only % annotation inside bars
    for _, row in data.iterrows():
        if row['Percentage'] > 0:
            fig_bar.add_annotation(
                x=row['Age'],
                y=row['Percentage'] / 2,  # đặt annotation chính giữa thanh % stacked
                text=f"{row['Percentage']:.0%}",
                showarrow=False,
                font=dict(color="white", size=font_size),
                xanchor="center",
                yanchor="middle"
            )

    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    # Area Chart with markers only (no lines, no annotations except dots)
    fig_area = go.Figure()
    for status in ['No', 'Yes']:
        status_data = data[data['Entrepreneurship'] == status]
        fig_area.add_trace(go.Scatter(
            x=status_data['Age'],
            y=status_data['Count'],
            mode='markers',
            marker=dict(color=color_map[status], size=8),
            name=status
        ))

    fig_area.update_layout(
        height=400,
        width=chart_width,
        title=f"{level} Level – Entrepreneurship by Age (Count)",
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis=dict(title='Age', tickangle=90),
        yaxis=dict(title='Count')
    )

    # Show charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)
