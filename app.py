import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar filters
st.sidebar.title("Filters")
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

selected_ent = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])

min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Filter data
df_filtered = df[
    (df['Current_Job_Level'] == selected_level) &
    (df['Entrepreneurship'].isin(selected_ent)) &
    (df['Age'].between(age_range[0], age_range[1]))
]

st.title("Entrepreneurship + Gender Analysis")
st.markdown(f"### Job Level: **{selected_level}**, Status: **{', '.join(selected_ent)}**")

if df_filtered.empty:
    st.warning("No data available for selected filters.")
else:
    # Donut Chart (default color)
    pie_data = df_filtered['Gender'].value_counts().reset_index()
    pie_data.columns = ['Gender', 'Count']
    fig_donut = px.pie(
        pie_data,
        names='Gender',
        values='Count',
        hole=0.5,
        title="Gender Distribution (Donut)"
    )

    # Grouped Bar Chart (default color)
    bar_data = df_filtered.groupby(['Age', 'Gender']).size().reset_index(name='Count')
    fig_bar = px.bar(
        bar_data,
        x='Age',
        y='Count',
        color='Gender',
        barmode='group',
        title="Age Distribution by Gender",
        labels={'Count': 'Number of People'}
    )
    fig_bar.update_layout(xaxis_tickangle=45)

    # Display charts side-by-side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        st.plotly_chart(fig_bar, use_container_width=True)
