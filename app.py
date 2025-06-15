import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import numpy as np

st.set_page_config(page_title="Entrepreneurship Insights", layout="wide")

from utils import apply_global_styles
apply_global_styles()

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #52504d;
        font-size: 15px;
    }

    .main-title {
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 20px;
        color: #222;
    }
    </style>
""", unsafe_allow_html=True)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

local_css("style/style.css")

@st.cache_data
def load_data():
    return pd.read_excel("education_career_success.xlsx")

df = load_data()


# Sidebar Filters
st.sidebar.title("Filters")

gender_density_notes = {
    "Entry": """
        - Most individuals fall between ages 22–25, consistent with recent graduates starting careers.<br>
        - The peak density shows a sharp entry age, suggesting a clear transition from education to employment.<br>
    """,
    "Mid": """
        - Concentrated around ages 23–26, indicating this is a common stage for early career growth.<br>
        - The curve shifts right compared to Entry, reflecting natural career progression.<br>
    """,
    "Senior": """
        - Age distribution is flatter and slightly older (24–27), showing a range of career pacing.<br>
        - The peak is less sharp, indicating diverse timing in reaching senior roles.<br>
    """,
    "Executive": """
        - Surprisingly younger skew, with a peak at 22–25, suggesting some reach this level early, likely via entrepreneurship.<br>
        - A broader spread indicates both early achievers and experienced individuals.<br>
    """
}

gender_pie_notes = {
    "Entry": """
        - Gender distribution is nearly equal, suggesting balanced access to entry-level opportunities.<br>
        - Female and male participation rates are the highest at this level, indicating wide entry into the workforce.<br>
    """,
    "Mid": """
        - Male proportion slightly increases, showing a potential gender gap in career progression.<br>
        - Female representation remains relatively high, but slightly lower than entry-level.<br>
    """,
    "Senior": """
        - Gender representation becomes more balanced again, possibly reflecting equal long-term commitment.<br>
        - The total number is smaller, suggesting fewer people reach this stage.<br>
    """,
    "Executive": """
        - Males dominate this level, revealing a strong gender imbalance at the top.<br>
        - Female and other gender groups are significantly underrepresented.<br>
    """
}
field_of_study_notes = {
    "Entry": """
        - Entry-level individuals are mostly between ages 24–26, with peaks in Computer Science and Engineering.<br>
        - Study field distribution is fairly balanced, with Mathematics leading, reflecting the general demand for STEM-related roles.<br>
    """,
    "Mid": """
        - Average age ranges from 25–27, with Computer Science and Law showing the highest density.<br>
        - Study fields are quite diverse, with Law and Business being the most prominent, reflecting varied career trajectories at this stage.<br>
    """,
    "Senior": """
        - Senior-level participants have a wider age range, mostly around 24–26, particularly in Medicine and Business.<br>
        - Engineering is the most common study field, while Computer Science is less frequent—possibly due to the higher seniority typically required in technical roles.<br>
    """,
    "Executive": """
        - Age distribution is broader, peaking around 25–27; Law and Arts tend to have older participants.<br>
        - Arts and Mathematics dominate the study fields, while Business and Engineering are less represented, indicating more specialized paths at this level.<br>
    """
}


# Gender Filter - Multiselect
gender_options = sorted(df['Gender'].dropna().unique())
selected_genders = st.sidebar.multiselect("Select Gender(s)", gender_options, default=gender_options)

# Handle Gender Filter
if not selected_genders:
    st.sidebar.warning("⚠️ No gender selected. Using full data. Please choose at least one option.")
    gender_filtered = df  # fallback to full data to avoid crash
elif 'All' in selected_genders:
    gender_filtered = df
else:
    gender_filtered = df[df['Gender'].isin(selected_genders)]

# Job Level Filter
job_levels = sorted(df['Current_Job_Level'].dropna().unique())
selected_level = st.sidebar.selectbox("Select Job Level", job_levels)

# Age Filter
min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
age_range = st.sidebar.slider("Select Age Range", min_value=min_age, max_value=max_age, value=(min_age, max_age))

# Check if only one age selected
if age_range[0] == age_range[1]:
    st.sidebar.warning(f"⚠️ Only one age ({age_range[0]}) selected. Using full age range.")
    age_range = (min_age, max_age)

# Entrepreneurship Status Filter - Individual Checkboxes
st.sidebar.markdown("**Select Entrepreneurship Status**")
show_yes = st.sidebar.checkbox("Yes", value=True)
show_no = st.sidebar.checkbox("No", value=True)

selected_statuses = []
if show_yes:
    selected_statuses.append("Yes")
if show_no:
    selected_statuses.append("No")

if not (show_yes or show_no):
    st.sidebar.warning("⚠️ No status selected. Using full data. Please choose at least one option.")
    selected_statuses = ['Yes', 'No']

color_map = {'Yes': '#FFD700', 'No': '#004080'}

# Main Tabs
graph_tab = st.tabs(["📈 Demographics", "📊 Job Offers"])

# === TAB 1 (Demographics) ===
with graph_tab[0]:
    st.markdown("""
        <h1 style='font-family: "Inter", sans-serif; color: #cf5a2e; font-size: 40px;'>📊 Demographics</h1>
    """, unsafe_allow_html=True)
    
    chart_option = st.selectbox("Select Variable for Visualization", ['Gender Distribution', 'Field of Study'])

    df_demo = gender_filtered[
        (gender_filtered['Current_Job_Level'] == selected_level) &
        (gender_filtered['Age'].between(age_range[0], age_range[1])) &
        (gender_filtered['Entrepreneurship'].isin(selected_statuses))
    ]

    if df_demo.empty:
        st.warning("⚠️ Not enough data to display charts. Please adjust the filters.")
    else:
        if chart_option == 'Gender Distribution':
            with st.container():
                st.markdown("""<div style="border: 2px solid #cf5a2e; border-radius: 12px; padding: 20px; margin-top: 10px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-around; text-align: center; line-height: 1.3;">
                        <div>
                            <div style="font-size: 14px; color: #555;">Total Records</div>
                            <div style="font-size: 28px;">{}</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #555;">Median Age</div>
                            <div style="font-size: 28px;">{:.1f}</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #555;">% Female</div>
                            <div style="font-size: 28px;">{:.1f}%</div>
                        </div>
                    </div></div>
                """.format(len(df_demo), df_demo['Age'].median(),
                           (df_demo['Gender'] == 'Female').mean() * 100),
                unsafe_allow_html=True)

        else:
            top_fields = df_demo['Field_of_Study'].value_counts().head(3).index.tolist()
            display_fields = ", ".join(top_fields) if top_fields else "N/A"
            with st.container():
                st.markdown("""<div style="border: 2px solid #cf5a2e; border-radius: 12px; padding: 20px; margin-top: 10px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
                    <div style="display: flex; justify-content: space-around; text-align: center; line-height: 1.3;">
                        <div>
                            <div style="font-size: 14px; color: #555;">Total Records</div>
                            <div style="font-size: 28px;">{}</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #555;">Top 3 Fields</div>
                            <div style="font-size: 20px;">{}</div>
                        </div>
                    </div></div>
                """.format(len(df_demo), display_fields),
                unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            fig_density = go.Figure()
            group_col = 'Gender' if chart_option == 'Gender Distribution' else 'Field_of_Study'
            title = f"Age Distribution by {group_col.replace('_', ' ')}"
            categories = df_demo[group_col].dropna().unique()

            for cat in categories:
                age_data = df_demo[df_demo[group_col] == cat]['Age']
                if len(age_data) > 1:
                    kde = gaussian_kde(age_data)
                    x_vals = np.linspace(age_range[0], age_range[1], 100)
                    y_vals = kde(x_vals)
                    fig_density.add_trace(go.Scatter(
                        x=x_vals,
                        y=y_vals,
                        mode='lines',
                        name=str(cat),
                        fill='tozeroy'
                    ))

            fig_density.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                title=title,
                xaxis_title="Age",
                yaxis_title="Density",
                height=500,
                margin=dict(t=40, l=40, r=40, b=80),
                legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_density, use_container_width=True)

        with col2:
            group_col = 'Gender' if chart_option == 'Gender Distribution' else 'Field_of_Study'
            pie_data = df_demo[group_col].value_counts().reset_index()
            pie_data.columns = [group_col, 'Count']

            labels = pie_data[group_col]
            values = pie_data['Count']

            # Create donut chart with matching background
            fig_donut = go.Figure(data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.5,  # This creates the donut hole
                    textinfo='percent+label',
                    insidetextorientation='radial',
                    marker=dict(
                        line=dict(color='#ffffff', width=2),
                        colors=px.colors.qualitative.Set3  # You can customize colors here
                    ),
                    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>"
                )
            ])

            fig_donut.update_layout(
                title={
                    'text': f"{group_col.replace('_', ' ')} Distribution (Donut Chart)",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': dict(size=18, color='#333')
                },
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=-0.3,
                    xanchor='center',  
                    x=0.5,
                    font=dict(size=12)
                ),
                height=500,
                margin=dict(t=40, l=20, r=20, b=80),
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent background to match page
                plot_bgcolor='rgba(0,0,0,0)',   # Transparent plot area
                font=dict(color='#333')
            )

            st.plotly_chart(fig_donut, use_container_width=True)

        # === Notes Section ===
        note_style = """
        <div style="
            background-color: #fff4ec;
            border-left: 6px solid #cf5a2e;
            padding: 18px 22px;
            margin-top: 25px;
            border-radius: 12px;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
            font-family: 'Inter', sans-serif;
        ">
            <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px; color: #cf5a2e;">
                📌 {title}
            </div>
            <div style="font-size: 14px; color: #444;">
                {text}
            </div>
        </div>
        """

        if chart_option == 'Gender Distribution':
            note_col1, note_col2 = st.columns(2)

            with note_col1:
                st.markdown(
                    note_style.format(
                        title=f"{chart_option} – Density Chart Insight ({selected_level})",
                        text=gender_density_notes.get(selected_level, "No density notes available.") if chart_option == 'Gender Distribution' else ""
                    ),
                    unsafe_allow_html=True
                )

            with note_col2:
                st.markdown(
                    note_style.format(
                        title=f"{chart_option} – Donut Chart Insight ({selected_level})",
                        text=gender_pie_notes.get(selected_level, "No donut chart notes available.") if chart_option == 'Gender Distribution' else ""
                    ),
                    unsafe_allow_html=True
                )

        elif chart_option == 'Field of Study':
            st.markdown(
                note_style.format(
                    title=f"Field of Study Insight – {selected_level}",
                    text=field_of_study_notes.get(selected_level, "No notes for this level.")
                ),
                unsafe_allow_html=True
            )



# === TAB 2 (Job Offers) ===
job_level_notes = {
    "Entry": """
        - Majority of individuals across all ages do not pursue entrepreneurship.<br>
        - A slight increase in entrepreneurial interest is seen between ages 21–23.<br>
    """,
    "Mid": """
        - Entrepreneurship participation remains relatively steady, with slight increases around age 21–23.<br>
        - Majority still fall under the non-entrepreneurship group across all ages.<br>
    """,
    "Senior": """
        - A fairly balanced distribution between entrepreneurs and non-entrepreneurs, with some age groups showing higher entrepreneurship (e.g., age 29).<br>
        - Proportion of entrepreneurs is more prominent than in mid and entry levels.<br>
    """,
    "Executive": """
        - Entrepreneurship (Yes) fluctuates across ages, with no clear increasing or decreasing pattern.<br>
        - Ages 20–22 show a relatively higher proportion of entrepreneurship compared to other ages.<br>
    """
}

job_offers_notes = {
    "Entry": """
        - Individuals with entrepreneurial intentions generally receive more job offers, especially at ages 18, 26, and 28.<br>
        - Entrepreneurial individuals maintain a more stable or slightly upward trend in offers.<br>
    """,
    "Mid": """
        - Highest job offer spike for entrepreneurs occurs around age 27.<br>
        - Despite fluctuations, the difference in job offers between groups is generally narrow (within ~0.5).<br>
    """,
    "Senior": """
        - Sharp spike for entrepreneurs at age 29 indicates potential late-career success.<br>
        - Entrepreneurs face more volatility in job offers, suggesting high risk–high reward dynamics at senior levels.<br>
    """,
    "Executive": """
        - Peak job offers for entrepreneurs occur around age 27, suggesting growing opportunities with age.<br>
        - Fluctuations in entrepreneurial job offers imply less stability compared to non-entrepreneurs.<br>
    """
}

with graph_tab[1]:
    st.markdown("""
        <h1 style='font-family: "Inter", sans-serif; color: #cf5a2e; font-size: 36px;'>Job Offers</h1>
    """, unsafe_allow_html=True)

    df_filtered = gender_filtered[
        (gender_filtered['Current_Job_Level'] == selected_level) &
        (gender_filtered['Age'].between(age_range[0], age_range[1])) &
        (gender_filtered['Entrepreneurship'].isin(selected_statuses))
    ]

    if df_filtered.empty:
        st.warning("⚠️ Not enough data to display charts. Please adjust the filters.")
    else:
        with st.container():
            st.markdown("""<div style="border: 2px solid #cf5a2e; border-radius: 12px; padding: 20px; margin-top: 10px; margin-bottom: 30px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
                <div style="display: flex; justify-content: space-around; text-align: center; line-height: 1.3;">
                    <div>
                        <div style="font-size: 14px; color: #555;">Total Records</div>
                        <div style="font-size: 28px;">{}</div>
                    </div>
                    <div>
                        <div style="font-size: 14px; color: #555;">Median Age</div>
                        <div style="font-size: 28px;">{:.1f}</div>
                    </div>
                    <div>
                        <div style="font-size: 14px; color: #555;">Entrepreneurs (%)</div>
                        <div style="font-size: 28px;">{:.1f}%</div>
                    </div>
                </div></div>
            """.format(len(df_filtered), df_filtered['Age'].median(),
                       (df_filtered['Entrepreneurship'] == "Yes").mean() * 100),
            unsafe_allow_html=True)

        df_grouped = (
            df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
            .size()
            .reset_index(name='Count')
        )
        df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

        df_bar = df_grouped[
            (df_grouped['Current_Job_Level'] == selected_level) &
            (df_grouped['Age'].between(age_range[0], age_range[1])) &
            (df_grouped['Entrepreneurship'].isin(selected_statuses))
        ]

        even_ages = sorted(df_bar['Age'].unique())
        even_ages = [age for age in even_ages if age % 2 == 0]

        fig_bar = px.bar(
            df_bar,
            x='Age',
            y='Percentage',
            color='Entrepreneurship',
            barmode='stack',
            color_discrete_map=color_map,
            category_orders={'Entrepreneurship': ['No', 'Yes']},
            labels={'Age': 'Age', 'Percentage': 'Percentage'},
            height=450,
            width=1250,
            title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
        )

        fig_bar.update_traces(
            hovertemplate="Entrepreneurship=%{customdata[0]}<br>Age=%{x}<br>Percentage=%{y:.0%}<extra></extra>",
            customdata=df_bar[['Entrepreneurship']].values,
            hoverinfo="skip"
        )

        fig_bar.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=40, l=40, r=40, b=40),
            legend_title_text='Entrepreneurship',
            xaxis_tickangle=0,
            bargap=0.1,
            xaxis=dict(tickvals=even_ages),
            yaxis=dict(title="Percentage", range=[0, 1], tickformat=".0%"),
            legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
        )

        df_avg_offers = (
            df_filtered
            .groupby(['Age', 'Entrepreneurship'])['Job_Offers']
            .mean()
            .reset_index()
        )

        fig_line = go.Figure()
        for status in selected_statuses:
            data_status = df_avg_offers[df_avg_offers["Entrepreneurship"] == status]
            fig_line.add_trace(go.Scatter(
                x=data_status["Age"],
                y=data_status["Job_Offers"],
                mode="lines+markers",
                name=status,
                line=dict(color=color_map[status], width=2),
                marker=dict(size=6),
                hovertemplate="%{y:.2f}"
            ))

        fig_line.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            title=f"Average Job Offers by Age – {selected_level} Level",
            margin=dict(t=40, l=40, r=40, b=40),
            legend_title_text='Entrepreneurship',
            xaxis_tickangle=0,
            hovermode="x unified",
            width=1250,
            xaxis=dict(
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                spikethickness=1.2,
                spikedash='dot',
                tickvals=even_ages
            ),
            yaxis=dict(
                title="Average Job Offers",
                showspikes=True,
                spikemode='across',
                spikesnap='cursor',
                spikethickness=1.2,
                spikedash='dot',
                gridcolor='#b4adae'
            ),
            legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
        )

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.plotly_chart(fig_line, use_container_width=True)
            
        # Add dual note boxes below the two charts
        note_bar = job_level_notes.get(selected_level, "No specific notes available for this level.")
        note_line = job_offers_notes.get(selected_level, "No specific notes available for this level.")
        
        note_style = """
        <div style="
            background-color: #fff4ec;
            border-left: 6px solid #cf5a2e;
            padding: 18px 22px;
            margin-top: 25px;
            border-radius: 12px;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.05);
            font-family: 'Segoe UI', sans-serif;
        ">
            <div style="font-size: 18px; font-weight: 600; margin-bottom: 8px; color: #cf5a2e;">
                📌 {title}
            </div>
            <div style="font-size: 14px; color: #444;">
                {text}
            </div>
        </div>
        """
        
        note_col1, note_col2 = st.columns(2)
        
        with note_col1:
            st.markdown(note_style.format(title=f"Entrepreneurship Distribution Key Note – {selected_level}", text=note_bar), unsafe_allow_html=True)
        
        with note_col2:
            st.markdown(note_style.format(title=f"Average Job Offers Key Note – {selected_level}", text=note_line), unsafe_allow_html=True)
