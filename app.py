import streamlit as st
import pandas as pd
import plotly.express as px

# Load and preprocess data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]
df = df[df['Gender'].notna()]  # loại bỏ dòng thiếu giới tính nếu có

# Sidebar filter for Job Level
st.sidebar.title("Filters")
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level for Heatmap", job_levels)

# Filter theo Job Level
df_filtered = df[df['Current_Job_Level'] == selected_level]

# Tính tỷ lệ khởi nghiệp theo Age và Gender
heat_df = (
    df_filtered.groupby(['Age', 'Gender'])['Entrepreneurship']
    .apply(lambda x: (x == 'Yes').mean())
    .reset_index(name='Entrepreneurship_Rate')
)

# Vẽ biểu đồ heatmap
fig_heatmap = px.density_heatmap(
    heat_df,
    x='Age',
    y='Gender',
    z='Entrepreneurship_Rate',
    color_continuous_scale='Viridis',
    title=f'Entrepreneurship Rate by Age and Gender – {selected_level} Level',
    labels={'Entrepreneurship_Rate': 'Rate of Entrepreneurship'}
)

fig_heatmap.update_layout(
    margin=dict(t=50, l=40, r=40, b=40),
    xaxis_title='Age',
    yaxis_title='Gender',
    coloraxis_colorbar=dict(title="Entrepreneurship Rate", tickformat=".0%")
)
fig_heatmap.update_traces(contours_coloring="none")

# Hiển thị biểu đồ
st.plotly_chart(fig_heatmap, use_container_width=True)
