import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('education_career_success.csv')

# Drop rows with missing required columns
required_cols = ['Current_Job_Level', 'Gender', 'Entrepreneurship']
df = df.dropna(subset=required_cols)
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar filter: Job Level
st.sidebar.title("Filters")
job_levels = sorted(df['Current_Job_Level'].unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Filter by Job Level
df_filtered = df[df['Current_Job_Level'] == selected_level]

# Check if data exists
if df_filtered.empty:
    st.warning(f"No data available for job level: {selected_level}")
    st.stop()

# Group data: Gender distribution within each Entrepreneurship group
for status in ['Yes', 'No']:
    subset = df_filtered[df_filtered['Entrepreneurship'] == status]
    if not subset.empty:
        gender_counts = subset['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        
        fig = px.pie(
            gender_counts,
            names='Gender',
            values='Count',
            title=f"Gender Distribution – Entrepreneurship: {status} – Level: {selected_level}",
            hole=0.4
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No data for Entrepreneurship = {status} at level {selected_level}")
