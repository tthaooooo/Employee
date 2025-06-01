import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("education_career_success.csv")

# Drop rows with missing values in required columns
df = df.dropna(subset=['Work_Life_Balance', 'Years_to_Promotion', 'Current_Job_Level'])

# Grouped data for bar chart
df_grouped_bar = df.groupby(['Current_Job_Level', 'Years_to_Promotion']).agg({
    'Work_Life_Balance': 'mean'
}).reset_index()

# Grouped data for line chart
job_levels_order = ['Entry', 'Mid', 'Senior', 'Executive']
df_grouped_line = df_grouped_bar.copy()
df_grouped_line['Current_Job_Level'] = pd.Categorical(df_grouped_line['Current_Job_Level'], categories=job_levels_order, ordered=True)

# Color map
color_map = {
    'Entry': '#1f77b4',
    'Mid': '#ff7f0e',
    'Senior': '#2ca02c',
    'Executive': '#d62728'
}

# Line chart with custom legend
fig_line = go.Figure()
for level in job_levels_order:
    level_data = df_grouped_line[df_grouped_line['Current_Job_Level'] == level]
    if not level_data.empty:
        avg_value = level_data['Work_Life_Balance'].mean()
        fig_line.add_trace(go.Scatter(
            x=level_data['Years_to_Promotion'],
            y=level_data['Work_Life_Balance'],
            mode='lines+markers',
            name=f"{level} : {avg_value:.2f}",
            line=dict(width=2, color=color_map[level]),
            marker=dict(symbol='circle', size=8)
        ))

# Add reference line
overall_avg = df['Work_Life_Balance'].mean()
fig_line.add_hline(y=overall_avg, line_dash="dot", line_color="black",
              annotation_text=f"Overall Avg: {overall_avg:.2f}",
              annotation_position="top left")

fig_line.update_layout(
    title="📊 Average Work-Life Balance by Years to Promotion",
    xaxis_title="Years to Promotion",
    yaxis_title="Average Work-Life Balance",
    legend_title_text="Job Level",
    height=500,
    margin=dict(t=40, l=40, r=40, b=40)
)

# Stacked bar chart
df_grouped_stacked = df.groupby(['Years_to_Promotion', 'Current_Job_Level']).agg({
    'Work_Life_Balance': 'mean'
}).reset_index()

fig_stacked = px.bar(df_grouped_stacked,
                     x='Years_to_Promotion',
                     y='Work_Life_Balance',
                     color='Current_Job_Level',
                     color_discrete_map=color_map,
                     title="Stacked Work-Life Balance by Years to Promotion",
                     labels={
                         'Years_to_Promotion': 'Years to Promotion',
                         'Work_Life_Balance': 'Average Work-Life Balance',
                         'Current_Job_Level': 'Job Level'
                     })
fig_stacked.update_layout(barmode='stack', height=500, margin=dict(t=40, l=40, r=40, b=40))

# Streamlit display
st.title("💼 Work-Life Balance by Job Level and Promotion Timeline")
st.plotly_chart(fig_line, use_container_width=True)
st.plotly_chart(fig_stacked, use_container_width=True)
