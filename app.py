import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load and preprocess data
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

df_grouped = df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship']).size().reset_index(name='Count')
df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# Sidebar toggle filter
st.sidebar.title("Settings")
show_filters = st.sidebar.checkbox("Show Filters", value=True)

# Filter values default
job_levels = sorted(df_grouped['Current_Job_Level'].unique())
min_age, max_age = int(df_grouped['Age'].min()), int(df_grouped['Age'].max())

if show_filters:
    selected_level = st.sidebar.selectbox("Select Job Level", job_levels)
    age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))
    selected_statuses = st.sidebar.multiselect("Select Entrepreneurship Status", ['Yes', 'No'], default=['Yes', 'No'])
else:
    # Mặc định khi ẩn filter
    selected_level = job_levels[0]
    age_range = (min_age, max_age)
    selected_statuses = ['Yes', 'No']

# Filter data
filtered = df_grouped[
    (df_grouped['Current_Job_Level'] == selected_level) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses)) &
    (df_grouped['Age'].between(age_range[0], age_range[1]))
]

def get_font_size(n):
    return {1: 20, 2: 18, 3: 16, 4: 14, 5: 12, 6: 11, 7: 10, 8: 9, 9: 8, 10: 7}.get(n, 6)

color_map = {'Yes': '#FFD700', 'No': '#004080'}

st.title("🚀 Education & Career Success Dashboard")

data = filtered
if data.empty:
    st.write(f"### {selected_level} – No data available")
else:
    ages = sorted(data['Age'].unique())
    font_size = get_font_size(len(ages))

    # Kích thước biểu đồ cố định (bỏ responsive)
    chart_width = 800
    chart_height = 400

    # Stacked Bar Chart (Percentage)
    fig_bar = px.bar(
        data,
        x='Age',
        y='Percentage',
        color='Entrepreneurship',
        barmode='stack',
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Percentage': 'Percentage'},
        height=chart_height,
        width=chart_width,
        title=f"{selected_level} Level – Entrepreneurship by Age (%)"
    )

    for status in ['No', 'Yes']:
        for _, row in data[data['Entrepreneurship'] == status].iterrows():
            if row['Percentage'] > 0:
                y_pos = 0.20 if status == 'No' else 0.90
                text = f"{row['Age']} y/o<br>{status}<br>{row['Percentage']:.0%}"
                fig_bar.add_annotation(
                    x=row['Age'],
                    y=y_pos,
                    text=text,
                    showarrow=False,
                    font=dict(color="white", size=font_size - 2),
                    xanchor="center",
                    yanchor="middle"
                )
    fig_bar.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90,
        bargap=0.1
    )
    fig_bar.update_yaxes(tickformat=".0%", title="Percentage")

    # Area Chart (Count) with markers
    fig_area = px.area(
        data,
        x='Age',
        y='Count',
        color='Entrepreneurship',
        markers=True,
        color_discrete_map=color_map,
        category_orders={'Entrepreneurship': ['No', 'Yes'], 'Age': ages},
        labels={'Age': 'Age', 'Count': 'Count'},
        height=chart_height,
        width=chart_width,
        title=f"{selected_level} Level – Entrepreneurship by Age (Count)"
    )

    for status in ['No', 'Yes']:
        status_data = data[data['Entrepreneurship'] == status]
        fig_area.add_trace(go.Scatter(
            x=status_data['Age'],
            y=status_data['Count'],
            mode='markers+text',
            name=f"{status}",
            text=[f"{age} y/o<br>{status}<br>{count} people" for age, count in zip(status_data['Age'], status_data['Count'])],
            textposition="top center",
            marker=dict(color=color_map[status], size=5),
            showlegend=False
        ))

    fig_area.update_traces(line=dict(width=2))
    fig_area.update_layout(
        margin=dict(t=40, l=40, r=40, b=40),
        legend_title_text='Entrepreneurship',
        xaxis_tickangle=90
    )
    fig_area.update_yaxes(title="Count")

    # Display charts side-by-side with equal width columns
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig_bar, use_container_width=True)
    with col2:
        st.plotly_chart(fig_area, use_container_width=True)
