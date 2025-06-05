import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Sidebar filters
st.sidebar.title("Filters")
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

# Filter data
filtered = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

# Font size based on number of bars
def get_font_size(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

# Chart colors
color_map = {'Yes': '#FFD700', 'No': '#004080'}

# Page title
st.title("🚀 Education & Career Success Dashboard")

data = filtered
if data.empty:
    st.write(f"### {selected_level} – No data available")
else:
    ages = sorted(data['Age'].unique())
    font_size = get_font_size(len(ages))

    # Stacked Bar Chart (Percentage)
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
        title=f"{selected_level} Level – Entrepreneurship by Age (%)"
    )

    for status in ['No', 'Yes']:
        for _, row in data[data['Entrepreneurship'] == status].iterrows():
            if row['Percentage'] > 0:
                y_pos = 0.20 if status == 'No' else 0.90
                fig_bar.add_annotation(
                    x=row['Age'],
                    y=y_pos,
                    text=f"{row['Percentage']:.0%}",
                    showarrow=False,
                    font=dict(color="white", size=font_size),
                    xanchor="center",
                    yanchor="middle"
                )

    fig_bar.update_layout(
        autosize=True,
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    # Area Chart (Count) with markers and annotations
    fig_area = px.area(
        data,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'},
        height=400,
        title=f"{selected_level} Level – Entrepreneurship by Age (Count)"
    )

    fig_area.update_traces(line=dict(width=2), marker=dict(size=4))

    for _, row in data.iterrows():
        fig_area.add_annotation(
            x=row['Age'],
            y=row['Count'],
            text=str(row['Count']),
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-25,
            font=dict(size=10),
            bgcolor='rgba(255,255,255,0.7)'
        )

    fig_area.update_layout(
        autosize=True,
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")

    # Display side-by-side with responsive width
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)
