import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np
import plotly.express as px

# Load and preprocess data
df = pd.read_csv("education_career_success.csv")
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar filters
st.sidebar.title("Filters")

# Dropdown Job Level
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age range slider
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Dropdown for Entrepreneurship status
status_options = ['All', 'Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", status_options)

# Filter data based on selections
filtered_df = df[df['Current_Job_Level'] == selected_level]
filtered_df = filtered_df[filtered_df['Age'].between(age_range[0], age_range[1])]

if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Entrepreneurship'] == selected_status]

# Check if enough data exists
if filtered_df.empty or filtered_df['Gender'].nunique() < 2:
    st.write("Not enough data to display charts.")
else:
    col1, col2 = st.columns(2)

    # === Density Curve ===
    with col1:
        fig_density = go.Figure()
        genders = filtered_df['Gender'].unique()

        for gender in genders:
            gender_ages = filtered_df[filtered_df['Gender'] == gender]['Age']
            if len(gender_ages) > 1:
                kde = gaussian_kde(gender_ages)
                x_vals = np.linspace(age_range[0], age_range[1], 100)
                y_vals = kde(x_vals)

                fig_density.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines',
                    name=gender
                ))

        fig_density.update_layout(
            title="Density Curve of Age by Gender",
            xaxis_title="Age",
            yaxis_title="Density",
            height=500,
            margin=dict(t=40, l=40, r=40, b=40)
        )
        st.plotly_chart(fig_density, use_container_width=True)

    # === Donut Chart ===
    with col2:
        donut_data = filtered_df.groupby('Gender').size().reset_index(name='Count')
        fig_donut = px.pie(
            donut_data,
            values='Count',
            names='Gender',
            hole=0.5,
            title="Gender Distribution"
        )
        st.plotly_chart(fig_donut, use_container_width=True)
