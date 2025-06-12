import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar
st.sidebar.title("Filters")
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Filter theo Job Level
subset = df[df['Current_Job_Level'] == selected_level]

if subset.empty:
    st.warning(f"No data available for job level: {selected_level}")
else:
    for ent_status in ['Yes', 'No']:
        st.markdown(f"## Entrepreneurship: **{ent_status}**")

        df_ent = subset[subset['Entrepreneurship'] == ent_status]

        if df_ent.empty:
            st.info("No data for this group.")
            continue

        # Pie Chart: Gender Distribution
        pie_data = df_ent['Gender'].value_counts().reset_index()
        pie_data.columns = ['Gender', 'Count']
        fig_pie = px.pie(
            pie_data,
            names='Gender',
            values='Count',
            title="Gender Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        # Grouped Bar Chart: Age Distribution by Gender
        bar_data = df_ent.groupby(['Age', 'Gender']).size().reset_index(name='Count')
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

        # Hiển thị song song
        col1, col2 = st.columns(2)
        col1.plotly_chart(fig_pie, use_container_width=True)
        col2.plotly_chart(fig_bar, use_container_width=True)
