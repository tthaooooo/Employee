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

ent_option = st.sidebar.selectbox("Entrepreneurship Status", ["All", "Yes", "No"])

min_age = int(df['Age'].min())
max_age = int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Filter data
df_filtered = df[df['Current_Job_Level'] == selected_level]
df_filtered = df_filtered[df_filtered['Age'].between(age_range[0], age_range[1])]

if ent_option != "All":
    df_filtered = df_filtered[df_filtered['Entrepreneurship'] == ent_option]

st.title("Entrepreneurship + Gender Analysis")

if df_filtered.empty:
    st.warning("No data available for selected filters.")
else:
    # Donut Chart
    pie_data = df_filtered['Gender'].value_counts().reset_index()
    pie_data.columns = ['Gender', 'Count']
    fig_donut = px.pie(
        pie_data,
        names='Gender',
        values='Count',
        hole=0.5,
        title="Gender Distribution (Donut)"
    )

    # KDE Line Chart using density estimate
    fig_kde = px.density_contour(
        df_filtered,
        x="Age",
        color="Gender",
        marginal="histogram",
        title="Age Distribution by Gender (Density Contour)"
    )

    # Display charts side by side
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        st.plotly_chart(fig_kde, use_container_width=True)
