import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load data
df = pd.read_csv("education_career_success.csv")

# Drop rows with missing values in required columns
df = df.dropna(subset=['Work_Life_Balance', 'Years_to_Promotion', 'Current_Job_Level'])

# Group by Job Level and Years to Promotion
df_grouped = df.groupby(['Current_Job_Level', 'Years_to_Promotion']).agg({
    'Work_Life_Balance': 'mean'
}).reset_index()

# Order job levels
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
df_grouped['Current_Job_Level'] = pd.Categorical(df_grouped['Current_Job_Level'], categories=job_levels_order, ordered=True)

# Color map for consistency
color_map = {
    'Entry': '#1f77b4',
    'Mid': '#ff7f0e',
    'Senior': '#2ca02c',
    'Executive': '#d62728'
}

# Create the line chart with markers using go.Figure
fig = go.Figure()

for level in job_levels_order:
    level_data = df_grouped[df_grouped['Current_Job_Level'] == level]
    if not level_data.empty:
        avg_value = level_data['Work_Life_Balance'].mean()
        fig.add_trace(go.Scatter(
            x=level_data['Years_to_Promotion'],
            y=level_data['Work_Life_Balance'],
            mode='lines+markers',
            name=f"{level} : {avg_value:.2f}",
            line=dict(width=2, color=color_map[level]),
            marker=dict(symbol='circle', size=8)
        ))

# Add reference line (horizontal)
overall_avg = df['Work_Life_Balance'].mean()
fig.add_hline(y=overall_avg, line_dash="dot", line_color="black",
              annotation_text=f"Overall Avg: {overall_avg:.2f}",
              annotation_position="top left")

# Update layout
fig.update_layout(
    title="📊 Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    legend_title_text="Job Level",
    height=500,
    margin=dict(t=40, l=40, r=40, b=40)
)

# Make line thinner and responsive
fig.update_traces(line=dict(width=2))

# Show in Streamlit
st.title("💼 Work-Life Balance by Job Level and Promotion Timeline")
st.plotly_chart(fig, use_container_width=True)
