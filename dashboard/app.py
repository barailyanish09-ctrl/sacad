import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE = "https://sacad-api.onrender.com"

st.set_page_config(
    page_title="SACAD Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ SACAD — South Asia Cyber Attack Dataset")
st.caption("Open dataset of cyber attacks across South Asia")

@st.cache_data(ttl=60)
def fetch_stats():
    try:
        return requests.get(f"{API_BASE}/stats").json()
    except:
        return None

@st.cache_data(ttl=60)
def fetch_attacks(country=None, attack_type=None, sector=None):
    params = {"limit": 500}
    if country:     params["country"] = country
    if attack_type: params["attack_type"] = attack_type
    if sector:      params["sector"] = sector
    try:
        return requests.get(f"{API_BASE}/attacks", params=params).json()
    except:
        return []

stats = fetch_stats()

if stats:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Attacks", stats["total_attacks"])
    col2.metric("Last 30 Days", stats["recent_30_days"])
    col3.metric("Countries", len(stats["by_country"]))
    col4.metric("Sectors", len(stats["by_sector"]))
    st.divider()

with st.sidebar:
    st.header("🔍 Filters")
    country_filter = st.selectbox("Country", ["All", "Nepal", "India", "Bangladesh", "Pakistan", "Sri Lanka"])
    type_filter = st.selectbox("Attack Type", ["All", "phishing", "malware", "ransomware", "scam", "ddos", "data_breach"])
    sector_filter = st.selectbox("Sector", ["All", "banking", "government", "healthcare", "education", "telecom", "individual"])

if stats:
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Attacks by Country")
        df = pd.DataFrame(list(stats["by_country"].items()), columns=["Country", "Count"])
        fig = px.bar(df, x="Country", y="Count", color="Country")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Attack Types")
        df2 = pd.DataFrame(list(stats["by_attack_type"].items()), columns=["Type", "Count"])
        fig2 = px.pie(df2, names="Type", values="Count")
        st.plotly_chart(fig2, use_container_width=True)

    col_left2, col_right2 = st.columns(2)

    with col_left2:
        st.subheader("Targeted Sectors")
        df3 = pd.DataFrame(list(stats["by_sector"].items()), columns=["Sector", "Count"])
        fig3 = px.bar(df3, x="Count", y="Sector", orientation="h", color="Count", color_continuous_scale="Reds")
        st.plotly_chart(fig3, use_container_width=True)

    with col_right2:
        st.subheader("Severity Breakdown")
        df4 = pd.DataFrame(list(stats["by_severity"].items()), columns=["Severity", "Count"])
        fig4 = px.bar(df4, x="Severity", y="Count", color="Severity")
        st.plotly_chart(fig4, use_container_width=True)

st.divider()
st.subheader("📋 Attack Records")

attacks = fetch_attacks(
    country=None if country_filter == "All" else country_filter,
    attack_type=None if type_filter == "All" else type_filter,
    sector=None if sector_filter == "All" else sector_filter,
)

if attacks:
    df = pd.DataFrame(attacks)
    display_cols = ["id", "title", "country", "attack_type", "severity", "target_sector", "verified", "incident_date"]
    available = [c for c in display_cols if c in df.columns]
    st.dataframe(df[available], use_container_width=True, hide_index=True)
else:
    st.info("No records found. Make sure the API is running.")