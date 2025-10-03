import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 🧭 1. PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Fashion Retail Dashboard",
    page_icon="👗",
    layout="wide",
)

# =========================
# 📥 2. LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("cleaned_fashion_data.xlsx")
    return df

data = load_data()

# =========================
# 🧼 3. DATA PREPROCESSING
# =========================
# 🧼 Pastikan kolom tanggal diproses dengan benar
if 'Purchased Date' in data.columns:
    data['purchase_date'] = pd.to_datetime(data['purchase_date'], errors='coerce')
    data['Month_Name'] = data['purchase_date'].dt.strftime('%B')

# =========================
# 🧾 4. HEADER SECTION
# =========================
st.title("👗 Fashion Boutique — Sales, Returns & Customer Insights")

# =========================
# 🧮 5. KPI METRICS (pakai Current_Price)
# =========================
total_sales = data['current_price'].sum()
avg_rating = data['customer_rating'].mean()
return_rate = data['is_returned'].mean() if 'is_returned' in data.columns else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sales (Current Price)", f"{total_sales:,.0f}")
with col2:
    st.metric("Avg of Customer Rate", f"{avg_rating:.2f}")
with col3:
    st.metric("Return Rate", f"{return_rate:.2f}")

# =========================
# 📈 6. CHARTS — Top Row
# =========================
col_a, col_b = st.columns(2)

# -- Line chart: Rating by Month
if 'Month_Name' in data.columns:
    with col_a:
        monthly_avg = data.groupby('Month_Name')['Average_Customer_Rating'].mean().reindex(
            ['January','February','March','April','May','June','July','August','September','October','November','December']
        )
        fig_month = px.line(
            monthly_avg,
            x=monthly_avg.index,
            y=monthly_avg.values,
            markers=True,
            title="Average of Customer Rating by Month"
        )
        fig_month.update_traces(line=dict(color="#b33b3b", width=3))
        fig_month.update_layout(xaxis_title="", yaxis_title="Rating")
        st.plotly_chart(fig_month, use_container_width=True)

# -- Line chart: Rating by Brand
if 'Brand' in data.columns:
    with col_b:
        brand_avg = data.groupby('Brand')['Average_Customer_Rating'].mean().sort_values(ascending=False)
        fig_brand_rating = px.line(
            brand_avg,
            x=brand_avg.index,
            y=brand_avg.values,
            markers=True,
            title="Average of Customer Rating by Brand"
        )
        fig_brand_rating.update_traces(line=dict(color="#b33b3b", width=3))
        fig_brand_rating.update_layout(xaxis_title="", yaxis_title="Rating")
        st.plotly_chart(fig_brand_rating, use_container_width=True)

# =========================
# 📊 7. CHARTS — Bottom Row
# =========================
col_c, col_d, col_e = st.columns([1,1,1.2])

# -- Pie chart: Sales by Category
if 'Category' in data.columns:
    with col_c:
        cat_sales = data.groupby('Category')['Current_Price'].sum()
        fig_cat = px.pie(
            names=cat_sales.index,
            values=cat_sales.values,
            title="Total Sales by Category (Current Price)",
            hole=0.3
        )
        st.plotly_chart(fig_cat, use_container_width=True)

# -- Bar chart: Sales by Season
if 'Season' in data.columns:
    with col_d:
        season_sales = data.groupby('Season')['Current_Price'].sum()
        fig_season = px.bar(
            x=season_sales.index,
            y=season_sales.values,
            text=season_sales.values,
            title="Total Sales by Season (Current Price)"
        )
        fig_season.update_traces(marker_color=["#e76f51", "#f4a261", "#e9c46a", "#f4a261"], textposition='outside')
        fig_season.update_layout(xaxis_title="", yaxis_title="Sales")
        st.plotly_chart(fig_season, use_container_width=True)

# -- Bar chart: Sales by Brand
if 'Brand' in data.columns:
    with col_e:
        brand_sales = data.groupby('Brand')['Current_Price'].sum().sort_values(ascending=False)
        fig_brand = px.bar(
            x=brand_sales.values,
            y=brand_sales.index,
            orientation='h',
            text=brand_sales.values,
            title="Total Sales by Brand (Current Price)"
        )
        fig_brand.update_traces(marker_color="#e07a5f", textposition='outside')
        fig_brand.update_layout(xaxis_title="Sales", yaxis_title="")
        st.plotly_chart(fig_brand, use_container_width=True)
