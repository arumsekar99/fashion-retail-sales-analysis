import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache
def load_data():
    # You should replace this with your actual data loading code
    data = pd.read_excel('cleaned_fashion_data.xlsx')
    return data

data = load_data()

# Title and Metrics
st.title("Fashion Boutique – Sales Returns & Customer Insights")
st.metric(label="Total Sales", value="142.35K")
st.metric(label="Avg. of Customer Rate", value="2.98")
st.metric(label="Return Rate", value="0.15")

# Average Customer Rating by Month
st.header("Average of Customer Rating by Month")
fig_month = px.line(data, x='Month', y='Average_Customer_Rating', markers=True)
st.plotly_chart(fig_month)

# Average Customer Rating by Brand
st.header("Average of Customer Rating by Brand")
fig_brand = px.line(data, x='Brand', y='Average_Customer_Rating', markers=True)
st.plotly_chart(fig_brand)

# Total Sales by Category (Pie Chart)
st.header("Total Sales by Category")
fig_category = px.pie(data, values='Sales', names='Category')
st.plotly_chart(fig_category)

# Total Sales by Season (Bar Chart)
st.header("Total Sales by Season")
fig_season = px.bar(data, x='Season', y='Sales', color='Season')
st.plotly_chart(fig_season)

# Total Sales by Brand (Horizontal Bar Chart)
st.header("Total Sales by Brand")
fig_sales_brand = px.bar(data, x='Sales', y='Brand', orientation='h')
st.plotly_chart(fig_sales_brand)
