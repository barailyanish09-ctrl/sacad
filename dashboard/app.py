import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

API_BASE = "https://sacad-api.onrender.com"

st.set_page_config(
    page_title="SACAD — South Asia Cyber Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Dark cyber theme ──
st.markdown("""
<style>
    .stApp { background-color: #0a0e1a; color: #e2e8f0; }
    .metric-card {
        background: linear-gradient(135deg, #1a1f35, #0d1226);
        border: 1px solid #2d3748;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value { font-size: 2.5rem; font-weight: 800; color: #63b3ed; }
    .metric-label { font-size: 0.85rem; color: #a0aec0; text-transform: uppercase; letter-spacing: 1px; }
    .critical { color: #fc8181 !important; }
    .high { color: #f6ad55 !important; }
    .medium { color: #f6e05e !important; }
    .low { color: #68d391 !important; }
    .header-title {
        font-size: 2.2rem;
        font-weight: 900;
        background: linear-gradient(90deg, #63b3ed, #76e4f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sidebar .sidebar-content { background-color: #0d1226; }
    div[data-testid="stSidebar"] { background-color: #0d1226; }
    .stDataFrame { background-color: #1a1f35; }
</style>
""", unsafe_allow_html=True)

# ── Header ──
st.markdown('<p class="header-title">🛡️ SACAD — South Asia Cyber Threat Intelligence</p>', unsafe_allow_html=True)
st.markdown("**The open cyber attack graph for South Asia** · Live dataset of real incidents, IoCs, and targets")
st.divider()

# ── Data fetching ──
@st.cache_data(ttl=60)
def fetch_stats():
    try:
        return requests.get(f"{API_BASE}/stats", timeout=10).json()
    except:
        return None

@st.cache_data(ttl=60)
def fetch_attacks(country=None, attack_type=None, sector=None, severity=None):
    params = {"limit": 500}
    if country:     params["country"] = country
    if attack_type: params["attack_type"] = attack_type
    if sector:      params["sector"] = sector
    if severity:    params["severity"] = severity
    try:
        return requests.get(f"{API_BASE}/attacks", params=params, timeout=10).json()
    except:
        return []

@st.cache_data(ttl=60)
def fetch_recent():
    try:
        return requests.get(f"{API_BASE}/attacks/recent?limit=5", timeout=10).json()
    except:
        return []

stats   = fetch_stats()
recent  = fetch_recent()

# ── KPI Cards ──
if stats:
    c1, c2, c3, c4, c5 = st.columns(5)
    cards = [
        (c1, stats["total_attacks"], "Total Attacks", ""),
        (c2, stats["recent_30_days"], "Last 30 Days", ""),
        (c3, len(stats["by_country"]), "Countries", ""),
        (c4, len(stats["by_sector"]), "Sectors Hit", ""),
        (c5, stats["by_severity"].get("critical", 0), "Critical", "critical"),
    ]
    for col, val, label, cls in cards:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value {cls}">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """, unsafe_allow_html=True)
    st.divider()

# ── Sidebar ──
with st.sidebar:
    st.markdown("### 🔍 Filters")
    country_filter  = st.selectbox("Country",     ["All", "Nepal", "India", "Bangladesh", "Pakistan", "Sri Lanka"])
    type_filter     = st.selectbox("Attack Type", ["All", "phishing", "malware", "ransomware", "defacement", "ddos", "data_breach", "scam"])
    sector_filter   = st.selectbox("Sector",      ["All", "banking", "government", "healthcare", "education", "telecom", "individual"])
    severity_filter = st.selectbox("Severity",    ["All", "critical", "high", "medium", "low"])
    st.divider()
    st.markdown("### 🔗 Links")
    st.markdown("[📡 Live API](https://sacad-api.onrender.com)")
    st.markdown("[📖 API Docs](https://sacad-api.onrender.com/docs)")
    st.markdown("[💻 GitHub](https://github.com/barailyanish09-ctrl/sacad)")

# ── Charts ──
COLORS = ["#63b3ed","#76e4f7","#68d391","#f6ad55","#fc8181","#b794f4","#fbb6ce","#90cdf4"]

if stats:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🌏 Attacks by Country")
        df = pd.DataFrame(list(stats["by_country"].items()), columns=["Country", "Count"])
        fig = px.bar(df, x="Country", y="Count", color="Country",
                     color_discrete_sequence=COLORS,
                     template="plotly_dark")
        fig.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1226", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### ⚡ Attack Types")
        df2 = pd.DataFrame(list(stats["by_attack_type"].items()), columns=["Type", "Count"])
        fig2 = px.pie(df2, names="Type", values="Count",
                      color_discrete_sequence=COLORS,
                      template="plotly_dark", hole=0.4)
        fig2.update_layout(paper_bgcolor="#0a0e1a")
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("#### 🏢 Targeted Sectors")
        df3 = pd.DataFrame(list(stats["by_sector"].items()), columns=["Sector", "Count"])
        fig3 = px.bar(df3, x="Count", y="Sector", orientation="h",
                      color="Count", color_continuous_scale="Blues",
                      template="plotly_dark")
        fig3.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1226")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("#### 🚨 Severity Breakdown")
        df4 = pd.DataFrame(list(stats["by_severity"].items()), columns=["Severity", "Count"])
        sev_colors = {"critical": "#fc8181", "high": "#f6ad55", "medium": "#f6e05e", "low": "#68d391"}
        fig4 = px.bar(df4, x="Severity", y="Count", color="Severity",
                      color_discrete_map=sev_colors,
                      template="plotly_dark")
        fig4.update_layout(paper_bgcolor="#0a0e1a", plot_bgcolor="#0d1226", showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

# ── Recent Attacks ──
st.divider()
st.markdown("#### 🕐 Most Recent Attacks")
if recent:
    for a in recent:
        sev = a.get("severity", "medium")
        sev_colors = {"critical": "#fc8181", "high": "#f6ad55", "medium": "#f6e05e", "low": "#68d391"}
        color = sev_colors.get(sev, "#a0aec0")
        st.markdown(f"""
        <div style="background:#1a1f35;border-left:4px solid {color};padding:10px 16px;margin:6px 0;border-radius:6px;">
            <strong>{a.get('title','')}</strong> &nbsp;
            <span style="color:{color};font-size:0.8rem;">● {sev.upper()}</span> &nbsp;
            <span style="color:#a0aec0;font-size:0.8rem;">{a.get('country','')} · {a.get('attack_type','')} · {a.get('target_sector','')}</span>
        </div>
        """, unsafe_allow_html=True)

# ── Attack Records Table ──
st.divider()
st.markdown("#### 📋 Attack Records")

attacks = fetch_attacks(
    country=None  if country_filter  == "All" else country_filter,
    attack_type=None if type_filter  == "All" else type_filter,
    sector=None   if sector_filter   == "All" else sector_filter,
    severity=None if severity_filter == "All" else severity_filter,
)

if attacks:
    df = pd.DataFrame(attacks)
    cols = ["id","title","country","attack_type","severity","target_sector","status","incident_date"]
    available = [c for c in cols if c in df.columns]
    st.dataframe(df[available], use_container_width=True, hide_index=True)
    st.caption(f"Showing {len(df)} records · API: sacad-api.onrender.com")
else:
    st.info("No records found. Try adjusting filters.")

# ── Threat Map ──
st.divider()
st.markdown("#### 🗺️ Global Threat Map")

if attacks:
    map_data = []
    coords = {
        "Nepal":      (28.3949, 84.1240),
        "India":      (20.5937, 78.9629),
        "Bangladesh": (23.6850, 90.3563),
        "Pakistan":   (30.3753, 69.3451),
        "Sri Lanka":  (7.8731,  80.7718),
        "Bhutan":     (27.5142, 90.4336),
        "Myanmar":    (21.9162, 95.9560),
        "Regional":   (23.0000, 80.0000),
    }
    sev_colors = {
        "critical": "#fc8181",
        "high":     "#f6ad55",
        "medium":   "#f6e05e",
        "low":      "#68d391"
    }
    for a in attacks:
        country = a.get("country", "")
        if country in coords:
            lat, lon = coords[country]
            import random
            lat += random.uniform(-1.5, 1.5)
            lon += random.uniform(-1.5, 1.5)
            map_data.append({
                "lat":    lat,
                "lon":    lon,
                "title":  a.get("title", ""),
                "country": country,
                "type":   a.get("attack_type", ""),
                "severity": a.get("severity", "medium"),
                "sector": a.get("target_sector", ""),
                "color":  sev_colors.get(a.get("severity", "medium"), "#a0aec0")
            })

    if map_data:
        map_df = pd.DataFrame(map_data)
        fig_map = go.Figure()
        for sev, color in sev_colors.items():
            subset = map_df[map_df["severity"] == sev]
            if not subset.empty:
                fig_map.add_trace(go.Scattergeo(
                    lat=subset["lat"],
                    lon=subset["lon"],
                    mode="markers",
                    name=sev.upper(),
                    marker=dict(size=12, color=color, opacity=0.85,
                                line=dict(width=1, color="#0a0e1a")),
                    text=subset.apply(lambda r: f"{r['title']}<br>{r['country']} · {r['type']}<br>Sector: {r['sector']}", axis=1),
                    hoverinfo="text"
                ))
        fig_map.update_layout(
            geo=dict(
                scope="asia",
                showland=True, landcolor="#1a1f35",
                showocean=True, oceancolor="#0a0e1a",
                showcoastlines=True, coastlinecolor="#2d3748",
                showcountries=True, countrycolor="#2d3748",
                bgcolor="#0a0e1a",
                center=dict(lat=23, lon=82),
                projection_scale=3.5,
            ),
            paper_bgcolor="#0a0e1a",
            legend=dict(bgcolor="#1a1f35", font=dict(color="#e2e8f0")),
            margin=dict(l=0, r=0, t=0, b=0),
            height=450,
        )
        st.plotly_chart(fig_map, use_container_width=True)
        st.caption("🔴 Critical  🟠 High  🟡 Medium  🟢 Low — hover over dots for details")

# ── IOC Search ──
st.divider()
st.markdown("#### 🔎 IOC Search")
col_a, col_b = st.columns([3,1])
with col_a:
    ioc_query = st.text_input("Search by IP address, URL, or hash", placeholder="e.g. 185.220.101")
with col_b:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("Search IOCs")

if search_btn and ioc_query:
    try:
        res = requests.get(f"{API_BASE}/ioc/search", params={"ip": ioc_query}, timeout=10).json()
        if res["total"] > 0:
            st.success(f"Found {res['total']} match(es)")
            for m in res["matches"]:
                st.markdown(f"""
                <div style="background:#1a1f35;border:1px solid #2d3748;padding:12px;border-radius:8px;margin:4px 0;">
                    <strong>{m['title']}</strong> · {m['country']} · 
                    <span style="color:#fc8181;">{m['severity']}</span><br>
                    <small style="color:#a0aec0;">IPs: {m.get('ioc_ips','N/A')} · URLs: {m.get('ioc_urls','N/A')}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matches found for that IOC.")
    except:
        st.error("Could not reach API.")