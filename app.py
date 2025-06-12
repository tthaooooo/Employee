import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import gaussian_kde
import numpy as np

# Set page layout
st.set_page_config(page_title="Gender & Age Insights", layout="wide")

# Title & description
st.title("🎯 Gender & Age Insights")
st.markdown("Analyze age distribution and gender proportions by job level and entrepreneurship status.")

# Load and preprocess data
df = pd.read_csv("education_career_success.csv")
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# Sidebar filters
st.sidebar.title("Filters")

job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

status_options = ['All', 'Yes', 'No']
selected_status = st.sidebar.selectbox("Select Entrepreneurship Status", status_options)

# Apply filters
filtered_df = df[df['Current_Job_Level'] == selected_level]
filtered_df = filtered_df[filtered_df['Age'].between(age_range[0], age_range[1])]

if selected_status != 'All':
    filtered_df = filtered_df[filtered_df['Entrepreneurship'] == selected_status]

# Display charts
if filtered_df.empty or filtered_df['Gender'].nunique() < 2:
    st.warning("Not enough data to display charts.")
else:
    col1, col2 = st.columns([1, 1])

    # Histogram + Density Curve
    with col1:
        fig_combined = go.Figure()
        genders = filtered_df['Gender'].unique()
        colors = {'Male': 'blue', 'Female': 'red'}

        for gender in genders:
            gender_data = filtered_df[filtered_df['Gender'] == gender]
            gender_ages = gender_data['Age']
            
            # Histogram
            fig_combined.add_trace(go.Histogram(
                x=gender_ages,
                name=f"{gender} (hist)",
                opacity=0.5,
                marker_color=colors.get(gender, None),
                nbinsx=20
            ))

            # Density curve
            if len(gender_ages) > 1:
                kde = gaussian_kde(gender_ages)
                x_vals = np.linspace(age_range[0], age_range[1], 200)
                y_vals = kde(x_vals)
                fig_combined.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines',
                    name=f"{gender} (kde)",
                    line=dict(color=colors.get(gender, None), width=2)
                ))

        fig_combined.update_layout(
            title="Age Distribution by Gender (Histogram + Curve)",
            xaxis_title="Age",
            yaxis_title="Frequency / Density",
            barmode='overlay',
            height=500,
            margin=dict(t=40, l=40, r=40, b=40)
        )
        fig_combined.update_traces(opacity=0.6)
        st.plotly_chart(fig_combined, use_container_width=True)

    # Donut Chart
    with col2:
        donut_data = filtered_df.groupby('Gender').size().reset_index(name='Count')
        fig_donut = px.pie(
            donut_data,
            values='Count',
            names='Gender',
            hole=0.5,
            title="Gender Proportion"
        )
        fig_donut.update_layout(
            height=500,
            margin=dict(t=40, l=40, r=40, b=40)
        )
        st.plotly_chart(fig_donut, use_container_width=True)
