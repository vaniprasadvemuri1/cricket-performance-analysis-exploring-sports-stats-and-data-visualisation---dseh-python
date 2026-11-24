"""IPL dashboard — streamlit run streamlit.py"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parent
CSV, ASSETS = ROOT / "data/processed/IPL_Batting_Statistics_Cleaned.csv", ROOT / "assets"
BGS = {"match": ASSETS / "cricket_bg.jpg", "search": ASSETS / "ipl_trophy.png"}
PHOTOS = {"dhoni": "ms_dhoni.png", "kohli": "virat_kohli.png", "rohit": "rohit_sharma.png"}
PLOT = ["Runs", "Batting_Average", "Strike_Rate", "Sixes"]
N, G, I = "#002350", "#F7C948", "#2C2416"
HUB_LOG = ["Season", "Teams_Played", "Matches_Played", "Runs", "Batting_Average", "Strike_Rate", "Sixes", "Death_Overs_Strike_Rate"]
MC_LOG = ["Season", "Teams_Played", "Runs", "Batting_Average", "Strike_Rate", "Sixes", "Death_Overs_Strike_Rate"]
PH_RUNS = ["Powerplay_Runs", "Middle_Overs_Runs", "Death_Overs_Runs"]
PH_BALLS = ["Powerplay_Balls", "Middle_Overs_Balls", "Death_Overs_Balls"]
CSS = """<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html,body,[class*="css"]{{font-family:Inter,sans-serif}}
.stApp{{background:#FFF8E7;background-image:linear-gradient(rgba(255,248,231,.93),rgba(255,252,245,.96)),{layer};
background-size:cover;background-attachment:fixed}}
[data-testid="stSidebar"]{{background:linear-gradient(180deg,#FFFCF5,#FFF8E7);border-right:1px solid #E8DFC8}}
.main .block-container{{max-width:1200px;padding:1.25rem 1.5rem 2rem}}
div[data-testid="stMetric"]{{background:#fff;border:1px solid #E8DFC8;border-radius:10px;box-shadow:0 1px 3px rgba(0,35,80,.06);padding:.35rem .5rem}}
div[data-testid="stMetric"] label{{font-size:.72rem;text-transform:uppercase;letter-spacing:.06em;color:#64748b}}
.sa-hero{{background:linear-gradient(135deg,#002350,#0a3d7a 55%,#1a4d8c);color:#fff;border-radius:12px;padding:1.1rem 1.35rem;margin-bottom:1.25rem;box-shadow:0 8px 24px rgba(0,35,80,.18)}}
.sa-hero h1{{margin:0;font-size:1.55rem;font-weight:700}}.sa-hero p{{margin:.35rem 0 0;font-size:.88rem;opacity:.88}}
.sa-hero .tag{{display:inline-block;margin-top:.5rem;font-size:.7rem;text-transform:uppercase;letter-spacing:.12em;background:rgba(247,201,72,.25);padding:.2rem .55rem;border-radius:4px}}
.sa-section{{border-top:2px solid #B8860B;margin:1.5rem 0 .75rem;padding-top:.65rem}}
.sa-section .kicker{{font-size:.68rem;font-weight:600;letter-spacing:.14em;color:#B8860B;text-transform:uppercase}}
.sa-section h3{{margin:.15rem 0 0;color:#002350;font-size:1.05rem;font-weight:600}}
.sa-profile{{background:#fff;border:1px solid #E8DFC8;border-radius:12px;padding:1rem 1.15rem;margin-bottom:1rem}}
.sa-profile .name{{font-size:1.35rem;font-weight:700;color:#002350;margin:0}}
.sa-profile .sub{{color:#64748b;font-size:.85rem;margin:.25rem 0 0}}
.sa-vs{{text-align:center;font-weight:700;color:#B8860B;font-size:.9rem;padding:.5rem}}
footer.sa-foot{{margin-top:2rem;padding-top:.75rem;border-top:1px solid #E8DFC8;font-size:.75rem;color:#94a3b8;text-align:center}}
</style>"""


@st.cache_data
def df():
    if not CSV.is_file():
        st.error("Run notebooks 01–02 first.")
        st.stop()
    return pd.read_csv(CSV)


def style(bg):
    u = bg.as_posix() if isinstance(bg, Path) and bg.is_file() else ""
    st.markdown(CSS.format(layer=f'url("{u}")' if u else "none"), unsafe_allow_html=True)


def say(tag, html, *, unsafe=True):
    st.markdown(html, unsafe_allow_html=unsafe)


def hero(t, s, tag="Batting · Cricsheet aggregates"):
    say("", f'<div class="sa-hero"><h1>{t}</h1><p>{s}</p><span class="tag">{tag}</span></div>')


def section(k, t):
    say("", f'<div class="sa-section"><div class="kicker">{k}</div><h3>{t}</h3></div>')


def foot(t):
    say("", f'<footer class="sa-foot">{t}</footer>')


def photo(name):
    f = next((PHOTOS[k] for k in PHOTOS if k in name.lower()), None)
    return (ASSETS / "players" / f) if f and (ASSETS / "players" / f).is_file() else None


def rates(p):
    r, d, b = p["Runs"].sum(), p["Dismissals"].sum(), p["Balls_Faced"].sum()
    return r, (r / d if d else None), (r / b * 100 if b else None)


def fig(f, h=340, title=""):
    f.update_layout(
        template="plotly_white", height=h, title=dict(text=title, font=dict(size=13, color=N)),
        paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="rgba(255,255,255,0.5)",
        font=dict(family="Inter, sans-serif", size=11, color=I), margin=dict(l=48, r=24, t=48, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    f.update_xaxes(gridcolor="#E8DFC8", linecolor="#E8DFC8")
    f.update_yaxes(gridcolor="#E8DFC8", linecolor="#E8DFC8")
    return f


def banner(name, p):
    teams = ", ".join(sorted({str(t) for t in p["Teams_Played"].dropna() if str(t) != "nan"}))
    _, a, s = rates(p)
    a, s = (f"{a:.1f}" if a else "—", f"{s:.1f}" if s else "—")
    c1, c2 = st.columns([1, 5])
    with c1:
        if img := photo(name):
            st.image(str(img), width=120)
    with c2:
        say(
            "",
            f'<div class="sa-profile" style="margin:0;box-shadow:none"><p class="name">{name}</p>'
            f'<p class="sub">{len(p)} IPL seasons · {teams or "—"}</p>'
            f'<p class="sub">Career avg <b>{a}</b> · SR <b>{s}</b> · HS <b>{int(p["Highest_Score"].max())}</b></p></div>',
        )


def kpis(p):
    r, a, s = rates(p)
    for col, lab, val in zip(
        st.columns(6), ["Runs", "Avg", "Strike rate", "Innings", "Sixes", "50+"],
        [f"{int(r):,}", f"{a:.1f}" if a else "—", f"{s:.1f}" if s else "—",
         f"{int(p['Innings'].sum()):,}", f"{int(p['Sixes'].sum()):,}", f"{int(p['Scores_50_Plus'].sum()):,}"],
    ):
        col.metric(lab, val)
    st.caption(
        f"Peak season — avg {p['Batting_Average'].max():.1f}, SR {p['Strike_Rate'].max():.1f} · Season key = Cricsheet JSON"
    )


def phase(p, title="Phase scoring (career runs)"):
    labels, runs = ["Powerplay", "Middle", "Death"], [p[c].sum() for c in PH_RUNS]
    balls = [p[c].sum() for c in PH_BALLS]
    srs = [x / y * 100 if y else 0 for x, y in zip(runs, balls)]
    f = go.Figure()
    f.add_trace(go.Bar(name="Runs", x=labels, y=runs, marker_color=[G, N, "#1D4ED8"],
                       text=[f"{v:,.0f}" for v in runs], textposition="outside"))
    f.add_trace(go.Scatter(name="Phase SR", x=labels, y=srs, mode="lines+markers", yaxis="y2",
                           line=dict(color="#B8860B", width=2), marker=dict(size=8)))
    f.update_layout(yaxis=dict(title="Runs"), yaxis2=dict(title="Strike rate", overlaying="y", side="right",
                        range=[0, max(srs) * 1.15 + 10]), barmode="group", showlegend=True)
    return fig(f, 300, title)


def rollup(sub):
    tot = pd.DataFrame([sub.select_dtypes("number").sum()])
    tot["Highest_Score"] = sub["Highest_Score"].max()
    if tot["Dismissals"].iloc[0]:
        tot["Batting_Average"] = tot["Runs"] / tot["Dismissals"]
    if tot["Balls_Faced"].iloc[0]:
        tot["Strike_Rate"] = tot["Runs"] / tot["Balls_Faced"] * 100
    return tot.round(2)


def vs(p1, p2):
    return p2 != "—" and p2 != p1


icon = ASSETS / "favicon.png"
st.set_page_config("IPL Batting Analytics", str(icon) if icon.is_file() else "🏏", layout="wide",
                   initial_sidebar_state="expanded")
if (ASSETS / "logo.png").is_file():
    st.logo(str(ASSETS / "logo.png"))

d = df()
st.sidebar.markdown("### IPL Batting Intelligence")
st.sidebar.caption("Player–season aggregates from Cricsheet ball-by-ball data.")
st.sidebar.divider()
page = st.sidebar.radio("Workspace", ["Match Centre", "Player Hub"])
st.sidebar.metric("Players tracked", f"{d['Player'].nunique():,}")
st.sidebar.metric("Player–seasons", f"{len(d):,}")
style(BGS["search" if page.startswith("Player") else "match"])

if page.startswith("Player"):
    hero("PLAYER HUB", "Scout profiles, season trends, and career totals", "Individual analysis")
    q = st.text_input("Search player", placeholder="e.g. Kohli, Sharma, Dhoni")
    if not q.strip():
        st.info("Enter a name to load a player profile.")
        st.stop()
    hit = d[d["Player"].str.contains(q.strip(), case=False, na=False)]
    if not (names := sorted(hit["Player"].unique())):
        st.warning("No players matched — try a shorter name.")
        st.stop()
    pick = st.selectbox("Select player", names)
    sub = hit[hit["Player"] == pick].sort_values("Season")
    banner(pick, sub)
    kpis(sub)
    t1, t2, t3 = st.tabs(["Season trend", "Phase attack", "Season log"])
    with t1:
        y = st.selectbox("Metric", [c for c in PLOT if c in sub.columns], key="hub_met")
        st.plotly_chart(fig(px.bar(sub, x="Season", y=y, text_auto=".2s", color_discrete_sequence=[G]), 320,
                            f"{y.replace('_', ' ')} by season"), width="stretch")
    with t2:
        st.plotly_chart(phase(sub), width="stretch")
    with t3:
        st.markdown("**Career rollup**")
        st.dataframe(rollup(sub), width="stretch", hide_index=True)
        st.dataframe(sub[HUB_LOG].round(2), width="stretch", hide_index=True)
    foot("Source: Cricsheet IPL · Batting only · Academic analytics build")
    st.stop()

hero("MATCH CENTRE", "Head-to-head trends, ranked leaderboards, season filters", "Comparative analysis")
season = st.sidebar.selectbox("Season filter", ["All", *sorted(d["Season"].unique())])
pl = sorted(d["Player"].unique())
p1 = st.sidebar.selectbox("Primary player", pl, index=pl.index("V Kohli") if "V Kohli" in pl else 0)
p2 = st.sidebar.selectbox("Compare with", ["—", *pl])
for nm in filter(None, [p1, None if p2 == "—" else p2]):
    if p := photo(nm):
        st.sidebar.image(str(p), caption=nm, width=110)
st.sidebar.divider()
met, board, min_b = st.sidebar.selectbox("Trend metric", PLOT), st.sidebar.selectbox(
    "Leaderboard", ["Runs", "Sixes", "Strike_Rate"]), st.sidebar.slider("Min balls faced (SR board)", 0, 400, 100, 25)

view = d if season == "All" else d[d["Season"] == season]
prof = d[d["Player"] == p1].sort_values("Season")
if season != "All":
    prof = prof[prof["Season"] == season]
    if not view.empty:
        st.sidebar.caption(f"Season {season}: {view['Runs'].sum():,.0f} runs in dataset slice")
if prof.empty:
    prof = d[d["Player"] == p1].sort_values("Season")
banner(p1, prof if len(prof) else d[d["Player"] == p1])
kpis(prof)
if vs(p1, p2):
    say("", f'<div class="sa-vs">VS {p2}</div>')

section("Trajectory", "Season-on-season performance")
a, b = st.columns(2)
with a:
    if vs(p1, p2):
        c = pd.concat([prof.assign(Player=p1), d[d["Player"] == p2].sort_values("Season").assign(Player=p2)])
        ch = px.line(c, x="Season", y=met, color="Player", markers=True, color_discrete_sequence=[G, N])
    else:
        ch = px.line(prof, x="Season", y=met, markers=True, color_discrete_sequence=[G])
    st.plotly_chart(fig(ch, 360, met.replace("_", " ")), width="stretch")
with b:
    pool = view if board != "Strike_Rate" else view[view["Balls_Faced"] >= min_b]
    top = pool.nlargest(10, board).reset_index(drop=True).assign(Rank=lambda x: range(1, len(x) + 1))
    top["Label"] = top["Rank"].astype(str).str.zfill(2) + " · " + top["Player"] + " · " + top["Season"].astype(str)
    bar = px.bar(top, x=board, y="Label", orientation="h", color=board, color_continuous_scale=[[0, N], [1, G]])
    bar.update_layout(showlegend=False, coloraxis_showscale=False, yaxis=dict(categoryorder="total ascending"))
    tit = f"Top 10 — {board.replace('_', ' ')}" + (f" (season {season})" if season != "All" else "")
    st.plotly_chart(fig(bar, 360, tit), width="stretch")

section("Phase", "Where runs are scored (career phase split)")
st.plotly_chart(phase(prof, "Primary player — phase runs & strike rate"), width="stretch")
section("Data", "Season-by-season batting log")
tab = prof[MC_LOG]
if vs(p1, p2):
    tab = pd.concat([tab, d[d["Player"] == p2].sort_values("Season")[MC_LOG]])
st.dataframe(tab.round(2), width="stretch", hide_index=True)
foot("Source: Cricsheet IPL · Min 100 balls rule for SR leaderboard · Batting-only scope")