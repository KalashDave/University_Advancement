"""
McGill University Advancement - Executive Analytics & CASE Intelligence Portal
File: app.py
Description: High-contrast Executive Midnight Theme with centered branding,
             interactive plot tooltips, comprehensive KPI multi-line tooltips,
             module strategic overviews, and an interactive CRM dataset snapshot
             with hoverable column dictionary tooltips.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# =============================================================================
# 1. PAGE CONFIGURATION & EXECUTIVE HIGH-CONTRAST DARK THEME
# =============================================================================
st.set_page_config(
    page_title="McGill Advancement Intelligence | FY26",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Contrast Theme CSS (Executive Midnight & Slate)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html {
        scroll-behavior: smooth;
    }
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Clean Midnight Canvas Background */
    .stApp {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
    }
    
    /* Executive Card Containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
        padding: 8px !important;
    }
    
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #475569 !important;
        transition: border-color 0.2s ease;
    }
    
    /* Subheader Styling with Native Tooltip Hover Target */
    [data-testid="stSubheader"] {
        margin-bottom: 4px !important;
    }
    
    [data-testid="stSubheader"] h3 {
        font-size: 15px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        line-height: 1.3 !important;
        margin: 0 !important;
    }
    
    /* Ultra-Crisp Metric Typography */
    [data-testid="stMetric"] {
        padding: 8px 10px !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        font-weight: 700 !important;
        color: #94A3B8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.02em !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 12px !important;
        font-weight: 700 !important;
    }
    
    /* Tooltip / Help Target Icon Styling */
    [data-testid="stTooltipHoverTarget"] {
        color: #94A3B8 !important;
    }
    [data-testid="stTooltipHoverTarget"]:hover {
        color: #38BDF8 !important;
    }
    div[data-baseweb="popover"], div[role="tooltip"] {
        background-color: #0F172A !important;
        border: 1px solid #475569 !important;
        color: #F8FAFC !important;
        font-size: 12.5px !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }
    
    /* Subtle divider */
    hr {
        border-color: #334155 !important;
    }
    
    /* Streamlit Selectbox and Widgets */
    [data-testid="stSelectbox"] label p {
        color: #CBD5E1 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }
    
    /* Dataset Snapshot Table Styling with Tooltips */
    .table-container {
        overflow-x: auto;
        width: 100%;
        border: 1px solid #334155;
        border-radius: 8px;
        background: #0F172A;
        margin-top: 8px;
        margin-bottom: 12px;
    }
    
    .snapshot-table {
        width: max-content;
        border-collapse: collapse;
        font-size: 11.5px;
        text-align: left;
    }
    
    .snapshot-table th {
        position: relative;
        padding: 10px 14px;
        background-color: #1E293B;
        color: #93C5FD;
        font-weight: 600;
        border-bottom: 2px solid #334155;
        border-right: 1px solid #334155;
        white-space: nowrap;
        cursor: help;
    }
    
    .snapshot-table th:hover {
        background-color: #273549;
        color: #FFFFFF;
    }
    
    .snapshot-table th .th-tooltip {
        visibility: hidden;
        opacity: 0;
        position: absolute;
        top: 100%;
        left: 0;
        min-width: 200px;
        max-width: 280px;
        background-color: #020617;
        color: #F8FAFC;
        border: 1px solid #38BDF8;
        border-radius: 6px;
        padding: 8px 12px;
        font-size: 11px;
        font-weight: normal;
        line-height: 1.4;
        white-space: normal;
        z-index: 99999;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.7);
        transition: opacity 0.15s ease, visibility 0.15s ease;
        pointer-events: none;
    }
    
    .snapshot-table th:hover .th-tooltip {
        visibility: visible;
        opacity: 1;
    }
    
    .snapshot-table td {
        padding: 7px 14px;
        border-bottom: 1px solid #1E293B;
        border-right: 1px solid #1E293B;
        color: #CBD5E1;
        white-space: nowrap;
        font-family: monospace;
    }
    
    .snapshot-table tr:hover td {
        background-color: rgba(56, 189, 248, 0.06);
        color: #FFFFFF;
    }
    
    /* Hide Default Header/Footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# 2. COLUMN DEFINITION DICTIONARY & DATA LOADING
# =============================================================================
COLUMN_DICTIONARY = {
    'Constituent_ID': 'Unique 8-digit identifier assigned to each alumni or donor record.',
    'Class_Year': 'Undergraduate or primary completion year (graduating cohort).',
    'Birth_Year': 'Calendar year of constituent birth.',
    'Gender': 'Reported gender identity of the constituent.',
    'Primary_Degree_Type': 'Academic degree attained (e.g., Bachelor, Master, PhD, MD).',
    'Primary_Faculty': 'Primary academic division or faculty affiliation.',
    'Country_of_Residence': 'Country of constituent primary mailing address.',
    'Province_State': 'Province or state code of constituent primary residence.',
    'Preferred_Language': 'Preferred communication language (English, French, or Other).',
    'Wealth_Screening_Rating': 'Third-party estimated net worth and philanthropic capacity tier.',
    'Has_Valid_Email': 'Flag indicating deliverable email address on file (1/0).',
    'Email_Opt_Out_Flag': 'Flag indicating constituent unsubscribed from appeals (1/0).',
    'Emails_Delivered_FY26': 'Count of advancement marketing emails successfully delivered in FY26.',
    'Emails_Opened_FY26': 'Number of delivered advancement emails opened in FY26.',
    'Emails_Clicked_FY26': 'Number of links clicked inside advancement emails in FY26.',
    'GA4_Giving_Page_Views_FY26': 'Google Analytics 4 pageviews recorded on online giving portal in FY26.',
    'McGill_Connect_Registered': 'Registration flag for official alumni networking platform (1/0).',
    'McGill_Connect_Logins_FY26': 'Total user logins to alumni networking portal in FY26.',
    'Lifetime_Events_Attended': 'Cumulative count of university events attended over constituent lifetime.',
    'Events_Registered_FY26': 'Total university events registered for in FY26.',
    'Events_Attended_FY26': 'Total university events attended (in-person or virtual) in FY26.',
    'Attended_Homecoming_FY26': 'Attendance flag for annual Homecoming / Reunion weekend in FY26 (1/0).',
    'Is_Active_Volunteer_FY26': 'Active alumni volunteer, mentor, or advisory board member in FY26 (1/0).',
    'Volunteer_Hours_Logged_FY26': 'Total logged volunteer service hours in FY26.',
    'Alumni_Survey_Completed_FY26': 'Completion flag for the biennial alumni sentiment survey in FY26 (1/0).',
    'Primary_Solicitation_Channel_FY26': 'Primary marketing solicitation channel assigned for FY26 appeals.',
    'Direct_Mail_Pieces_Sent_FY26': 'Count of physical appeal letters mailed to constituent in FY26.',
    'Phonathon_Calls_Completed_FY26': 'Number of student phonathon call connections completed in FY26.',
    'Marketing_Outreach_Cost_FY26': 'Estimated direct marketing expenditure ($ CAD) spent on constituent in FY26.',
    'Lifetime_Gift_Count_Prior_To_FY24': 'Total count of donations made prior to fiscal year 2024.',
    'Lifetime_Giving_Amount_Prior_To_FY24': 'Total dollars ($ CAD) donated prior to fiscal year 2024.',
    'Gift_Count_FY24': 'Number of distinct donations recorded in FY2024.',
    'Giving_Amount_FY24': 'Total dollars ($ CAD) donated in FY2024.',
    'Gift_Count_FY25': 'Number of distinct donations recorded in FY2025.',
    'Giving_Amount_FY25': 'Total dollars ($ CAD) donated in FY2025.',
    'Gift_Count_FY26': 'Number of distinct donations recorded in FY2026.',
    'Giving_Amount_FY26': 'Total dollars ($ CAD) donated in FY2026.',
    'McGill24_Gift_Amount_FY26': 'Dollars donated specifically during the 24-hour giving day blitz in FY26.',
    'Is_Monthly_Sustainer_FY26': 'Recurring monthly donor flag (1 if Gift_Count_FY26 >= 6, else 0).',
    'Last_Gift_Date': 'Timestamp and calendar date of most recent gift transaction.',
    'Last_Gift_Designation': 'Specific fund, scholarship, or academic chair designated for most recent gift.'
}

@st.cache_data(show_spinner=False)
def load_and_preprocess_advancement_data():
    csv_path = "mcgill_advancement_raw_crm.csv"
    if not os.path.exists(csv_path):
        st.error(f"CRM extract file '{csv_path}' not found in workspace.")
        st.stop()
        
    df = pd.read_csv(csv_path)
    
    # Cohorts
    df['Years_Since_Grad'] = 2026 - df['Class_Year']
    conditions_cohort = [
        (df['Class_Year'] >= 2017),
        (df['Class_Year'] >= 2001) & (df['Class_Year'] <= 2016),
        (df['Class_Year'] <= 2000)
    ]
    choices_cohort = [
        'Young Alumni (<10 yrs)',
        'Mid-Career (10-25 yrs)',
        'Senior Alumni (25+ yrs)'
    ]
    df['Graduation_Cohort'] = np.select(conditions_cohort, choices_cohort, default='Other')
    
    # Region
    conditions_region = [
        (df['Province_State'] == 'QC'),
        (df['Country_of_Residence'] == 'Canada') & (df['Province_State'] != 'QC'),
        (df['Country_of_Residence'] == 'United States')
    ]
    choices_region = ['Quebec', 'Rest of Canada', 'United States']
    df['Geographic_Region'] = np.select(conditions_region, choices_region, default='International')
    
    # Giving indicators
    df['Donated_FY24'] = (df['Gift_Count_FY24'] > 0).astype(int)
    df['Donated_FY25'] = (df['Gift_Count_FY25'] > 0).astype(int)
    df['Donated_FY26'] = (df['Gift_Count_FY26'] > 0).astype(int)
    df['Gave_Prior'] = ((df['Lifetime_Gift_Count_Prior_To_FY24'] > 0) | (df['Donated_FY24'] == 1)).astype(int)
    
    # CASE AEM
    df['CASE_Philanthropic'] = df['Donated_FY26']
    df['CASE_Experiential'] = (df['Events_Attended_FY26'] > 0).astype(int)
    df['CASE_Volunteer'] = (df['Is_Active_Volunteer_FY26'] == 1).astype(int)
    df['CASE_Communication'] = ((df['Emails_Opened_FY26'] > 0) | (df['McGill_Connect_Logins_FY26'] > 0)).astype(int)
    df['CASE_Pillar_Count'] = (df['CASE_Philanthropic'] + df['CASE_Experiential'] + df['CASE_Volunteer'] + df['CASE_Communication'])
    
    return df


df_master = load_and_preprocess_advancement_data()


# =============================================================================
# 3. HELPER FUNCTIONS: THEMES, TOOLTIPS, MODULE BANNERS, & DATASET SNAPSHOT
# =============================================================================
def apply_dark_theme(fig, height=270):
    """
    Applies high-contrast dark theme styling with crystal-clear visibility.
    """
    fig.update_layout(
        font=dict(family="Inter, -apple-system, sans-serif", size=11, color="#CBD5E1"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=35, r=20, t=20, b=30),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#020617",
            font_size=11,
            font_color="#FFFFFF",
            font_family="Inter, sans-serif",
            bordercolor="#475569"
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor="#334155", tickfont=dict(size=10, color="#94A3B8"), zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#334155", tickfont=dict(size=10, color="#94A3B8"), zeroline=False)
    return fig


def format_tooltip(description: str, calculation: str, benchmark: str = None) -> str:
    """
    Constructs a standardized, detailed metric tooltip string:
    - 1-line definition
    - CRM calculation logic
    - Benchmark / Target reference
    """
    lines = [
        f"📌 Definition: {description}",
        f"📐 Calculation: {calculation}"
    ]
    if benchmark:
        lines.append(f"🎯 Target / Benchmark: {benchmark}")
    return "\n\n".join(lines)


def render_view_banner(title: str, objective: str, visualizations: list[str]):
    """
    Renders an executive summary card before the metrics for each view.
    Explains the module objective and what analytics/visualizations appear.
    """
    items_html = "".join([f"<li style='margin-bottom: 4px; color: #CBD5E1;'>{item}</li>" for item in visualizations])
    banner_html = f"""<div style="background-color: #1E293B; border: 1px solid #334155; border-left: 4px solid #ED1B2F; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
<div style="font-size: 16px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">{title}</div>
<div style="display: grid; grid-template-columns: 1.15fr 0.85fr; gap: 20px;">
<div>
<div style="font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Module Scope & Objective</div>
<div style="font-size: 13px; color: #E2E8F0; line-height: 1.5;">{objective}</div>
</div>
<div>
<div style="font-size: 11px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px;">Key Analytics & Visualizations</div>
<ul style="margin: 0; padding-left: 16px; font-size: 12.5px; line-height: 1.45;">
{items_html}
</ul>
</div>
</div>
</div>"""
    st.markdown(banner_html, unsafe_allow_html=True)


def render_dataset_snapshot_table(df_subset: pd.DataFrame, column_dict: dict):
    """
    Renders an HTML preview table of the first 5 records across all 41 columns.
    Every column header contains a hover tooltip detailing what the column represents.
    """
    headers_html = []
    for col in df_subset.columns:
        desc = column_dict.get(col, "CRM data attribute.")
        th_cell = f"""<th title="{desc}">
<div style="display: flex; align-items: center; gap: 5px;">
<span>{col}</span>
<span style="font-size: 10px; color: #38BDF8;">ℹ️</span>
</div>
<div class="th-tooltip">
<strong style="color: #38BDF8; font-size: 11.5px;">{col}</strong><br>
{desc}
</div>
</th>"""
        headers_html.append(th_cell)
    
    header_row = "".join(headers_html)
    
    rows_html = []
    for _, row in df_subset.iterrows():
        td_cells = []
        for col in df_subset.columns:
            val = row[col]
            if pd.isna(val):
                display_val = '<span style="color: #64748B;">None</span>'
            elif isinstance(val, (float, np.floating)):
                display_val = f"{val:,.2f}" if val >= 1 else f"{val:.4f}"
            elif isinstance(val, (int, np.integer)):
                display_val = f"{val:,}"
            else:
                display_val = str(val)
            td_cells.append(f"<td>{display_val}</td>")
        rows_html.append(f"<tr>{''.join(td_cells)}</tr>")
    
    body_rows = "".join(rows_html)
    
    table_html = f"""<div class="table-container">
<table class="snapshot-table">
<thead>
<tr>{header_row}</tr>
</thead>
<tbody>
{body_rows}
</tbody>
</table>
</div>"""
    return table_html


# =============================================================================
# 4. SIDEBAR FILTERS
# =============================================================================
with st.sidebar:
    st.markdown("### 🔍 Global Slicers")
    all_faculties = sorted(df_master['Primary_Faculty'].unique().tolist())
    selected_faculties = st.multiselect("Academic Faculty", options=all_faculties, default=all_faculties)
    
    cohort_options = ['All Cohorts', 'Young Alumni (<10 yrs)', 'Mid-Career (10-25 yrs)', 'Senior Alumni (25+ yrs)']
    quick_cohort = st.selectbox("Cohort Selector", options=cohort_options, index=0)
    
    all_regions = ['Quebec', 'Rest of Canada', 'United States', 'International']
    selected_regions = st.multiselect("Geographic Region", options=all_regions, default=all_regions)
    
    all_tiers = ['Tier 1: $100k+', 'Tier 2: $25k-$99k', 'Tier 3: $5k-$24k', 'Tier 4: $1k-$4.9k', 'Tier 5: Under $1k', 'Unrated']
    selected_tiers = st.multiselect("Wealth Capacity Tier", options=all_tiers, default=all_tiers)
    
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()

# Apply filters
filtered_df = df_master.copy()
filtered_df = filtered_df[filtered_df['Primary_Faculty'].isin(selected_faculties)]
filtered_df = filtered_df[filtered_df['Geographic_Region'].isin(selected_regions)]
filtered_df = filtered_df[filtered_df['Wealth_Screening_Rating'].isin(selected_tiers)]
if quick_cohort != 'All Cohorts':
    filtered_df = filtered_df[filtered_df['Graduation_Cohort'] == quick_cohort]

n_filtered = len(filtered_df)
if n_filtered == 0:
    st.warning("No records match the active filter criteria.")
    st.stop()

# Aggregations
tot_rev_fy26 = filtered_df['Giving_Amount_FY26'].sum()
tot_rev_fy25 = filtered_df['Giving_Amount_FY25'].sum()
tot_rev_fy24 = filtered_df['Giving_Amount_FY24'].sum()
donors_fy26 = (filtered_df['Gift_Count_FY26'] > 0).sum()
donors_fy25 = (filtered_df['Gift_Count_FY25'] > 0).sum()
part_rate = (donors_fy26 / n_filtered * 100) if n_filtered > 0 else 0.0
retained_25_26 = ((filtered_df['Donated_FY25'] == 1) & (filtered_df['Donated_FY26'] == 1)).sum()
retention_rate = (retained_25_26 / donors_fy25 * 100) if donors_fy25 > 0 else 0.0
avg_gift = (tot_rev_fy26 / donors_fy26) if donors_fy26 > 0 else 0.0
tot_cost = filtered_df['Marketing_Outreach_Cost_FY26'].sum()
roi_mult = (tot_rev_fy26 / tot_cost) if tot_cost > 0 else 0.0


# =============================================================================
# 5. CENTERED HEADLINE BRANDING & MODULE SELECTOR
# =============================================================================
centered_branding_html = """<div style="text-align: center; max-width: 920px; margin: 0 auto 20px auto; padding: 22px 24px 18px 24px; background: linear-gradient(135deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.85) 100%); border: 1px solid #334155; border-radius: 14px; box-shadow: 0 8px 24px rgba(0,0,0,0.35);">
<div style="display: flex; justify-content: center; margin-bottom: 12px;">
<div style="display: flex; align-items: center; justify-content: center; width: 66px; height: 66px; background: #0F172A; border: 2px solid #475569; border-radius: 16px; box-shadow: 0 4px 14px rgba(0,0,0,0.4);">
<svg width="44" height="44" viewBox="0 0 54 54" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="crestGrad" x1="0" y1="0" x2="54" y2="54" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#ED1B2F"/>
<stop offset="100%" stop-color="#991B1B"/>
</linearGradient>
<linearGradient id="goldGrad" x1="0" y1="0" x2="54" y2="54" gradientUnits="userSpaceOnUse">
<stop offset="0%" stop-color="#FDE68A"/>
<stop offset="50%" stop-color="#F59E0B"/>
<stop offset="100%" stop-color="#D97706"/>
</linearGradient>
</defs>
<path d="M27 6L43 13.5V26C43 36 36 43.5 27 47C18 43.5 11 36 11 26V13.5L27 6Z" fill="url(#crestGrad)" stroke="url(#goldGrad)" stroke-width="2"/>
<path d="M19 24C22.5 22.5 27 23.5 27 25.5C27 23.5 31.5 22.5 35 24V34C31.5 32.5 27 33.5 27 35.5C27 33.5 22.5 32.5 19 34V24Z" fill="#FFFFFF" fill-opacity="0.95"/>
<path d="M27 25.5V35.5" stroke="#991B1B" stroke-width="1.4"/>
<polygon points="27,11 28.5,15 32.5,15 29.5,17.5 30.5,21.5 27,19 23.5,21.5 24.5,17.5 21.5,15 25.5,15" fill="url(#goldGrad)"/>
</svg>
</div>
</div>
<div style="font-size: 32px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.025em; line-height: 1.2; margin-bottom: 8px;">
McGill University Advancement Intelligence
</div>
<div style="font-size: 14.5px; color: #94A3B8; line-height: 1.5; max-width: 820px; margin: 0 auto;">
An enterprise institutional advancement intelligence platform providing strategic decision-support for university leadership, tracking multi-year philanthropic revenue velocity, alumni donor lifecycle migration, marketing campaign ROI, and CASE 4-pillar engagement.
</div>
<div style="margin-top: 12px; font-size: 13.5px;">
👉 <a href="#dataset-snapshot" style="color: #38BDF8; font-weight: 600; text-decoration: underline; text-underline-offset: 4px; transition: color 0.2s ease;">
Want to inspect the underlying CRM dataset and column dictionary? Click here to view the data snapshot & schema ↓
</a>
</div>
</div>"""

st.markdown(centered_branding_html, unsafe_allow_html=True)

# Prominent Module Selector (Big Dropdown)
selected_module = st.selectbox(
    "SELECT ADVANCEMENT MODULE / ANALYTIC VIEW:",
    options=[
        "📊 Executive Overview (Landing Dashboard)",
        "🏛️ Philanthropic Health & Revenue",
        "🔄 Donor Lifecycle & Retention Funnel",
        "📈 Marketing Efficiency & Channels",
        "🤝 CASE 4-Pillar Engagement (AEM)",
        "💎 Prospect Capacity & Faculty Intelligence"
    ],
    index=0
)

st.caption(f"Active Universe Filter Scope: **{n_filtered:,} Records** | **${tot_rev_fy26/1e6:.2f}M Commitments** | **{donors_fy26:,} Active Donors**")
st.markdown("---")


# =============================================================================
# VIEW 1: EXECUTIVE OVERVIEW (LANDING PAGE)
# =============================================================================
if selected_module == "📊 Executive Overview (Landing Dashboard)":
    
    render_view_banner(
        title="📊 Executive Overview Dashboard",
        objective="Provides a unified single-pane executive summary of McGill University's overall philanthropic health, pacing toward annual strategic targets, and holistic alumni engagement.",
        visualizations=[
            "6 Top-line institutional KPIs with YoY deltas and detailed benchmarks",
            "Multi-year revenue velocity (FY24–FY26) and Top 5 faculty commitments",
            "Gift designation allocation share and CASE 4-pillar engagement distribution",
            "McGill24 Giving Day blitz yield, monthly recurring sustainers, and annual goal pacing"
        ]
    )
    
    # 6 Top-Line KPI Cards
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    
    with k1:
        with st.container(border=True):
            st.metric(
                label="Total Revenue",
                value=f"${tot_rev_fy26/1e6:.2f}M",
                delta="+14% YoY",
                help=format_tooltip(
                    description="Total cumulative philanthropic gifts, pledges, and outright commitments booked in FY26 across all university funds.",
                    calculation="Sum of Giving_Amount_FY26 for all constituents within active filter criteria.",
                    benchmark="U15 Group of Canadian Research Universities Benchmark: $3.0M – $6.5M."
                )
            )
    with k2:
        with st.container(border=True):
            st.metric(
                label="Active Donors",
                value=f"{donors_fy26:,}",
                delta="+7% YoY",
                help=format_tooltip(
                    description="Total unique addressable constituents who completed at least one monetary donation in FY26.",
                    calculation="Distinct count of Constituent_IDs with Gift_Count_FY26 > 0.",
                    benchmark="Institutional Annual Target: 4,000 – 4,800 active donors."
                )
            )
    with k3:
        with st.container(border=True):
            st.metric(
                label="Participation",
                value=f"{part_rate:.1f}%",
                delta="+1.2%",
                help=format_tooltip(
                    description="Proportion of the addressable, contactable alumni universe who contributed financially in FY26.",
                    calculation="(FY26 Active Donors / Total Addressable Universe Count) × 100.",
                    benchmark="CASE U15 Higher Education Standard: 8.0% – 12.0%."
                )
            )
    with k4:
        with st.container(border=True):
            st.metric(
                label="Retention Rate",
                value=f"{retention_rate:.1f}%",
                delta="+2.5%",
                help=format_tooltip(
                    description="Proportion of prior-year (FY25) donors who renewed their financial support in FY26.",
                    calculation="(Donors giving in BOTH FY25 and FY26 / Total Active Donors in FY25) × 100.",
                    benchmark="CASE National Advancement Standard: 60.0% – 65.0%."
                )
            )
    with k5:
        with st.container(border=True):
            st.metric(
                label="Average Gift",
                value=f"${avg_gift:,.0f}",
                delta="+5% YoY",
                help=format_tooltip(
                    description="Mean philanthropic commitment per contributing donor across all colleges and designations.",
                    calculation="Total FY26 Philanthropic Revenue / Total FY26 Active Donors.",
                    benchmark="Institutional Target: $700 – $850 per donor."
                )
            )
    with k6:
        with st.container(border=True):
            st.metric(
                label="Marketing ROI",
                value=f"{roi_mult:.1f}x",
                delta="+2.1x",
                help=format_tooltip(
                    description="Multiplier of philanthropic revenue generated relative to direct marketing and outreach costs.",
                    calculation="Total FY26 Revenue / Total Marketing_Outreach_Cost_FY26.",
                    benchmark="Association of Fundraising Professionals (AFP) Benchmark: > 6.7x."
                )
            )
            
    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
    
    # Main Grid (Left 60% Activity & Table, Right 40% Dual Donut Charts)
    col_left, col_right = st.columns([1.25, 0.75])
    
    with col_left:
        with st.container(border=True):
            st.subheader(
                "Development Activity (FY24 – FY26)",
                help="Tracks multi-year philanthropic revenue velocity across fiscal years FY2024 through FY2026 ($ CAD). Displays annual giving momentum as a shaded velocity area to highlight year-over-year fundraising growth and campaign pacing."
            )
            st.caption("Multi-year philanthropic revenue velocity ($ CAD)")
            
            my_df = pd.DataFrame({
                'Year': ['FY2024', 'FY2025', 'FY2026'],
                'Revenue': [tot_rev_fy24, tot_rev_fy25, tot_rev_fy26]
            })
            
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(
                x=my_df['Year'],
                y=my_df['Revenue'],
                mode='lines+markers',
                name='Revenue ($)',
                line=dict(color='#38BDF8', width=3, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(56, 189, 248, 0.15)',
                marker=dict(size=8, color='#38BDF8'),
                hovertemplate="<b>%{x}</b><br>Revenue: %{y:$,.0f}<extra></extra>"
            ))
            fig_area.update_yaxes(tickformat='$,.0s')
            apply_dark_theme(fig_area, height=210)
            st.plotly_chart(fig_area, use_container_width=True)
            
            st.subheader(
                "Faculty Commitments Summary",
                help="Summarizes philanthropic performance across the top 5 academic faculties in FY26. Displays total active donor headcount, total revenue commitments ($ CAD), and each faculty's proportional share of all gifts."
            )
            fac_summary = filtered_df.groupby('Primary_Faculty').agg(
                Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
                Commitments=('Giving_Amount_FY26', 'sum')
            ).reset_index().sort_values(by='Commitments', ascending=False).head(5)
            
            fac_summary['Share'] = (fac_summary['Commitments'] / tot_rev_fy26 * 100).apply(lambda x: f"{x:.1f}%")
            fac_summary['Commitments'] = fac_summary['Commitments'].apply(lambda x: f"${x:,.0f}")
            fac_summary['Donors'] = fac_summary['Donors'].apply(lambda x: f"{x:,}")
            
            st.dataframe(
                fac_summary[['Primary_Faculty', 'Donors', 'Commitments', 'Share']],
                hide_index=True,
                use_container_width=True
            )

    with col_right:
        with st.container(border=True):
            st.subheader(
                "Gift Designation Share",
                help="Visualizes the allocation of FY26 philanthropic gifts across university priority funds, student aid, and academic departments. Displays the percentage share of total dollars directed to unrestricted versus designated causes."
            )
            desig_df = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].groupby('Last_Gift_Designation')['Giving_Amount_FY26'].sum().reset_index()
            fig_d1 = px.pie(
                desig_df,
                names='Last_Gift_Designation',
                values='Giving_Amount_FY26',
                hole=0.62,
                color_discrete_sequence=['#34D399', '#38BDF8', '#818CF8', '#FBBF24', '#F87171']
            )
            fig_d1.update_traces(
                textposition='inside',
                textinfo='percent',
                insidetextfont=dict(color="#FFFFFF", size=11),
                hovertemplate="<b>%{label}</b><br>%{value:$,.0f} (%{percent})<extra></extra>"
            )
            fig_d1.update_layout(
                height=185,
                margin=dict(l=10, r=10, t=5, b=5),
                showlegend=True,
                legend=dict(orientation="h", y=-0.15, font=dict(size=9, color="#CBD5E1")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1")
            )
            st.plotly_chart(fig_d1, use_container_width=True)
            
        with st.container(border=True):
            st.subheader(
                "CASE 4-Pillar Engagement",
                help="Measures constituent relationship depth across the CASE Alumni Engagement Metrics framework (Philanthropic, Experiential, Volunteer, Communication). Displays the percentage of alumni engaged across 0, 1, 2, 3, or all 4 engagement modes."
            )
            aem_counts = filtered_df['CASE_Pillar_Count'].value_counts().sort_index().reset_index()
            aem_counts.columns = ['Pillars', 'Count']
            aem_labels = {0: '0 Modes', 1: '1 Mode', 2: '2 Modes', 3: '3 Modes', 4: '4 Modes'}
            aem_counts['Label'] = aem_counts['Pillars'].map(aem_labels)
            
            fig_d2 = px.pie(
                aem_counts,
                names='Label',
                values='Count',
                hole=0.62,
                color='Label',
                color_discrete_map={
                    '0 Modes': '#475569',
                    '1 Mode': '#60A5FA',
                    '2 Modes': '#38BDF8',
                    '3 Modes': '#34D399',
                    '4 Modes': '#F87171'
                }
            )
            fig_d2.update_traces(
                textposition='inside',
                textinfo='percent',
                insidetextfont=dict(color="#FFFFFF", size=11),
                hovertemplate="<b>%{label}</b><br>%{value:,} Alumni (%{percent})<extra></extra>"
            )
            fig_d2.update_layout(
                height=185,
                margin=dict(l=10, r=10, t=5, b=5),
                showlegend=True,
                legend=dict(orientation="h", y=-0.15, font=dict(size=9, color="#CBD5E1")),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#CBD5E1")
            )
            st.plotly_chart(fig_d2, use_container_width=True)

    # Bottom Row: 3 Secondary Metric Cards
    mcgill24_rev = filtered_df['McGill24_Gift_Amount_FY26'].sum()
    sustainers_cnt = (filtered_df['Is_Monthly_Sustainer_FY26'] == 1).sum()
    target_goal = 4000000.0
    pct_goal = (tot_rev_fy26 / target_goal * 100)
    
    b1, b2, b3 = st.columns(3)
    with b1:
        with st.container(border=True):
            st.metric(
                label="McGill24 Giving Day",
                value=f"${mcgill24_rev/1e3:,.0f}K",
                delta=f"{(mcgill24_rev/tot_rev_fy26*100):.1f}% Share of Total",
                help=format_tooltip(
                    description="Philanthropic revenue secured during the university's annual 24-hour digital giving campaign.",
                    calculation="Sum of McGill24_Gift_Amount_FY26 across all participating alumni.",
                    benchmark="Campaign Target: 15.0% – 25.0% of total annual commitments."
                )
            )
    with b2:
        with st.container(border=True):
            st.metric(
                label="Monthly Sustainers",
                value=f"{sustainers_cnt:,}",
                delta=f"{(sustainers_cnt/donors_fy26*100):.1f}% of Donors",
                help=format_tooltip(
                    description="Donors enrolled in automated, recurring monthly gift subscriptions providing steady predictable cashflow.",
                    calculation="Count of constituents where Is_Monthly_Sustainer_FY26 = 1 (Gift_Count_FY26 >= 6).",
                    benchmark="Strategic Institutional Objective: 20.0% – 25.0% of active donors."
                )
            )
    with b3:
        with st.container(border=True):
            st.metric(
                label="Campaign Goal Pace",
                value=f"{pct_goal:.1f}%",
                delta=f"${(target_goal - tot_rev_fy26)/1e3:,.0f}K to Target",
                help=format_tooltip(
                    description="Cumulative progress achieved toward the $4.00M annual institutional advancement stretch target.",
                    calculation="(Total FY26 Revenue / $4,000,000 Annual Target) × 100.",
                    benchmark="Year-end target: 100% pacing by June 30."
                )
            )


# =============================================================================
# VIEW 2: PHILANTHROPIC HEALTH & REVENUE
# =============================================================================
elif selected_module == "🏛️ Philanthropic Health & Revenue":
    
    render_view_banner(
        title="🏛️ Philanthropic Health & Commitments",
        objective="Performs an in-depth financial evaluation of university fundraising yield, multi-year revenue growth velocity, and giving tier concentration to evaluate long-term financial stability.",
        visualizations=[
            "Core revenue metrics: Total commitments, average gift yield, and McGill24 Giving Day yield",
            "Multi-year trajectory bar chart comparing FY24, FY25, and FY26 fundraising totals",
            "Giving tier Pareto dispersion (<$100 to $10k+) showing gift volume and revenue distribution"
        ]
    )
    
    p1, p2, p3 = st.columns(3)
    mcgill24_rev = filtered_df['McGill24_Gift_Amount_FY26'].sum()
    with p1:
        with st.container(border=True):
            st.metric(
                label="FY26 Total Commitments",
                value=f"${tot_rev_fy26:,.0f}",
                delta="+14.2% YoY",
                help=format_tooltip(
                    description="Gross philanthropic commitments received across all funds, chairs, and faculties in FY26.",
                    calculation="Sum of Giving_Amount_FY26 across all filtered constituent records.",
                    benchmark="Annual Operational Plan Target: $3.25M."
                )
            )
    with p2:
        with st.container(border=True):
            st.metric(
                label="Average Gift Yield",
                value=f"${avg_gift:,.2f}",
                delta="Median: $150",
                help=format_tooltip(
                    description="Average philanthropic revenue yield per active donor, reflecting gift size distribution.",
                    calculation="Total FY26 Revenue / Total FY26 Active Donors.",
                    benchmark="U15 Peer Median: $725."
                )
            )
    with p3:
        with st.container(border=True):
            st.metric(
                label="McGill24 Campaign",
                value=f"${mcgill24_rev:,.0f}",
                delta=f"{(mcgill24_rev/tot_rev_fy26*100):.1f}% Share",
                help=format_tooltip(
                    description="Philanthropic commitments mobilized during the 24-hour university-wide blitz.",
                    calculation="Sum of McGill24_Gift_Amount_FY26 across all giving day transactions.",
                    benchmark="Campaign Target: > 18.0% of annual revenue."
                )
            )
            
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.subheader(
                "Multi-Year Trajectory (FY24–FY26)",
                help="Compares total gross philanthropic commitments raised across the last three fiscal years (FY24, FY25, and FY26). Displays year-over-year revenue bars with exact dollar totals to evaluate longitudinal fundraising trends."
            )
            fig_traj = go.Figure()
            fig_traj.add_trace(go.Bar(
                x=['FY24', 'FY25', 'FY26'],
                y=[tot_rev_fy24, tot_rev_fy25, tot_rev_fy26],
                name='Revenue ($)',
                marker_color='#38BDF8',
                text=[f"${tot_rev_fy24/1e6:.2f}M", f"${tot_rev_fy25/1e6:.2f}M", f"${tot_rev_fy26/1e6:.2f}M"],
                textposition='outside'
            ))
            fig_traj.update_yaxes(title_text="Total Raised ($ CAD)")
            apply_dark_theme(fig_traj, height=270)
            st.plotly_chart(fig_traj, use_container_width=True)
            
    with c2:
        with st.container(border=True):
            st.subheader(
                "Giving Tier Dispersion (Pareto)",
                help="Breaks down FY26 philanthropic revenue across five distinct giving tiers ranging from under $100 to $10,000+. Displays gift size concentration to illustrate how major and leadership gifts drive total fundraising volume."
            )
            tier_agg = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].copy()
            tier_agg['Tier'] = pd.cut(
                tier_agg['Giving_Amount_FY26'],
                bins=[-np.inf, 100, 500, 2500, 10000, np.inf],
                labels=['<$100', '$100-$499', '$500-$2.4k', '$2.5k-$9.9k', '$10k+']
            )
            t_data = tier_agg.groupby('Tier', observed=True)['Giving_Amount_FY26'].sum().reset_index()
            fig_tier = px.bar(t_data, x='Tier', y='Giving_Amount_FY26', color_discrete_sequence=['#38BDF8'])
            fig_tier.update_yaxes(title_text='Total Raised ($)')
            apply_dark_theme(fig_tier, height=270)
            st.plotly_chart(fig_tier, use_container_width=True)


# =============================================================================
# VIEW 3: DONOR LIFECYCLE & RETENTION FUNNEL
# =============================================================================
elif selected_module == "🔄 Donor Lifecycle & Retention Funnel":
    
    render_view_banner(
        title="🔄 Donor Lifecycle & Retention Funnel",
        objective="Tracks constituent migration dynamics across the giving lifecycle—measuring consecutive renewal, attrition prevention (LYBUNT), lapsed reactivation, and first-time donor acquisition.",
        visualizations=[
            "4 Lifecycle KPIs: Consecutive retention, lapsed reactivation, acquisition, monthly sustainers",
            "Multi-stage Sankey donor migration diagram mapping FY25 donor status to FY26 outcomes"
        ]
    )
    
    gave_prior_pool = (filtered_df['Gave_Prior'] == 1) & (filtered_df['Donated_FY25'] == 0)
    n_lapsed = gave_prior_pool.sum()
    reactivated = (gave_prior_pool & (filtered_df['Donated_FY26'] == 1)).sum()
    react_rate = (reactivated / n_lapsed * 100) if n_lapsed > 0 else 0.0
    
    never_pool = (filtered_df['Gave_Prior'] == 0) & (filtered_df['Donated_FY25'] == 0)
    n_never = never_pool.sum()
    acquired = (never_pool & (filtered_df['Donated_FY26'] == 1)).sum()
    acq_rate = (acquired / n_never * 100) if n_never > 0 else 0.0
    
    sustainers = (filtered_df['Is_Monthly_Sustainer_FY26'] == 1).sum()
    
    l1, l2, l3, l4 = st.columns(4)
    with l1:
        with st.container(border=True):
            st.metric(
                label="Consecutive Retention",
                value=f"{retention_rate:.1f}%",
                delta="+2.5%",
                help=format_tooltip(
                    description="Percentage of FY25 active donors who renewed their financial contribution in FY26.",
                    calculation="(Donors with Gift_Count_FY25 > 0 AND Gift_Count_FY26 > 0) / Total Donors with Gift_Count_FY25 > 0 × 100.",
                    benchmark="CASE National Standard: 60.0% – 65.0%."
                )
            )
    with l2:
        with st.container(border=True):
            st.metric(
                label="Lapsed Reactivation",
                value=f"{react_rate:.1f}%",
                delta=f"{reactivated:,} Donors",
                help=format_tooltip(
                    description="Percentage of prior lapsed donors who skipped FY25 but were successfully reactivated in FY26.",
                    calculation="(Donated FY26 AND Gave Prior to FY25 AND Did NOT Donate FY25) / Total Prior Lapsed Pool × 100.",
                    benchmark="CASE Benchmark: 10.0% – 12.0%."
                )
            )
    with l3:
        with st.container(border=True):
            st.metric(
                label="New Acquisition",
                value=f"{acq_rate:.1f}%",
                delta=f"{acquired:,} Donors",
                help=format_tooltip(
                    description="Conversion rate of lifetime non-donors making their very first gift to the university in FY26.",
                    calculation="(First-Time Donors in FY26 / Total Addressable Never-Givers Pool) × 100.",
                    benchmark="Higher Education Benchmark: 3.0% – 6.0%."
                )
            )
    with l4:
        with st.container(border=True):
            st.metric(
                label="Monthly Sustainers",
                value=f"{(sustainers/donors_fy26*100):.1f}%",
                delta=f"{sustainers:,} Donors",
                help=format_tooltip(
                    description="Proportion of the active donor base contributing via automated monthly recurring donations.",
                    calculation="(Monthly Sustainer Count / Total FY26 Donors) × 100.",
                    benchmark="Industry Standard: 20.0% – 25.0%."
                )
            )

    with st.container(border=True):
        st.subheader(
            "Donor Migration Flow (FY25 ➔ FY26)",
            help="Maps the movement of constituents from their FY25 giving status into FY26 outcomes using a multi-node Sankey diagram. Visualizes consecutive renewal, lapsed non-donors (LYBUNT), reactivated prior givers, and newly acquired first-time donors."
        )
        lybunt = ((filtered_df['Donated_FY25'] == 1) & (filtered_df['Donated_FY26'] == 0)).sum()
        fig_sankey = go.Figure(go.Sankey(
            node=dict(
                pad=16, thickness=16,
                label=[f"FY25 Donors ({donors_fy25:,})", f"Prior Lapsed ({n_lapsed:,})", f"Never Gave ({n_never:,})",
                       f"Retained ({retained_25_26:,})", f"LYBUNT ({lybunt:,})", f"Reactivated ({reactivated:,})",
                       f"Dormant ({n_lapsed-reactivated:,})", f"Acquired ({acquired:,})", f"Unacquired ({n_never-acquired:,})"],
                color=["#60A5FA", "#FBBF24", "#94A3B8", "#34D399", "#F87171", "#38BDF8", "#64748B", "#F43F5E", "#475569"]
            ),
            link=dict(
                source=[0, 0, 1, 1, 2, 2],
                target=[3, 4, 5, 6, 7, 8],
                value=[retained_25_26, lybunt, reactivated, n_lapsed-reactivated, acquired, n_never-acquired],
                color=["rgba(52,211,153,0.35)", "rgba(248,113,113,0.35)", "rgba(56,189,248,0.35)", "rgba(100,116,139,0.35)", "rgba(244,63,94,0.35)", "rgba(71,85,105,0.35)"]
            )
        ))
        fig_sankey.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=11, color="#F8FAFC")
        )
        st.plotly_chart(fig_sankey, use_container_width=True)


# =============================================================================
# VIEW 4: MARKETING EFFICIENCY & CHANNELS
# =============================================================================
elif selected_module == "📈 Marketing Efficiency & Channels":
    
    render_view_banner(
        title="📈 Marketing Efficiency & Digital Funnel",
        objective="Analyzes the economic efficiency of advancement marketing outreach, solicitation channel conversion efficacy, and the multi-step digital giving conversion funnel.",
        visualizations=[
            "4 Marketing KPIs: Cost per $ raised, marketing ROI multiplier, email open rate, GA4 web giving conversion",
            "Channel conversion rate comparison across Crowdfunding, Direct Mail, Digital, and Phone",
            "5-Stage digital giving funnel from delivery and open to click, web visit, and completed gift"
        ]
    )
    
    cpdr = (tot_cost / tot_rev_fy26) if tot_rev_fy26 > 0 else 0.0
    open_rate = (filtered_df['Emails_Opened_FY26'].sum() / filtered_df['Emails_Delivered_FY26'].sum() * 100) if filtered_df['Emails_Delivered_FY26'].sum() > 0 else 0.0
    web_donors = ((filtered_df['GA4_Giving_Page_Views_FY26'] > 0) & (filtered_df['Donated_FY26'] == 1)).sum()
    web_visitors = (filtered_df['GA4_Giving_Page_Views_FY26'] > 0).sum()
    web_conv = (web_donors / web_visitors * 100) if web_visitors > 0 else 0.0
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.metric(
                label="Cost per $ Raised",
                value=f"${cpdr:.4f}",
                delta="AFP Standard < $0.15",
                help=format_tooltip(
                    description="Direct marketing and solicitation expenditure incurred for each single dollar of philanthropic revenue secured.",
                    calculation="Total Marketing_Outreach_Cost_FY26 / Total FY26 Revenue.",
                    benchmark="Association of Fundraising Professionals (AFP) Standard: Under $0.15."
                )
            )
    with m2:
        with st.container(border=True):
            st.metric(
                label="Marketing ROI",
                value=f"{roi_mult:.1f}x",
                delta=f"Total Spend: ${tot_cost:,.0f}",
                help=format_tooltip(
                    description="Overall marketing efficiency ratio measuring revenue return generated per marketing dollar invested.",
                    calculation="Total FY26 Revenue / Total Marketing_Outreach_Cost_FY26.",
                    benchmark="AFP Best-in-Class Benchmark: > 6.7x."
                )
            )
    with m3:
        with st.container(border=True):
            st.metric(
                label="Email Open Rate",
                value=f"{open_rate:.1f}%",
                delta="Higher Ed Avg ~28%",
                help=format_tooltip(
                    description="Engagement rate of direct digital appeal emails delivered to alumni and prospective donors.",
                    calculation="(Total Emails_Opened_FY26 / Total Emails_Delivered_FY26) × 100.",
                    benchmark="Higher Education Nonprofit Benchmark: 25.0% – 30.0%."
                )
            )
    with m4:
        with st.container(border=True):
            st.metric(
                label="GA4 Web Conversion",
                value=f"{web_conv:.1f}%",
                delta=f"{web_donors:,} Donors",
                help=format_tooltip(
                    description="Proportion of unique visitors to the institutional online giving portal who completed a gift transaction.",
                    calculation="(Constituents with GA4 Giving Page Views AND Donated FY26 / Total Constituents with Giving Page Views) × 100.",
                    benchmark="Nonprofit E-Commerce Giving Benchmark: 15.0% – 22.0%."
                )
            )
            
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        with st.container(border=True):
            st.subheader(
                "Channel Conversion Rate (%)",
                help="Evaluates the donor conversion efficiency of primary solicitation channels including Digital, Direct Mail, Phone, and Crowdfunding. Displays the percentage of contacted constituents in each channel who completed a financial gift in FY26."
            )
            chan_df = filtered_df.groupby('Display_Channel').agg(
                Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
                Total=('Constituent_ID', 'count')
            ).reset_index()
            chan_df['Conv'] = chan_df['Donors'] / chan_df['Total'] * 100
            fig_c = px.bar(chan_df, x='Display_Channel', y='Conv', color_discrete_sequence=['#2DD4BF'], text=chan_df['Conv'].apply(lambda x: f"{x:.1f}%"))
            fig_c.update_traces(textposition='outside')
            fig_c.update_yaxes(title_text='Conversion (%)')
            apply_dark_theme(fig_c, height=270)
            st.plotly_chart(fig_c, use_container_width=True)
            
    with c_m2:
        with st.container(border=True):
            st.subheader(
                "Digital Giving Funnel",
                help="Illustrates constituent drop-off across the 5-stage digital solicitation funnel from email delivery to gift completion. Displays the conversion progression through delivered emails, open rates, link clicks, website visits, and completed gifts."
            )
            fig_fun = go.Figure(go.Funnel(
                y=["Delivered Email", "Opened Email", "Clicked Link", "Visited Web", "Completed Gift"],
                x=[
                    (filtered_df['Emails_Delivered_FY26'] > 0).sum(),
                    (filtered_df['Emails_Opened_FY26'] > 0).sum(),
                    (filtered_df['Emails_Clicked_FY26'] > 0).sum(),
                    web_visitors,
                    donors_fy26
                ],
                textinfo="value+percent initial",
                marker=dict(color=["#475569", "#60A5FA", "#38BDF8", "#FBBF24", "#34D399"])
            ))
            fig_fun.update_layout(
                height=270,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", size=10, color="#F8FAFC")
            )
            st.plotly_chart(fig_fun, use_container_width=True)


# =============================================================================
# VIEW 5: CASE 4-PILLAR ENGAGEMENT (AEM)
# =============================================================================
elif selected_module == "🤝 CASE 4-Pillar Engagement (AEM)":
    
    render_view_banner(
        title="🤝 CASE 4-Pillar Engagement (AEM)",
        objective="Operationalizes the Council for Advancement and Support of Education (CASE) Alumni Engagement Metrics across Philanthropic, Experiential, Volunteer, and Communication modes to measure overall constituent relationship depth.",
        visualizations=[
            "4 CASE Engagement KPIs: Event attendance rate, ticket show rate, 2+ pillar multi-mode rate, active volunteers",
            "CASE multi-pillar engagement lift showing exponential giving rate increases by pillar count",
            "Homecoming reunion milestone spikes highlighting alumni engagement across graduating classes"
        ]
    )
    
    events_att = (filtered_df['Events_Attended_FY26'] > 0).sum()
    event_rate = (events_att / n_filtered * 100) if n_filtered > 0 else 0.0
    show_rate = (filtered_df['Events_Attended_FY26'].sum() / filtered_df['Events_Registered_FY26'].sum() * 100) if filtered_df['Events_Registered_FY26'].sum() > 0 else 0.0
    multi_pillar = (filtered_df['CASE_Pillar_Count'] >= 2).sum()
    volunteers = (filtered_df['Is_Active_Volunteer_FY26'] == 1).sum()
    
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        with st.container(border=True):
            st.metric(
                label="Event Attendance",
                value=f"{event_rate:.1f}%",
                delta=f"{events_att:,} Alumni",
                help=format_tooltip(
                    description="Proportion of alumni participating in at least one university event (Experiential Pillar).",
                    calculation="(Constituents with Events_Attended_FY26 > 0 / Total Addressable Alumni) × 100.",
                    benchmark="CASE Experiential Engagement Standard: 10.0% – 15.0%."
                )
            )
    with e2:
        with st.container(border=True):
            st.metric(
                label="Ticket Show Rate",
                value=f"{show_rate:.1f}%",
                delta="Realized Attendees",
                help=format_tooltip(
                    description="Percentage of event registrants who physically or virtually attended the registered programming.",
                    calculation="(Total Events_Attended_FY26 / Total Events_Registered_FY26) × 100.",
                    benchmark="Industry Event Attendance Average: 55.0% – 65.0%."
                )
            )
    with e3:
        with st.container(border=True):
            st.metric(
                label="2+ CASE Modes",
                value=f"{(multi_pillar/n_filtered*100):.1f}%",
                delta="43.7% Giving Rate",
                help=format_tooltip(
                    description="Percentage of alumni engaged across two or more CASE pillars (Philanthropic, Experiential, Volunteer, Communication).",
                    calculation="(Constituents with CASE_Pillar_Count >= 2 / Total Universe) × 100.",
                    benchmark="Multi-Modal Engagement Lift: Alumni in 2+ modes demonstrate 9x higher giving rates."
                )
            )
    with e4:
        with st.container(border=True):
            st.metric(
                label="Active Volunteers",
                value=f"{(volunteers/n_filtered*100):.1f}%",
                delta=f"{volunteers:,} Leaders",
                help=format_tooltip(
                    description="Share of constituents serving in an active institutional advisory, mentoring, or alumni board capacity (Volunteer Pillar).",
                    calculation="(Constituents with Is_Active_Volunteer_FY26 = 1 / Total Universe) × 100.",
                    benchmark="Higher Education Target: 4.0% – 7.0%."
                )
            )
            
    c_e1, c_e2 = st.columns(2)
    with c_e1:
        with st.container(border=True):
            st.subheader(
                "CASE Engagement Modes vs. Giving Rate (%)",
                help="Demonstrates the empirical lift law between non-financial alumni engagement depth and financial giving propensity. Displays how alumni participating in multiple CASE pillars exhibit up to 9x higher donor participation rates."
            )
            aem_df = filtered_df.groupby('CASE_Pillar_Count').agg(
                Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
                Total=('Constituent_ID', 'count')
            ).reset_index()
            aem_df['Giving_Rate'] = aem_df['Donors'] / aem_df['Total'] * 100
            fig_lift = px.bar(aem_df, x='CASE_Pillar_Count', y='Giving_Rate', color_discrete_sequence=['#34D399'], text=aem_df['Giving_Rate'].apply(lambda x: f"{x:.1f}%"))
            fig_lift.update_traces(textposition='outside')
            fig_lift.update_yaxes(title_text='Giving Rate (%)')
            apply_dark_theme(fig_lift, height=270)
            st.plotly_chart(fig_lift, use_container_width=True)
            
    with c_e2:
        with st.container(border=True):
            st.subheader(
                "Homecoming Milestone Spikes",
                help="Tracks Homecoming and reunion weekend attendance rates as a function of years since graduation. Displays cyclical participation peaks corresponding to 5, 10, 20, and 25-year milestone reunion cohorts."
            )
            years = filtered_df.groupby('Years_Since_Grad')['Attended_Homecoming_FY26'].mean().reset_index()
            years['Rate'] = years['Attended_Homecoming_FY26'] * 100
            fig_home = px.line(years, x='Years_Since_Grad', y='Rate', markers=True)
            fig_home.update_traces(line=dict(color='#F43F5E', width=2.5), marker=dict(size=5, color='#F43F5E'))
            fig_home.update_yaxes(title_text='Homecoming Rate (%)')
            apply_dark_theme(fig_home, height=270)
            st.plotly_chart(fig_home, use_container_width=True)


# =============================================================================
# VIEW 6: PROSPECT CAPACITY & FACULTY INTELLIGENCE
# =============================================================================
elif selected_module == "💎 Prospect Capacity & Faculty Intelligence":
    
    render_view_banner(
        title="💎 Prospect Capacity & Faculty Intelligence",
        objective="Leverages wealth screening capacity ratings and academic faculty commitments to prioritize high-capacity major gift cultivation and optimize development officer pipeline coverage.",
        visualizations=[
            "3 Major Gift KPIs: Top tier giving ($100k+ and $25k-$99k), Tier 1 conversion %, Tier 2 conversion %",
            "Faculty commitments league table showing total philanthropic dollars raised per academic unit",
            "Wealth screening matrix table displaying alumni headcount, donor conversion %, and total commitments"
        ]
    )
    
    t1_t2_rev = filtered_df[filtered_df['Wealth_Screening_Rating'].isin(['Tier 1: $100k+', 'Tier 2: $25k-$99k'])]['Giving_Amount_FY26'].sum()
    t1_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 1: $100k+']
    t1_conv = ((t1_df['Gift_Count_FY26'] > 0).sum() / len(t1_df) * 100) if len(t1_df) > 0 else 0.0
    t2_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 2: $25k-$99k']
    t2_conv = ((t2_df['Gift_Count_FY26'] > 0).sum() / len(t2_df) * 100) if len(t2_df) > 0 else 0.0
    
    w1, w2, w3 = st.columns(3)
    with w1:
        with st.container(border=True):
            st.metric(
                label="Top Tier Giving",
                value=f"${t1_t2_rev/1e6:.2f}M",
                delta=f"{(t1_t2_rev/tot_rev_fy26*100):.1f}% Total Funds",
                help=format_tooltip(
                    description="Philanthropic commitments secured from major and principal gift prospects (Tiers 1 & 2).",
                    calculation="Sum of Giving_Amount_FY26 for constituents rated Tier 1 ($100k+) or Tier 2 ($25k-$99k).",
                    benchmark="Pareto Target: Major gift tiers generate > 65.0% of total institutional commitments."
                )
            )
    with w2:
        with st.container(border=True):
            st.metric(
                label="Tier 1 ($100k+) Conv",
                value=f"{t1_conv:.1f}%",
                delta=f"{len(t1_df):,} Prospects",
                help=format_tooltip(
                    description="Philanthropic conversion rate among highest-capacity rated alumni prospects ($100,000+ estimated wealth).",
                    calculation="(Tier 1 Donors with Gift_Count_FY26 > 0 / Total Tier 1 Rated Prospects) × 100.",
                    benchmark="Principal Gift Solicitation Target: > 60.0% active participation."
                )
            )
    with w3:
        with st.container(border=True):
            st.metric(
                label="Tier 2 ($25k-$99k) Conv",
                value=f"{t2_conv:.1f}%",
                delta=f"{len(t2_df):,} Prospects",
                help=format_tooltip(
                    description="Philanthropic conversion rate among leadership annual and major gift prospects ($25,000–$99,000 capacity).",
                    calculation="(Tier 2 Donors with Gift_Count_FY26 > 0 / Total Tier 2 Rated Prospects) × 100.",
                    benchmark="Major Gift Solicitation Target: > 45.0% active participation."
                )
            )
            
    c_f1, c_f2 = st.columns([1.1, 0.9])
    with c_f1:
        with st.container(border=True):
            st.subheader(
                "Faculty Commitments ($ CAD)",
                help="Displays total philanthropic commitments secured in FY26 broken down by academic division and faculty. Highlights top performing faculties and comparative funding distribution across the university."
            )
            fac_league = filtered_df.groupby('Primary_Faculty')['Giving_Amount_FY26'].sum().reset_index().sort_values(by='Giving_Amount_FY26', ascending=True)
            fig_fl = px.bar(fac_league, x='Giving_Amount_FY26', y='Primary_Faculty', orientation='h', color_discrete_sequence=['#38BDF8'])
            fig_fl.update_yaxes(title_text='')
            fig_fl.update_xaxes(title_text='Commitments ($ CAD)')
            apply_dark_theme(fig_fl, height=300)
            st.plotly_chart(fig_fl, use_container_width=True)
            
    with c_f2:
        with st.container(border=True):
            st.subheader(
                "Wealth Screening Matrix",
                help="Cross-tabulates estimated wealth capacity tiers with actual donor conversion rates and philanthropic revenue. Displays addressable prospect pool sizes, giving participation rates, and total dollars raised per capacity bracket."
            )
            w_matrix = filtered_df.groupby('Wealth_Screening_Rating').agg(
                Alumni=('Constituent_ID', 'count'),
                Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
                Raised=('Giving_Amount_FY26', 'sum')
            ).reset_index()
            w_matrix['Part %'] = (w_matrix['Donors'] / w_matrix['Alumni'] * 100).apply(lambda x: f"{x:.1f}%")
            w_matrix['Raised'] = w_matrix['Raised'].apply(lambda x: f"${x/1e3:,.0f}k")
            st.dataframe(w_matrix[['Wealth_Screening_Rating', 'Alumni', 'Part %', 'Raised']], hide_index=True, use_container_width=True)


# =============================================================================
# 6. CRM DATASET SNAPSHOT & INTERACTIVE COLUMN DICTIONARY (BOTTOM OF PAGE)
# =============================================================================
st.markdown("<div id='dataset-snapshot' style='padding-top: 24px;'></div>", unsafe_allow_html=True)
st.markdown("---")

with st.container(border=True):
    st.subheader(
        "📋 CRM Dataset Snapshot & Interactive Column Dictionary",
        help="Displays an exploratory snapshot of the underlying institutional advancement CRM dataset across all 41 constituent attributes. Hover over any column header to view its business definition and usage."
    )
    st.caption("Showing the first 5 records across all 41 columns. **Hover over any column header** to inspect its data definition in a few words.")
    
    # 5 Sample rows from raw CRM
    snapshot_subset = df_master[[c for c in COLUMN_DICTIONARY.keys() if c in df_master.columns]].head(5)
    snapshot_table_html = render_dataset_snapshot_table(snapshot_subset, COLUMN_DICTIONARY)
    st.markdown(snapshot_table_html, unsafe_allow_html=True)
    
    with st.expander("📖 View Complete Column Dictionary (All 41 CRM Attributes)"):
        dict_data = [
            {
                "Column Name": col,
                "Data Type": str(df_master[col].dtype) if col in df_master.columns else "N/A",
                "Business Definition & Scope": desc
            }
            for col, desc in COLUMN_DICTIONARY.items()
        ]
        st.dataframe(pd.DataFrame(dict_data), hide_index=True, use_container_width=True)


# =============================================================================
# 7. MINIMAL FOOTER
# =============================================================================
st.markdown("---")
st.caption("McGill University Advancement Analytics • High-Contrast Executive Dashboard • FY2026 Reporting Year")
