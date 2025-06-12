import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('education_career_success.csv')

# Drop missing values in required columns
required_cols = ['Current_Job_Level', 'Gender', 'Entrepreneurship', 'Age']
df = df.dropna(subset=required_cols)
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar filter: Job Level
st.sidebar.title("Filters")
job_levels = sorted(df['Current_Job_Level'].unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Filter data by job level
df_filtered = df[df['Current_Job_Level'] == selected_level]

st.header(f"Job Level: {selected_level}")

# --- Pie Charts by Gender within each Entrepreneurship status ---
st.subheader("Gender Distribution by Entrepreneurship")

cols = st.columns(2)
for i, status in enumerate(['Yes', 'No']):
    subset = df_filtered[df_filtered['Entrepreneurship'] == status]
    if not subset.empty:
        gender_counts = subset['Gender'].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        fig_pie = px.pie(
            gender_counts,
            names='Gender',
            values='Count',
            title=f"Entrepreneurship: {status}",
            hole=0.4
        )
        fig_pie.update_traces(textinfo='percent+label')
        cols[i].plotly_chart(fig_pie, use_container_width=True)
    else:
        cols[i].info(f"No data for Entrepreneurship = {status}")

# --- Line Chart: Age vs Count by Gender ---
st.subheader("Age Distribution by Gender")

line_data = df_filtered.groupby(['Age', 'Gender']).size().reset_index(name='Count')
fig_line = px.line(
    line_data,
    x='Age',
    y='Count',
    color='Gender',
    markers=True,
    title=f"Age Distribution by Gender – {selected_level}",
    labels={'Count': 'Number of People'}
)
st.plotly_chart(fig_line, use_container_width=True)
