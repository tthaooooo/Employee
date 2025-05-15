import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. Tải dữ liệu ---
df = pd.read_csv('education_career_success.csv')
df = df[df['Entrepreneurship'].isin(['Yes', 'No'])]

# --- 2. Tính toán ---
df_grouped = (
    df.groupby(['Current_Job_Level', 'Age', 'Entrepreneurship'])
    .size()
    .reset_index(name='Count')
)

df_grouped['Percentage'] = df_grouped.groupby(['Current_Job_Level', 'Age'])['Count'].transform(lambda x: x / x.sum())

# --- 3. Sidebar: Tùy chọn lọc ---
st.sidebar.title("🔍 Bộ lọc dữ liệu")

job_levels = sorted(df_grouped['Current_Job_Level'].unique())
selected_levels = st.sidebar.multiselect("Chọn cấp bậc công việc", job_levels, default=job_levels)

ages = sorted(df_grouped['Age'].unique())
selected_ages = st.sidebar.multiselect("Chọn độ tuổi", ages, default=ages)

statuses = ['Yes', 'No']
selected_statuses = st.sidebar.multiselect("Tình trạng khởi nghiệp", statuses, default=statuses)

# --- 4. Chế độ biểu đồ ---
st.sidebar.title("📊 Tùy chọn hiển thị")
mode = st.sidebar.radio("Hiển thị theo", ["Phần trăm (%)", "Số lượng (Count)"])

# --- 5. Lọc dữ liệu ---
filtered_df = df_grouped[
    (df_grouped['Current_Job_Level'].isin(selected_levels)) &
    (df_grouped['Age'].isin(selected_ages)) &
    (df_grouped['Entrepreneurship'].isin(selected_statuses))
]

# --- 6. Thiết lập trục y và nhãn ---
if mode == "Phần trăm (%)":
    y_col = "Percentage"
    y_label = "Percentage"
    text_values = filtered_df[y_col].apply(lambda x: f"{x:.0%}")
    y_format = ".0%"
else:
    y_col = "Count"
    y_label = "Count"
    text_values = filtered_df[y_col].astype(str)
    y_format = None

# --- 7. Tạo biểu đồ ---
fig = px.bar(
    filtered_df,
    x='Age',
    y=y_col,
    color='Entrepreneurship',
    barmode='stack',
    facet_col='Current_Job_Level',
    category_orders={'Entrepreneurship': ['No', 'Yes']},
    color_discrete_map={'Yes': '#1f77b4', 'No': '#ff7f0e'},
    text=text_values,
    height=600,
    width=1200,
)

fig.update_layout(
    title=dict(
        text="📊 Tỷ lệ hoặc số lượng người khởi nghiệp theo độ tuổi và cấp bậc công việc",
        x=0.5,
        font=dict(size=20)
    ),
    legend_title_text='Khởi nghiệp',
    bargap=0.15,
    uniformtext_minsize=8,
    uniformtext_mode='hide',
    margin=dict(t=80, l=40, r=40, b=50),
)

fig.update_yaxes(title=y_label)
if y_format:
    fig.update_yaxes(tickformat=y_format)

fig.update_traces(textposition='inside')

# ➤ Xóa tiền tố trong tiêu đề các biểu đồ con
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

# --- 8. Hiển thị ---
st.title("🚀 Phân tích nghề nghiệp & khởi nghiệp")
st.plotly_chart(fig, use_container_width=True)
