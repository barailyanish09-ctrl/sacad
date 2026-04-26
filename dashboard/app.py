import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import random
from datetime import datetime, timedelta

API_BASE = "https://sacad-api.onrender.com"

# ── Fallback data if API is offline ──
FALLBACK_DATA = {
    "stats": {
        "total_attacks": 61,
        "recent_30_days": 12,
        "by_country": {"India": 26, "Nepal": 14, "Bangladesh": 10, "Pakistan": 8, "Sri Lanka": 3},
        "by_attack_type": {"data_breach": 28, "phishing": 12, "ransomware": 10, "malware": 6, "defacement": 3, "ddos": 2},
        "by_sector": {"banking": 20, "government": 18, "healthcare": 10, "ecommerce": 8, "telecom": 5},
        "by_severity": {"critical": 22, "high": 28, "medium": 8, "low": 3}
    },
    "attacks": []
}

st.set_page_config(
    page_title="SACAD Threat Intelligence",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background-color: #060910; color: #c9d1d9; font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem 4rem; max-width: 1400px; }

.topbar { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1c2333; padding-bottom: 1rem; margin-bottom: 1.5rem; }
.topbar-logo { font-family: 'IBM Plex Mono', monospace; font-size: 1.1rem; font-weight: 600; color: #f0f6fc; letter-spacing: 0.12em; text-transform: uppercase; }
.topbar-sub { font-size: 0.72rem; color: #6e7681; letter-spacing: 0.05em; text-transform: uppercase; margin-left: 1rem; }
.topbar-right { display: flex; align-items: center; gap: 1.5rem; }
.status-online { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #3fb950; }
.status-offline { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #f85149; }
.last-updated { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: #6e7681; }
.status-dot-on { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #3fb950; margin-right: 5px; animation: pulse 2s infinite; }
.status-dot-off { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #f85149; margin-right: 5px; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }

.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1px; background: #1c2333; border: 1px solid #1c2333; border-radius: 6px; overflow: hidden; margin-bottom: 1.5rem; }
.kpi-cell { background: #0d1117; padding: 1rem 1.2rem; }
.kpi-value { font-family: 'IBM Plex Mono', monospace; font-size: 1.8rem; font-weight: 600; color: #f0f6fc; line-height: 1; margin-bottom: 0.3rem; }
.kpi-value.red { color: #f85149; }
.kpi-value.blue { color: #58a6ff; }
.kpi-value.orange { color: #d29922; }
.kpi-value.green { color: #3fb950; }
.kpi-label { font-size: 0.68rem; color: #6e7681; text-transform: uppercase; letter-spacing: 0.08em; }
.kpi-delta { font-size: 0.65rem; color: #3fb950; margin-top: 0.2rem; }

.section-header { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #6e7681; text-transform: uppercase; letter-spacing: 0.12em; border-bottom: 1px solid #1c2333; padding-bottom: 0.4rem; margin-bottom: 0.8rem; margin-top: 1.2rem; }

.insight-card { background: #0d1117; border: 1px solid #1c2333; border-radius: 4px; padding: 1rem 1.2rem; margin: 0.4rem 0; }
.insight-title { font-size: 0.72rem; color: #6e7681; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.3rem; }
.insight-value { font-family: 'IBM Plex Mono', monospace; font-size: 1.1rem; color: #f0f6fc; }
.insight-sub { font-size: 0.75rem; color: #8b949e; margin-top: 0.2rem; }

.alert-critical { background: #3d1f1f; border: 1px solid #f85149; border-radius: 4px; padding: 0.6rem 1rem; margin: 0.3rem 0; font-size: 0.8rem; color: #f85149; }
.alert-high { background: #2d1f0a; border: 1px solid #d29922; border-radius: 4px; padding: 0.6rem 1rem; margin: 0.3rem 0; font-size: 0.8rem; color: #d29922; }

.feed-item { display: grid; grid-template-columns: 85px 1fr 75px 95px; gap: 0.8rem; align-items: center; padding: 0.6rem 0; border-bottom: 1px solid #0d1117; font-size: 0.8rem; cursor: pointer; }
.feed-item:hover { background: #0d1117; padding-left: 4px; transition: all 0.1s; }
.feed-sev { font-family: 'IBM Plex Mono', monospace; font-size: 0.6rem; font-weight: 600; letter-spacing: 0.1em; padding: 2px 6px; border-radius: 3px; text-align: center; }
.sev-critical { background: #3d1f1f; color: #f85149; border: 1px solid #f85149; }
.sev-high { background: #2d1f0a; color: #d29922; border: 1px solid #d29922; }
.sev-medium { background: #2d2a0a; color: #e3b341; border: 1px solid #e3b341; }
.sev-low { background: #0d2318; color: #3fb950; border: 1px solid #3fb950; }
.feed-title { color: #c9d1d9; }
.feed-meta { color: #6e7681; font-size: 0.72rem; }
.feed-country { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #58a6ff; }

.case-study { background: #0d1117; border: 1px solid #21262d; border-left: 3px solid #58a6ff; border-radius: 4px; padding: 1.2rem; margin: 0.6rem 0; }
.case-title { font-size: 0.95rem; font-weight: 600; color: #f0f6fc; margin-bottom: 0.5rem; }
.case-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin: 0.5rem 0; }
.case-field { font-size: 0.72rem; }
.case-field-label { color: #6e7681; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.1rem; }
.case-field-value { font-family: 'IBM Plex Mono', monospace; color: #c9d1d9; }
.case-desc { font-size: 0.8rem; color: #8b949e; line-height: 1.6; margin-top: 0.6rem; border-top: 1px solid #1c2333; padding-top: 0.6rem; }
.mitre-badge { display: inline-block; background: #161b22; border: 1px solid #30363d; border-radius: 3px; padding: 2px 8px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: #79c0ff; margin: 0.2rem 0.2rem 0 0; }
.actor-badge { display: inline-block; background: #1c1f2e; border: 1px solid #30363d; border-radius: 3px; padding: 2px 8px; font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem; color: #bc8cff; margin: 0.2rem 0.2rem 0 0; }
.source-link { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: #58a6ff; }

.top5-item { display: flex; justify-content: space-between; align-items: center; padding: 0.4rem 0; border-bottom: 1px solid #0d1117; }
.top5-rank { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: #6e7681; width: 20px; }
.top5-name { font-size: 0.8rem; color: #c9d1d9; }
.top5-count { font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem; color: #58a6ff; }
.top5-bar { height: 3px; background: #58a6ff; border-radius: 2px; margin-top: 2px; }

.datasource-item { background: #0d1117; border: 1px solid #1c2333; border-radius: 4px; padding: 0.8rem 1rem; margin: 0.3rem 0; font-size: 0.8rem; }
.datasource-name { font-family: 'IBM Plex Mono', monospace; color: #58a6ff; font-size: 0.75rem; }
.datasource-desc { color: #6e7681; font-size: 0.72rem; margin-top: 0.2rem; }

div[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #1c2333; }
.stSelectbox > div > div { background: #0d1117 !important; border: 1px solid #1c2333 !important; color: #c9d1d9 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.78rem !important; }
.stTextInput input { background: #0d1117 !important; border: 1px solid #1c2333 !important; color: #c9d1d9 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.78rem !important; border-radius: 4px !important; }
.stButton button { background: #1c2333 !important; border: 1px solid #30363d !important; color: #c9d1d9 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.72rem !important; letter-spacing: 0.05em !important; border-radius: 4px !important; }
.stButton button:hover { border-color: #58a6ff !important; color: #58a6ff !important; }
.stTabs [data-baseweb="tab"] { background: #0d1117; color: #6e7681; font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; }
.stTabs [aria-selected="true"] { color: #f0f6fc !important; border-bottom-color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

# ── Data fetching with fallback ──
@st.cache_data(ttl=120)
def fetch_stats():
    try:
        r = requests.get(f"{API_BASE}/stats", timeout=8)
        if r.status_code == 200:
            return r.json(), True
    except:
        pass
    return FALLBACK_DATA["stats"], False

@st.cache_data(ttl=120)
def fetch_attacks(country=None, attack_type=None, sector=None, severity=None):
    params = {"limit": 500}
    if country:     params["country"] = country
    if attack_type: params["attack_type"] = attack_type
    if sector:      params["sector"] = sector
    if severity:    params["severity"] = severity
    try:
        r = requests.get(f"{API_BASE}/attacks", params=params, timeout=8)
        if r.status_code == 200:
            return r.json(), True
    except:
        pass
    return FALLBACK_DATA["attacks"], False

@st.cache_data(ttl=120)
def fetch_recent(limit=8):
    try:
        r = requests.get(f"{API_BASE}/attacks/recent", params={"limit": limit}, timeout=8)
        if r.status_code == 200:
            return r.json(), True
    except:
        pass
    return [], False

@st.cache_data(ttl=120)
def fetch_timeline():
    try:
        r = requests.get(f"{API_BASE}/attacks/timeline", timeout=8)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0 and "month" in data[0]:
                return data, True
    except:
        pass
    return [], False

@st.cache_data(ttl=120)
def fetch_threat_actors():
    try:
        r = requests.get(f"{API_BASE}/attacks/threat-actors", timeout=8)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and len(data) > 0 and "actor" in data[0]:
                return data, True
    except:
        pass
    return [], False

# ── Load all data ──
stats, api_online       = fetch_stats()
recent_attacks, _       = fetch_recent(10)
timeline_data, _        = fetch_timeline()
threat_actors_data, _   = fetch_threat_actors()

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)
    country_filter  = st.selectbox("Country",     ["All", "Nepal", "India", "Bangladesh", "Pakistan", "Sri Lanka", "Bhutan", "Myanmar"])
    type_filter     = st.selectbox("Attack Type", ["All", "phishing", "malware", "ransomware", "defacement", "ddos", "data_breach", "scam", "social_engineering", "supply_chain"])
    sector_filter   = st.selectbox("Sector",      ["All", "banking", "government", "healthcare", "education", "telecom", "ecommerce", "military", "ngo", "individual"])
    severity_filter = st.selectbox("Severity",    ["All", "critical", "high", "medium", "low"])
    st.markdown("---")
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    st.markdown("---")
    st.markdown('<div class="section-header">Links</div>', unsafe_allow_html=True)
    st.markdown("[API](https://sacad-api.onrender.com)  ·  [Docs](https://sacad-api.onrender.com/docs)  ·  [GitHub](https://github.com/barailyanish09-ctrl/sacad)")

attacks_all, _ = fetch_attacks(
    country=None     if country_filter  == "All" else country_filter,
    attack_type=None if type_filter     == "All" else type_filter,
    sector=None      if sector_filter   == "All" else sector_filter,
    severity=None    if severity_filter == "All" else severity_filter,
)

# ── Top bar ──
api_status_html = f'<span class="status-dot-on"></span><span class="status-online">API ONLINE</span>' if api_online else f'<span class="status-dot-off"></span><span class="status-offline">API OFFLINE — CACHED DATA</span>'
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

st.markdown(f"""
<div class="topbar">
    <div style="display:flex;align-items:baseline;gap:1rem;">
        <span class="topbar-logo">SACAD</span>
        <span class="topbar-sub">South Asia Cyber Attack Dataset</span>
    </div>
    <div class="topbar-right">
        <span class="last-updated">Updated: {now}</span>
        {api_status_html}
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──
total     = stats.get("total_attacks", 0)
recent30  = stats.get("recent_30_days", 0)
countries = len(stats.get("by_country", {}))
sectors   = len(stats.get("by_sector", {}))
critical  = stats.get("by_severity", {}).get("critical", 0)

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-cell"><div class="kpi-value blue">{total}</div><div class="kpi-label">Total Incidents</div><div class="kpi-delta">all time</div></div>
    <div class="kpi-cell"><div class="kpi-value orange">{recent30}</div><div class="kpi-label">Last 30 Days</div></div>
    <div class="kpi-cell"><div class="kpi-value">{countries}</div><div class="kpi-label">Countries</div></div>
    <div class="kpi-cell"><div class="kpi-value">{sectors}</div><div class="kpi-label">Sectors Hit</div></div>
    <div class="kpi-cell"><div class="kpi-value red">{critical}</div><div class="kpi-label">Critical</div></div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Threat Map", "Incidents", "Case Studies", "Data Sources"])

COLORS = ["#58a6ff","#3fb950","#d29922","#f85149","#bc8cff","#76e3ea","#ffa657","#79c0ff"]
BG, PLOT_BG, GRID, FONT = "#060910", "#0d1117", "#1c2333", "#6e7681"

def base_layout(height=280):
    return dict(
        paper_bgcolor=BG, plot_bgcolor=PLOT_BG,
        font=dict(family="IBM Plex Mono", color=FONT, size=10),
        margin=dict(l=10, r=10, t=10, b=10), height=height,
        xaxis=dict(gridcolor=GRID, linecolor=GRID),
        yaxis=dict(gridcolor=GRID, linecolor=GRID),
    )

# ────────────────────────────────────────
# TAB 1 — OVERVIEW
# ────────────────────────────────────────
with tab1:
    # Insights Panel
    by_country    = stats.get("by_country", {})
    by_type       = stats.get("by_attack_type", {})
    by_sector     = stats.get("by_sector", {})
    by_severity   = stats.get("by_severity", {})

    top_country = max(by_country, key=by_country.get) if by_country else "N/A"
    top_type    = max(by_type,    key=by_type.get)    if by_type    else "N/A"
    top_sector  = max(by_sector,  key=by_sector.get)  if by_sector  else "N/A"
    high_count  = by_severity.get("high", 0) + by_severity.get("critical", 0)

    st.markdown('<div class="section-header">Insights</div>', unsafe_allow_html=True)
    ic1, ic2, ic3, ic4 = st.columns(4)
    with ic1:
        st.markdown(f'<div class="insight-card"><div class="insight-title">Most Targeted Country</div><div class="insight-value">{top_country}</div><div class="insight-sub">{by_country.get(top_country, 0)} incidents</div></div>', unsafe_allow_html=True)
    with ic2:
        st.markdown(f'<div class="insight-card"><div class="insight-title">Most Common Attack</div><div class="insight-value">{top_type}</div><div class="insight-sub">{by_type.get(top_type, 0)} incidents</div></div>', unsafe_allow_html=True)
    with ic3:
        st.markdown(f'<div class="insight-card"><div class="insight-title">Most Targeted Sector</div><div class="insight-value">{top_sector}</div><div class="insight-sub">{by_sector.get(top_sector, 0)} incidents</div></div>', unsafe_allow_html=True)
    with ic4:
        st.markdown(f'<div class="insight-card"><div class="insight-title">High + Critical Alerts</div><div class="insight-value" style="color:#f85149">{high_count}</div><div class="insight-sub">{round(high_count/total*100) if total else 0}% of total</div></div>', unsafe_allow_html=True)

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Incidents by Country</div>', unsafe_allow_html=True)
        df = pd.DataFrame(list(by_country.items()), columns=["Country","Count"]).sort_values("Count", ascending=False)
        fig = px.bar(df, x="Country", y="Count", color="Country", color_discrete_sequence=COLORS)
        fig.update_layout(**base_layout(), showlegend=False, bargap=0.4)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Attack Type Distribution</div>', unsafe_allow_html=True)
        df2 = pd.DataFrame(list(by_type.items()), columns=["Type","Count"])
        fig2 = px.pie(df2, names="Type", values="Count", color_discrete_sequence=COLORS, hole=0.55)
        fig2.update_layout(paper_bgcolor=BG, font=dict(family="IBM Plex Mono", color=FONT, size=10),
                          margin=dict(l=10,r=10,t=10,b=10), height=280,
                          legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=9)))
        fig2.update_traces(textfont_color="#c9d1d9", textfont_size=9)
        st.plotly_chart(fig2, use_container_width=True)

    # Timeline
    if timeline_data:
        st.markdown('<div class="section-header">Attack Timeline</div>', unsafe_allow_html=True)
        tdf = pd.DataFrame(timeline_data)
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(
            x=tdf["month"], y=tdf["count"],
            mode="lines+markers",
            line=dict(color="#58a6ff", width=2),
            marker=dict(color="#58a6ff", size=5),
            fill="tozeroy", fillcolor="rgba(88,166,255,0.08)"
        ))
        fig_t.update_layout(**base_layout(height=180))
        st.plotly_chart(fig_t, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Top 5 Countries</div>', unsafe_allow_html=True)
        top5_countries = sorted(by_country.items(), key=lambda x: x[1], reverse=True)[:5]
        max_c = top5_countries[0][1] if top5_countries else 1
        for i, (name, count) in enumerate(top5_countries):
            pct = int(count/max_c*100)
            st.markdown(f'<div class="top5-item"><span class="top5-rank">#{i+1}</span><div style="flex:1;margin:0 0.8rem"><span class="top5-name">{name}</span><div class="top5-bar" style="width:{pct}%"></div></div><span class="top5-count">{count}</span></div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-header">Severity Breakdown</div>', unsafe_allow_html=True)
        sev_colors = {"critical":"#f85149","high":"#d29922","medium":"#e3b341","low":"#3fb950"}
        df4 = pd.DataFrame(list(by_severity.items()), columns=["Severity","Count"])
        fig4 = px.bar(df4, x="Severity", y="Count", color="Severity", color_discrete_map=sev_colors)
        fig4.update_layout(**base_layout(height=220), showlegend=False, bargap=0.4)
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

    # Critical Alerts
    if attacks_all:
        critical_list = [a for a in attacks_all if a.get("severity") == "critical"][:5]
        if critical_list:
            st.markdown('<div class="section-header">Active Critical Alerts</div>', unsafe_allow_html=True)
            for a in critical_list:
                st.markdown(f'<div class="alert-critical">CRITICAL — {a.get("title","")} ({a.get("country","")} / {a.get("target_sector","")})</div>', unsafe_allow_html=True)

    # Threat Actors
    if threat_actors_data:
        st.markdown('<div class="section-header">Top Threat Actors</div>', unsafe_allow_html=True)
        ta_df = pd.DataFrame(threat_actors_data)
        fig_ta = px.bar(ta_df, x="count", y="actor", orientation="h",
                       color="count", color_continuous_scale=[[0,"#1c2333"],[1,"#f85149"]])
        fig_ta.update_layout(**base_layout(height=220), coloraxis_showscale=False, bargap=0.3)
        fig_ta.update_traces(marker_line_width=0)
        st.plotly_chart(fig_ta, use_container_width=True)

    # Recent Feed
    st.markdown('<div class="section-header">Latest Incidents</div>', unsafe_allow_html=True)
    feed_source = recent_attacks if recent_attacks else attacks_all[:8]
    for a in feed_source[:8]:
        sev = a.get("severity","medium")
        st.markdown(f"""
        <div class="feed-item">
            <span class="feed-sev sev-{sev}">{sev.upper()}</span>
            <span class="feed-title">{a.get('title','')}</span>
            <span class="feed-meta">{a.get('attack_type','')}</span>
            <span class="feed-country">{a.get('country','')}</span>
        </div>
        """, unsafe_allow_html=True)


# ────────────────────────────────────────
# TAB 2 — THREAT MAP
# ────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Geographic Threat Distribution</div>', unsafe_allow_html=True)

    coords = {
        "Nepal":(28.39,84.12),"India":(20.59,78.96),"Bangladesh":(23.68,90.35),
        "Pakistan":(30.37,69.34),"Sri Lanka":(7.87,80.77),"Bhutan":(27.51,90.43),
        "Myanmar":(21.91,95.95),"Regional":(23.00,80.00),
    }
    sev_map = {"critical":"#f85149","high":"#d29922","medium":"#e3b341","low":"#3fb950"}

    if attacks_all:
        map_data = []
        for a in attacks_all:
            c = a.get("country","")
            if c in coords:
                lat, lon = coords[c]
                lat += random.uniform(-1.5,1.5)
                lon += random.uniform(-1.5,1.5)
                map_data.append({
                    "lat":lat,"lon":lon,
                    "title":a.get("title",""),
                    "country":c,
                    "type":a.get("attack_type",""),
                    "severity":a.get("severity","medium"),
                    "sector":a.get("target_sector",""),
                    "actor":a.get("threat_actor","Unknown"),
                    "color":sev_map.get(a.get("severity","medium"),"#6e7681")
                })
        if map_data:
            mdf = pd.DataFrame(map_data)
            fig_map = go.Figure()
            for sev, color in sev_map.items():
                sub = mdf[mdf["severity"]==sev]
                if not sub.empty:
                    fig_map.add_trace(go.Scattergeo(
                        lat=sub["lat"],lon=sub["lon"],
                        mode="markers",name=sev.upper(),
                        marker=dict(size=16,color=color,opacity=0.85,line=dict(width=1,color="#060910")),
                        text=sub.apply(lambda r: f"<b>{r['title']}</b><br>{r['country']} / {r['type']}<br>Sector: {r['sector']}<br>Actor: {r['actor']}",axis=1),
                        hoverinfo="text",hovertemplate="%{text}<extra></extra>"
                    ))
            fig_map.update_layout(
                geo=dict(scope="asia",showland=True,landcolor="#0d1117",showocean=True,oceancolor="#060910",
                        showcoastlines=True,coastlinecolor="#1c2333",showcountries=True,countrycolor="#21262d",
                        bgcolor="#060910",center=dict(lat=22,lon=80),projection_scale=3.0),
                paper_bgcolor="#060910",
                legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(family="IBM Plex Mono",color="#6e7681",size=9),orientation="h",y=-0.02),
                margin=dict(l=0,r=0,t=0,b=0),height=500,
            )
            st.plotly_chart(fig_map, use_container_width=True)
            st.caption(f"Showing {len(map_data)} incidents · Hover dots for details · Red=Critical Orange=High Yellow=Medium Green=Low")
    else:
        st.info("No attack data available for map.")

    # Country breakdown table
    st.markdown('<div class="section-header">Country Breakdown</div>', unsafe_allow_html=True)
    if by_country:
        country_df = pd.DataFrame(list(by_country.items()), columns=["Country","Incidents"]).sort_values("Incidents", ascending=False)
        st.dataframe(country_df, use_container_width=True, hide_index=True)


# ────────────────────────────────────────
# TAB 3 — INCIDENTS TABLE
# ────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Incident Records</div>', unsafe_allow_html=True)

    # IOC Search
    col_a, col_b = st.columns([4,1])
    with col_a:
        ioc_query = st.text_input("", placeholder="Search by IP address, URL, file hash, or keyword")
    with col_b:
        st.markdown("<br>", unsafe_allow_html=True)
        search_btn = st.button("SEARCH")

    if search_btn and ioc_query:
        try:
            res = requests.get(f"{API_BASE}/ioc/search", params={"ip": ioc_query}, timeout=8).json()
            if res.get("total", 0) > 0:
                st.success(f"{res['total']} IOC match(es) found")
                for m in res.get("matches", []):
                    st.markdown(f"""
                    <div style="background:#0d1117;border:1px solid #1c2333;border-left:3px solid #58a6ff;padding:12px 16px;border-radius:4px;margin:4px 0;font-size:0.8rem;">
                        <strong style="color:#f0f6fc;">{m.get('title','')}</strong>
                        <span style="color:#6e7681;margin-left:12px;">{m.get('country','')} · {m.get('severity','').upper()}</span><br>
                        <span style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#6e7681;">IPs: {m.get('ioc_ips','—')} | URLs: {m.get('ioc_urls','—')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No IOC matches found.")
        except:
            # Fallback keyword search
            results = [a for a in attacks_all if ioc_query.lower() in a.get("title","").lower() or ioc_query.lower() in a.get("description","").lower()]
            if results:
                st.success(f"{len(results)} keyword match(es) found")
            else:
                st.warning("No matches found.")

    if attacks_all:
        df = pd.DataFrame(attacks_all)
        cols = ["id","title","country","attack_type","severity","target_sector","threat_actor","technique","status","incident_date"]
        available = [c for c in cols if c in df.columns]
        st.dataframe(
            df[available].fillna("—"),
            use_container_width=True,
            hide_index=True,
            height=500
        )
        st.caption(f"{len(df)} records matching current filters · sacad-api.onrender.com")

        # Download
        csv = df[available].to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"sacad_export_{datetime.utcnow().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No records match the current filters.")


# ────────────────────────────────────────
# TAB 4 — CASE STUDIES
# ────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">Critical Incident Case Studies</div>', unsafe_allow_html=True)
    st.caption("Detailed analysis of high-impact cyber incidents across South Asia")

    if attacks_all:
        # Show critical and high severity attacks
        case_attacks = [a for a in attacks_all if a.get("severity") in ["critical", "high"]][:15]

        if not case_attacks:
            case_attacks = attacks_all[:10]

        for a in case_attacks:
            sev       = a.get("severity","medium")
            technique = a.get("technique","")
            tactic    = a.get("mitre_tactic","")
            actor     = a.get("threat_actor","")
            actor_type = a.get("actor_type","")
            source_url = a.get("source_url","")
            source_name = a.get("source_name","")
            ioc_ips   = a.get("ioc_ips","")
            ioc_urls  = a.get("ioc_urls","")
            conf      = a.get("confidence_score", 0)
            status    = a.get("status","pending")

            mitre_html = f'<span class="mitre-badge">MITRE: {technique}</span>' if technique else ""
            tactic_html = f'<span class="mitre-badge">Tactic: {tactic}</span>' if tactic else ""
            actor_html = f'<span class="actor-badge">Actor: {actor}{" ("+actor_type+")" if actor_type else ""}</span>' if actor else ""
            source_html = f'<a href="{source_url}" class="source-link" target="_blank">{source_name}</a>' if source_url else f'<span class="source-link">{source_name}</span>'
            conf_html = f'<span style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:#3fb950;">Confidence: {int(conf*100)}%</span>' if conf else ""
            status_color = "#3fb950" if status == "verified" else "#d29922" if status == "partial" else "#6e7681"

            ioc_html = ""
            if ioc_ips or ioc_urls:
                ioc_html = f"""
                <div style="margin-top:0.5rem;padding-top:0.5rem;border-top:1px solid #1c2333;">
                    <div style="font-size:0.68rem;color:#6e7681;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.2rem;">Indicators of Compromise</div>
                    {"<div style='font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#f85149;'>IPs: "+ioc_ips+"</div>" if ioc_ips else ""}
                    {"<div style='font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#d29922;'>URLs: "+ioc_urls+"</div>" if ioc_urls else ""}
                </div>
                """

            st.markdown(f"""
            <div class="case-study">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                    <div class="case-title">{a.get('title','')}</div>
                    <span class="feed-sev sev-{sev}">{sev.upper()}</span>
                </div>
                <div class="case-grid">
                    <div class="case-field"><div class="case-field-label">Country</div><div class="case-field-value">{a.get('country','—')}</div></div>
                    <div class="case-field"><div class="case-field-label">Sector</div><div class="case-field-value">{a.get('target_sector','—')}</div></div>
                    <div class="case-field"><div class="case-field-label">Attack Type</div><div class="case-field-value">{a.get('attack_type','—')}</div></div>
                    <div class="case-field"><div class="case-field-label">Vector</div><div class="case-field-value">{a.get('attack_vector','—')}</div></div>
                </div>
                <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin:0.3rem 0;">
                    {mitre_html}{tactic_html}{actor_html}
                </div>
                <div class="case-desc">{a.get('description','No description available.')}</div>
                {ioc_html}
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:0.6rem;padding-top:0.4rem;border-top:1px solid #0d1117;">
                    <div>{source_html}</div>
                    <div style="display:flex;gap:1rem;">
                        {conf_html}
                        <span style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:{status_color};">{status.upper()}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No case studies available. Add attack records via the API.")


# ────────────────────────────────────────
# TAB 5 — DATA SOURCES
# ────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">Data Sources & Methodology</div>', unsafe_allow_html=True)

    sources = [
        ("CERT-NP", "Nepal", "Official Computer Emergency Response Team of Nepal. Primary source for Nepal-specific incidents.", "https://www.cert.gov.np"),
        ("CERT-In", "India", "Indian Computer Emergency Response Team under Ministry of Electronics. Advisories and alerts.", "https://www.cert-in.org.in"),
        ("BGD e-GOV CIRT", "Bangladesh", "Bangladesh Government Computer Incident Response Team. Official advisories.", "https://www.cirt.gov.bd"),
        ("CERT Pakistan", "Pakistan", "Pakistan CERT under Ministry of IT. Security alerts and incident reports.", "https://www.cert.gov.pk"),
        ("BleepingComputer", "Global", "Leading cybersecurity news outlet covering major incidents and threat intelligence.", "https://www.bleepingcomputer.com"),
        ("Cyble", "Global", "Dark web and threat intelligence monitoring platform. Data breach disclosures.", "https://cyble.com"),
        ("Resecurity", "Global", "Cybersecurity intelligence firm. ICMR breach and other South Asia coverage.", "https://resecurity.com"),
        ("KrebsOnSecurity", "Global", "Investigative cybersecurity journalism by Brian Krebs.", "https://krebsonsecurity.com"),
        ("Reuters / AP", "Global", "Major wire services covering high-impact cyber incidents.", "https://www.reuters.com"),
        ("SWIFT", "Global", "Official SWIFT advisories on banking system compromises.", "https://www.swift.com"),
    ]

    for name, region, desc, url in sources:
        st.markdown(f"""
        <div class="datasource-item">
            <div style="display:flex;justify-content:space-between;">
                <span class="datasource-name">{name}</span>
                <span style="font-family:IBM Plex Mono,monospace;font-size:0.65rem;color:#6e7681;">{region}</span>
            </div>
            <div class="datasource-desc">{desc}</div>
            <a href="{url}" target="_blank" style="font-family:IBM Plex Mono,monospace;font-size:0.62rem;color:#58a6ff;">{url}</a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">Verification Status</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.82rem;color:#8b949e;line-height:1.7;">
        <div style="margin-bottom:0.5rem;"><span style="font-family:IBM Plex Mono,monospace;color:#3fb950;">VERIFIED</span> — Confirmed by official CERT advisory or multiple credible sources</div>
        <div style="margin-bottom:0.5rem;"><span style="font-family:IBM Plex Mono,monospace;color:#d29922;">PARTIAL</span> — Reported by credible source but not officially confirmed</div>
        <div><span style="font-family:IBM Plex Mono,monospace;color:#6e7681;">PENDING</span> — Community submitted, awaiting verification</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">About SACAD</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.82rem;color:#8b949e;line-height:1.7;">
        SACAD is an open-source threat intelligence platform for South Asia. Built and maintained by
        <span style="color:#c9d1d9;">Anish Bishwokarma</span>, 1st semester cybersecurity student at
        Softwarica College of IT & E-Commerce, Kathmandu, Nepal.<br><br>
        The dataset is openly accessible via REST API at sacad-api.onrender.com.
        All data is sourced from public CERT advisories, news outlets, and security research firms.
        No proprietary or classified information is included.<br><br>
        <span style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#58a6ff;">
        License: MIT (code) · CC BY 4.0 (dataset)
        </span>
    </div>
    """, unsafe_allow_html=True)