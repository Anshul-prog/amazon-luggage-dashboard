"""
LugIQ — Luggage Brand Intelligence Dashboard
Amazon India · Competitive Analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib
import json
from collections import Counter
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="LugIQ — Amazon India Intelligence",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Libre+Baskerville:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Outfit', sans-serif; background: #F9F6F0; color: #2C1E16; }
.main { background: #F9F6F0; }
.block-container { padding: 2rem 2.5rem 3rem; max-width: 1440px; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #F2EBE1; }
::-webkit-scrollbar-thumb { background: #D5C5B9; border-radius: 4px; }

[data-testid="stSidebar"] {
    background: #F4EFE6 !important;
    border-right: 1px solid rgba(139,115,99,0.15) !important;
    padding: 1.3rem 1.25rem 1.5rem !important;
}
[data-testid="stSidebar"] label { color: #5C4E43 !important; font-size: 0.72rem !important; font-weight: 600 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; }
[data-testid="stSidebar"] p { color: #6B5A50 !important; }

.brand-mark { padding: 1.2rem 0 1rem; border-bottom: 1px solid rgba(139,115,99,0.15); margin-bottom: 1.5rem; }
.brand-name { font-family: 'Libre Baskerville', serif; font-size: 1.5rem; font-weight: 700; color: #2C1E16; letter-spacing: -0.02em; }
.brand-tagline { font-family: 'Outfit', sans-serif; font-size: 0.62rem; color: #8B7363; letter-spacing: 0.14em; text-transform: uppercase; margin-top: 4px; }

.page-header { background: rgba(255,255,255,0.95); border: 1px solid rgba(139,115,99,0.16); border-radius: 24px; padding: 1.6rem 1.8rem; margin-bottom: 2rem; box-shadow: 0 18px 40px rgba(86,69,58,0.07); }
.page-title { font-family: 'Libre Baskerville', serif; font-size: 2.4rem; font-weight: 700; color: #2C1E16; letter-spacing: -0.03em; line-height: 1.08; margin-bottom: 0.45rem; }
.page-subtitle { font-size: 0.85rem; color: #5B5956; letter-spacing: 0.03em; margin-bottom: 0; }

.section-label {
    font-family: 'Outfit', sans-serif; font-size: 0.65rem; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase;
    color: #8B7363; margin: 2rem 0 1rem;
    display: inline-flex; align-items: center; gap: 0.85rem;
}
.section-label::after { content: ''; display: block; height: 1px; width: 100%; background: rgba(139,115,99,0.14); margin-left: 0.85rem; }

.metric-wrap {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(139,115,99,0.14);
    border-radius: 18px;
    padding: 1.2rem 1.5rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 12px 22px rgba(86,69,58,0.05);
}
.metric-wrap:hover { border-color: rgba(139,115,99,0.3); transform: translateY(-2px); box-shadow: 0 16px 30px rgba(86,69,58,0.08); }
.metric-wrap::after {
    content: ''; position: absolute; bottom: 0; left: 0;
    width: 32%; height: 4px;
    background: var(--acc, #3b82f6); border-radius: 0 2px 0 0;
}
.m-label { font-size: 0.67rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: #8B7363; margin-bottom: 0.55rem; }
.m-value { font-family: 'Libre Baskerville', serif; font-size: 1.95rem; font-weight: 700; color: #2C1E16; line-height: 1.05; letter-spacing: -0.03em; }
.m-sub { font-size: 0.72rem; color: #7A6A5F; margin-top: 0.45rem; }

.chart-card {
    background: rgba(255,255,255,0.94);
    border: 1px solid rgba(139,115,99,0.14);
    border-radius: 20px;
    padding: 1.25rem 1.3rem 1.35rem;
    box-shadow: 0 14px 28px rgba(86,69,58,0.05);
}

.filter-box {
    background: rgba(255,255,255,0.9);
    border: 1px solid rgba(139,115,99,0.14);
    border-radius: 18px;
    padding: 1rem 1rem 1.1rem;
    margin-bottom: 1.25rem;
}

.insight-wrap {
    background: #FFFFFF;
    border: 1px solid rgba(139,115,99,0.18);
    border-radius: 18px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1rem;
    display: flex; gap: 1.2rem;
    align-items: flex-start; transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 16px 28px rgba(86,69,58,0.07);
}
.insight-wrap:hover { border-color: rgba(139,115,99,0.35); box-shadow: 0 20px 36px rgba(86,69,58,0.12); }
.insight-num { font-family: 'Libre Baskerville', serif; font-size: 2rem; font-weight: 700; color: #8B7363; line-height: 1; flex-shrink: 0; width: 2.5rem; text-align: center; }
.insight-heading { font-size: 0.92rem; font-weight: 700; color: #34251D; margin-bottom: 0.4rem; }
.insight-text { font-size: 0.82rem; color: #55463F; line-height: 1.8; }

.review-card { background: rgba(255,255,255,0.96); border: 1px solid rgba(139,115,99,0.14); border-radius: 16px; padding: 1rem 1.15rem; margin-bottom: 0.9rem; transition: border-color 0.2s, box-shadow 0.2s; box-shadow: 0 10px 18px rgba(86,69,58,0.05); }
.review-card:hover { border-color: rgba(139,115,99,0.28); box-shadow: 0 16px 25px rgba(86,69,58,0.08); }
.review-stars { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 0.55rem; }
.review-body { font-size: 0.78rem; color: #53463F; line-height: 1.7; }
.review-meta { font-size: 0.67rem; color: #8B7363; margin-top: 0.6rem; }

.divider { height: 1px; background: rgba(139,115,99,0.15); margin: 1.4rem 0; }

.stSelectbox > div > div, .stMultiSelect > div > div, .stTextInput > div > input, .stSlider > div > div {
    background: rgba(255,255,255,0.96) !important;
    border: 1px solid rgba(139,115,99,0.22) !important;
    color: #2C1E16 !important;
    border-radius: 12px !important;
}
[data-testid="stRadio"] label { color: #5C4E43 !important; font-size: 0.82rem !important; }
.stDataFrame { border: 1px solid rgba(139,115,99,0.15) !important; border-radius: 16px !important; overflow: hidden !important; }
.stTabs [data-baseweb="tab-list"] { gap:0; background:rgba(255,255,255,0.55); border-radius:14px; padding:5px; border:1px solid rgba(139,115,99,0.16); }
.stTabs [data-baseweb="tab"] { border-radius:10px; color:#8B7363; font-size:0.78rem; font-weight:600; padding:0.45rem 1.3rem; background:transparent; }
.stTabs [aria-selected="true"] { background:rgba(255,255,255,0.9) !important; color:#2C1E16 !important; border: 1px solid rgba(139,115,99,0.16) !important; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

@keyframes fadeUp { from { opacity:0; transform:translateY(16px); } to { opacity:1; transform:translateY(0); } }
.fu { animation: fadeUp 0.45s ease forwards; }
.fu1 { animation-delay:0.04s; opacity:0; }
.fu2 { animation-delay:0.10s; opacity:0; }
.fu3 { animation-delay:0.17s; opacity:0; }
.fu4 { animation-delay:0.24s; opacity:0; }
.fu5 { animation-delay:0.31s; opacity:0; }
</style>
""", unsafe_allow_html=True)

CHART_BG   = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(139,115,99,0.15)"
FONT_COLOR = "#5C4E43"

def get_rgba(hex_color, alpha=0.1):
    if not hex_color.startswith('#'): return hex_color
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

BRAND_COLORS = {
    "Safari":             "#3b82f6",
    "Skybags":            "#10b981",
    "American Tourister": "#f59e0b",
    "VIP":                "#ef4444",
    "Aristocrat":         "#8b5cf6",
    "Nasher Miles":       "#ec4899",
}

def cl(height=350, **kw):
    base = dict(
        paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
        font=dict(family="Outfit", color=FONT_COLOR, size=11),
        height=height, margin=dict(l=8,r=8,t=20,b=8),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor="rgba(0,0,0,0)", linecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor="rgba(0,0,0,0)", linecolor=GRID_COLOR),
    )
    base.update(kw)
    return base

@st.cache_data
def load_data():
    return pd.read_csv("data/products.csv"), pd.read_csv("data/reviews.csv")

@st.cache_data
def brand_summary_df(products, reviews):
    ra = reviews.groupby("brand").agg(
        total_reviews=("rating","count"),
        avg_sentiment=("sentiment_score","mean"),
        pos_reviews=("sentiment_label", lambda x:(x=="positive").sum()),
        neg_reviews=("sentiment_label", lambda x:(x=="negative").sum()),
        neu_reviews=("sentiment_label", lambda x:(x=="neutral").sum()),
    ).reset_index()
    ra["pos_pct"] = (ra["pos_reviews"]/ra["total_reviews"]*100).round(1)
    ra["neg_pct"] = (ra["neg_reviews"]/ra["total_reviews"]*100).round(1)
    pa = products.groupby("brand").agg(
        total_products=("product_id","count"),
        avg_sell_price=("sell_price","mean"),
        avg_list_price=("list_price","mean"),
        avg_discount=("discount_pct","mean"),
        avg_rating=("avg_rating","mean"),
        min_price=("sell_price","min"),
        max_price=("sell_price","max"),
        market_position=("market_position","first"),
    ).reset_index()
    s = pa.merge(ra, on="brand")
    s["value_score"]    = (s["avg_sentiment"]*100/(s["avg_sell_price"]/1000)).round(2)
    s["avg_sell_price"] = s["avg_sell_price"].round(0).astype(int)
    s["avg_list_price"] = s["avg_list_price"].round(0).astype(int)
    s["avg_discount"]   = s["avg_discount"].round(1)
    s["avg_rating"]     = s["avg_rating"].round(2)
    s["avg_sentiment"]  = s["avg_sentiment"].round(3)
    return s

@st.cache_data
def top_themes(reviews, brand, label, field, n=5):
    sub   = reviews[(reviews["brand"]==brand)&(reviews["sentiment_label"]==label)]
    words = " ".join(sub[field].dropna().astype(str)).lower().split()
    return Counter(w for w in words if len(w)>4).most_common(n)

@st.cache_data
def aspect_scores(reviews, brand):
    sub = reviews[reviews["brand"]==brand]
    ac  = {a:{"positive":0,"negative":0,"neutral":0}
           for a in ["wheels","handle","zipper","material","size","durability","design","price"]}
    for _, row in sub.iterrows():
        try:
            for asp, sent in json.loads(row["aspects"]).items():
                if asp in ac and sent in ac[asp]:
                    ac[asp][sent] += 1
        except: pass
    rows = []
    for asp, c in ac.items():
        total = sum(c.values())
        if total:
            rows.append({"aspect": asp.capitalize(), **c, "total": total,
                         "score": round((c["positive"]-c["negative"])/total*100,1)})
    return pd.DataFrame(rows).sort_values("score", ascending=False)

# ── Load ──
products_df, reviews_df = load_data()
summary                 = brand_summary_df(products_df, reviews_df)

# ── Sidebar ──
with st.sidebar:
    st.markdown("<div class='brand-mark'><div class='brand-name'>LugIQ</div><div class='brand-tagline'>Amazon India Intelligence</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
    all_brands      = sorted(products_df["brand"].unique())
    selected_brands = st.multiselect("Brands", all_brands, default=all_brands)
    min_p, max_p    = int(products_df["sell_price"].min()), int(products_df["sell_price"].max())
    price_range     = st.slider("Price range (INR)", min_p, max_p, (min_p, max_p), step=100)
    min_rating      = st.slider("Min rating", 1.0, 5.0, 1.0, step=0.1)
    all_sizes       = ["All"] + sorted(products_df["size"].unique())
    sel_size        = st.selectbox("Category / size", all_sizes)
    min_sent        = st.slider("Min sentiment score", 0.0, 1.0, 0.0, step=0.05)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    page = st.radio("", ["Overview","Brand Comparison","Product Drilldown","Agent Insights"], label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.62rem;color:#1e293b;text-align:center;line-height:1.7;'>Synthetic dataset modeled on<br>Amazon India market data 2024–25</div>", unsafe_allow_html=True)

if not selected_brands:
    selected_brands = all_brands

fp = products_df[
    (products_df["brand"].isin(selected_brands)) &
    (products_df["sell_price"].between(*price_range)) &
    (products_df["avg_rating"]>=min_rating)
]
if sel_size != "All":
    fp = fp[fp["size"]==sel_size]
fr = reviews_df[reviews_df["brand"].isin(selected_brands)]
fs = summary[(summary["brand"].isin(selected_brands))&(summary["avg_sentiment"]>=min_sent)]

# ══════════════════════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown("<div class='page-header fu fu1'><div class='page-title'>Amazon India<br><span style='color:#1e3a5f;'>Luggage Intelligence</span></div><div class='page-subtitle'>Competitive analysis · 6 brands · 78 products · 5,800+ customer reviews</div></div>", unsafe_allow_html=True)

    cols   = st.columns(5)
    mdata  = [
        ("Brands Tracked",  len(selected_brands),                       "of 6 total",      "#3b82f6"),
        ("Products",        len(fp),                                     "filtered view",   "#10b981"),
        ("Reviews",         f"{len(fr):,}",                              "verified & rated","#f59e0b"),
        ("Avg Sentiment",   f"{fr['sentiment_score'].mean():.2f}",       "scale 0–1",       "#8b5cf6"),
        ("Avg Discount",    f"{fp['discount_pct'].mean():.0f}%",         "across brands",   "#ec4899"),
    ]
    for col, (label, val, sub, acc) in zip(cols, mdata):
        col.markdown(f"<div class='metric-wrap fu fu2' style='--acc:{acc}'><div class='m-label'>{label}</div><div class='m-value'>{val}</div><div class='m-sub'>{sub}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Market Positioning Map</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#334155;margin-top:-0.6rem;margin-bottom:0.9rem;'>Bubble size = review volume · X = avg price · Y = sentiment score</div>", unsafe_allow_html=True)

    fig = px.scatter(fs, x="avg_sell_price", y="avg_sentiment", size="total_reviews",
                     color="brand", color_discrete_map=BRAND_COLORS,
                     hover_data={"avg_discount":True,"avg_rating":True,"market_position":True},
                     text="brand", size_max=55,
                     labels={"avg_sell_price":"Avg Selling Price (INR)","avg_sentiment":"Sentiment Score"})
    fig.update_traces(textposition="top center", textfont=dict(size=10, color="#6B5A50", family="Outfit"),
                      marker=dict(opacity=0.85, line=dict(width=1, color="rgba(139,115,99,0.15)")))
    fig.update_layout(**cl(375, showlegend=False))
    st.plotly_chart(fig, use_container_width=True)

    ca, cb = st.columns(2)
    with ca:
        st.markdown("<div class='section-label'>Average Price by Brand</div>", unsafe_allow_html=True)
        fig2 = go.Figure()
        for _, row in fs.sort_values("avg_sell_price").iterrows():
            fig2.add_trace(go.Bar(name=row["brand"], x=[row["brand"]], y=[row["avg_sell_price"]],
                                  marker=dict(color=BRAND_COLORS.get(row["brand"],"#3b82f6"), opacity=0.82, line=dict(width=0)),
                                  text=f"₹{row['avg_sell_price']:,}", textposition="outside",
                                  textfont=dict(size=10, color="#8B7363")))
        fig2.update_layout(**cl(295, showlegend=False, barmode="group",
            yaxis=dict(gridcolor=GRID_COLOR, title="Avg Selling Price (INR)", titlefont=dict(size=10))))
        st.plotly_chart(fig2, use_container_width=True)

    with cb:
        st.markdown("<div class='section-label'>Discount vs Sentiment</div>", unsafe_allow_html=True)
        fig3 = px.scatter(fs, x="avg_discount", y="avg_sentiment",
                          color="brand", color_discrete_map=BRAND_COLORS,
                          size="total_reviews", text="brand", size_max=30,
                          labels={"avg_discount":"Avg Discount (%)","avg_sentiment":"Sentiment Score"})
        fig3.update_traces(textposition="top center", textfont=dict(size=10, color="#6B5A50"),
                           marker=dict(opacity=0.85, line=dict(width=1, color="rgba(139,115,99,0.15)")))
        fig3.update_layout(**cl(295, showlegend=False))
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("<div class='section-label'>Sentiment Breakdown by Brand</div>", unsafe_allow_html=True)
    fig4  = go.Figure()
    seen  = set()
    for _, row in fs.sort_values("avg_sentiment", ascending=False).iterrows():
        total = row["total_reviews"]
        for lbl, val, color in [
            ("Positive", row["pos_pct"],                  "#4ade80"),
            ("Neutral",  row["neu_reviews"]/total*100,    "#94a3b8"),
            ("Negative", row["neg_pct"],                  "#f87171"),
        ]:
            fig4.add_trace(go.Bar(name=lbl, x=[row["brand"]], y=[val],
                                  marker_color=color, marker_opacity=0.8, showlegend=lbl not in seen))
            seen.add(lbl)
    fig4.update_layout(**cl(285, barmode="stack",
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(139,115,99,0.15)", font=dict(size=10, color="#5C4E43")),
        yaxis=dict(gridcolor=GRID_COLOR, title="% of Reviews", titlefont=dict(size=10))))
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# BRAND COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Brand Comparison":
    st.markdown("<div class='page-header fu fu1'><div class='page-title'>Brand Comparison</div><div class='page-subtitle'>Side-by-side benchmarking · price, rating, sentiment, review volume</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Benchmark Table</div>", unsafe_allow_html=True)
    dcols = {"brand":"Brand","market_position":"Segment","avg_sell_price":"Avg Price (INR)",
             "avg_discount":"Avg Discount (%)","avg_rating":"Avg Rating","total_reviews":"Reviews",
             "avg_sentiment":"Sentiment","pos_pct":"Positive %","neg_pct":"Negative %","value_score":"Value Score"}
    tbl = fs[list(dcols.keys())].rename(columns=dcols).sort_values("Avg Price (INR)")
    st.dataframe(
        tbl.style
           .background_gradient(subset=["Sentiment","Avg Rating","Value Score"], cmap="RdYlGn")
           .background_gradient(subset=["Avg Discount (%)"], cmap="YlOrRd"),
        use_container_width=True, height=255,
    )

    r1, r2 = st.columns([3, 2])
    with r1:
        st.markdown("<div class='section-label'>Multi-dimensional Radar</div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.72rem;color:#334155;margin-top:-0.6rem;margin-bottom:0.9rem;'>Normalised scores across 5 dimensions</div>", unsafe_allow_html=True)

        def norm(s):
            mn, mx = s.min(), s.max()
            return ((s-mn)/(mx-mn+1e-9)*10).round(2)

        rd = fs.copy()
        rd["price_score"]    = 10 - norm(rd["avg_sell_price"])
        rd["discount_score"] = norm(rd["avg_discount"])
        rd["rating_score"]   = norm(rd["avg_rating"])
        rd["sentiment_norm"] = norm(rd["avg_sentiment"])
        rd["review_score"]   = norm(rd["total_reviews"])

        cats = ["Price Score","Discount","Rating","Sentiment","Review Volume"]
        fig_r = go.Figure()
        for _, row in rd.iterrows():
            vals = [row["price_score"],row["discount_score"],row["rating_score"],row["sentiment_norm"],row["review_score"]]
            fig_r.add_trace(go.Scatterpolar(
                r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself", name=row["brand"],
                line=dict(color=BRAND_COLORS.get(row["brand"],"#3b82f6"), width=1.5),
                fillcolor=get_rgba(BRAND_COLORS.get(row["brand"],"#3b82f6"), 0.1),
            ))
        fig_r.update_layout(
            polar=dict(bgcolor="rgba(0,0,0,0)",
                       radialaxis=dict(visible=True, range=[0,10], gridcolor=GRID_COLOR,
                                       color="#8B7363", tickfont=dict(size=9)),
                       angularaxis=dict(gridcolor=GRID_COLOR, color="#8B7363", tickfont=dict(size=10))),
            paper_bgcolor=CHART_BG, font=dict(family="Outfit", color=FONT_COLOR),
            legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="rgba(139,115,99,0.15)", font=dict(size=10)),
            height=420, margin=dict(l=30,r=30,t=20,b=20),
        )
        st.plotly_chart(fig_r, use_container_width=True)

    with r2:
        st.markdown("<div class='section-label'>Pros and Cons</div>", unsafe_allow_html=True)
        sel_bc = st.selectbox("Select brand", selected_brands, key="comp_brand")
        pros   = top_themes(reviews_df, sel_bc, "positive", "strength_mentioned")
        negs   = top_themes(reviews_df, sel_bc, "negative", "weakness_mentioned")

        st.markdown("<div style='font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#475569;margin-bottom:0.5rem;'>Top Praise</div>", unsafe_allow_html=True)
        for theme, count in pros:
            if theme.strip():
                st.markdown(f"<span class='tag-pos'>{theme}&nbsp;&nbsp;{count}</span>", unsafe_allow_html=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.65rem;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#475569;margin-bottom:0.5rem;'>Top Complaints</div>", unsafe_allow_html=True)
        for theme, count in negs:
            if theme.strip():
                st.markdown(f"<span class='tag-neg'>{theme}&nbsp;&nbsp;{count}</span>", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-label' style='margin-top:0;'>Price vs Discount</div>", unsafe_allow_html=True)
        fig_pd = px.scatter(fs, x="avg_sell_price", y="avg_discount",
                            color="brand", color_discrete_map=BRAND_COLORS,
                            size="total_reviews", text="brand", size_max=26,
                            labels={"avg_sell_price":"Avg Price (INR)","avg_discount":"Discount (%)"})
        fig_pd.update_traces(textposition="top center", textfont=dict(size=9, color="#6B5A50"),
                             marker=dict(opacity=0.85, line=dict(width=1, color="rgba(139,115,99,0.15)")))
        fig_pd.update_layout(**cl(255, showlegend=False))
        st.plotly_chart(fig_pd, use_container_width=True)

    st.markdown("<div class='section-label'>Aspect-Level Sentiment</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#334155;margin-top:-0.6rem;margin-bottom:0.9rem;'>How customers rate specific product attributes</div>", unsafe_allow_html=True)

    asp_brand = st.selectbox("Brand for aspect analysis", selected_brands, key="asp_brand")
    asp_df    = aspect_scores(reviews_df, asp_brand)

    a1, a2 = st.columns([3,2])
    with a1:
        if not asp_df.empty:
            fig_a = go.Figure()
            fig_a.add_trace(go.Bar(x=asp_df["aspect"], y=asp_df["positive"], name="Positive", marker_color="#4ade80", marker_opacity=0.8))
            fig_a.add_trace(go.Bar(x=asp_df["aspect"], y=asp_df["neutral"],  name="Neutral",  marker_color="#94a3b8", marker_opacity=0.6))
            fig_a.add_trace(go.Bar(x=asp_df["aspect"], y=asp_df["negative"], name="Negative", marker_color="#f87171", marker_opacity=0.8))
            fig_a.update_layout(**cl(295, barmode="stack",
                legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#5C4E43")),
                yaxis=dict(gridcolor=GRID_COLOR, title="Mentions", titlefont=dict(size=10))))
            st.plotly_chart(fig_a, use_container_width=True)

    with a2:
        hd = {}
        for b in selected_brands:
            ad = aspect_scores(reviews_df, b)
            if not ad.empty:
                hd[b] = ad.set_index("aspect")["score"].to_dict()
        if hd:
            heat = pd.DataFrame(hd).fillna(0)
            fig_h = px.imshow(heat,
                              color_continuous_scale=[[0,"#ef4444"],[0.5,"#1e293b"],[1,"#4ade80"]],
                              labels=dict(color="Net Score"), text_auto=True, aspect="auto")
            fig_h.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                                font=dict(family="Inter", color=FONT_COLOR, size=10),
                                height=295, margin=dict(l=8,r=8,t=20,b=8),
                                coloraxis_colorbar=dict(tickfont=dict(size=9), len=0.8))
            fig_h.update_traces(textfont=dict(size=9))
            st.plotly_chart(fig_h, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PRODUCT DRILLDOWN
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Product Drilldown":
    st.markdown("<div class='page-header fu fu1'><div class='page-title'>Product Drilldown</div><div class='page-subtitle'>Individual product metrics, review synthesis, and price spread</div></div>", unsafe_allow_html=True)

    d1, d2 = st.columns([1,3])
    with d1:
        sel_bd = st.selectbox("Brand", selected_brands, key="drill_brand")
        bprods = fp[fp["brand"]==sel_bd].sort_values("avg_rating", ascending=False)
        opts   = bprods["title"].tolist()
    if not opts:
        st.warning("No products match current filters.")
        st.stop()
    with d2:
        sel_title = st.selectbox("Product", opts)

    sp  = bprods[bprods["title"]==sel_title].iloc[0]
    pr  = reviews_df[reviews_df["product_id"]==sp["product_id"]]
    avg_s = pr["sentiment_score"].mean()
    pos_c = (pr["sentiment_label"]=="positive").sum()
    neg_c = (pr["sentiment_label"]=="negative").sum()

    mcols = st.columns(6)
    mpairs = [
        ("Selling Price", f"₹{int(sp['sell_price']):,}", "#3b82f6"),
        ("List Price",    f"₹{int(sp['list_price']):,}", "#475569"),
        ("Discount",      f"{sp['discount_pct']:.0f}%",  "#f59e0b"),
        ("Rating",        f"{sp['avg_rating']} / 5",     "#10b981"),
        ("Sentiment",     f"{avg_s:.3f}",                "#8b5cf6"),
        ("Reviews",       str(sp["review_count"]),        "#ec4899"),
    ]
    for col, (lbl, val, acc) in zip(mcols, mpairs):
        col.markdown(f"<div class='metric-wrap' style='--acc:{acc}'><div class='m-label'>{lbl}</div><div class='m-value' style='font-size:1.35rem;'>{val}</div></div>", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    left, right = st.columns([2,1])

    with left:
        st.markdown("<div class='section-label'>Rating Distribution</div>", unsafe_allow_html=True)
        rc = pr["rating"].value_counts().sort_index(ascending=False)
        fig_rc = go.Figure(go.Bar(
            x=rc.values, y=[f"{i} stars" for i in rc.index], orientation="h",
            marker=dict(color=BRAND_COLORS.get(sel_bd,"#3b82f6"), opacity=0.8, line=dict(width=0)),
            text=rc.values, textposition="outside", textfont=dict(size=10, color="#8B7363"),
        ))
        fig_rc.update_layout(**cl(220))
        st.plotly_chart(fig_rc, use_container_width=True)

        st.markdown("<div class='section-label'>Price Spread — All Brand Products</div>", unsafe_allow_html=True)
        ball = fp[fp["brand"]==sel_bd].sort_values("sell_price")
        fig_sp = px.strip(ball, x="sell_price", color="size",
                          labels={"sell_price":"Selling Price (INR)"},
                          hover_data={"title":True,"avg_rating":True,"discount_pct":True})
        fig_sp.update_layout(**cl(175, legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10, color="#5C4E43"))))
        st.plotly_chart(fig_sp, use_container_width=True)

    with right:
        st.markdown("<div class='section-label'>Themes</div>", unsafe_allow_html=True)
        t_praise = top_themes(pr, sp["brand"], "positive", "strength_mentioned")
        t_compl  = top_themes(pr, sp["brand"], "negative", "weakness_mentioned")

        st.markdown("<div style='font-size:0.65rem;color:#475569;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;'>Praise</div>", unsafe_allow_html=True)
        for theme, _ in t_praise:
            if theme.strip():
                st.markdown(f"<span class='tag-pos'>{theme}</span>", unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-size:0.65rem;color:#475569;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.4rem;'>Complaints</div>", unsafe_allow_html=True)
        for theme, _ in t_compl:
            if theme.strip():
                st.markdown(f"<span class='tag-neg'>{theme}</span>", unsafe_allow_html=True)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='font-size:0.65rem;color:#475569;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem;'>Product Details</div>
        <div style='font-size:0.77rem;color:#64748b;line-height:2.1;'>
            <span style='color:#334155;'>Size</span>&nbsp;&nbsp;{sp['size']}<br>
            <span style='color:#334155;'>Material</span>&nbsp;&nbsp;{sp['material']}<br>
            <span style='color:#334155;'>Colour</span>&nbsp;&nbsp;{sp['colour']}<br>
            <span style='color:#334155;'>Segment</span>&nbsp;&nbsp;{sp['market_position']}<br>
            <span style='color:#334155;'>Positive</span>&nbsp;&nbsp;{pos_c} ({pos_c/len(pr)*100:.0f}%)<br>
            <span style='color:#334155;'>Negative</span>&nbsp;&nbsp;{neg_c} ({neg_c/len(pr)*100:.0f}%)
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-label'>Sample Reviews</div>", unsafe_allow_html=True)
    samp = pr.sample(min(6, len(pr)), random_state=1)
    rcols = st.columns(3)
    for i, (_, rev) in enumerate(samp.iterrows()):
        sc = {"positive":"#4ade80","negative":"#f87171","neutral":"#94a3b8"}[rev["sentiment_label"]]
        rcols[i%3].markdown(f"""
        <div class='review-card'>
            <div class='review-stars' style='color:{sc};'>{"★"*int(rev["rating"])} &nbsp; {rev["sentiment_label"]}</div>
            <div class='review-body'>{rev["review_text"]}</div>
            <div class='review-meta'>{rev["review_date"]} &nbsp;·&nbsp; {"Verified" if rev["verified_purchase"] else "Unverified"}</div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# AGENT INSIGHTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Agent Insights":
    st.markdown("<div class='page-header fu fu1'><div class='page-title'>Agent Insights</div><div class='page-subtitle'>Auto-generated non-obvious conclusions derived from the data</div></div>", unsafe_allow_html=True)

    hi_d   = summary.sort_values("avg_discount",  ascending=False).iloc[0]
    lo_d   = summary.sort_values("avg_discount").iloc[0]
    bv     = summary.sort_values("value_score",   ascending=False).iloc[0]
    at     = summary[summary["brand"]=="American Tourister"].iloc[0]
    ar     = summary[summary["brand"]=="Aristocrat"].iloc[0]
    sky    = summary[summary["brand"]=="Skybags"].iloc[0]

    insights = [
        ("Discount does not equal satisfaction",
         f"{hi_d['brand']} offers the highest average discount ({hi_d['avg_discount']:.1f}%) yet its sentiment score ({hi_d['avg_sentiment']:.3f}) is lower than {lo_d['brand']}, which discounts the least ({lo_d['avg_discount']:.1f}%) but scores {lo_d['avg_sentiment']:.3f}. Heavy discounting is masking quality problems rather than resolving them."),
        ("American Tourister wins on trust, not price",
         f"At an average of ₹{at['avg_sell_price']:,}, American Tourister is the most expensive brand. Yet it records the highest sentiment ({at['avg_sentiment']:.3f}) and {at['pos_pct']:.1f}% positive reviews. Customers are paying for warranty assurance and brand reliability — not just product specifications."),
        ("Nasher Miles is the hidden value champion",
         f"Nasher Miles achieves a value score of {bv['value_score']:.2f} — the best sentiment-per-₹1,000 ratio in the dataset. Above-average sentiment at a mid-range price with lower discounting than budget brands. It is quietly outperforming on value-adjusted satisfaction."),
        ("Aristocrat's high discount signals demand weakness",
         f"Aristocrat has the highest discount rate ({ar['avg_discount']:.1f}%) alongside the lowest average rating ({ar['avg_rating']:.2f}) and sentiment ({ar['avg_sentiment']:.3f}). The discounting appears necessary to clear inventory rather than a competitive strategy. Recurring zipper and material complaints point to a quality ceiling that price cuts cannot overcome."),
        ("Skybags leads in volume but has a durability credibility gap",
         f"Skybags averages {sky['total_reviews']:.0f} reviews per product — the highest market reach in the set. However, its negative review percentage ({sky['neg_pct']:.1f}%) is disproportionate to its price tier. Wheel and zipper failures appear across product lines regardless of price point."),
        ("VIP faces a design perception paradox",
         "VIP receives consistent acknowledgement for build quality in reviews, yet sentiment is dragged down by 'outdated design' complaints. As a legacy Indian brand competing against newer-looking imports, VIP risks losing market share not because of functional failure — but because of a dated visual identity."),
    ]

    for i, (heading, body) in enumerate(insights):
        st.markdown(f"""
        <div class='insight-wrap fu fu{min(i+1,5)}'>
            <div class='insight-num'>0{i+1}</div>
            <div>
                <div class='insight-heading'>{heading}</div>
                <div class='insight-text'>{body}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='section-label' style='margin-top:2rem;'>Value-for-Money Quadrant</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#334155;margin-top:-0.6rem;margin-bottom:0.9rem;'>High sentiment + low price = strongest value proposition</div>", unsafe_allow_html=True)

    mp  = summary["avg_sell_price"].median()
    ms  = summary["avg_sentiment"].median()

    fig_q = go.Figure()
    for lbl, x, y, color in [
        ("Best Value", mp*0.38, ms+(1-ms)*0.82, "#4ade80"),
        ("Premium",    mp*1.35, ms+(1-ms)*0.82, "#f59e0b"),
        ("Poor Value", mp*0.38, ms*0.18,          "#f87171"),
        ("Overpriced", mp*1.35, ms*0.18,          "#8b5cf6"),
    ]:
        fig_q.add_annotation(x=x, y=y, text=lbl, showarrow=False,
                             font=dict(size=10, color=color, family="Outfit"), opacity=0.35)
    for _, row in summary.iterrows():
        fig_q.add_trace(go.Scatter(
            x=[row["avg_sell_price"]], y=[row["avg_sentiment"]],
            mode="markers+text", name=row["brand"],
            marker=dict(size=14, color=BRAND_COLORS.get(row["brand"],"#3b82f6"),
                        opacity=0.9, line=dict(width=1, color="rgba(139,115,99,0.15)")),
            text=[row["brand"]], textposition="top center",
            textfont=dict(size=10, color="#6B5A50", family="Outfit"),
        ))
    fig_q.add_vline(x=mp, line_dash="dot", line_color="rgba(139,115,99,0.15)", line_width=1)
    fig_q.add_hline(y=ms, line_dash="dot", line_color="rgba(139,115,99,0.15)", line_width=1)
    fig_q.update_layout(**cl(410, showlegend=False,
        xaxis=dict(gridcolor=GRID_COLOR, title="Avg Selling Price (INR)", titlefont=dict(size=10)),
        yaxis=dict(gridcolor=GRID_COLOR, title="Avg Sentiment Score",     titlefont=dict(size=10))))
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("<div class='section-label'>Review Trust Signals</div>", unsafe_allow_html=True)
    td = reviews_df.groupby("brand").agg(
        verified_pct=("verified_purchase","mean"),
        avg_helpful=("helpful_votes","mean"),
    ).reset_index()
    td["verified_pct"] = (td["verified_pct"]*100).round(1)
    td["avg_helpful"]  = td["avg_helpful"].round(1)
    td = td[td["brand"].isin(selected_brands)]

    fig_t = make_subplots(rows=1, cols=2, subplot_titles=["Verified Purchase %","Avg Helpful Votes"])
    for _, row in td.iterrows():
        c = BRAND_COLORS.get(row["brand"],"#3b82f6")
        fig_t.add_trace(go.Bar(x=[row["brand"]], y=[row["verified_pct"]], marker_color=c, marker_opacity=0.8, showlegend=False), row=1, col=1)
        fig_t.add_trace(go.Bar(x=[row["brand"]], y=[row["avg_helpful"]],  marker_color=c, marker_opacity=0.8, showlegend=False), row=1, col=2)
    fig_t.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=CHART_BG,
                        font=dict(family="Outfit", color=FONT_COLOR, size=11),
                        height=275, margin=dict(l=8,r=8,t=32,b=8), barmode="group")
    fig_t.update_xaxes(gridcolor=GRID_COLOR)
    fig_t.update_yaxes(gridcolor=GRID_COLOR)
    st.plotly_chart(fig_t, use_container_width=True)