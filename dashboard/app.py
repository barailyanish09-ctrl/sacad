import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

API_BASE = "https://sacad-api.onrender.com"

st.set_page_config(
    page_title="SACAD Threat Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp { background-color: #060910; color: #c9d1d9; font-family: 'IBM Plex Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 4rem; max-width: 1400px; }

.topbar { display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1c2333; padding-bottom: 1.2rem; margin-bottom: 2rem; }
.topbar-logo { font-family: 'IBM Plex Mono', monospace; font-size: 1.1rem; font-weight: 600; color: #f0f6fc; letter-spacing: 0.12em; text-transform: uppercase; }
.topbar-sub { font-size: 0.75rem; color: #6e7681; letter-spacing: 0.05em; text-transform: uppercase; margin-left: 1rem; }
.status-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #3fb950; margin-right: 6px; animation: pulse 2s infinite; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.live-badge { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #3fb950; letter-spacing: 0.1em; }

.kpi-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1px; background: #1c2333; border: 1px solid #1c2333; border-radius: 6px; overflow: hidden; margin-bottom: 2rem; }
.kpi-cell { background: #0d1117; padding: 1.2rem 1.4rem; }
.kpi-value { font-family: 'IBM Plex Mono', monospace; font-size: 2rem; font-weight: 600; color: #f0f6fc; line-height: 1; margin-bottom: 0.4rem; }
.kpi-value.red { color: #f85149; }
.kpi-value.blue { color: #58a6ff; }
.kpi-value.green { color: #3fb950; }
.kpi-label { font-size: 0.7rem; color: #6e7681; text-transform: uppercase; letter-spacing: 0.08em; }

.section-header { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #6e7681; text-transform: uppercase; letter-spacing: 0.12em; border-bottom: 1px solid #1c2333; padding-bottom: 0.5rem; margin-bottom: 1rem; margin-top: 1.5rem; }

.feed-item { display: grid; grid-template-columns: 90px 1fr 80px 100px; gap: 1rem; align-items: center; padding: 0.7rem 0; border-bottom: 1px solid #0d1117; font-size: 0.82rem; }
.feed-sev { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em; padding: 2px 7px; border-radius: 3px; text-align: center; }
.sev-critical { background: #3d1f1f; color: #f85149; border: 1px solid #f85149; }
.sev-high { background: #2d1f0a; color: #d29922; border: 1px solid #d29922; }
.sev-medium { background: #2d2a0a; color: #e3b341; border: 1px solid #e3b341; }
.sev-low { background: #0d2318; color: #3fb950; border: 1px solid #3fb950; }
.feed-title { color: #c9d1d9; }
.feed-meta { color: #6e7681; font-size: 0.75rem; }
.feed-country { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #58a6ff; }

.case-study { background: #0d1117; border: 1px solid #1c2333; border-left: 3px solid #58a6ff; border-radius: 4px; padding: 1.2rem 1.4rem; margin: 0.5rem 0; }
.case-title { font-size: 0.95rem; font-weight: 600; color: #f0f6fc; margin-bottom: 0.5rem; }
.case-meta { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #6e7681; margin-bottom: 0.5rem; }
.case-desc { font-size: 0.82rem; color: #8b949e; line-height: 1.5; }
.mitre-badge { display: inline-block; background: #1c2333; border: 1px solid #30363d; border-radius: 3px; padding: 2px 8px; font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: #79c0ff; margin-top: 0.4rem; }

div[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #1c2333; }
.stSelectbox > div > div { background: #0d1117 !important; border: 1px solid #1c2333 !important; color: #c9d1d9 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.8rem !important; }
.stTextInput input { background: #0d1117 !important; border: 1px solid #1c2333 !important; color: #c9d1d9 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.8rem !important; border-radius: 4px !important; }
.stButton button { background: #1c2333 !important; border: 1px solid #30363d !important; color: #c9d1d9 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 0.75rem !important; letter-spacing: 0.05em !important; border-radius: 4px !important; }
.stButton button:hover { background: #21262d !important; border-color: #58a6ff !important; color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

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
        return requests.get(f"{API_BASE}/attacks/recent?limit=8", timeout=10).json()
    except:
        return []

@st.cache_data(ttl=60)
def fetch_timeline():
    try:
        return requests.get(f"{API_BASE}/attacks/timeline", timeout=10).json()
    except:
        return []

@st.cache_data(ttl=60)
def fetch_threat_actors():
    try:
        return requests.get(f"{API_BASE}/attacks/threat-actors", timeout=10).json()
    except:
        return []

stats        = fetch_stats()
recent       = fetch_recent()
timeline     = fetch_timeline()
threat_actors = fetch_threat_actors()

# ── Top bar ──
st.markdown("""
<div class="topbar">
    <div style="display:flex;align-items:baseline;gap:1rem;">
        <span class="topbar-logo">SACAD</span>
        <span class="topbar-sub">South Asia Cyber Attack Dataset</span>
    </div>
    <div><span class="status-dot"></span><span class="live-badge">LIVE</span></div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──
total     = stats["total_attacks"] if stats else 0
recent30  = stats["recent_30_days"] if stats else 0
countries = len(stats["by_country"]) if stats else 0
sectors   = len(stats["by_sector"]) if stats else 0
critical  = stats["by_severity"].get("critical", 0) if stats else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-cell"><div class="kpi-value blue">{total}</div><div class="kpi-label">Total Incidents</div></div>
    <div class="kpi-cell"><div class="kpi-value">{recent30}</div><div class="kpi-label">Last 30 Days</div></div>
    <div class="kpi-cell"><div class="kpi-value">{countries}</div><div class="kpi-label">Countries</div></div>
    <div class="kpi-cell"><div class="kpi-value">{sectors}</div><div class="kpi-label">Sectors</div></div>
    <div class="kpi-cell"><div class="kpi-value red">{critical}</div><div class="kpi-label">Critical</div></div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown('<div class="section-header">Filters</div>', unsafe_allow_html=True)
    country_filter  = st.selectbox("Country",     ["All", "Nepal", "India", "Bangladesh", "Pakistan", "Sri Lanka", "Bhutan", "Myanmar"])
    type_filter     = st.selectbox("Attack Type", ["All", "phishing", "malware", "ransomware", "defacement", "ddos", "data_breach", "scam", "social_engineering", "supply_chain"])
    sector_filter   = st.selectbox("Sector",      ["All", "banking", "government", "healthcare", "education", "telecom", "ecommerce", "military", "ngo", "individual"])
    severity_filter = st.selectbox("Severity",    ["All", "critical", "high", "medium", "low"])
    st.markdown("---")
    st.markdown('<div class="section-header">Links</div>', unsafe_allow_html=True)
    st.markdown("[API](https://sacad-api.onrender.com) · [Docs](https://sacad-api.onrender.com/docs) · [GitHub](https://github.com/barailyanish09-ctrl/sacad)")

COLORS = ["#58a6ff","#3fb950","#d29922","#f85149","#bc8cff","#76e3ea","#ffa657","#79c0ff"]
BG = "#060910"
PLOT_BG = "#0d1117"
GRID = "#1c2333"
FONT = "#6e7681"

def base_layout(height=300):
    return dict(
        paper_bgcolor=BG, plot_bgcolor=PLOT_BG,
        font=dict(family="IBM Plex Mono", color=FONT, size=11),
        margin=dict(l=10, r=10, t=10, b=10),
        height=height,
        xaxis=dict(gridcolor=GRID, linecolor=GRID),
        yaxis=dict(gridcolor=GRID, linecolor=GRID),
    )

# ── Charts Row 1 ──
if stats:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Incidents by Country</div>', unsafe_allow_html=True)
        df = pd.DataFrame(list(stats["by_country"].items()), columns=["Country", "Count"])
        fig = px.bar(df, x="Country", y="Count", color="Country", color_discrete_sequence=COLORS)
        fig.update_layout(**base_layout(), showlegend=False, bargap=0.4)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Attack Vector Distribution</div>', unsafe_allow_html=True)
        df2 = pd.DataFrame(list(stats["by_attack_type"].items()), columns=["Type", "Count"])
        fig2 = px.pie(df2, names="Type", values="Count", color_discrete_sequence=COLORS, hole=0.55)
        fig2.update_layout(paper_bgcolor=BG, font=dict(family="IBM Plex Mono", color=FONT, size=11),
                          margin=dict(l=10,r=10,t=10,b=10), height=300,
                          legend=dict(bgcolor="rgba(0,0,0,0)"))
        fig2.update_traces(textfont_color="#c9d1d9")
        st.plotly_chart(fig2, use_container_width=True)

# ── Timeline ──
if timeline:
    st.markdown('<div class="section-header">Attack Timeline</div>', unsafe_allow_html=True)
    tdf = pd.DataFrame(timeline)
    if not tdf.empty and "month" in tdf.columns and "count" in tdf.columns:
        fig_t = go.Figure()
        fig_t.add_trace(go.Scatter(
            x=tdf["month"], y=tdf["count"],
            mode="lines+markers",
            line=dict(color="#58a6ff", width=2),
            marker=dict(color="#58a6ff", size=6),
            fill="tozeroy",
            fillcolor="rgba(88,166,255,0.1)"
        ))
        fig_t.update_layout(**base_layout(height=200))
        st.plotly_chart(fig_t, use_container_width=True)

# ── Charts Row 2 ──
if stats:
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-header">Targeted Sectors</div>', unsafe_allow_html=True)
        df3 = pd.DataFrame(list(stats["by_sector"].items()), columns=["Sector", "Count"])
        fig3 = px.bar(df3, x="Count", y="Sector", orientation="h",
                     color="Count", color_continuous_scale=[[0,"#1c2333"],[1,"#58a6ff"]])
        fig3.update_layout(**base_layout(), coloraxis_showscale=False, bargap=0.4)
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-header">Severity Distribution</div>', unsafe_allow_html=True)
        df4 = pd.DataFrame(list(stats["by_severity"].items()), columns=["Severity", "Count"])
        sev_colors = {"critical":"#f85149","high":"#d29922","medium":"#e3b341","low":"#3fb950"}
        fig4 = px.bar(df4, x="Severity", y="Count", color="Severity", color_discrete_map=sev_colors)
        fig4.update_layout(**base_layout(), showlegend=False, bargap=0.4)
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)

# ── Threat Actor Chart ──
if threat_actors and isinstance(threat_actors, list) and len(threat_actors) > 0 and "actor" in threat_actors[0]:
    st.markdown('<div class="section-header">Top Threat Actors</div>', unsafe_allow_html=True)
    ta_df = pd.DataFrame(threat_actors)
    fig_ta = px.bar(ta_df, x="count", y="actor", orientation="h",
                   color="count", color_continuous_scale=[[0,"#1c2333"],[1,"#f85149"]])
    fig_ta.update_layout(**base_layout(height=250), coloraxis_showscale=False, bargap=0.3)
    fig_ta.update_traces(marker_line_width=0)
    st.plotly_chart(fig_ta, use_container_width=True)

# ── Threat Map ──
attacks_all = fetch_attacks(
    country=None  if country_filter  == "All" else country_filter,
    attack_type=None if type_filter  == "All" else type_filter,
    sector=None   if sector_filter   == "All" else sector_filter,
    severity=None if severity_filter == "All" else severity_filter,
)

st.markdown('<div class="section-header">Threat Map — South Asia</div>', unsafe_allow_html=True)
coords = {
    "Nepal": (28.3949,84.1240), "India": (20.5937,78.9629),
    "Bangladesh": (23.6850,90.3563), "Pakistan": (30.3753,69.3451),
    "Sri Lanka": (7.8731,80.7718), "Bhutan": (27.5142,90.4336),
    "Myanmar": (21.9162,95.9560), "Regional": (23.0000,80.0000),
}
sev_map = {"critical":"#f85149","high":"#d29922","medium":"#e3b341","low":"#3fb950"}

if attacks_all:
    map_data = []
    for a in attacks_all:
        c = a.get("country","")
        if c in coords:
            lat, lon = coords[c]
            lat += random.uniform(-1.2,1.2)
            lon += random.uniform(-1.2,1.2)
            map_data.append({
                "lat":lat,"lon":lon,
                "title":a.get("title",""),
                "country":c,
                "type":a.get("attack_type",""),
                "severity":a.get("severity","medium"),
                "sector":a.get("target_sector",""),
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
                    marker=dict(size=14,color=color,opacity=0.9,line=dict(width=1,color="#060910")),
                    text=sub.apply(lambda r: f"{r['title']}<br>{r['country']} / {r['type']}<br>{r['sector']}",axis=1),
                    hoverinfo="text",hovertemplate="<b>%{text}</b><extra></extra>"
                ))
        fig_map.update_layout(
            geo=dict(scope="asia",showland=True,landcolor="#0d1117",
                    showocean=True,oceancolor="#060910",
                    showcoastlines=True,coastlinecolor="#1c2333",
                    showcountries=True,countrycolor="#1c2333",
                    bgcolor="#060910",center=dict(lat=23,lon=82),projection_scale=3.2),
            paper_bgcolor="#060910",
            legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(family="IBM Plex Mono",color="#6e7681",size=10),orientation="h",y=-0.02),
            margin=dict(l=0,r=0,t=0,b=0),height=420,
        )
        st.plotly_chart(fig_map, use_container_width=True)

# ── Recent Feed ──
st.markdown('<div class="section-header">Recent Incidents</div>', unsafe_allow_html=True)
if recent:
    for a in recent:
        sev = a.get("severity","medium")
        st.markdown(f"""
        <div class="feed-item">
            <span class="feed-sev sev-{sev}">{sev.upper()}</span>
            <span class="feed-title">{a.get('title','')}</span>
            <span class="feed-meta">{a.get('attack_type','')}</span>
            <span class="feed-country">{a.get('country','')}</span>
        </div>
        """, unsafe_allow_html=True)

# ── Case Study Panel ──
st.markdown('<div class="section-header">Case Study</div>', unsafe_allow_html=True)
if attacks_all:
    critical_attacks = [a for a in attacks_all if a.get("severity") == "critical"]
    if critical_attacks:
        for a in critical_attacks[:3]:
            mitre = a.get("technique","")
            tactic = a.get("mitre_tactic","")
            actor = a.get("threat_actor","Unknown")
            actor_type = a.get("actor_type","")
            st.markdown(f"""
            <div class="case-study">
                <div class="case-title">{a.get('title','')}</div>
                <div class="case-meta">
                    {a.get('country','')} &nbsp;·&nbsp;
                    {a.get('attack_type','').upper()} &nbsp;·&nbsp;
                    {a.get('target_sector','').upper()} &nbsp;·&nbsp;
                    Actor: {actor} {f'({actor_type})' if actor_type else ''}
                </div>
                <div class="case-desc">{a.get('description','')[:300]}...</div>
                {f'<div class="mitre-badge">MITRE: {mitre}</div>' if mitre else ''}
                {f'<div class="mitre-badge">Tactic: {tactic}</div>' if tactic else ''}
            </div>
            """, unsafe_allow_html=True)

# ── Records Table ──
st.markdown('<div class="section-header">Incident Records</div>', unsafe_allow_html=True)
if attacks_all:
    df = pd.DataFrame(attacks_all)
    cols = ["id","title","country","attack_type","severity","target_sector","technique","status","incident_date"]
    available = [c for c in cols if c in df.columns]
    st.dataframe(df[available], use_container_width=True, hide_index=True)
    st.caption(f"{len(df)} records · sacad-api.onrender.com")

# ── IOC Search ──
st.markdown('<div class="section-header">IOC Lookup</div>', unsafe_allow_html=True)
col_a, col_b = st.columns([4,1])
with col_a:
    ioc_query = st.text_input("", placeholder="Search by IP address, URL, or file hash")
with col_b:
    st.markdown("<br>", unsafe_allow_html=True)
    search_btn = st.button("SEARCH")

if search_btn and ioc_query:
    try:
        res = requests.get(f"{API_BASE}/ioc/search", params={"ip": ioc_query}, timeout=10).json()
        if res["total"] > 0:
            st.success(f"{res['total']} match(es) found")
            for m in res["matches"]:
                st.markdown(f"""
                <div style="background:#0d1117;border:1px solid #1c2333;border-left:3px solid #58a6ff;
                            padding:12px 16px;border-radius:4px;margin:6px 0;font-size:0.82rem;">
                    <strong style="color:#f0f6fc;">{m['title']}</strong>
                    <span style="color:#6e7681;margin-left:12px;">{m['country']} · {m['severity'].upper()}</span><br>
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.72rem;color:#6e7681;">
                        IPs: {m.get('ioc_ips','—')} &nbsp;|&nbsp; URLs: {m.get('ioc_urls','—')}
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matches found.")
    except:
        st.error("Could not reach API.")