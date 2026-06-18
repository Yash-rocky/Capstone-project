import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------
# LIGHT THEME CSS
# ---------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #F8FAFC;
}

.main-title {
    text-align: center;
    color: #1E293B;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #64748B;
    margin-bottom: 20px;
}

.kpi-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
    text-align: center;
    margin-bottom: 15px;
}

.kpi-title {
    color: #64748B;
    font-size: 15px;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background-color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------
st.markdown(
    "<h1 class='main-title'>🛒 E-Commerce Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h4 class='subtitle'>Capstone Project Dashboard</h4>",
    unsafe_allow_html=True
)

# ---------------------------------------------------
# FILE UPLOAD
# ---------------------------------------------------
uploaded_file = st.file_uploader(
    "📂 Upload E-Commerce Dataset",
    type=["csv"]
)

if uploaded_file:

    # ---------------------------------------------------
    # LOAD DATA
    # ---------------------------------------------------
    df = pd.read_csv(uploaded_file)

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    # ---------------------------------------------------
    # SIDEBAR FILTERS
    # ---------------------------------------------------
    st.sidebar.header("🔍 Filters")

    selected_region = st.sidebar.multiselect(
        "Region",
        options=df["Region"].unique(),
        default=df["Region"].unique()
    )

    selected_category = st.sidebar.multiselect(
        "Category",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    start_date = st.sidebar.date_input(
        "Start Date",
        value=df["Order Date"].min()
    )

    end_date = st.sidebar.date_input(
        "End Date",
        value=df["Order Date"].max()
    )

    # ---------------------------------------------------
    # FILTER DATA
    # ---------------------------------------------------
    filtered_df = df[
        (df["Region"].isin(selected_region)) &
        (df["Category"].isin(selected_category)) &
        (df["Order Date"] >= pd.to_datetime(start_date)) &
        (df["Order Date"] <= pd.to_datetime(end_date))
    ]

    # ---------------------------------------------------
    # KPI CALCULATIONS
    # ---------------------------------------------------
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    total_orders = filtered_df["Order ID"].nunique()
    total_customers = filtered_df["Customer ID"].nunique()

    # ---------------------------------------------------
    # KPI CARDS
    # ---------------------------------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 Total Sales</div>
            <div class="kpi-value" style="color:#2563EB;">
                ₹{total_sales:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 Total Profit</div>
            <div class="kpi-value" style="color:#10B981;">
                ₹{total_profit:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🛒 Total Orders</div>
            <div class="kpi-value" style="color:#F59E0B;">
                {total_orders:,}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">👥 Customers</div>
            <div class="kpi-value" style="color:#8B5CF6;">
                {total_customers:,}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ---------------------------------------------------
    # MONTHLY SALES TREND
    # ---------------------------------------------------
    st.subheader("📈 Monthly Sales Trend")

    monthly_sales = (
        filtered_df.groupby(
            filtered_df["Order Date"].dt.to_period("M")
        )["Sales"]
        .sum()
        .reset_index()
    )

    monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

    fig_trend = px.line(
        monthly_sales,
        x="Order Date",
        y="Sales",
        markers=True,
        template="plotly_white",
        color_discrete_sequence=["#3B82F6"]
    )

    fig_trend.update_layout(height=400)

    st.plotly_chart(fig_trend, use_container_width=True)

    # ---------------------------------------------------
    # REGION & CATEGORY ANALYSIS
    # ---------------------------------------------------
    col5, col6 = st.columns(2)

    with col5:

        st.subheader("🌍 Sales by Region")

        region_sales = (
            filtered_df.groupby("Region")["Sales"]
            .sum()
            .reset_index()
        )

        fig_region = px.bar(
            region_sales,
            x="Region",
            y="Sales",
            color="Region",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        st.plotly_chart(
            fig_region,
            use_container_width=True
        )

    with col6:

        st.subheader("📦 Category Contribution")

        category_sales = (
            filtered_df.groupby("Category")["Sales"]
            .sum()
            .reset_index()
        )

        fig_category = px.pie(
            category_sales,
            names="Category",
            values="Sales",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        st.plotly_chart(
            fig_category,
            use_container_width=True
        )

    # ---------------------------------------------------
    # TOP PRODUCTS
    # ---------------------------------------------------
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_products = px.bar(
        top_products,
        x="Sales",
        y="Product Name",
        orientation="h",
        color="Sales",
        template="plotly_white",
        color_continuous_scale="Blues"
    )

    fig_products.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )

    # ---------------------------------------------------
    # TOP CUSTOMERS
    # ---------------------------------------------------
    st.subheader("👥 Top 10 Customers")

    top_customers = (
        filtered_df.groupby("Customer Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_customer = px.bar(
        top_customers,
        x="Sales",
        y="Customer Name",
        orientation="h",
        color="Sales",
        template="plotly_white",
        color_continuous_scale="Teal"
    )

    fig_customer.update_layout(
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig_customer,
        use_container_width=True
    )

    # ---------------------------------------------------
    # PROFIT VS SALES
    # ---------------------------------------------------
    st.subheader("💹 Profit vs Sales Analysis")

    fig_profit = px.scatter(
        filtered_df,
        x="Sales",
        y="Profit",
        color="Category",
        size="Quantity",
        hover_data=["Product Name"],
        template="plotly_white",
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )

    # ---------------------------------------------------
    # DISCOUNT ANALYSIS
    # ---------------------------------------------------
    if "Discount" in filtered_df.columns:

        st.subheader("🎯 Discount Impact on Profit")

        fig_discount = px.scatter(
            filtered_df,
            x="Discount",
            y="Profit",
            color="Category",
            template="plotly_white",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )

        st.plotly_chart(
            fig_discount,
            use_container_width=True
        )

    # ---------------------------------------------------
    # DATA TABLE
    # ---------------------------------------------------
    st.subheader("📋 Filtered Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=350
    )

    # ---------------------------------------------------
    # DOWNLOAD BUTTON
    # ---------------------------------------------------
    csv = filtered_df.to_csv(index=False)

    st.download_button(
        label="⬇ Download Filtered Data",
        data=csv,
        file_name="filtered_ecommerce_data.csv",
        mime="text/csv"
    )

else:
    st.info("📂 Please upload an E-Commerce CSV file to begin analysis.")