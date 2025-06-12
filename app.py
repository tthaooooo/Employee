import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

# Load and preprocess
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
df = df.dropna(subset=['Age', 'Gender', 'Entrepreneurship', 'Current_Job_Level'])

# Sidebar filters
st.sidebar.title("Filters")

job_levels = sorted(df['Current_Job_Level'].unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

status_option = st.sidebar.selectbox("Entrepreneurship Status", ["All", "Yes", "No"])

min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Filter data
df_filtered = df[
    (df['Current_Job_Level'] == selected_level) &
    (df['Age'].between(age_range[0], age_range[1]))
]
if status_option != "All":
    df_filtered = df_filtered[df_filtered['Entrepreneurship'] == status_option]

if df_filtered.empty:
    st.warning("No data available for selected filters.")
else:
    st.title("Gender Distribution & Age Density Curve")

    # === Donut Chart ===
    gender_counts = df_filtered['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']
    fig_donut = go.Figure(data=[
        go.Pie(
            labels=gender_counts['Gender'],
            values=gender_counts['Count'],
            hole=0.5
        )
    ])
    fig_donut.update_layout(title="Gender Distribution (Donut Chart)")

    # === Density Curve ===
    fig_density = go.Figure()
    for gender in df_filtered['Gender'].unique():
        age_values = df_filtered[df_filtered['Gender'] == gender]['Age'].values
        if len(age_values) > 1:
            kde = gaussian_kde(age_values)
            x_vals = np.linspace(age_range[0], age_range[1], 200)
            y_vals = kde(x_vals)
            fig_density.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                name=gender
            ))

    fig_density.update_layout(
        title="Age Density Curve by Gender",
        xaxis_title="Age",
        yaxis_title="Density",
        height=400
    )

    # === Layout 2 chart song song ===
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        st.plotly_chart(fig_density, use_container_width=True)
