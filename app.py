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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
        color: #4a5568;
        font-size: 15px;
        background-color: #f8fafc !important;
    }

    .main > div {
        background-color: #f8fafc;
        padding-top: 1rem;
    }

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 20px;
        color: #2d3748;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
    }

    .get-started-btn {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 1rem 2rem;
        border: none;
        border-radius: 50px;
        font-size: 18px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
        margin-top: 2rem;
        box-shadow: 0 10px 20px rgba(238, 90, 36, 0.3);
    }

    .get-started-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(238, 90, 36, 0.4);
    }

    .next-page-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.8rem 1.5rem;
        border: none;
        border-radius: 25px;
        font-size: 16px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 2rem auto;
        display: block;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }

    .next-page-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.4);
    }

    .stTabs > div > div > div > div {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
    }

    .code-container {
        background: linear-gradient(135deg, #1a202c, #2d3748);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
    }

    .code-title {
        color: #63b3ed;
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .team-section {
        background: white;
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-top: 3rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        text-align: center;
    }

    .team-member {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 8px 20px rgba(240, 147, 251, 0.3);
        transition: transform 0.3s ease;
    }

    .team-member:hover {
        transform: translateY(-5px);
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

# Create anchor points for navigation
def scroll_to_section(section_id):
    st.markdown(f'<div id="{section_id}"></div>', unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h1 style="font-size: 3rem; margin-bottom: 1rem; font-weight: 700;">
            🚀 Entrepreneurship Insights Dashboard
        </h1>
        <p style="font-size: 1.3rem; opacity: 0.9; margin-bottom: 2rem;">
            Khám phá dữ liệu và xu hướng kinh doanh với các biểu đồ tương tác mạnh mẽ
        </p>
        <a href="#team-section" class="get-started-btn">
            GET STARTED 🎯
        </a>
    </div>
""", unsafe_allow_html=True)

# Team Section
scroll_to_section("team-section")
st.markdown("""
    <div class="team-section">
        <h2 style="color: #2d3748; font-size: 2.5rem; margin-bottom: 2rem; font-weight: 700;">
            👥 Đội Ngũ Phát Triển
        </h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-top: 2rem;">
            <div class="team-member">
                <h3 style="margin-bottom: 0.5rem;">🎨 Frontend Developer</h3>
                <p>Thiết kế giao diện và trải nghiệm người dùng</p>
            </div>
            <div class="team-member">
                <h3 style="margin-bottom: 0.5rem;">📊 Data Analyst</h3>
                <p>Phân tích và xử lý dữ liệu kinh doanh</p>
            </div>
            <div class="team-member">
                <h3 style="margin-bottom: 0.5rem;">🛠️ Backend Engineer</h3>
                <p>Xây dựng hệ thống và API mạnh mẽ</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.title("🎛️ Filters")

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
    gender_filtered = df
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

# Soft color palette matching the light background
color_map = {'Yes': '#667eea', 'No': '#764ba2'}
soft_colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#63b3ed', '#68d391', '#fbb6ce', '#f6e05e']

# Main Tabs
tabs = st.tabs(["📈 Demographics", "📊 Job Offers", "💻 CODE"])

# === TAB 1 (Demographics) ===
with tabs[0]:
    st.markdown("""
        <h1 style='font-family: "Inter", sans-serif; color: #667eea; font-size: 40px; text-align: center; margin-bottom: 2rem;'>
            📊 Demographics Analysis
        </h1>
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
                st.markdown("""<div style="border: 2px solid #667eea; border-radius: 15px; padding: 25px; margin: 20px 0; background: linear-gradient(135deg, #f8fafc, #edf2f7); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1);">
                    <div style="display: flex; justify-content: space-around; text-align: center; line-height: 1.4;">
                        <div>
                            <div style="font-size: 14px; color: #667eea; font-weight: 600;">Total Records</div>
                            <div style="font-size: 32px; color: #2d3748; font-weight: 700;">{}</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #667eea; font-weight: 600;">Median Age</div>
                            <div style="font-size: 32px; color: #2d3748; font-weight: 700;">{:.1f}</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #667eea; font-weight: 600;">% Female</div>
                            <div style="font-size: 32px; color: #2d3748; font-weight: 700;">{:.1f}%</div>
                        </div>
                    </div></div>
                """.format(len(df_demo), df_demo['Age'].median(),
                           (df_demo['Gender'] == 'Female').mean() * 100),
                unsafe_allow_html=True)
        else:
            top_fields = df_demo['Field_of_Study'].value_counts().head(3).index.tolist()
            display_fields = ", ".join(top_fields) if top_fields else "N/A"
            with st.container():
                st.markdown("""<div style="border: 2px solid #667eea; border-radius: 15px; padding: 25px; margin: 20px 0; background: linear-gradient(135deg, #f8fafc, #edf2f7); box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1);">
                    <div style="display: flex; justify-content: space-around; text-align: center; line-height: 1.4;">
                        <div>
                            <div style="font-size: 14px; color: #667eea; font-weight: 600;">Total Records</div>
                            <div style="font-size: 32px; color: #2d3748; font-weight: 700;">{}</div>
                        </div>
                        <div>
                            <div style="font-size: 14px; color: #667eea; font-weight: 600;">Top 3 Fields</div>
                            <div style="font-size: 22px; color: #2d3748; font-weight: 600;">{}</div>
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

            for i, cat in enumerate(categories):
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
                        fill='tozeroy',
                        line=dict(color=soft_colors[i % len(soft_colors)], width=3),
                        fillcolor=f"rgba{(*[int(soft_colors[i % len(soft_colors)][j:j+2], 16) for j in (1, 3, 5)], 0.3)}"
                    ))

            fig_density.update_layout(
                paper_bgcolor='rgba(248, 250, 252, 0.8)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                title=dict(text=title, font=dict(size=18, color='#2d3748', family='Inter')),
                xaxis_title="Age",
                yaxis_title="Density",
                height=500,
                margin=dict(t=50, l=50, r=50, b=80),
                legend=dict(orientation="h", yanchor="bottom", y=-0.35, xanchor="center", x=0.5),
                font=dict(family='Inter', color='#4a5568')
            )
            st.plotly_chart(fig_density, use_container_width=True)

        with col2:
            group_col = 'Gender' if chart_option == 'Gender Distribution' else 'Field_of_Study'
            pie_data = df_demo[group_col].value_counts().reset_index()
            pie_data.columns = [group_col, 'Count']

            labels = pie_data[group_col]
            values = pie_data['Count']

            fig_donut = go.Figure(data=[
                go.Pie(
                    labels=labels,
                    values=values,
                    hole=0.5,
                    textinfo='percent+label',
                    insidetextorientation='radial',
                    marker=dict(
                        line=dict(color='#ffffff', width=3),
                        colors=soft_colors[:len(labels)]
                    ),
                    hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
                    textfont=dict(size=14, family='Inter')
                )
            ])

            fig_donut.update_layout(
                title={
                    'text': f"{group_col.replace('_', ' ')} Distribution",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': dict(size=18, color='#2d3748', family='Inter')
                },
                legend=dict(
                    orientation='h',
                    yanchor='bottom',
                    y=-0.3,
                    xanchor='center',  
                    x=0.5,
                    font=dict(size=12, family='Inter')
                ),
                height=500,
                margin=dict(t=50, l=20, r=20, b=80),
                paper_bgcolor='rgba(248, 250, 252, 0.8)',
                plot_bgcolor='rgba(255, 255, 255, 0.9)',
                font=dict(color='#4a5568', family='Inter')
            )

            st.plotly_chart(fig_donut, use_container_width=True)

        # Notes Section with improved styling
        note_style = """
        <div style="
            background: linear-gradient(135deg, #f8fafc, #edf2f7);
            border-left: 6px solid #667eea;
            padding: 25px;
            margin-top: 30px;
            border-radius: 15px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.1);
            font-family: 'Inter', sans-serif;
        ">
            <div style="font-size: 20px; font-weight: 700; margin-bottom: 12px; color: #667eea;">
                📌 {title}
            </div>
            <div style="font-size: 15px; color: #4a5568; line-height: 1.6;">
                {text}
            </div>
        </div>
        """

        if chart_option == 'Gender Distribution':
            note_col1, note_col2 = st.columns(2)
            with note_col1:
                st.markdown(
                    note_style.format(
                        title=f"Density Chart Insights ({selected_level})",
                        text=gender_density_notes.get(selected_level, "No density notes available.")
                    ),
                    unsafe_allow_html=True
                )
            with note_col2:
                st.markdown(
                    note_style.format(
                        title=f"Donut Chart Insights ({selected_level})",
                        text=gender_pie_notes.get(selected_level, "No donut chart notes available.")
                    ),
                    unsafe_allow_html=True
                )
        elif chart_option == 'Field of Study':
            st.markdown(
                note_style.format(
                    title=f"Field of Study Insights – {selected_level}",
                    text=field_of_study_notes.get(selected_level, "No notes for this level.")
                ),
                unsafe_allow_html=True
            )

    # Next page button
    st.markdown("""
        <button class="next-page-btn" onclick="document.querySelector('[data-testid=\"stTabs\"] button:nth-child(2)').click()">
            Next: Job Offers Analysis →
        </button>
    """, unsafe_allow_html=True)

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

with tabs[1]:
    st.markdown("""
        <h1 style='font-family: "Inter", sans-serif; color: #764ba2; font-size: 40px; text-align: center; margin-bottom: 2rem;'>
            📊 Job Offers Analysis
        </h1>
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
            st.markdown("""<div style="border: 2px solid #764ba2; border-radius: 15px; padding: 25px; margin: 20px 0; background: linear-gradient(135deg, #f8fafc, #edf2f7); box-shadow: 0 8px 25px rgba(118, 75, 162, 0.1);">
                <div style="display: flex; justify-content: space-around; text-align: center; line-height: 1.4;">
                    <div>
                        <div style="font-size: 14px; color: #764ba2; font-weight: 600;">Total Records</div>
                        <div style="font-size: 32px; color: #2d3748; font-weight: 700;">{}</div>
                    </div>
                    <div>
                        <div style="font-size: 14px; color: #764ba2; font-weight: 600;">Median Age</div>
                        <div style="font-size: 32px; color: #2d3748; font-weight: 700;">{:.1f}</div>
                    </div>
                    <div>
                        <div style="font-size: 14px; color: #764ba2; font-weight: 600;">Entrepreneurs (%)</div>
                        <div style="font-size: 32px; color: #2d3748; font-weight: 700;">{:.1f}%</div>
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
            title=f"Entrepreneurship Distribution by Age – {selected_level} Level"
        )

        fig_bar.update_traces(
            hovertemplate="Entrepreneurship=%{customdata[0]}<br>Age=%{x}<br>Percentage=%{y:.0%}<extra></extra>",
            customdata=df_bar[['Entrepreneurship']].values,
            hoverinfo="skip"
        )

        fig_bar.update_layout(
            paper_bgcolor='rgba(248, 250, 252, 0.8)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)',
            margin=dict(t=50, l=50, r=50, b=50),
            legend_title_text='Entrepreneurship',
            xaxis_tickangle=0,
            bargap=0.1,
            xaxis=dict(tickvals=even_ages),
            yaxis=dict(title="Percentage", range=[0, 1], tickformat=".0%"),
            legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5),
            font=dict(family='Inter', color='#4a5568'),
            title=dict(font=dict(size=18, color='#2d3748', family='Inter'))
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
                line=dict(color=color_map[status], width=4),
                marker=dict(size=8, line=dict(width=2, color='white')),
                hovertemplate="%{y:.2f}"
