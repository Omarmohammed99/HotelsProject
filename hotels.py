import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st

# Load hotels dataset
df = pd.read_csv("hotels.csv")

# PAGE SETUP
st.set_page_config(layout="wide", page_title="Hotel Bookings Dashboard")

# SIDEBAR
st.sidebar.header("Hotel Bookings Dashboard")
st.sidebar.image("hotelsPhoto.jpg")
st.sidebar.write("Explore hotel bookings data, cancellations, room types, and more.")

# FILTER
cat_filter = st.sidebar.selectbox(
    'Filter By:',
    ['hotel', 'country', 'customer_type', None]
)

# KPIs
k1, k2, k3 = st.columns(3)
k1.metric("Total Bookings", len(df))
k2.metric("Average Lead Time", f"{df['lead_time'].mean():.1f} days")
cancel_rate = (df['is_canceled'].sum() / len(df)) * 100
k3.metric("Cancellation Rate", f"{cancel_rate:.2f}%")

# Scatter Plot: Lead Time vs ADR
st.subheader("Lead Time vs Average Daily Rate (ADR)")
fig = px.scatter(
    df, x='lead_time', y='adr', color=cat_filter,
    size='adr', opacity=0.6,
    title="ADR by Lead Time Grouped by Selected Category"
)
st.plotly_chart(fig, use_container_width=True)

# Bar Plot: Average ADR by Hotel Type
st.subheader("Average ADR by Hotel Type")
avg_adr = df.groupby('hotel')['adr'].mean().reset_index()
fig1 = px.bar(avg_adr, x='hotel', y='adr', color='hotel', title="Average ADR")
st.plotly_chart(fig1, use_container_width=True)

# Pie Chart: Distribution of Customer Types
st.subheader("Customer Type Distribution")
cust_type = df['customer_type'].value_counts().reset_index()
cust_type.columns = ['Customer Type', 'Count']
fig2 = px.pie(cust_type, names='Customer Type', values='Count')
st.plotly_chart(fig2, use_container_width=False)

# Correlation Heatmap for numerical features
st.subheader("Correlation Heatmap")
num_cols = ['lead_time', 'adr', 'stays_in_weekend_nights', 'stays_in_week_nights',
            'adults', 'children', 'babies', 'previous_cancellations']
df_num = df[num_cols]
fig_corr, ax = plt.subplots(figsize=(7, 4))
sns.heatmap(df_num.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
st.pyplot(fig_corr)


st.set_page_config(page_title="Hotel Insights", layout="wide")

st.title("📊 Hotel Booking Insights")
st.sidebar.header("Insights Navigation")
insight_option = st.sidebar.selectbox("Select an Insight", [
    "1. Booking Distribution by Country",
    "2. Average Lead Time per Hotel",
    "3. Customer Type vs Hotel Bookings",
    "4. ADR by Hotel",
    "5. Cancellation Rate by Hotel",
    "6. Top 5 Room Types Reserved"
])

# 1. Booking Distribution by Country
if insight_option.startswith("1"):
    st.subheader("🌍 Booking Distribution by Country")
    country_booking = df['country'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=country_booking.index, y=country_booking.values, palette='plasma', ax=ax)
    ax.set_title("Top 10 Countries by Number of Bookings")
    ax.set_xlabel("Country")
    ax.set_ylabel("Number of Bookings")
    st.pyplot(fig)

# 2. Average Lead Time per Hotel
elif insight_option.startswith("2"):
    st.subheader("⏳ Average Lead Time per Hotel")
    avg_leadtime = df.groupby('hotel')['lead_time'].mean()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=avg_leadtime.index, y=avg_leadtime.values, palette='mako', ax=ax)
    ax.set_title("Average Lead Time per Hotel")
    ax.set_xlabel("Hotel")
    ax.set_ylabel("Average Lead Time (days)")
    st.pyplot(fig)

# 3. Customer Type vs Hotel Bookings
elif insight_option.startswith("3"):
    st.subheader("🧑‍💼 Customer Type vs Hotel Bookings")
    cus_hotel = df.groupby('customer_type')['hotel'].value_counts().reset_index(name='count')
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x='customer_type', y='count', hue='hotel', data=cus_hotel, palette='rocket', ax=ax)
    ax.set_title("Distribution of Customer Types by Hotel")
    ax.set_xlabel("Customer Type")
    ax.set_ylabel("Number of Bookings")
    st.pyplot(fig)

# 4. ADR by Hotel
elif insight_option.startswith("4"):
    st.subheader("💰 Average Daily Rate by Hotel")
    adr_avg = df.groupby('hotel')['adr'].mean().reset_index()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x='hotel', y='adr', data=adr_avg, palette='viridis', ax=ax)
    ax.set_title("ADR (Average Daily Rate) per Hotel")
    ax.set_ylabel("ADR (USD)")
    st.pyplot(fig)

# 5. Cancellation Rate by Hotel
elif insight_option.startswith("5"):
    st.subheader("❌ Cancellation Rate by Hotel")
    cancel_rate = df.groupby('hotel')['is_canceled'].mean().reset_index()
    cancel_rate['is_canceled'] *= 100  # Convert to percentage
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x='hotel', y='is_canceled', data=cancel_rate, palette='flare', ax=ax)
    ax.set_title("Cancellation Rate per Hotel (%)")
    ax.set_ylabel("Cancellation Rate (%)")
    st.pyplot(fig)

# 6. Top 5 Room Types Reserved
elif insight_option.startswith("6"):
    st.subheader("🛏️ Top 5 Reserved Room Types")
    top_rooms = df['reserved_room_type'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x=top_rooms.index, y=top_rooms.values, palette='crest', ax=ax)
    ax.set_title("Top 5 Room Types Reserved")
    ax.set_xlabel("Room Type")
    ax.set_ylabel("Number of Reservations")
    st.pyplot(fig)