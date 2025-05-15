import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Load Data ---
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# --- 2. Group and Calculate ---
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)

# Calculate percentage within each (Job Level + Age) group
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# --- 3. Sidebar Filters ---
st.sidebar.title("🔍 Data Filters")

job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Select Job Levels", job_levels, default=job_levels)

ages = sorted(df_grouped['Age'].unique())
selected_ages = st.sidebar.multiselect("Select Ages", ages, default=ages)

statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Entrepreneurship Status", statuses, default=statuses)

# --- 4. Display Mode Toggle ---
st.sidebar.title("📊 Display Options")
mode = st.sidebar.radio("Show data as:", ["Percentage (%)", "Count"])

# --- 5. Apply Filters ---
filtered_df = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Age'].isin(selected_ages)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses))
]

# --- 6. Define Axis Labels and Tooltip ---
if mode == "Percentage (%)":
    y_col = "Percentage"
    y_label = "Percentage"
    text_values = filtered_df[y_col].apply(lambda x: f"{x:.0%}")
    y_format = ".0%"
else:
    y_col = "Count"
    y_label = "Count"
    text_values = filtered_df[y_col].astype(str)
    y_format = None

# --- 7. Create Plot ---
fig = px.bar(
    filtered_df,
    x='Age',
    y=y_col,
    color='Entrepreneurship',
    barmode='stack',
    facet_col='Current_Job_Level',
    category_orders={'Entrepreneurship': ['No', 'Yes']},
    color_discrete_map={'Yes': '#FFD700', 'No': '#004080'},  # Bright yellow and dark blue
    text=text_values,
    height=600,
    width=1200,
)

fig.update_layout(
    title=dict(
        text="📊 Entrepreneurship by Age and Job Level",
        x=0.5,
        font=dict(size=20)
    ),
    legend_title_text='Entrepreneurship',
    bargap=0.15,
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    margin=dict(t=80, l=40, r=40, b=50),
)

fig.update_yaxes(title=y_label)
if y_format:
    fig.update_yaxes(tickformat=y_format)

fig.update_traces(textposition='inside')

# ➤ Clean up facet titles
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# --- 8. Display in App ---
st.title("🚀 Education & Career Success Dashboard")
st.plotly_chart(fig, use_container_width=True)
