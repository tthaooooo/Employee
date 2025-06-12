import streamlit as st
import pandas as pd
import plotly.express as px

# Load and filter data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar
st.sidebar.title("Filters")

job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

ent_status = st.sidebar.selectbox("Entrepreneurship Status", ["All", "Yes", "No"])

min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Filter
df_filtered = df[
    (df['Current_Job_Level'] == selected_level) &
    (df['Age'].between(age_range[0], age_range[1]))
]

if ent_status != "All":
    df_filtered = df_filtered[df_filtered['Entrepreneurship'] == ent_status]

# Check empty
if df_filtered.empty:
    st.warning("No data available for selected filters.")
else:
    st.title("Gender Distribution & Age Density by Job Level")

    # Donut chart
    pie_data = df_filtered['Gender'].value_counts().reset_index()
    pie_data.columns = ['Gender', 'Count']
    fig_donut = px.pie(
        pie_data,
        names='Gender',
        values='Count',
        hole=0.5,
        title="Gender Distribution"
    )

    # Density chart (Age vs Gender)
    fig_density = px.violin(
        df_filtered,
        x="Gender",
        y="Age",
        color="Gender",
        box=True,
        points="all",
        title="Age Distribution by Gender (Violin Density)",
    )

    # Layout
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        st.plotly_chart(fig_density, use_container_width=True)
