import base64
from html import escape
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# ==========================================================
# SCE READING HABITS DASHBOARD
# ==========================================================
st.set_page_config(
    page_title="Reading Habits of SCE Students",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bright, high-contrast palette
CREAM = "#F8FAFF"
CREAM_DARK = "#EEF2FF"
BLUSH = "#E7FFFA"
PINK = "#FFB000"
ROSE = "#FF5A5F"
DEEP_ROSE = "#E84393"
COCOA = "#172B4D"
MUTED = "#637083"
WHITE = "#FFFFFF"
BORDER = "#E3E9F2"
PALETTE = [ROSE, "#FFB000", "#00C2A8", "#5B5FEF", "#27AE60", "#FF7A00", DEEP_ROSE]

# -------------------------- Styling --------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F8FAFF; color: #172B4D; }
.block-container { padding-top: 1.6rem; padding-bottom: 2.5rem; max-width: 1500px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #EEF2FF 0%, #E7FFFA 100%);
    border-right: 1px solid #E3E9F2;
}
[data-testid="stSidebar"] * { color: #172B4D; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { font-family: 'Playfair Display', serif; color: #172B4D; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 7px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
    border-radius: 12px; padding: 10px 12px; transition: all .2s ease;
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover {
    background: #FFFFFF; transform: translateX(3px);
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
    background: #5B5FEF; color: white; font-weight: 700;
    border-left: 4px solid #FFB000;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) * { color: white !important; }
[data-testid="stSidebar"] hr { border-color: #D7DFF0; }

/* Header and section headings */
.hero {
    background: linear-gradient(115deg, #5B5FEF 0%, #00A993 55%, #FF7A00 100%);
    border-radius: 22px; padding: 34px 38px; color: white;
    margin-bottom: 25px; box-shadow: 0 12px 30px rgba(49,62,129,.18);
    position: relative; overflow: hidden;
}
.hero:after {
    content: "📖"; position: absolute; right: 42px; top: -18px;
    opacity: .2; font-size: 142px; transform: rotate(-8deg);
}
.hero h1 {
    display: inline-block; font-family: 'Playfair Display', serif; color: white;
    font-size: 42px; margin: 0 0 10px;
}
.hero h1:after {
    content: ""; display: block; width: 82px; height: 4px; margin-top: 12px;
    border-radius: 4px; background: #FFF1A8;
}
.hero p { color: #F4F7FF; font-size: 16px; max-width: 850px; line-height: 1.65; margin-bottom: 0; }
.section-title {
    font-family: 'Playfair Display', serif; font-size: 27px; font-weight: 700;
    color: #172B4D; margin: 24px 0 4px;
}
.section-sub { color: #637083; font-size: 14px; margin-bottom: 18px; }

/* Metric cards */
.metric {
    background: white; border: 1px solid #E3E9F2; border-bottom: 4px solid #FF5A5F;
    border-radius: 17px; padding: 19px 20px; min-height: 128px;
    box-shadow: 0 5px 18px rgba(70,35,48,.045); transition: .2s ease;
}
.metric:hover {
    transform: translateY(-4px); background: #F0F3FF; border-bottom-color: #5B5FEF;
    box-shadow: 0 10px 22px rgba(70,35,48,.09);
}
.metric:active { background: #E1E7FF; }
.metric-label { color: #637083; font-size: 13px; font-weight: 700; }
.metric-value { color: #5B5FEF; font-size: 31px; font-weight: 800; margin-top: 8px; }
.metric-note { color: #7D899A; font-size: 12px; margin-top: 3px; }
.insight {
    background: white; border: 1px solid #E3E9F2; border-left: 5px solid #00C2A8;
    border-radius: 14px; padding: 17px 19px; margin: 8px 0;
    box-shadow: 0 4px 14px rgba(70,35,48,.035); transition: .2s ease;
}
.insight:hover {
    transform: translateX(4px); background: #EFFFFB; border-left-color: #5B5FEF;
    box-shadow: 0 8px 20px rgba(49,62,129,.10);
}
.insight:active { background: #D9FFF5; }
.insight h4 { color: #172B4D; font-size: 16px; margin: 0 0 6px; }
.insight p { color: #637083; font-size: 14px; line-height: 1.55; margin: 0; }
.note-box {
    background: #FFF7D6; border: 1px solid #FFE79A; border-left: 5px solid #FFB000;
    color: #493B12; border-radius: 12px; padding: 17px 19px; margin: 16px 0;
    line-height: 1.6; transition: .2s ease;
}
.note-box:hover { background: #FFF0B8; box-shadow: 0 6px 16px rgba(145,110,24,.12); }
.note-box:active { background: #FFE79A; }
[data-testid="stPlotlyChart"] {
    background: white; border: 1px solid #E3E9F2; border-radius: 16px;
    padding: 7px; box-shadow: 0 4px 15px rgba(70,35,48,.035); transition: .2s ease;
}
[data-testid="stPlotlyChart"]:hover {
    border-color: #A7ACFF; box-shadow: 0 9px 22px rgba(49,62,129,.10);
    transform: translateY(-2px);
}
[data-testid="stPlotlyChart"]:active { background: #F0F3FF; }
.stButton button, [data-testid="stDownloadButton"] button {
    background: #5B5FEF; color: white; border: none; border-radius: 10px;
    font-weight: 700; padding: 9px 17px;
}
.stButton button:hover, [data-testid="stDownloadButton"] button:hover {
    background: #4549D8; color: white;
}
.stTabs [data-baseweb="tab"] { color: #172B4D; font-weight: 700; }
.stTabs [aria-selected="true"] { border-bottom-color: #FF5A5F !important; }
[data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label { color: #172B4D; font-weight: 700; }
.footer {
    margin-top: 30px; background: #172B4D; color: #F4F7FF; border-radius: 12px;
    padding: 20px; text-align: center;
}
.footer strong { color: #FFFFFF; font-family: 'Playfair Display', serif; font-size: 19px; }
.footer-rights { color: #AEBBD4; font-size: 12px; }
.team-grid {
    display: grid; grid-template-columns: repeat(6, minmax(0, 1fr));
    gap: 16px; max-width: 1100px; margin: 0 auto;
}
.team-card {
    min-width: 0; padding: 16px 10px 13px; text-align: center;
    background: #FFFFFF; border: 1px solid #E3E9F2; border-radius: 18px;
    box-shadow: 0 5px 18px rgba(49,62,129,.06); transition: .2s ease;
}
.team-card:hover {
    transform: translateY(-5px); background: #EEF2FF; border-color: #777BFF;
    box-shadow: 0 12px 24px rgba(49,62,129,.14);
}
.supervisor-card {
    display: flex; flex-direction: column; align-items: center;
    width: 100%; max-width: 320px; margin: 22px auto 0; padding: 20px 24px 18px;
    box-sizing: border-box; text-align: center;
    background: linear-gradient(145deg, #EEF2FF, #E7FFFA);
    border: 1px solid #DDE3FF; border-top: 4px solid #5B5FEF;
    border-radius: 20px; box-shadow: 0 8px 24px rgba(49,62,129,.10);
    transition: .2s ease;
}
.supervisor-card:hover {
    transform: translateY(-5px); background: linear-gradient(145deg, #E3E8FF, #D9FFF5);
    border-color: #777BFF; box-shadow: 0 14px 28px rgba(49,62,129,.16);
}
.team-photo, .team-fallback {
    display: block; width: 104px; height: 104px; margin: 0 auto;
    object-fit: cover; object-position: center; border: 4px solid #FFFFFF;
    border-radius: 50%; box-shadow: 0 5px 16px rgba(49,62,129,.16);
}
.team-fallback {
    display: flex; align-items: center; justify-content: center;
    background: linear-gradient(135deg, #00C2A8, #5B5FEF);
    color: #FFFFFF; font-size: 24px; font-weight: 800;
}
.team-member-name {
    min-height: 38px; margin-top: 12px; display: flex;
    align-items: center; justify-content: center;
    color: #52627C; font-size: 14px; font-weight: 700; text-align: center;
}
.supervisor-photo {
    display: block; width: 120px; height: 120px; margin: 0 auto;
    object-fit: cover; object-position: center; border: 4px solid #FFFFFF;
    border-radius: 50%; box-shadow: 0 5px 16px rgba(49,62,129,.18);
}
.supervisor-name {
    color: #172B4D; font-size: 19px; font-weight: 800;
    text-align: center; margin-top: 12px;
}
.supervisor-role {
    display: inline-block; margin: 10px auto 0; padding: 5px 12px;
    color: #5B5FEF; background: #FFFFFF; border-radius: 999px;
    font-size: 12px; font-weight: 800; text-align: center;
    letter-spacing: 1.2px; text-transform: uppercase;
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { transition-duration: .01ms !important; scroll-behavior: auto !important; }
}
@media (max-width: 768px) {
    .hero { padding: 24px; } .hero h1 { font-size: 29px; }
    .hero:after { right: 8px; font-size: 85px; }
}
@media (max-width: 760px) {
    .team-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; }
}
@media (max-width: 540px) {
    .team-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .team-photo, .team-fallback { width: 88px; height: 88px; }
    .supervisor-photo { width: 108px; height: 108px; }
}
@media (max-width: 350px) {
    .team-grid { grid-template-columns: 1fr; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------- Respondent Data --------------------------
SHORT_COLUMNS = [
    "Age_Group", "Gender", "Programme", "Year_Study", "Read_Frequency",
    "Read_Hours", "Books_Month", "Read_Material", "Read_Format",
    "Read_Content", "Read_Purpose", "Screen_Hours", "Social_Hours",
    "Read_Barriers", "Read_Help"
]
FREQUENCY_ORDER = [
    "Never", "Rarely", "A few times a month", "Once a week",
    "Several times a week", "Daily"
]
YEAR_ORDER = ["Year I", "Year II", "Year III", "Year IV"]
AGE_ORDER = ["16-20", "21-25", "26-30", "Above 31"]
READ_HOURS_MAP = {
    "Less than 1 hour": 0.5, "1–3 hours": 2, "4–6 hours": 5,
    "7–9 hours": 8, "10–12 hours": 11, "More than 12 hours": 13
}
SCREEN_HOURS_MAP = {
    "Less than 1 hour": 0.5, "1–2 hours": 1.5, "3–4 hours": 3.5,
    "5–6 hours": 5.5, "7–8 hours": 7.5, "More than 8 hours": 9
}

@st.cache_data
def load_data():
    candidates = [
        Path(__file__).with_name("cleaned_data.xlsx"),
        Path(__file__).with_name("RAW data.xlsx"),
        Path(__file__).with_name("RAW_data.xlsx"),
        Path.home() / "Downloads" / "Telegram Desktop" / "RAW data.xlsx",
        Path.home() / "Downloads" / "RAW data.xlsx"
    ]
    source = next((path for path in candidates if path.is_file()), None)
    if source is None:
        return None

    data = pd.read_excel(source)
    if len(data.columns) != len(SHORT_COLUMNS):
        raise ValueError(
            f"Expected {len(SHORT_COLUMNS)} survey columns in {source.name}, "
            f"found {len(data.columns)}."
        )
    data = data.dropna(how="all").copy()
    data.columns = SHORT_COLUMNS
    data = data.drop_duplicates().copy()

    for column in SHORT_COLUMNS:
        data[column] = data[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    def clean_book_count(value):
        if pd.isna(value):
            return "No Response"
        numeric = pd.to_numeric(value, errors="coerce")
        if pd.notna(numeric) and float(numeric).is_integer():
            return str(int(numeric))
        return str(value).strip()

    data["Books_Month"] = data["Books_Month"].map(clean_book_count)
    data["Read_Help"] = data["Read_Help"].fillna("No Response")
    frequency_lookup = {value.lower(): value for value in FREQUENCY_ORDER}
    data["Read_Frequency"] = data["Read_Frequency"].map(
        lambda value: frequency_lookup.get(str(value).lower(), value)
    )
    data["Read_Hours_Num"] = data["Read_Hours"].map(READ_HOURS_MAP)
    data["Screen_Hours_Num"] = data["Screen_Hours"].map(SCREEN_HOURS_MAP)
    data["Social_Hours_Num"] = data["Social_Hours"].map(SCREEN_HOURS_MAP)
    return data.reset_index(drop=True)

full_data = load_data()
if full_data is None:
    st.error("Survey data not found. Place RAW data.xlsx beside app.py.")
    st.stop()

with st.sidebar:
    st.caption("SCE READING INSIGHTS")
    st.markdown("---")
    st.markdown("### Dashboard Navigation")
    page = st.radio(
        "Choose a page",
        ["Overview", "Reading Frequency & Time", "Reading Preferences",
         "Student Profile", "Screen Time & Barriers"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**SURVEY SUMMARY**")
    st.caption(f"{len(full_data):,} cleaned survey responses")
    st.caption("Use respondent filters to update findings.")

# -------------------------- Helpers --------------------------
def section(title, subtitle):
    st.markdown(f"<div class='section-title'>{title}</div><div class='section-sub'>{subtitle}</div>", unsafe_allow_html=True)

def metric(label, value, note, icon):
    st.markdown(f"""<div class="metric"><div class="metric-label">{icon} &nbsp; {label}</div>
    <div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>""", unsafe_allow_html=True)

def insight(title, body):
    st.markdown(f"<div class='insight'><h4>{title}</h4><p>{body}</p></div>", unsafe_allow_html=True)

def note(body):
    st.markdown(f"<div class='note-box'>{body}</div>", unsafe_allow_html=True)

def numpy_mean(series: pd.Series) -> float:
    values = series.to_numpy(dtype=float)
    finite_values = values[np.isfinite(values)]
    return float(np.mean(finite_values)) if finite_values.size else float("nan")

def format_correlation(value):
    return f"{value:.2f}" if pd.notna(value) else "N/A"

def chart_style(fig, height=390):
    fig.update_layout(
        height=height, margin=dict(l=35, r=25, t=65, b=45),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=COCOA, size=12),
        title_font=dict(family="Playfair Display", size=20, color=COCOA),
        legend_title_text="", hoverlabel=dict(bgcolor=WHITE, font_color=COCOA)
    )
    fig.update_xaxes(showgrid=False, linecolor=BORDER, tickfont=dict(size=11))
    fig.update_yaxes(gridcolor="#E8EDF5", zeroline=False, tickfont=dict(size=11))
    return fig

def show(fig, height=390):
    st.plotly_chart(
        chart_style(fig, height),
        width="stretch",
        config={
            "displaylogo": False,
            "modeBarButtonsToRemove": [
                "zoom2d", "pan2d", "select2d", "lasso2d",
                "zoomIn2d", "zoomOut2d", "autoScale2d", "resetScale2d",
                "hoverClosestCartesian", "hoverCompareCartesian", "toggleSpikelines"
            ]
        }
    )

def count_bar(counts, title, x_title="Number of students", horizontal=False):
    counts = pd.DataFrame({"Category": list(counts), "Students": list(counts.values())})
    if horizontal:
        counts = counts.sort_values("Students")
        fig = px.bar(counts, x="Students", y="Category", orientation="h",
                     text="Students", title=title, color="Students",
                     color_continuous_scale=["#FFE79A", "#FF5A5F", "#5B5FEF"])
        fig.update_layout(coloraxis_showscale=False, xaxis_title=x_title, yaxis_title="")
    else:
        fig = px.bar(counts, x="Category", y="Students", text="Students",
                     title=title, color="Category", color_discrete_sequence=PALETTE)
        fig.update_layout(xaxis_title="", yaxis_title=x_title, showlegend=False)
        fig.update_xaxes(tickangle=-25)
    fig.update_traces(textposition="outside", cliponaxis=False)
    return fig

def percentage_table(counts, name):
    result = pd.DataFrame({"Response": list(counts), "Students": list(counts.values())})
    result["Percentage"] = (result["Students"] / TOTAL_RESPONSES * 100).round(1)
    return result.rename(columns={"Response": name})

# -------------------------- Header --------------------------
st.markdown("""
<div class="hero">
  <h1>Reading Habits of SCE Students</h1>
  <p>Discover how our college community reads, learns, and makes time for books.
  Explore the survey findings and compare student groups using the filters below.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### Choose respondents")
st.caption(
    "Choose any combination of programme, year, gender and age. All findings update to match."
)
filter_cols = st.columns(4, gap="small")
programmes = sorted(full_data["Programme"].dropna().unique())
years = [value for value in YEAR_ORDER if value in set(full_data["Year_Study"])]
genders = sorted(full_data["Gender"].dropna().unique())
ages = [value for value in AGE_ORDER if value in set(full_data["Age_Group"])]
with filter_cols[0]:
    chosen_programme = st.selectbox("Programme", ["All programmes"] + programmes)
with filter_cols[1]:
    chosen_year = st.selectbox("Year of study", ["All years"] + years)
with filter_cols[2]:
    chosen_gender = st.selectbox("Gender", ["All genders"] + genders)
with filter_cols[3]:
    chosen_age = st.selectbox("Age group", ["All ages"] + ages)

filter_mask = pd.Series(True, index=full_data.index)
if chosen_programme != "All programmes":
    filter_mask &= full_data["Programme"] == chosen_programme
if chosen_year != "All years":
    filter_mask &= full_data["Year_Study"] == chosen_year
if chosen_gender != "All genders":
    filter_mask &= full_data["Gender"] == chosen_gender
if chosen_age != "All ages":
    filter_mask &= full_data["Age_Group"] == chosen_age
data = full_data.loc[filter_mask].copy()
total = len(full_data)
respondent_count = len(data)
active_filters = [
    value for value in [
        chosen_programme if chosen_programme != "All programmes" else None,
        chosen_year if chosen_year != "All years" else None,
        chosen_gender if chosen_gender != "All genders" else None,
        chosen_age if chosen_age != "All ages" else None
    ] if value is not None
]
filter_summary = " • ".join(active_filters) if active_filters else "All respondents"
st.caption(f"Showing {respondent_count:,} of {total:,} respondents • {filter_summary}")
if respondent_count == 0:
    st.warning("No respondents match this combination. Adjust one or more filters.")
    st.stop()

def counts_of(series, order=None):
    observed = series.dropna().value_counts()
    result = {}
    if order:
        for value in order:
            if value in observed.index:
                result[value] = int(observed[value])
    for value, count in observed.items():
        if value not in result:
            result[value] = int(count)
    return result

def top_item(counts):
    return max(counts.items(), key=lambda item: item[1])

FREQUENCY_COUNTS = counts_of(data["Read_Frequency"], FREQUENCY_ORDER)
READ_HOURS_COUNTS = counts_of(data["Read_Hours"])
BOOK_VALUES = counts_of(data["Books_Month"], ["0", "1", "2", "3", "4", "5 or more"])
BOOKS_MONTH_COUNTS = {
    ("5 or more" if value == "5 or more" else f"{value} book" + ("" if value == "1" else "s")): count
    for value, count in BOOK_VALUES.items()
}
MATERIAL_COUNTS = counts_of(data["Read_Material"])
FORMAT_COUNTS = counts_of(data["Read_Format"])
CONTENT_COUNTS = counts_of(data["Read_Content"])
PURPOSE_COUNTS = counts_of(data["Read_Purpose"])
SCREEN_HOURS_COUNTS = counts_of(data["Screen_Hours"])
SOCIAL_HOURS_COUNTS = counts_of(data["Social_Hours"])
barrier_responses = (
    data["Read_Barriers"].dropna().astype(str).str.split(r"\s*,\s*").explode().str.strip()
)
BARRIER_COUNTS = counts_of(barrier_responses[barrier_responses.ne("")])
PROFILE_COUNTS = {
    "Age group": counts_of(data["Age_Group"], AGE_ORDER),
    "Gender": counts_of(data["Gender"]),
    "Programme": counts_of(data["Programme"], programmes),
    "Year of study": counts_of(data["Year_Study"], YEAR_ORDER)
}
GROUP_FREQUENCY = {
    label: (
        pd.crosstab(data[column], data["Read_Frequency"], normalize="index") * 100
    )
    for label, column in {
        "Gender": "Gender", "Programme": "Programme",
        "Year of Study": "Year_Study", "Age Group": "Age_Group"
    }.items()
}
CORRELATION = data[
    ["Read_Hours_Num", "Screen_Hours_Num", "Social_Hours_Num"]
].corr()
CORRELATION.index = ["Reading hours/week", "Screen hours/day", "Social media hours/day"]
CORRELATION.columns = ["Reading hours/week", "Screen hours/day", "Social media hours/day"]
TOTAL_RESPONSES = respondent_count

# ========================== OVERVIEW ==========================
if page == "Overview":
    section("Research Overview", "The clearest patterns in the completed SCE reading-habits survey.")
    freq_mode, freq_count = top_item(FREQUENCY_COUNTS)
    top_material, top_material_count = top_item(MATERIAL_COUNTS)
    top_barrier, top_barrier_count = top_item(BARRIER_COUNTS)
    most_read_time, most_read_time_count = top_item(READ_HOURS_COUNTS)
    top_purpose, top_purpose_count = top_item(PURPOSE_COUNTS)
    top_format, top_format_count = top_item(FORMAT_COUNTS)
    cols = st.columns(4)
    with cols[0]: metric("Selected respondents", f"{respondent_count:,}", f"Of {total:,} cleaned responses", "👥")
    with cols[1]: metric("Read several times/week", f"{FREQUENCY_COUNTS.get('Several times a week', 0) / respondent_count * 100:.1f}%", f"{FREQUENCY_COUNTS.get('Several times a week', 0)} students", "📖")
    with cols[2]: metric("Most-read material", top_material, f"{top_material_count / respondent_count * 100:.1f}% of respondents", "📚")
    with cols[3]: metric("Top reported barrier", top_barrier, f"{top_barrier_count / respondent_count * 100:.1f}% of respondents", "📱")

    left, right = st.columns([1.15, 1])
    with left:
        show(count_bar(FREQUENCY_COUNTS, "How Often Do Students Read?", horizontal=True), 390)
    with right:
        show(count_bar(MATERIAL_COUNTS, "Most-Read Materials", horizontal=True), 390)

    section("What stands out", "A quick read of the strongest findings.")
    left, right = st.columns(2)
    with left:
        insight("Reading frequency",
                f"{freq_mode} is the most common habit ({freq_count / respondent_count * 100:.1f}%). "
                f"The leading weekly reading-time response is {most_read_time.lower()} "
                f"({most_read_time_count / respondent_count * 100:.1f}%).")
        insight("Why students read",
                f"{top_purpose} is the leading purpose ({top_purpose_count / respondent_count * 100:.1f}%). "
                f"{top_material} is the most-read material ({top_material_count / respondent_count * 100:.1f}%).")
    with right:
        insight("Preferred format",
                f"{top_format} is the most common choice "
                f"({top_format_count / respondent_count * 100:.1f}% of this group).")
        insight("Screen-related barriers are prominent",
                f"{top_barrier} leads at {top_barrier_count / respondent_count * 100:.1f}% "
                "of the selected respondents.")
    note("The filters above apply to every chart and finding. Hour averages use category midpoints and are estimates.")

# ========================== RQ1 ==========================
elif page == "Reading Frequency & Time":
    section("Reading Frequency & Time", "Explore how regularly students read and how much time they spend reading each week.")
    left, right = st.columns(2)
    with left: show(count_bar(FREQUENCY_COUNTS, "Reading Frequency", horizontal=True), 400)
    with right: show(count_bar(READ_HOURS_COUNTS, "Weekly Reading Time", horizontal=True), 400)
    show(count_bar(BOOKS_MONTH_COUNTS, "Books Read per Month", horizontal=True), 390)

    st.markdown("<div class='section-title'>Estimated Reading and Screen Hours</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: metric("Reading", f"{numpy_mean(data['Read_Hours_Num']):.2f} hrs", "Estimated weekly mean", "📖")
    with c2: metric("Non-academic screen", f"{numpy_mean(data['Screen_Hours_Num']):.2f} hrs", "Estimated daily mean", "📱")
    with c3: metric("Social media", f"{numpy_mean(data['Social_Hours_Num']):.2f} hrs", "Estimated daily mean", "💬")
    note("Hours are estimates based on the midpoint of each selected response range. These averages and distributions reflect only respondents selected above.")

# ========================== RQ2 ==========================
elif page == "Reading Preferences":
    section("Reading Preferences", "Explore the materials, formats, content and purposes students selected.")
    questions = [
        ("Reading Materials", MATERIAL_COUNTS),
        ("Preferred Reading Format", FORMAT_COUNTS),
        ("Preferred Reading Content", CONTENT_COUNTS),
        ("Main Purpose for Reading", PURPOSE_COUNTS)
    ]
    for idx in range(0, len(questions), 2):
        left, right = st.columns(2)
        for col, (label, counts) in zip([left, right], questions[idx:idx+2]):
            with col:
                show(count_bar(counts, label, horizontal=True), 370)
    tabs = st.tabs(["Materials", "Format", "Content", "Purpose"])
    for tab, (label, counts) in zip(tabs, questions):
        with tab:
            st.dataframe(percentage_table(counts, label), width="stretch", hide_index=True)

# ========================== RQ3 ==========================
elif page == "Student Profile":
    section("Student Profile", "See who responded, then compare reading frequency within each student group.")
    profile_cols = st.columns(4)
    for col, (label, counts) in zip(profile_cols, PROFILE_COUNTS.items()):
        with col:
            show(count_bar(counts, label, horizontal=True), 300)

    st.markdown("<div class='section-title'>Reading Frequency by Group</div>", unsafe_allow_html=True)
    field_label = st.selectbox("Choose a student group", {
        "Gender": "Gender", "Programme": "Programme",
        "Year of Study": "Year of Study", "Age Group": "Age Group"
    }.keys())
    cross = GROUP_FREQUENCY[field_label].reindex(columns=FREQUENCY_ORDER, fill_value=0)
    fig = go.Figure()
    for i, category in enumerate(FREQUENCY_ORDER):
        fig.add_trace(go.Bar(name=category, x=cross.index.astype(str), y=cross[category],
                             marker_color=PALETTE[i % len(PALETTE)],
                             hovertemplate="%{x}<br>%{y:.1f}%<extra>"+category+"</extra>"))
    fig.update_layout(barmode="stack", title=f"Reading Frequency by {field_label}",
                      xaxis_title=field_label, yaxis_title="Percentage of students (%)",
                      yaxis=dict(range=[0,100], ticksuffix="%"))
    show(fig, 470)
    st.markdown("#### Percentage breakdown")
    st.dataframe(cross.round(1).reset_index(), width="stretch", hide_index=True)
    weekly_reading = cross["Several times a week"]
    if not weekly_reading.empty:
        leading_group = weekly_reading.idxmax()
        insight(
            "Group comparison",
            f"{leading_group} has the highest share reporting reading several times a week "
            f"({weekly_reading.loc[leading_group]:.1f}%) in this selection. "
            "This is a descriptive comparison; group sizes differ and no significance test is applied."
        )
    note("Percentages are calculated within each group and the table reflects only respondents selected above.")

# ========================== RQ4 ==========================
elif page == "Screen Time & Barriers":
    section("Screen Time & Reading Barriers", "Explore reported screen use, social media use and the factors that make reading difficult.")
    c1, c2 = st.columns(2)
    with c1: show(count_bar(SCREEN_HOURS_COUNTS, "Daily Non-Academic Screen Time", horizontal=True), 390)
    with c2: show(count_bar(SOCIAL_HOURS_COUNTS, "Daily Social Media Time", horizontal=True), 390)

    st.markdown("<div class='section-title'>Relationship Between Time Use</div>", unsafe_allow_html=True)
    correlation_text = CORRELATION.round(2).astype(object).where(CORRELATION.notna(), "N/A")
    heat = go.Figure(go.Heatmap(z=CORRELATION.values, x=CORRELATION.columns, y=CORRELATION.index,
                                zmin=-1, zmax=1, colorscale=[[0,"#5B5FEF"],[0.5,"#FFFFFF"],[1,"#00C2A8"]],
                                text=correlation_text.values, texttemplate="%{text}",
                                colorbar=dict(title="Correlation")))
    heat.update_layout(title="Correlation Matrix: Reading and Screen Use", height=350,
                       margin=dict(l=25,r=25,t=60,b=30))
    show(heat, 370)
    read_screen = CORRELATION.loc["Reading hours/week", "Screen hours/day"]
    read_social = CORRELATION.loc["Reading hours/week", "Social media hours/day"]
    screen_social = CORRELATION.loc["Screen hours/day", "Social media hours/day"]
    insight(
        "How to read these relationships",
        f"Reading and screen time: r = {format_correlation(read_screen)}; "
        f"reading and social media time: r = {format_correlation(read_social)}; "
        f"screen and social media time: r = {format_correlation(screen_social)}. "
        "These correlations describe association, not cause and effect. "
        "Hours are estimated from response-range midpoints."
    )

    st.markdown("<div class='section-title'>Reported Barriers to Reading</div>", unsafe_allow_html=True)
    show(count_bar(BARRIER_COUNTS, "Barriers Selected by Students", horizontal=True), 450)
    note("Students could report more than one barrier. Therefore, the total number of barrier selections can be higher than the number of respondents. Correlation indicates association and does not prove cause and effect.")

# -------------------------- Team and Footer --------------------------
st.markdown("<div class='section-title'>Meet the team</div>", unsafe_allow_html=True)
team_members = [
    ("Sangay Wangmo", "sangay.png"),
    ("Tshering Choden", "tshering.png"),
    ("Chimi Wangmo", "chimi.png"),
    ("Rinzin Wangmo", "rinzin.png"),
    ("Ugyen Yangzom", "ugyen.png"),
    ("Jamyang Choden", "jamyang.png")
]
asset_dir = Path(__file__).parent / "assets"

def portrait_html(path, name, image_class, fallback):
    if path.is_file() and path.stat().st_size > 0:
        image_data = base64.b64encode(path.read_bytes()).decode("ascii")
        return (
            f"<img class='{image_class}' src='data:image/png;base64,{image_data}' "
            f"alt='Portrait of {escape(name)}'>"
        )
    return (
        f"<div class='{image_class} team-fallback' role='img' "
        f"aria-label='Portrait unavailable for {escape(name)}'>{escape(fallback)}</div>"
    )

team_cards = []
for name, image_name in team_members:
    initials = "".join(part[0] for part in name.split()[:2])
    portrait = portrait_html(asset_dir / image_name, name, "team-photo", initials)
    team_cards.append(
        f"<article class='team-card'>{portrait}"
        f"<div class='team-member-name'>{escape(name)}</div></article>"
    )

supervisor_path = asset_dir / "Mr.Sangay.png"
if not supervisor_path.is_file() or supervisor_path.stat().st_size == 0:
    supervisor_path = asset_dir / "thinley.png"
supervisor_portrait = portrait_html(
    supervisor_path, "Mr. Sangay Thinley", "supervisor-photo", "ST"
)
st.markdown(
    "<section class='team-grid' aria-label='Student team'>"
    + "".join(team_cards)
    + "</section>"
    + "<section class='supervisor-card' aria-label='Project supervisor'>"
    + supervisor_portrait
    + "<div class='supervisor-name'>Mr. Sangay Thinley</div>"
    + "<div class='supervisor-role'>Supervisor</div></section>",
    unsafe_allow_html=True
)

st.markdown(f"""
<div class="footer">
  <strong>Samtse College of Education</strong>
  <div class="footer-rights">© {datetime.now().year}. All rights reserved.</div>
</div>
""", unsafe_allow_html=True)
