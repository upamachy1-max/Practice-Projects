# Superstore Interactive Dashboard 

# Step 1: Import libraries

import streamlit as st              # For interactive dashboard
import pandas as pd                 # For data analysis
import seaborn as sns               # For charts
import matplotlib.pyplot as plt     # For charts

# Set Seaborn style and palette globally
sns.set_style("darkgrid")
sns.set_palette("Set2")

# Step 2: Load the Data

# @st.cache_data helps Streamlit load faster when data doesn't change
@st.cache_data
def load_data():
    df = pd.read_excel("superstore.xls")   
    return df

df = load_data()  # Load the data into a dataframe


# Step 3: Create Sidebar Filters

st.sidebar.header("Filters")

# Region Filter
regions = ["All"] + sorted(df["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Category Filter
categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)


# Step 4: Apply Filters to the Main Dataset

filtered_df = df.copy()

# Apply region filter
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

# Apply category filter
if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]


# Step 5: Summary Metrics (KPIs)

st.title("Superstore Sales Dashboard")

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
col3.metric("Total Quantity Sold", int(filtered_df["Quantity"].sum()))


# Step 6: Sales by Category (Bar Chart)

st.subheader("Sales by Category")

# Group data by Category and sum Sales
category_summary = (
    filtered_df.groupby("Category")[["Sales"]].sum().sort_values("Sales", ascending=False)
)

# Create Seaborn barplot with correct axis reference
fig1, ax1 = plt.subplots(figsize=(6,4))
sns.barplot(
    x=category_summary.index,
    y=category_summary["Sales"],
    ax=ax1                     
)

ax1.set_xlabel("Category")
ax1.set_ylabel("Total Sales")
ax1.set_title("Total Sales by Category")

st.pyplot(fig1)

# Step 6: Sales Over Time

st.subheader("Sales Over Time")
# Side note: group sales by date (daily). If many days exist, this will still work.
time_summary = filtered_df.groupby("Order Date")[["Sales"]].sum().sort_index()

fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(time_summary.index, time_summary["Sales"].values, marker="o", linestyle="-", linewidth=1.5, color="#2ca02c")
ax2.set_xlabel("Order Date")
ax2.set_ylabel("Sales")
ax2.set_title("Daily Sales Trend", fontsize=12, fontweight="bold")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig2)


# Step 7: Profit by Sub-Category

st.subheader("Profit by Sub-Category")
# Side note: aggregate profit by Sub-Category
subcat_summary = (
    filtered_df.groupby("Sub-Category", dropna=False)[["Profit"]]
    .sum()
    .sort_values("Profit", ascending=False)
)

fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.barplot(
    x=subcat_summary.index,
    y=subcat_summary["Profit"].values,
    ax=ax3,
    palette="coolwarm"   # side note: coolwarm provides a gradient emphasizing negative/positive values
)
ax3.set_xlabel("Sub-Category")
ax3.set_ylabel("Total Profit")
ax3.set_title("Profit by Sub-Category", fontsize=12, fontweight="bold")
plt.xticks(rotation=60)
plt.tight_layout()
st.pyplot(fig3)


