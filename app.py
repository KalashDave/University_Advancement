"""
McDill University Advancement - Executive Analytics & CASE Intelligence Portal
File: app.py
Description: Production-grade Higher Education Advancement Executive Dashboard
             incorporating Power BI-style visual cards, interactive tooltips,
             and polished high-contrast visualizations across 5 strategic CASE pillars.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# =============================================================================
# 1. PAGE CONFIGURATION & MCDILL DESIGN SYSTEM
# =============================================================================
st.set_page_config(
    page_title="McDill Advancement Analytics | FY26",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom McDill Visual Identity & Modern Power BI Dashboard Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #0F172A;
    }
    
    /* Clean Canvas Background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Top Corporate Header */
    .executive-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        border-top: 5px solid #ED1B2F;
        border-radius: 12px;
        padding: 22px 30px;
        margin-bottom: 16px;
        color: #FFFFFF;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }
    
    .executive-header-left h1 {
        color: #FFFFFF !important;
        font-size: 24px;
        font-weight: 800;
        margin: 0 0 6px 0;
        letter-spacing: -0.02em;
    }
    
    .executive-header-left p {
        color: #94A3B8;
        font-size: 13px;
        margin: 0;
        font-weight: 400;
    }
    
    .live-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(237, 27, 47, 0.15);
        border: 1px solid rgba(237, 27, 47, 0.4);
        color: #FECACA;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .live-dot {
        width: 8px;
        height: 8px;
        background-color: #ED1B2F;
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 8px #ED1B2F;
    }
    
    /* Slicer / Context Bar */
    .filter-summary-bar {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 12px 20px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 10px;
        font-size: 13px;
        font-weight: 500;
        color: #475569;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .filter-stat-pill {
        display: inline-flex;
        align-items: center;
        background: #F1F5F9;
        color: #0F172A;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: 700;
        margin-left: 6px;
    }
    
    .filter-stat-pill.highlight {
        background: #FEF2F2;
        color: #ED1B2F;
    }
    
    /* =========================================================================
       CLEAN KPI CARDS WITH HOVER TOOLTIPS
       ========================================================================= */
    .kpi-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-top: 4px solid #ED1B2F;
        border-radius: 10px;
        padding: 16px 18px;
        box-shadow: 0 2px 4px rgba(15, 23, 42, 0.03);
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 125px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
        margin-bottom: 14px;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(15, 23, 42, 0.08);
    }
    
    .kpi-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 6px;
    }
    
    .kpi-title-group {
        display: flex;
        align-items: center;
        gap: 6px;
        flex-wrap: wrap;
    }
    
    .kpi-title {
        font-size: 11px;
        font-weight: 700;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .pillar-badge {
        font-size: 9px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    
    .pillar-badge.red { background: #FEE2E2; color: #DC2626; }
    .pillar-badge.blue { background: #DBEAFE; color: #1D4ED8; }
    .pillar-badge.green { background: #D1FAE5; color: #047857; }
    .pillar-badge.purple { background: #EDE9FE; color: #6D28D9; }
    
    /* Interactive Tooltip in Top Right Corner */
    .kpi-tooltip-wrapper {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    
    .kpi-info-btn {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        background: #F1F5F9;
        color: #64748B;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 800;
        transition: all 0.15s ease;
        user-select: none;
    }
    
    .kpi-tooltip-wrapper:hover .kpi-info-btn {
        background: #ED1B2F;
        color: #FFFFFF;
    }
    
    .kpi-tooltip-content {
        visibility: hidden;
        opacity: 0;
        width: 260px;
        background: #0F172A;
        color: #F8FAFC;
        text-align: left;
        border-radius: 8px;
        padding: 10px 14px;
        font-size: 11px;
        line-height: 1.45;
        position: absolute;
        z-index: 9999;
        top: 26px;
        right: 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        border: 1px solid #334155;
        transition: opacity 0.2s ease, transform 0.2s ease;
        transform: translateY(-4px);
        pointer-events: none;
    }
    
    .kpi-tooltip-wrapper:hover .kpi-tooltip-content {
        visibility: visible;
        opacity: 1;
        transform: translateY(0);
    }
    
    .kpi-value {
        font-size: 26px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.15;
        margin: 4px 0 6px 0;
    }
    
    .kpi-footer {
        display: flex;
        align-items: center;
        justify-content: flex-start;
        gap: 6px;
    }
    
    .delta-pill {
        display: inline-flex;
        align-items: center;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 9999px;
    }
    
    .delta-pill.good { background: #DEF7EC; color: #03543F; }
    .delta-pill.warning { background: #FEF3C7; color: #92400E; }
    .delta-pill.neutral { background: #F1F5F9; color: #475569; }
    
    /* =========================================================================
       VISUALLY IMPRESSIVE TABS & CHART CONTAINERS
       ========================================================================= */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 6px 8px;
        margin-bottom: 24px;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
    }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 13px;
        font-weight: 600;
        color: #475569;
        padding: 9px 16px;
        border-radius: 8px;
        border: none;
        background: transparent;
        transition: all 0.15s ease;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ED1B2F !important;
        background-color: #FEF2F2 !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(237, 27, 47, 0.12);
    }
    
    /* Chart Enclosing Cards */
    .chart-card-wrapper {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px 22px 14px 22px;
        margin-bottom: 22px;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.02);
    }
    
    .chart-card-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 12px;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 10px;
    }
    
    .chart-title-text {
        font-size: 14px;
        font-weight: 700;
        color: #0F172A;
        margin: 0 0 3px 0;
    }
    
    .chart-subtitle-text {
        font-size: 11px;
        color: #64748B;
        margin: 0;
    }
    
    .chart-badge-pill {
        display: inline-flex;
        align-items: center;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        color: #475569;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    /* Strategic Overview Highlight Cards */
    .exec-brief-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #ED1B2F;
        border-radius: 8px;
        padding: 14px 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .exec-brief-title {
        font-size: 13px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    .exec-brief-text {
        font-size: 12px;
        color: #475569;
        line-height: 1.4;
        margin: 0;
    }
    
    /* Section Subheaders */
    .section-header {
        font-size: 16px;
        font-weight: 700;
        color: #0F172A;
        margin: 18px 0 12px 0;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# 2. DATA CACHING & ADVANCED FEATURE ENGINEERING
# =============================================================================
@st.cache_data(show_spinner=False)
def load_and_preprocess_advancement_data():
    """
    Loads raw constituent extract, creates derived lifecycle segments, CASE AEM metrics,
    and structured gift brackets.
    """
    csv_path = "mcgill_advancement_raw_crm.csv"
    if not os.path.exists(csv_path):
        st.error(f"CRM extract file '{csv_path}' not found in workspace.")
        st.stop()
        
    df = pd.read_csv(csv_path)
    
    # 1. Graduation Cohort & Career Era
    df['Years_Since_Grad'] = 2026 - df['Class_Year']
    conditions_cohort = [
        (df['Class_Year'] >= 2017),
        (df['Class_Year'] >= 2001) & (df['Class_Year'] <= 2016),
        (df['Class_Year'] <= 2000)
    ]
    choices_cohort = [
        'Young Alumni (<10 yrs: 2017-2025)',
        'Mid-Career (10-25 yrs: 2001-2016)',
        'Senior Alumni (25+ yrs: 1965-2000)'
    ]
    df['Graduation_Cohort'] = np.select(conditions_cohort, choices_cohort, default='Other')
    
    # 2. Regional Footprint
    conditions_region = [
        (df['Province_State'] == 'QC'),
        (df['Country_of_Residence'] == 'Canada') & (df['Province_State'] != 'QC'),
        (df['Country_of_Residence'] == 'United States')
    ]
    choices_region = ['Quebec', 'Rest of Canada', 'United States']
    df['Geographic_Region'] = np.select(conditions_region, choices_region, default='International')
    
    # 3. Giving & Donor Lifecycle Segmentation
    df['Donated_FY24'] = (df['Gift_Count_FY24'] > 0).astype(int)
    df['Donated_FY25'] = (df['Gift_Count_FY25'] > 0).astype(int)
    df['Donated_FY26'] = (df['Gift_Count_FY26'] > 0).astype(int)
    df['Gave_Prior'] = ((df['Lifetime_Gift_Count_Prior_To_FY24'] > 0) | (df['Donated_FY24'] == 1)).astype(int)
    
    conditions_lifecycle = [
        (df['Donated_FY25'] == 1) & (df['Donated_FY26'] == 1),
        (df['Donated_FY25'] == 1) & (df['Donated_FY26'] == 0),
        (df['Gave_Prior'] == 1) & (df['Donated_FY25'] == 0) & (df['Donated_FY26'] == 1),
        (df['Gave_Prior'] == 1) & (df['Donated_FY25'] == 0) & (df['Donated_FY26'] == 0),
        (df['Gave_Prior'] == 0) & (df['Donated_FY25'] == 0) & (df['Donated_FY26'] == 1)
    ]
    choices_lifecycle = [
        'Retained FY25 Donor',
        'LYBUNT (Lapsed FY25)',
        'Reactivated Donor',
        'Dormant Lapsed',
        'New Acquired Donor'
    ]
    df['Donor_Lifecycle_Segment'] = np.select(conditions_lifecycle, choices_lifecycle, default='Non-Donor (Never Gave)')
    
    # 4. CASE 4-Pillar Alumni Engagement Metrics (AEM)
    df['CASE_Philanthropic'] = df['Donated_FY26']
    df['CASE_Experiential'] = (df['Events_Attended_FY26'] > 0).astype(int)
    df['CASE_Volunteer'] = (df['Is_Active_Volunteer_FY26'] == 1).astype(int)
    df['CASE_Communication'] = ((df['Emails_Opened_FY26'] > 0) | (df['McGill_Connect_Logins_FY26'] > 0)).astype(int)
    
    df['CASE_Pillar_Count'] = (
        df['CASE_Philanthropic'] +
        df['CASE_Experiential'] +
        df['CASE_Volunteer'] +
        df['CASE_Communication']
    )
    
    # 5. Gift Size Tier Brackets (for Pareto visual clarity)
    conditions_tier = [
        (df['Giving_Amount_FY26'] >= 10000),
        (df['Giving_Amount_FY26'] >= 2500) & (df['Giving_Amount_FY26'] < 10000),
        (df['Giving_Amount_FY26'] >= 500) & (df['Giving_Amount_FY26'] < 2500),
        (df['Giving_Amount_FY26'] >= 100) & (df['Giving_Amount_FY26'] < 500),
        (df['Giving_Amount_FY26'] > 0) & (df['Giving_Amount_FY26'] < 100)
    ]
    choices_tier = [
        'Principal ($10k+)',
        'Major ($2.5k–$9.9k)',
        'Leadership ($500–$2.4k)',
        'Centennial ($100–$499)',
        'Grassroots (<$100)'
    ]
    df['Gift_Size_Tier'] = np.select(conditions_tier, choices_tier, default='Non-Donor')
    
    # Designation display alias
    df['Last_Gift_Designation'] = df['Last_Gift_Designation'].replace({
        'The McGill Fund (Unrestricted)': 'The McDill Fund (Unrestricted)'
    })
    
    # Channel display alias
    df['Display_Channel'] = df['Primary_Solicitation_Channel_FY26'].replace({
        'Crowdfunding_McGill24': 'Crowdfunding_McDill24'
    })
    
    return df


df_master = load_and_preprocess_advancement_data()


# =============================================================================
# 3. REUSABLE KPI CARD & PLOTLY THEMING HELPERS
# =============================================================================
def render_kpi_card(title: str, value: str, pillar_badge: str, benchmark_text: str,
                    benchmark_status: str = "good", badge_color: str = "red",
                    tooltip_def: str = "", tooltip_bench: str = "", tooltip_impact: str = ""):
    """
    Renders a clean Power BI-style KPI card with an interactive tooltip at the top-right corner.
    """
    html_code = f"""
    <div class="kpi-card">
        <div class="kpi-header">
            <div class="kpi-title-group">
                <span class="kpi-title">{title}</span>
                <span class="pillar-badge {badge_color}">{pillar_badge}</span>
            </div>
            <div class="kpi-tooltip-wrapper">
                <div class="kpi-info-btn">ℹ</div>
                <div class="kpi-tooltip-content">
                    <div style="font-weight:700; color:#FFFFFF; margin-bottom:4px; font-size:12px;">{title}</div>
                    <div style="color:#CBD5E1; margin-bottom:6px;">{tooltip_def}</div>
                    <div style="border-top:1px solid #334155; padding-top:4px; color:#93C5FD; font-size:10px;">
                        <b>Benchmark:</b> {tooltip_bench}
                    </div>
                    <div style="color:#A7F3D0; font-size:10px; margin-top:2px;">
                        <b>Strategic Impact:</b> {tooltip_impact}
                    </div>
                </div>
            </div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-footer">
            <span class="delta-pill {benchmark_status}">{benchmark_text}</span>
        </div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)


def render_chart_card(title: str, subtitle: str, badge_text: str = ""):
    """Renders the top header for an enclosed chart card."""
    badge_html = f'<span class="chart-badge-pill">{badge_text}</span>' if badge_text else ''
    st.markdown(f"""
    <div class="chart-card-header">
        <div>
            <div class="chart-title-text">{title}</div>
            <div class="chart-subtitle-text">{subtitle}</div>
        </div>
        {badge_html}
    </div>
    """, unsafe_allow_html=True)


def apply_custom_chart_theme(fig, height=350):
    """
    Applies high-contrast, modern publication-grade styling to all Plotly figures.
    """
    fig.update_layout(
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#1E293B"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=45, r=30, t=25, b=35),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=12,
            font_color="#FFFFFF",
            font_family="Inter, sans-serif",
            bordercolor="#334155"
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=11, color="#64748B"))
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=11, color="#64748B"))
    return fig


# =============================================================================
# 4. REDESIGNED SLEEK EXECUTIVE SIDEBAR FILTERS
# =============================================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 12px 0 16px 0; border-bottom: 2px solid #F1F5F9; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="font-size: 30px; background: #FEF2F2; padding: 6px 10px; border-radius: 10px; border: 1px solid #FEE2E2;">🎓</div>
            <div>
                <div style="font-size: 17px; font-weight: 800; color: #ED1B2F; letter-spacing: -0.01em;">McDill University</div>
                <div style="font-size: 12px; font-weight: 600; color: #64748B;">Advancement Analytics</div>
            </div>
        </div>
        <div style="margin-top: 10px; background: #F8FAFC; border: 1px solid #E2E8F0; padding: 6px 10px; border-radius: 6px; font-size: 11px; color: #475569;">
            <b>Universe:</b> 30,000 Verified Records
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='font-size: 11px; font-weight: 700; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.05em; margin-bottom: 8px;'>🎯 Slicers & Scope</div>", unsafe_allow_html=True)
    
    # 1. Academic Faculty
    with st.expander("🏛️ Academic Faculty", expanded=True):
        all_faculties = sorted(df_master['Primary_Faculty'].unique().tolist())
        selected_faculties = st.multiselect(
            "Select Faculties",
            options=all_faculties,
            default=all_faculties,
            label_visibility="collapsed"
        )
    
    # 2. Graduation Cohort & Class Year Range
    with st.expander("🎓 Cohort & Graduation Era", expanded=False):
        cohort_options = ['All Cohorts', 'Young Alumni (<10 yrs: 2017-2025)', 'Mid-Career (10-25 yrs: 2001-2016)', 'Senior Alumni (25+ yrs: 1965-2000)']
        quick_cohort = st.selectbox("Preset Cohort", options=cohort_options, index=0)
        
        min_year = int(df_master['Class_Year'].min())
        max_year = int(df_master['Class_Year'].max())
        
        if quick_cohort == 'Young Alumni (<10 yrs: 2017-2025)':
            default_range = (2017, 2025)
        elif quick_cohort == 'Mid-Career (10-25 yrs: 2001-2016)':
            default_range = (2001, 2016)
        elif quick_cohort == 'Senior Alumni (25+ yrs: 1965-2000)':
            default_range = (1965, 2000)
        else:
            default_range = (min_year, max_year)
            
        class_year_range = st.slider("Class Year Range", min_value=min_year, max_value=max_year, value=default_range)
    
    # 3. Geographic Region
    with st.expander("🌍 Geographic Region", expanded=False):
        all_regions = ['Quebec', 'Rest of Canada', 'United States', 'International']
        selected_regions = st.multiselect(
            "Select Regions",
            options=all_regions,
            default=all_regions,
            label_visibility="collapsed"
        )
        
    # 4. Wealth Screening Tier
    with st.expander("💎 Wealth Screening Tier", expanded=False):
        all_tiers = [
            'Tier 1: $100k+', 'Tier 2: $25k-$99k', 'Tier 3: $5k-$24k',
            'Tier 4: $1k-$4.9k', 'Tier 5: Under $1k', 'Unrated'
        ]
        selected_tiers = st.multiselect(
            "Select Tiers",
            options=all_tiers,
            default=all_tiers,
            label_visibility="collapsed"
        )
        
    # 5. Solicitation Channel & Language
    with st.expander("📬 Channels & Language", expanded=False):
        all_channels = sorted(df_master['Display_Channel'].unique().tolist())
        selected_channels = st.multiselect(
            "Solicitation Channel",
            options=all_channels,
            default=all_channels
        )
        selected_lang = st.radio("Preferred Language", options=['All', 'EN', 'FR'], horizontal=True)
    
    st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()


# Apply Filters
filtered_df = df_master.copy()
filtered_df = filtered_df[filtered_df['Primary_Faculty'].isin(selected_faculties)]
filtered_df = filtered_df[(filtered_df['Class_Year'] >= class_year_range[0]) & (filtered_df['Class_Year'] <= class_year_range[1])]
filtered_df = filtered_df[filtered_df['Geographic_Region'].isin(selected_regions)]
filtered_df = filtered_df[filtered_df['Wealth_Screening_Rating'].isin(selected_tiers)]
filtered_df = filtered_df[filtered_df['Display_Channel'].isin(selected_channels)]
if selected_lang != 'All':
    filtered_df = filtered_df[filtered_df['Preferred_Language'] == selected_lang]

n_filtered = len(filtered_df)
if n_filtered == 0:
    st.warning("⚠️ No constituent records match the current filter criteria. Please adjust your sidebar slicers.")
    st.stop()


# Core Aggregations
tot_rev_fy26 = filtered_df['Giving_Amount_FY26'].sum()
tot_rev_fy25 = filtered_df['Giving_Amount_FY25'].sum()
tot_rev_fy24 = filtered_df['Giving_Amount_FY24'].sum()
donors_fy26 = (filtered_df['Gift_Count_FY26'] > 0).sum()
donors_fy25 = (filtered_df['Gift_Count_FY25'] > 0).sum()
tot_cost = filtered_df['Marketing_Outreach_Cost_FY26'].sum()
cpdr = (tot_cost / tot_rev_fy26) if tot_rev_fy26 > 0 else 0.0
roi_mult = (tot_rev_fy26 / tot_cost) if tot_cost > 0 else 0.0
part_rate = (donors_fy26 / n_filtered * 100) if n_filtered > 0 else 0.0
retained_25_26 = ((filtered_df['Donated_FY25'] == 1) & (filtered_df['Donated_FY26'] == 1)).sum()
retention_rate = (retained_25_26 / donors_fy25 * 100) if donors_fy25 > 0 else 0.0
yoy_rev_pct = ((tot_rev_fy26 - tot_rev_fy25) / tot_rev_fy25 * 100) if tot_rev_fy25 > 0 else 0.0


# =============================================================================
# 5. TOP CORPORATE EXECUTIVE BANNER & SLICER CONTEXT
# =============================================================================
st.markdown(f"""
<div class="executive-header">
    <div class="executive-header-left">
        <h1>McDill University Advancement | Executive Intelligence & CASE Analytics Portal</h1>
        <p>FY26 Strategic Close Platform • Unified CRM, Marketing Cloud, Eventbrite & GA4 Intelligence</p>
    </div>
    <div class="executive-header-right">
        <div class="live-badge">
            <span class="live-dot"></span>
            <span>FY26 Certified Extract</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Power BI Style Slicer Context Indicator
st.markdown(f"""
<div class="filter-summary-bar">
    <div>
        <span>Active Cohort:</span>
        <span class="filter-stat-pill highlight">{n_filtered:,} / {len(df_master):,} Alumni ({n_filtered/len(df_master)*100:.1f}%)</span>
    </div>
    <div>
        <span>FY26 Total Revenue:</span>
        <span class="filter-stat-pill">${tot_rev_fy26:,.2f}</span>
    </div>
    <div>
        <span>Active Donors:</span>
        <span class="filter-stat-pill">{donors_fy26:,} Donors</span>
    </div>
    <div>
        <span>Segment Scope:</span>
        <span class="filter-stat-pill">{'Full McDill Universe' if n_filtered == len(df_master) else 'Filtered Cohort Active'}</span>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# 6. TABBED PAGE ARCHITECTURE (EXECUTIVE OVERVIEW + 5 STRATEGIC PILLARS)
# =============================================================================
tabs = st.tabs([
    "📊 Overview",
    "🏛️ 1. Philanthropic Health",
    "🔄 2. Donor Lifecycle & Retention",
    "📈 3. Marketing & Channels",
    "🤝 4. CASE 4-Pillar Engagement",
    "💎 5. Prospect Capacity & Benchmarking"
])


# =============================================================================
# TAB 0: EXECUTIVE OVERVIEW (LANDING DASHBOARD)
# =============================================================================
with tabs[0]:
    # 1. Top Power BI KPI Ribbon
    h_col1, h_col2, h_col3, h_col4 = st.columns(4)
    
    with h_col1:
        render_kpi_card(
            title="Total FY26 Revenue",
            value=f"${tot_rev_fy26/1e6:.2f}M" if tot_rev_fy26 >= 1e6 else f"${tot_rev_fy26:,.0f}",
            pillar_badge="Revenue Health",
            benchmark_text=f"{yoy_rev_pct:+.1f}% YoY vs FY25",
            benchmark_status="good" if yoy_rev_pct >= 0 else "neutral",
            badge_color="red",
            tooltip_def="Cumulative philanthropic cash flow and booked commitments in FY26 across all designations.",
            tooltip_bench="U15 Canadian Benchmark: $3.0M – $6.5M annual fund commitments.",
            tooltip_impact="Ensures institutional budget realization and unrestricted student bursary funding."
        )
    with h_col2:
        render_kpi_card(
            title="Alumni Participation",
            value=f"{part_rate:.2f}%",
            pillar_badge="Participation",
            benchmark_text=f"{donors_fy26:,} Active Donors",
            benchmark_status="good" if part_rate >= 14.0 else ("neutral" if part_rate >= 8.0 else "warning"),
            badge_color="blue",
            tooltip_def="Percentage of addressable alumni who contributed at least one philanthropic gift in FY26.",
            tooltip_bench="U15 Average: 8%–12% | McDill FY26 Target: 14%–16%.",
            tooltip_impact="Key barometer of alumni affinity, national prestige rankings, and grassroots loyalty."
        )
    with h_col3:
        render_kpi_card(
            title="Consecutive Retention",
            value=f"{retention_rate:.2f}%",
            pillar_badge="Retention",
            benchmark_text=f"{retained_25_26:,} of {donors_fy25:,} Retained",
            benchmark_status="good" if retention_rate >= 60.0 else "warning",
            badge_color="green",
            tooltip_def="Percentage of FY25 active donors who renewed their philanthropic support in FY26.",
            tooltip_bench="CASE National Standard: 60% – 65% repeat retention rate.",
            tooltip_impact="Retaining an existing donor is 5x more cost-efficient than acquiring a new donor."
        )
    with h_col4:
        render_kpi_card(
            title="Cost Per Dollar Raised",
            value=f"${cpdr:.4f}",
            pillar_badge="Campaign ROI",
            benchmark_text=f"{roi_mult:.1f}x Marketing ROI",
            benchmark_status="good" if cpdr < 0.10 else "warning",
            badge_color="purple",
            tooltip_def="Total marketing, call center, and postage expenditure divided by total philanthropic revenue.",
            tooltip_bench="Association of Fundraising Professionals (AFP) Standard: < $0.15 per dollar raised.",
            tooltip_impact="Signals operational stewardship integrity to major donors and Board of Governors."
        )

    # 2. Executive Strategic Highlights
    b_col1, b_col2, b_col3, b_col4 = st.columns(4)
    with b_col1:
        st.markdown("""
        <div class="exec-brief-card">
            <div class="exec-brief-title">🎯 Revenue Momentum</div>
            <p class="exec-brief-text"><b>$3.39M</b> commitments booked, delivering <b>84.8%</b> of annual budget target with strong student aid growth.</p>
        </div>
        """, unsafe_allow_html=True)
    with b_col2:
        st.markdown("""
        <div class="exec-brief-card">
            <div class="exec-brief-title">🔄 Retention Exceeds CASE</div>
            <p class="exec-brief-text"><b>62.5%</b> repeat donor retention surpasses the CASE 60% benchmark, safeguarding long-term pipeline value.</p>
        </div>
        """, unsafe_allow_html=True)
    with b_col3:
        st.markdown("""
        <div class="exec-brief-card">
            <div class="exec-brief-title">⚡ High-Efficiency Channels</div>
            <p class="exec-brief-text">Email Digital generated <b>$1.93M</b> at just <b>$14.59</b> cost per acquired donor, maximizing net proceeds.</p>
        </div>
        """, unsafe_allow_html=True)
    with b_col4:
        st.markdown("""
        <div class="exec-brief-card">
            <div class="exec-brief-title">🤝 Engagement Multiplier</div>
            <p class="exec-brief-text">Constituents active in 2+ CASE engagement modes demonstrate a <b>43.7%</b> giving rate vs 4.8% for single-touch alumni.</p>
        </div>
        """, unsafe_allow_html=True)

    # 3. Visual Grid: Row 1
    ov_r1_c1, ov_r1_c2 = st.columns([1.25, 0.75])
    
    with ov_r1_c1:
        render_chart_card(
            title="📈 Multi-Year Revenue Trajectory & Active Donors (FY24–FY26)",
            subtitle="Dual-axis view showing revenue booked ($ CAD) against active donor headcount",
            badge_text="Actuals"
        )
        my_df = pd.DataFrame({
            'Fiscal Year': ['FY2024', 'FY2025', 'FY2026'],
            'Revenue ($)': [tot_rev_fy24, tot_rev_fy25, tot_rev_fy26],
            'Donors': [
                (filtered_df['Gift_Count_FY24'] > 0).sum(),
                donors_fy25,
                donors_fy26
            ]
        })
        fig_my = go.Figure()
        fig_my.add_trace(go.Bar(
            x=my_df['Fiscal Year'],
            y=my_df['Revenue ($)'],
            name='Total Revenue ($)',
            marker_color='#ED1B2F',
            marker_line=dict(color='#B91C1C', width=1),
            text=my_df['Revenue ($)'].apply(lambda x: f"${x/1e6:.2f}M"),
            textposition='outside',
            textfont=dict(size=12, color='#0F172A', family='Inter'),
            hovertemplate="<b>%{x}</b><br>Revenue: %{y:$,.0f}<extra></extra>",
            yaxis='y'
        ))
        fig_my.add_trace(go.Scatter(
            x=my_df['Fiscal Year'],
            y=my_df['Donors'],
            name='Active Donors',
            mode='lines+markers+text',
            text=my_df['Donors'].apply(lambda x: f"{x:,}"),
            textposition='top center',
            textfont=dict(size=11, color='#0F172A', family='Inter'),
            line=dict(color='#0F172A', width=3),
            marker=dict(size=9, color='#FFFFFF', line=dict(width=3, color='#0F172A')),
            hovertemplate="<b>%{x}</b><br>Active Donors: %{y:,}<extra></extra>",
            yaxis='y2'
        ))
        fig_my.update_layout(
            yaxis=dict(title='Total Revenue ($ CAD)', showgrid=True, gridcolor='#F1F5F9', tickformat='$,.0s'),
            yaxis2=dict(title='Active Donors', overlaying='y', side='right', showgrid=False),
            legend=dict(orientation='h', yanchor='bottom', y=1.04, xanchor='right', x=1),
            height=330
        )
        apply_custom_chart_theme(fig_my, height=330)
        st.plotly_chart(fig_my, use_container_width=True)

    with ov_r1_c2:
        render_chart_card(
            title="🎯 FY26 Annual Campaign Goal Pace",
            subtitle="Progress toward $4.0M annual strategic fund commitment target",
            badge_text="Target Progress"
        )
        target_goal = 4000000.0
        pct_goal = min(100.0, (tot_rev_fy26 / target_goal) * 100) if target_goal > 0 else 0.0
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=tot_rev_fy26,
            delta={'reference': target_goal, 'valueformat': '$,.0f', 'increasing': {'color': '#10B981'}},
            number={'valueformat': '$,.0f', 'font': {'size': 26, 'color': '#0F172A', 'family': 'Inter'}},
            gauge={
                'axis': {'range': [0, 4500000], 'tickformat': '$,.0s', 'tickfont': {'size': 10}},
                'bar': {'color': '#ED1B2F'},
                'steps': [
                    {'range': [0, 2500000], 'color': '#F1F5F9'},
                    {'range': [2500000, 3500000], 'color': '#E2E8F0'},
                    {'range': [3500000, 4000000], 'color': '#FEF2F2'}
                ],
                'threshold': {
                    'line': {'color': '#0F172A', 'width': 3},
                    'thickness': 0.8,
                    'value': target_goal
                }
            }
        ))
        fig_gauge.update_layout(
            height=250,
            margin=dict(l=25, r=25, t=15, b=15),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.markdown(f"<div style='text-align: center; font-size: 12px; color: #475569;'><b>{pct_goal:.1f}%</b> of annual target realized | <b>${max(0.0, target_goal - tot_rev_fy26):,.0f}</b> remaining</div>", unsafe_allow_html=True)

    # 4. Visual Grid: Row 2
    ov_r2_c1, ov_r2_c2 = st.columns(2)
    
    with ov_r2_c1:
        render_chart_card(
            title="🏛️ Top Faculties by Commitments & Participation Heat",
            subtitle="Ranked annual giving by academic faculty with participation rate color scale",
            badge_text="Faculty League"
        )
        fac_league_ov = filtered_df.groupby('Primary_Faculty').agg(
            Alumni=('Constituent_ID', 'count'),
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Total_Raised=('Giving_Amount_FY26', 'sum')
        ).reset_index()
        fac_league_ov['Participation_Rate'] = (fac_league_ov['Donors'] / fac_league_ov['Alumni']) * 100
        fac_league_ov = fac_league_ov.sort_values(by='Total_Raised', ascending=True)
        
        fig_fac_ov = px.bar(
            fac_league_ov,
            x='Total_Raised',
            y='Primary_Faculty',
            orientation='h',
            color='Participation_Rate',
            color_continuous_scale=['#FED7AA', '#FB7185', '#E11D48', '#881337'],
            text=fac_league_ov['Total_Raised'].apply(lambda x: f"${x/1e3:,.0f}k"),
            labels={'Total_Raised': 'Commitments ($ CAD)', 'Primary_Faculty': '', 'Participation_Rate': 'Part %'}
        )
        fig_fac_ov.update_traces(
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Total Commitments: %{x:$,.0f}<extra></extra>"
        )
        apply_custom_chart_theme(fig_fac_ov, height=310)
        fig_fac_ov.update_layout(coloraxis_colorbar=dict(title="Part %", thickness=12, len=0.8))
        st.plotly_chart(fig_fac_ov, use_container_width=True)

    with ov_r2_c2:
        render_chart_card(
            title="🤝 CASE 4-Pillar Alumni Engagement Distribution",
            subtitle="Breakdown of alumni constituent body across CASE engagement modes",
            badge_text="AEM Framework"
        )
        aem_dist = filtered_df['CASE_Pillar_Count'].value_counts().sort_index().reset_index()
        aem_dist.columns = ['Pillars_Active', 'Constituent_Count']
        pillar_labels = {
            0: '0 Pillars (Disengaged)',
            1: '1 Pillar (Single Touch)',
            2: '2 Pillars (Engaged)',
            3: '3 Pillars (Highly Engaged)',
            4: '4 Pillars (Super Core)'
        }
        aem_dist['Segment'] = aem_dist['Pillars_Active'].map(pillar_labels)
        
        fig_aem_donut = px.pie(
            aem_dist,
            names='Segment',
            values='Constituent_Count',
            hole=0.55,
            color='Segment',
            color_discrete_map={
                '0 Pillars (Disengaged)': '#E2E8F0',
                '1 Pillar (Single Touch)': '#94A3B8',
                '2 Pillars (Engaged)': '#2563EB',
                '3 Pillars (Highly Engaged)': '#10B981',
                '4 Pillars (Super Core)': '#ED1B2F'
            }
        )
        fig_aem_donut.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Alumni: %{value:,}<br>Share: %{percent}<extra></extra>"
        )
        fig_aem_donut.update_layout(
            showlegend=False,
            height=310,
            margin=dict(l=20, r=20, t=10, b=10)
        )
        st.plotly_chart(fig_aem_donut, use_container_width=True)

    # 5. Direct Section Directory Cards
    st.markdown("<div class='section-header'>🧭 Strategic Pillar Deep-Dive Modules</div>", unsafe_allow_html=True)
    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.info("**🏛️ Tab 1: Philanthropic Health**\n\nCommitments velocity, Pareto gift distribution, designation allocation, and McDill24 Giving Day impact analysis.")
        st.success("**🔄 Tab 2: Donor Lifecycle & Retention**\n\nInteractive migration Sankey diagram, LYBUNT win-backs, new donor acquisition, and monthly sustainers.")
    with d_col2:
        st.info("**📈 Tab 3: Marketing & Channels**\n\nMarketing CPDR, multichannel ROI comparison, Marketing Cloud deliverability, and GA4 giving web conversion.")
        st.success("**🤝 Tab 4: CASE 4-Pillar AEM**\n\nCASE Global Engagement index, event participation, show rate, volunteer hours, and reunion cycle spikes.")
    with d_col3:
        st.info("**💎 Tab 5: Prospect Capacity**\n\nWealth screening concentration, Tier 1 & Tier 2 conversion yields, faculty league benchmarking, and geographic spread.")


# =============================================================================
# TAB 1: PHILANTHROPIC HEALTH & REVENUE VELOCITY
# =============================================================================
with tabs[1]:
    t1_c1, t1_c2, t1_c3 = st.columns(3)
    avg_gift = (tot_rev_fy26 / donors_fy26) if donors_fy26 > 0 else 0.0
    median_gift = filtered_df.loc[filtered_df['Giving_Amount_FY26'] > 0, 'Giving_Amount_FY26'].median() if donors_fy26 > 0 else 0.0
    
    mcdill24_rev = filtered_df['McGill24_Gift_Amount_FY26'].sum()
    mcdill24_donors = (filtered_df['McGill24_Gift_Amount_FY26'] > 0).sum()
    mcdill24_rev_pct = (mcdill24_rev / tot_rev_fy26 * 100) if tot_rev_fy26 > 0 else 0.0
    mcdill24_donor_pct = (mcdill24_donors / donors_fy26 * 100) if donors_fy26 > 0 else 0.0
    
    with t1_c1:
        render_kpi_card(
            title="KPI 1: FY26 Commitments",
            value=f"${tot_rev_fy26:,.2f}",
            pillar_badge="Revenue",
            benchmark_text=f"FY25: ${tot_rev_fy25/1e6:.2f}M | FY24: ${tot_rev_fy24/1e6:.2f}M",
            benchmark_status="good",
            badge_color="red",
            tooltip_def="Total cumulative philanthropic gifts booked across all funds and faculties in FY26.",
            tooltip_bench="Annual institutional operating target: $3.0M – $6.5M.",
            tooltip_impact="Assesses annual budget realization and multi-year philanthropic cash flow sustainability."
        )
    with t1_c2:
        render_kpi_card(
            title="KPI 2: Donor Yield (Average Gift)",
            value=f"${avg_gift:,.2f}",
            pillar_badge="Gift Yield",
            benchmark_text=f"Median Gift: ${median_gift:,.2f}",
            benchmark_status="good",
            badge_color="blue",
            tooltip_def="Total philanthropic revenue divided by active donor headcount.",
            tooltip_bench="U15 Canadian Average: $600 – $850 for annual fund alumni programs.",
            tooltip_impact="Evaluates the equilibrium between grassroots donor volume and mid-level/major gift capacity."
        )
    with t1_c3:
        render_kpi_card(
            title="KPI 3: McDill24 Giving Day Share",
            value=f"{mcdill24_rev_pct:.1f}% Rev",
            pillar_badge="Giving Day",
            benchmark_text=f"${mcdill24_rev:,.0f} ({mcdill24_donor_pct:.1f}% Donors)",
            benchmark_status="good",
            badge_color="green",
            tooltip_def="Proportion of annual funds and donors mobilized during the 24-hour McDill24 digital campaign.",
            tooltip_bench="CASE North American Giving Day Benchmark: 15% – 25% of annual giving.",
            tooltip_impact="Validates campaign urgency, social gamification, and digital ambassador mobilization."
        )
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    col_t1_1, col_t1_2 = st.columns(2)
    with col_t1_1:
        render_chart_card(
            title="📊 Multi-Year Revenue & Donor Trajectory (FY24–FY26)",
            subtitle="Comparing annual philanthropic revenue ($ CAD) against donor headcount",
            badge_text="Multi-Year View"
        )
        fig_my_t1 = go.Figure()
        fig_my_t1.add_trace(go.Bar(
            x=['FY2024', 'FY2025', 'FY2026'],
            y=[tot_rev_fy24, tot_rev_fy25, tot_rev_fy26],
            name='Total Revenue ($)',
            marker_color='#ED1B2F',
            marker_line=dict(color='#B91C1C', width=1),
            text=[f"${tot_rev_fy24/1e6:.2f}M", f"${tot_rev_fy25/1e6:.2f}M", f"${tot_rev_fy26/1e6:.2f}M"],
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Revenue: %{y:$,.0f}<extra></extra>",
            yaxis='y'
        ))
        fig_my_t1.add_trace(go.Scatter(
            x=['FY2024', 'FY2025', 'FY2026'],
            y=[(filtered_df['Gift_Count_FY24'] > 0).sum(), donors_fy25, donors_fy26],
            name='Active Donors',
            mode='lines+markers+text',
            text=[f"{(filtered_df['Gift_Count_FY24'] > 0).sum():,}", f"{donors_fy25:,}", f"{donors_fy26:,}"],
            textposition='top center',
            line=dict(color='#0F172A', width=3),
            marker=dict(size=8, color='#FFFFFF', line=dict(width=3, color='#0F172A')),
            hovertemplate="<b>%{x}</b><br>Donors: %{y:,}<extra></extra>",
            yaxis='y2'
        ))
        fig_my_t1.update_layout(
            yaxis=dict(title='Total Revenue ($ CAD)', showgrid=True, gridcolor='#F1F5F9', tickformat='$,.0s'),
            yaxis2=dict(title='Active Donors', overlaying='y', side='right', showgrid=False),
            legend=dict(orientation='h', yanchor='bottom', y=1.04, xanchor='right', x=1),
            height=340
        )
        apply_custom_chart_theme(fig_my_t1, height=340)
        st.plotly_chart(fig_my_t1, use_container_width=True)
        
    with col_t1_2:
        render_chart_card(
            title="📈 Pareto Gift Size Tier Breakdown (FY26)",
            subtitle="Donor headcount and total dollars captured across annual gift tiers",
            badge_text="Pareto Analysis"
        )
        tier_agg = filtered_df[filtered_df['Gift_Size_Tier'] != 'Non-Donor'].groupby('Gift_Size_Tier').agg(
            Donors=('Constituent_ID', 'count'),
            Total_Raised=('Giving_Amount_FY26', 'sum')
        ).reset_index()
        
        tier_order = ['Grassroots (<$100)', 'Centennial ($100–$499)', 'Leadership ($500–$2.4k)', 'Major ($2.5k–$9.9k)', 'Principal ($10k+)']
        tier_agg['Tier_Order'] = tier_agg['Gift_Size_Tier'].apply(lambda x: tier_order.index(x) if x in tier_order else 99)
        tier_agg = tier_agg.sort_values(by='Tier_Order')
        
        fig_tier = go.Figure()
        fig_tier.add_trace(go.Bar(
            x=tier_agg['Gift_Size_Tier'],
            y=tier_agg['Total_Raised'],
            name='Total Dollars ($)',
            marker_color='#0F172A',
            text=tier_agg['Total_Raised'].apply(lambda x: f"${x/1e3:,.0f}k"),
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Total Dollars: %{y:$,.0f}<extra></extra>",
            yaxis='y'
        ))
        fig_tier.add_trace(go.Scatter(
            x=tier_agg['Gift_Size_Tier'],
            y=tier_agg['Donors'],
            name='Donor Count',
            mode='lines+markers+text',
            text=tier_agg['Donors'].apply(lambda x: f"{x:,}"),
            textposition='top center',
            line=dict(color='#ED1B2F', width=2.5),
            marker=dict(size=8, color='#ED1B2F'),
            hovertemplate="<b>%{x}</b><br>Donors: %{y:,}<extra></extra>",
            yaxis='y2'
        ))
        fig_tier.update_layout(
            yaxis=dict(title='Total Dollars ($ CAD)', showgrid=True, gridcolor='#F1F5F9', tickformat='$,.0s'),
            yaxis2=dict(title='Donor Headcount', overlaying='y', side='right', showgrid=False),
            legend=dict(orientation='h', yanchor='bottom', y=1.04, xanchor='right', x=1),
            height=340
        )
        apply_custom_chart_theme(fig_tier, height=340)
        st.plotly_chart(fig_tier, use_container_width=True)
            
    col_t1_3, col_t1_4 = st.columns(2)
    with col_t1_3:
        render_chart_card(
            title="🎯 Philanthropic Designation Allocation",
            subtitle="Proportional distribution of FY26 gifts by institutional designation fund",
            badge_text="Fund Allocation"
        )
        desig_df = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].groupby('Last_Gift_Designation')['Giving_Amount_FY26'].agg(
            Revenue='sum', Donors='count'
        ).reset_index().sort_values(by='Revenue', ascending=False)
        
        if len(desig_df) > 0:
            fig_desig = px.pie(
                desig_df,
                names='Last_Gift_Designation',
                values='Revenue',
                hole=0.45,
                color_discrete_sequence=['#ED1B2F', '#0F172A', '#2563EB', '#10B981', '#F59E0B']
            )
            fig_desig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="<b>%{label}</b><br>Revenue: %{value:$,.0f}<br>Share: %{percent}<extra></extra>"
            )
            fig_desig.update_layout(
                height=330,
                margin=dict(l=20, r=20, t=10, b=10),
                showlegend=False
            )
            st.plotly_chart(fig_desig, use_container_width=True)
        else:
            st.info("No active gifts recorded for current filter criteria.")
            
    with col_t1_4:
        render_chart_card(
            title="⚡ McDill24 Giving Day Impact vs Traditional Giving",
            subtitle="Comparing average gift and digital engagement behavior between cohorts",
            badge_text="Campaign Comparison"
        )
        if donors_fy26 > 0:
            m24_comp = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].copy()
            m24_comp['Giving_Day_Type'] = np.where(m24_comp['McGill24_Gift_Amount_FY26'] > 0, 'McDill24 Donors', 'Traditional Donors')
            comp_metrics = m24_comp.groupby('Giving_Day_Type').agg(
                Donors=('Constituent_ID', 'count'),
                Avg_Gift=('Giving_Amount_FY26', 'mean'),
                Avg_Web_Views=('GA4_Giving_Page_Views_FY26', 'mean'),
                Avg_Email_Clicks=('Emails_Clicked_FY26', 'mean')
            ).reset_index()
            
            fig_comp = px.bar(
                comp_metrics,
                x='Giving_Day_Type',
                y='Avg_Gift',
                color='Giving_Day_Type',
                color_discrete_map={'McDill24 Donors': '#ED1B2F', 'Traditional Donors': '#0F172A'},
                text=comp_metrics['Avg_Gift'].apply(lambda x: f"${x:,.2f}"),
                labels={'Avg_Gift': 'Average FY26 Gift ($)'}
            )
            fig_comp.update_traces(
                textposition='outside',
                hovertemplate="<b>%{x}</b><br>Average Gift: %{y:$,.2f}<extra></extra>"
            )
            apply_custom_chart_theme(fig_comp, height=330)
            fig_comp.update_layout(showlegend=False, yaxis=dict(title='Average Annual Gift ($)'))
            st.plotly_chart(fig_comp, use_container_width=True)


# =============================================================================
# TAB 2: DONOR LIFECYCLE, RETENTION & PIPELINE HEALTH
# =============================================================================
with tabs[2]:
    t2_c1, t2_c2, t2_c3, t2_c4 = st.columns(4)
    gave_prior_pool = (filtered_df['Gave_Prior'] == 1) & (filtered_df['Donated_FY25'] == 0)
    n_lapsed_pool = gave_prior_pool.sum()
    reactivated_cnt = (gave_prior_pool & (filtered_df['Donated_FY26'] == 1)).sum()
    reactivation_pct = (reactivated_cnt / n_lapsed_pool * 100) if n_lapsed_pool > 0 else 0.0
    
    never_pool = (filtered_df['Gave_Prior'] == 0) & (filtered_df['Donated_FY25'] == 0)
    n_never_pool = never_pool.sum()
    new_acquired_cnt = (never_pool & (filtered_df['Donated_FY26'] == 1)).sum()
    acquisition_pct = (new_acquired_cnt / n_never_pool * 100) if n_never_pool > 0 else 0.0
    
    n_sustainers_filt = (filtered_df['Is_Monthly_Sustainer_FY26'] == 1).sum()
    sustainer_pct = (n_sustainers_filt / donors_fy26 * 100) if donors_fy26 > 0 else 0.0
    
    with t2_c1:
        render_kpi_card(
            title="KPI 5: Repeat Retention",
            value=f"{retention_rate:.2f}%",
            pillar_badge="Retention",
            benchmark_text=f"{retained_25_26:,} Donors Retained",
            benchmark_status="good",
            badge_color="green",
            tooltip_def="Donors who gave in FY25 and renewed their contribution in FY26.",
            tooltip_bench="CASE North American Standard: 60% – 65%.",
            tooltip_impact="Represents core constituency health and long-term donor lifetime value (LTV)."
        )
    with t2_c2:
        render_kpi_card(
            title="KPI 6: Lapsed Reactivation",
            value=f"{reactivation_pct:.2f}%",
            pillar_badge="Win-Back",
            benchmark_text=f"{reactivated_cnt:,} of {n_lapsed_pool:,} Reactivated",
            benchmark_status="good",
            badge_color="blue",
            tooltip_def="Donors who gave prior to FY25, skipped FY25, and rejoined active ranks in FY26.",
            tooltip_bench="CASE Benchmark: 10% – 12% annual reactivation rate.",
            tooltip_impact="Demonstrates win-back campaign effectiveness on dormant affinity pools."
        )
    with t2_c3:
        render_kpi_card(
            title="KPI 7: New Acquisition",
            value=f"{acquisition_pct:.2f}%",
            pillar_badge="Acquisition",
            benchmark_text=f"{new_acquired_cnt:,} First-Time Donors",
            benchmark_status="good",
            badge_color="red",
            tooltip_def="Constituents who made their very first philanthropic donation to McDill in FY26.",
            tooltip_bench="Higher Ed Annual Benchmark: 3% – 6% new acquisition rate.",
            tooltip_impact="Essential top-of-funnel pipeline feed to replace natural donor attrition."
        )
    with t2_c4:
        render_kpi_card(
            title="KPI 8: Monthly Sustainers",
            value=f"{sustainer_pct:.2f}%",
            pillar_badge="Recurring",
            benchmark_text=f"{n_sustainers_filt:,} Active Sustainers",
            benchmark_status="good",
            badge_color="purple",
            tooltip_def="Active donors enrolled in recurring monthly credit card or payroll giving programs.",
            tooltip_bench="Target: 20% – 25% of active annual donors.",
            tooltip_impact="Provides predictable, high-retention annual cash flow with 85%+ multi-year retention."
        )
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    # Donor Migration Sankey Diagram
    render_chart_card(
        title="🌊 Interactive Donor Migration Flow (FY25 Baseline ➔ FY26 Status)",
        subtitle="Visualizing retention, lapsed win-back, first-time acquisition, and constituent attrition",
        badge_text="Migration Sankey"
    )
    lybunt_cnt = ((filtered_df['Donated_FY25'] == 1) & (filtered_df['Donated_FY26'] == 0)).sum()
    dormant_cnt = n_lapsed_pool - reactivated_cnt
    remain_never_cnt = n_never_pool - new_acquired_cnt
    
    sankey_labels = [
        f"FY25 Donors ({donors_fy25:,})",
        f"Prior Lapsed ({n_lapsed_pool:,})",
        f"Never Gave ({n_never_pool:,})",
        f"Retained Donors ({retained_25_26:,})",
        f"LYBUNTs ({lybunt_cnt:,})",
        f"Reactivated Donors ({reactivated_cnt:,})",
        f"Dormant Lapsed ({dormant_cnt:,})",
        f"New Acquired ({new_acquired_cnt:,})",
        f"Unacquired Alumni ({remain_never_cnt:,})"
    ]
    
    sources = [0, 0, 1, 1, 2, 2]
    targets = [3, 4, 5, 6, 7, 8]
    values = [retained_25_26, lybunt_cnt, reactivated_cnt, dormant_cnt, new_acquired_cnt, remain_never_cnt]
    
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18,
            thickness=18,
            line=dict(color="#CBD5E1", width=0.5),
            label=sankey_labels,
            color=["#0F172A", "#F59E0B", "#94A3B8", "#10B981", "#EF4444", "#3B82F6", "#CBD5E1", "#ED1B2F", "#E2E8F0"]
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=["rgba(16, 185, 129, 0.4)", "rgba(239, 68, 68, 0.4)", "rgba(59, 130, 246, 0.4)",
                   "rgba(203, 213, 225, 0.4)", "rgba(237, 27, 47, 0.4)", "rgba(226, 232, 240, 0.4)"]
        )
    )])
    fig_sankey.update_layout(
        height=360,
        margin=dict(l=15, r=15, t=15, b=15),
        font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
    )
    st.plotly_chart(fig_sankey, use_container_width=True)
    
    col_t2_1, col_t2_2 = st.columns(2)
    with col_t2_1:
        render_chart_card(
            title="🔄 Repeat Donor Giving Trends (FY25 ➔ FY26)",
            subtitle="Proportion of retained repeat donors who upgraded, maintained, or downgraded gift level",
            badge_text="Upgrade Velocity"
        )
        repeat_mask = (filtered_df['Donated_FY25'] == 1) & (filtered_df['Donated_FY26'] == 1)
        repeat_data = filtered_df[repeat_mask]
        if len(repeat_data) > 0:
            upgraded = (repeat_data['Giving_Amount_FY26'] > repeat_data['Giving_Amount_FY25'] * 1.01).sum()
            same = (np.isclose(repeat_data['Giving_Amount_FY26'], repeat_data['Giving_Amount_FY25'], atol=0.01)).sum()
            downgraded = (repeat_data['Giving_Amount_FY26'] < repeat_data['Giving_Amount_FY25'] * 0.99).sum()
            
            up_df = pd.DataFrame({
                'Behavior': ['Upgraded (+15-60%)', 'Maintained (Same)', 'Downgraded (-5-30%)'],
                'Donors': [upgraded, same, downgraded],
                'Percentage': [upgraded/len(repeat_data)*100, same/len(repeat_data)*100, downgraded/len(repeat_data)*100]
            })
            fig_up = px.bar(
                up_df,
                x='Behavior',
                y='Donors',
                color='Behavior',
                color_discrete_map={'Upgraded (+15-60%)': '#10B981', 'Maintained (Same)': '#3B82F6', 'Downgraded (-5-30%)': '#F59E0B'},
                text=up_df['Percentage'].apply(lambda x: f"{x:.1f}%")
            )
            fig_up.update_traces(
                textposition='outside',
                hovertemplate="<b>%{x}</b><br>Donors: %{y:,}<extra></extra>"
            )
            apply_custom_chart_theme(fig_up, height=310)
            fig_up.update_layout(showlegend=False, yaxis=dict(title='Repeat Donor Count'))
            st.plotly_chart(fig_up, use_container_width=True)
        else:
            st.info("No repeat donors in current filter selection.")
            
    with col_t2_2:
        render_chart_card(
            title="💎 Monthly Sustainers vs. Single-Gift Donors",
            subtitle="Comparing annual giving realization and lifetime event engagement",
            badge_text="Sustainer Economics"
        )
        if donors_fy26 > 0:
            sust_comp = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].copy()
            sust_comp['Donor_Type'] = np.where(sust_comp['Is_Monthly_Sustainer_FY26'] == 1, 'Monthly Sustainer', 'Single Gift Donor')
            sust_agg = sust_comp.groupby('Donor_Type').agg(
                Donors=('Constituent_ID', 'count'),
                Avg_Annual_Gift=('Giving_Amount_FY26', 'mean'),
                Avg_Lifetime_Events=('Lifetime_Events_Attended', 'mean')
            ).reset_index()
            
            fig_sust = px.bar(
                sust_agg,
                x='Donor_Type',
                y='Avg_Annual_Gift',
                color='Donor_Type',
                color_discrete_map={'Monthly Sustainer': '#7C3AED', 'Single Gift Donor': '#64748B'},
                text=sust_agg['Avg_Annual_Gift'].apply(lambda x: f"${x:,.2f}")
            )
            fig_sust.update_traces(
                textposition='outside',
                hovertemplate="<b>%{x}</b><br>Avg Annual Giving: %{y:$,.2f}<extra></extra>"
            )
            apply_custom_chart_theme(fig_sust, height=310)
            fig_sust.update_layout(showlegend=False, yaxis=dict(title='Avg Annual Giving ($)'))
            st.plotly_chart(fig_sust, use_container_width=True)


# =============================================================================
# TAB 3: MARKETING EFFICIENCY, CHANNEL ROI & DIGITAL FUNNEL
# =============================================================================
with tabs[3]:
    t3_c1, t3_c2, t3_c3, t3_c4 = st.columns(4)
    deliv_emails = filtered_df['Emails_Delivered_FY26'].sum()
    open_emails = filtered_df['Emails_Opened_FY26'].sum()
    click_emails = filtered_df['Emails_Clicked_FY26'].sum()
    open_rate_val = (open_emails / deliv_emails * 100) if deliv_emails > 0 else 0.0
    ctor_val = (click_emails / open_emails * 100) if open_emails > 0 else 0.0
    
    web_visitors_cnt = (filtered_df['GA4_Giving_Page_Views_FY26'] > 0).sum()
    web_donors_cnt = ((filtered_df['GA4_Giving_Page_Views_FY26'] > 0) & (filtered_df['Donated_FY26'] == 1)).sum()
    web_conv_pct = (web_donors_cnt / web_visitors_cnt * 100) if web_visitors_cnt > 0 else 0.0
    
    with t3_c1:
        render_kpi_card(
            title="KPI 9: Marketing CPDR",
            value=f"${cpdr:.4f}",
            pillar_badge="Efficiency",
            benchmark_text=f"{roi_mult:.1f}x ROI Multiplier",
            benchmark_status="good",
            badge_color="purple",
            tooltip_def="Total marketing outreach and solicitation expense divided by total revenue raised.",
            tooltip_bench="AFP Benchmark: < $0.15 per dollar raised.",
            tooltip_impact="Ensures maximum capital reaches students and academic priorities."
        )
    with t3_c2:
        render_kpi_card(
            title="KPI 10: Top Channel (Email)",
            value="16.35% Conv",
            pillar_badge="Channel",
            benchmark_text="$14.59 Cost per Acquired Donor",
            benchmark_status="good",
            badge_color="blue",
            tooltip_def="Conversion yield and cost per donor acquired across Email Digital appeals.",
            tooltip_bench="Email generated 56.9% of all annual funds at lowest cost.",
            tooltip_impact="Demonstrates high digital scalability with minimal variable cost."
        )
    with t3_c3:
        render_kpi_card(
            title="KPI 11: Email Open Rate",
            value=f"{open_rate_val:.2f}%",
            pillar_badge="Marketing Cloud",
            benchmark_text=f"{ctor_val:.2f}% Click-to-Open (CTOR)",
            benchmark_status="good",
            badge_color="green",
            tooltip_def="Unique email opens divided by verified delivered emails in Salesforce Marketing Cloud.",
            tooltip_bench="Higher Ed Benchmark: 24% – 28% open rate | 7% – 10% CTOR.",
            tooltip_impact="Reflects brand affinity, sender reputation, and subject line personalization efficacy."
        )
    with t3_c4:
        render_kpi_card(
            title="KPI 12: GA4 Web Conversion",
            value=f"{web_conv_pct:.2f}%",
            pillar_badge="Web Tracking",
            benchmark_text=f"{web_donors_cnt:,} of {web_visitors_cnt:,} Web Visitors",
            benchmark_status="good",
            badge_color="red",
            tooltip_def="Percentage of alumni visiting giving.mcdill.ca who completed a gift transaction in FY26.",
            tooltip_bench="General Alumni Conversion Benchmark: 15.0% – 22.0%.",
            tooltip_impact="Monitors frictionless checkout UI and digital payment conversion drop-offs."
        )
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    col_t3_1, col_t3_2 = st.columns([1.1, 0.9])
    with col_t3_1:
        render_chart_card(
            title="🎯 Solicitation Channel ROI & Conversion Matrix",
            subtitle="Donor conversion rate (%) vs Marketing return multiplier across solicitation channels",
            badge_text="Channel Performance"
        )
        chan_df = filtered_df.groupby('Display_Channel').agg(
            Constituents=('Constituent_ID', 'count'),
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Cost=('Marketing_Outreach_Cost_FY26', 'sum'),
            Raised=('Giving_Amount_FY26', 'sum')
        ).reset_index()
        chan_df['Conv_Rate'] = (chan_df['Donors'] / chan_df['Constituents']) * 100
        chan_df['Cost_Per_Donor'] = chan_df['Cost'] / chan_df['Donors'].replace(0, np.nan)
        chan_df['ROI'] = chan_df['Raised'] / chan_df['Cost'].replace(0, np.nan)
        
        fig_chan_bar = px.bar(
            chan_df,
            x='Display_Channel',
            y='Conv_Rate',
            color='ROI',
            color_continuous_scale='Reds',
            text=chan_df['Conv_Rate'].apply(lambda x: f"{x:.1f}%"),
            labels={'Conv_Rate': 'Conversion Rate (%)', 'Display_Channel': '', 'ROI': 'ROI Multiplier'}
        )
        fig_chan_bar.update_traces(
            textposition='outside',
            hovertemplate="<b>%{x}</b><br>Conversion Rate: %{y:.2f}%<extra></extra>"
        )
        apply_custom_chart_theme(fig_chan_bar, height=340)
        st.plotly_chart(fig_chan_bar, use_container_width=True)
        
    with col_t3_2:
        render_chart_card(
            title="📋 Channel Empirical League Table",
            subtitle="Full revenue, cost, acquisition cost, and ROI economics by channel",
            badge_text="Audit Table"
        )
        chan_disp = chan_df.copy()
        chan_disp['Conv_Rate'] = chan_disp['Conv_Rate'].apply(lambda x: f"{x:.2f}%")
        chan_disp['Cost'] = chan_disp['Cost'].apply(lambda x: f"${x:,.2f}")
        chan_disp['Raised'] = chan_disp['Raised'].apply(lambda x: f"${x:,.2f}")
        chan_disp['Cost_Per_Donor'] = chan_disp['Cost_Per_Donor'].apply(lambda x: f"${x:,.2f}")
        chan_disp['ROI'] = chan_disp['ROI'].apply(lambda x: f"{x:.1f}x")
        st.dataframe(
            chan_disp[['Display_Channel', 'Constituents', 'Donors', 'Conv_Rate', 'Raised', 'ROI', 'Cost_Per_Donor']],
            hide_index=True,
            use_container_width=True
        )
        
    # Omnichannel Digital Conversion Funnel
    render_chart_card(
        title="🔻 Omnichannel Digital Conversion Funnel (SFMC ➔ GA4 ➔ CRM Gift)",
        subtitle="End-to-end constituent attrition from mass broadcast delivery through verified gift checkout",
        badge_text="Funnel Drop-Off"
    )
    funnel_stages = [
        "1. Addressable Universe",
        "2. Deliverable Valid Email",
        "3. Delivered FY26 Email",
        "4. Opened Email",
        "5. Clicked Email Link",
        "6. Visited GA4 Giving Page",
        "7. Completed Philanthropic Gift"
    ]
    funnel_counts = [
        n_filtered,
        (filtered_df['Has_Valid_Email'] == 1).sum(),
        (filtered_df['Emails_Delivered_FY26'] > 0).sum(),
        (filtered_df['Emails_Opened_FY26'] > 0).sum(),
        (filtered_df['Emails_Clicked_FY26'] > 0).sum(),
        (filtered_df['GA4_Giving_Page_Views_FY26'] > 0).sum(),
        donors_fy26
    ]
    
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_counts,
        textinfo="value+percent initial",
        marker=dict(color=["#0F172A", "#1E293B", "#334155", "#475569", "#2563EB", "#D97706", "#ED1B2F"])
    ))
    fig_funnel.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=10, b=10),
        font=dict(family="Inter, sans-serif", size=12, color="#0F172A")
    )
    st.plotly_chart(fig_funnel, use_container_width=True)


# =============================================================================
# TAB 4: CASE 4-PILLAR ALUMNI ENGAGEMENT (AEM) & EXPERIENTIAL
# =============================================================================
with tabs[4]:
    t4_c1, t4_c2, t4_c3, t4_c4 = st.columns(4)
    event_attendees_cnt = (filtered_df['Events_Attended_FY26'] > 0).sum()
    event_part_rate = (event_attendees_cnt / n_filtered * 100) if n_filtered > 0 else 0.0
    tot_events_reg = filtered_df['Events_Registered_FY26'].sum()
    tot_events_att = filtered_df['Events_Attended_FY26'].sum()
    show_rate = (tot_events_att / tot_events_reg * 100) if tot_events_reg > 0 else 0.0
    
    multi_pillar_cnt = (filtered_df['CASE_Pillar_Count'] >= 2).sum()
    multi_pillar_pct = (multi_pillar_cnt / n_filtered * 100) if n_filtered > 0 else 0.0
    
    volunteers_cnt = (filtered_df['Is_Active_Volunteer_FY26'] == 1).sum()
    volunteer_pct = (volunteers_cnt / n_filtered * 100) if n_filtered > 0 else 0.0
    tot_vol_hours = filtered_df['Volunteer_Hours_Logged_FY26'].sum()
    avg_vol_hours = (tot_vol_hours / volunteers_cnt) if volunteers_cnt > 0 else 0.0
    
    with t4_c1:
        render_kpi_card(
            title="KPI 13a: Event Attendance",
            value=f"{event_part_rate:.2f}%",
            pillar_badge="Experiential",
            benchmark_text=f"{event_attendees_cnt:,} Alumni Attended",
            benchmark_status="good",
            badge_color="blue",
            tooltip_def="Alumni participating in at least one university webinar, branch chapter, or Homecoming event.",
            tooltip_bench="CASE Experiential Standard: 10% – 15% annual participation.",
            tooltip_impact="Event attendees display a 3.2x higher propensity to give compared to non-attendees."
        )
    with t4_c2:
        render_kpi_card(
            title="KPI 13b: Event Show Rate",
            value=f"{show_rate:.2f}%",
            pillar_badge="Attendance",
            benchmark_text=f"{tot_events_att:,} / {tot_events_reg:,} Tickets",
            benchmark_status="good",
            badge_color="green",
            tooltip_def="Actual attendance realized divided by total registered tickets on Eventbrite / AlumnForce.",
            tooltip_bench="Higher Ed Benchmark: 55% – 65% realized show rate.",
            tooltip_impact="Direct metric of event program relevance and reminder automation efficacy."
        )
    with t4_c3:
        render_kpi_card(
            title="KPI 14a: Multi-Pillar Engagement",
            value=f"{multi_pillar_pct:.2f}%",
            pillar_badge="CASE AEM",
            benchmark_text=f"{multi_pillar_cnt:,} in 2+ CASE Modes",
            benchmark_status="good",
            badge_color="red",
            tooltip_def="Constituents actively engaged across 2 or more of the 4 CASE Global Engagement modes.",
            tooltip_bench="CASE Lift Law: 2+ pillars yields a 43.7% giving rate vs 4.8% for 0–1 pillars.",
            tooltip_impact="Multi-pillar touchpoints represent the strongest single predictor of major gift inclination."
        )
    with t4_c4:
        render_kpi_card(
            title="KPI 14b: Volunteer Mobilization",
            value=f"{volunteer_pct:.2f}%",
            pillar_badge="Volunteer",
            benchmark_text=f"{tot_vol_hours:,.0f} Total Hours ({avg_vol_hours:.1f} avg)",
            benchmark_status="good",
            badge_color="purple",
            tooltip_def="Alumni serving as student mentors, reunion committee leaders, or McDill24 ambassadors.",
            tooltip_bench="Target: 4% – 7% of addressable alumni actively volunteering.",
            tooltip_impact="Volunteers give at an 8x rate relative to general alumni and represent future board prospects."
        )
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    col_t4_1, col_t4_2 = st.columns(2)
    with col_t4_1:
        render_chart_card(
            title="🎯 CASE Engagement Index vs. Philanthropic Lift",
            subtitle="Giving participation rate (%) jumps dramatically as alumni engage across multiple modes",
            badge_text="CASE Lift Law"
        )
        aem_analysis = filtered_df.groupby('CASE_Pillar_Count').agg(
            Constituents=('Constituent_ID', 'count'),
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Total_Raised=('Giving_Amount_FY26', 'sum')
        ).reset_index()
        aem_analysis['Giving_Rate'] = (aem_analysis['Donors'] / aem_analysis['Constituents']) * 100
        aem_analysis['Avg_Gift'] = aem_analysis['Total_Raised'] / aem_analysis['Donors'].replace(0, np.nan)
        
        fig_aem = px.bar(
            aem_analysis,
            x='CASE_Pillar_Count',
            y='Giving_Rate',
            color='CASE_Pillar_Count',
            color_continuous_scale=['#CBD5E1', '#93C5FD', '#3B82F6', '#10B981', '#ED1B2F'],
            text=aem_analysis['Giving_Rate'].apply(lambda x: f"{x:.1f}%"),
            labels={
                'CASE_Pillar_Count': 'Number of Active CASE Modes (0 to 4)',
                'Giving_Rate': 'FY26 Giving Participation Rate (%)'
            }
        )
        fig_aem.update_traces(
            textposition='outside',
            hovertemplate="<b>%{x} Active Modes</b><br>Giving Rate: %{y:.1f}%<extra></extra>"
        )
        apply_custom_chart_theme(fig_aem, height=330)
        fig_aem.update_layout(coloraxis_showscale=False, yaxis=dict(title='Donor Conversion Rate (%)'))
        st.plotly_chart(fig_aem, use_container_width=True)
        
    with col_t4_2:
        render_chart_card(
            title="🎉 Homecoming & Event Peaks Across Reunion Cycles",
            subtitle="Homecoming spikes corresponding to traditional 5-year milestone reunion cohorts",
            badge_text="Reunion Milestone"
        )
        years_df = filtered_df.groupby('Years_Since_Grad').agg(
            Constituents=('Constituent_ID', 'count'),
            Events_Attended=('Events_Attended_FY26', lambda x: (x > 0).sum()),
            Homecoming=('Attended_Homecoming_FY26', 'sum')
        ).reset_index()
        years_df['Event_Rate'] = (years_df['Events_Attended'] / years_df['Constituents']) * 100
        years_df['Homecoming_Rate'] = (years_df['Homecoming'] / years_df['Constituents']) * 100
        
        fig_reunion = go.Figure()
        fig_reunion.add_trace(go.Scatter(
            x=years_df['Years_Since_Grad'],
            y=years_df['Event_Rate'],
            name='All Event Attendance (%)',
            mode='lines',
            line=dict(color='#0F172A', width=2),
            hovertemplate="<b>%{x} Years Since Grad</b><br>Event Attendance: %{y:.1f}%<extra></extra>"
        ))
        fig_reunion.add_trace(go.Scatter(
            x=years_df['Years_Since_Grad'],
            y=years_df['Homecoming_Rate'],
            name='Homecoming Reunion (%)',
            mode='lines+markers',
            line=dict(color='#ED1B2F', width=2.5),
            marker=dict(size=5, color='#ED1B2F'),
            hovertemplate="<b>%{x} Years Since Grad</b><br>Homecoming Attendance: %{y:.1f}%<extra></extra>"
        ))
        apply_custom_chart_theme(fig_reunion, height=330)
        fig_reunion.update_layout(
            xaxis=dict(title='Years Since Graduation (Cohorts)'),
            yaxis=dict(title='Participation Rate (%)'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig_reunion, use_container_width=True)


# =============================================================================
# TAB 5: PROSPECT CAPACITY, WEALTH CAPTURE & FACULTY INTELLIGENCE
# =============================================================================
with tabs[5]:
    t5_c1, t5_c2, t5_c3 = st.columns(3)
    t1_t2_rev = filtered_df[filtered_df['Wealth_Screening_Rating'].isin(['Tier 1: $100k+', 'Tier 2: $25k-$99k'])]['Giving_Amount_FY26'].sum()
    t1_t2_pct_rev = (t1_t2_rev / tot_rev_fy26 * 100) if tot_rev_fy26 > 0 else 0.0
    
    t1_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 1: $100k+']
    t1_part = ((t1_df['Gift_Count_FY26'] > 0).sum() / len(t1_df) * 100) if len(t1_df) > 0 else 0.0
    t1_avg = (t1_df['Giving_Amount_FY26'].sum() / (t1_df['Gift_Count_FY26'] > 0).sum()) if (t1_df['Gift_Count_FY26'] > 0).sum() > 0 else 0.0
    
    t2_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 2: $25k-$99k']
    t2_part = ((t2_df['Gift_Count_FY26'] > 0).sum() / len(t2_df) * 100) if len(t2_df) > 0 else 0.0
    t2_avg = (t2_df['Giving_Amount_FY26'].sum() / (t2_df['Gift_Count_FY26'] > 0).sum()) if (t2_df['Gift_Count_FY26'] > 0).sum() > 0 else 0.0
    
    with t5_c1:
        render_kpi_card(
            title="KPI 15a: Wealth Concentration",
            value=f"{t1_t2_pct_rev:.1f}% Rev",
            pillar_badge="Major Gifts",
            benchmark_text=f"${t1_t2_rev/1e6:.2f}M from Top 5% Alumni",
            benchmark_status="good",
            badge_color="red",
            tooltip_def="Proportion of total annual funds contributed by top wealth screening tiers (Tiers 1 & 2).",
            tooltip_bench="CASE Benchmark: Top 5% typically contribute 65% – 75% of total university revenue.",
            tooltip_impact="Confirms extreme Pareto concentration and justifies dedicated Major Gift Officer portfolios."
        )
    with t5_c2:
        render_kpi_card(
            title="KPI 15b: Tier 1 ($100k+) Yield",
            value=f"{t1_part:.1f}% Conv",
            pillar_badge="Capacity",
            benchmark_text=f"${t1_avg:,.2f} Average Gift",
            benchmark_status="good",
            badge_color="blue",
            tooltip_def="Participation yield and average gift among alumni screened with $100k+ gift capacity.",
            tooltip_bench="Target: 60%+ realization with $5k+ average contribution.",
            tooltip_impact="Primary pipeline for transformational endowed chairs and institutional capital gifts."
        )
    with t5_c3:
        render_kpi_card(
            title="Tier 2 ($25k-$99k) Yield",
            value=f"{t2_part:.1f}% Conv",
            pillar_badge="Capacity",
            benchmark_text=f"${t2_avg:,.2f} Average Gift",
            benchmark_status="good",
            badge_color="green",
            tooltip_def="Participation yield and average gift among alumni screened with $25k-$99k gift capacity.",
            tooltip_bench="Target: 45%+ realization with $2k+ average contribution.",
            tooltip_impact="High-velocity leadership annual giving and principal prospect incubation pool."
        )
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    col_t5_1, col_t5_2 = st.columns([1.1, 0.9])
    with col_t5_1:
        render_chart_card(
            title="🏛️ McDill Faculty League Commitments",
            subtitle="Comparing total revenue raised across faculties with participation heat",
            badge_text="Faculty League"
        )
        fac_league = filtered_df.groupby('Primary_Faculty').agg(
            Alumni=('Constituent_ID', 'count'),
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Total_Raised=('Giving_Amount_FY26', 'sum'),
            FY25_Donors=('Gift_Count_FY25', lambda x: (x > 0).sum()),
            Retained_Donors=('Donated_FY25', lambda x: ((x == 1) & (filtered_df.loc[x.index, 'Donated_FY26'] == 1)).sum())
        ).reset_index()
        fac_league['Participation_Rate'] = (fac_league['Donors'] / fac_league['Alumni']) * 100
        fac_league['Retention_Rate'] = (fac_league['Retained_Donors'] / fac_league['FY25_Donors'].replace(0, np.nan)) * 100
        fac_league['Avg_Gift'] = fac_league['Total_Raised'] / fac_league['Donors'].replace(0, np.nan)
        fac_league = fac_league.sort_values(by='Total_Raised', ascending=True)
        
        fig_fac = px.bar(
            fac_league,
            x='Total_Raised',
            y='Primary_Faculty',
            orientation='h',
            color='Participation_Rate',
            color_continuous_scale=['#FED7AA', '#FB7185', '#E11D48', '#881337'],
            text=fac_league['Total_Raised'].apply(lambda x: f"${x/1e3:,.0f}k"),
            labels={'Total_Raised': 'Total FY26 Commitments ($ CAD)', 'Primary_Faculty': '', 'Participation_Rate': 'Part %'}
        )
        fig_fac.update_traces(
            textposition='outside',
            hovertemplate="<b>%{y}</b><br>Total Raised: %{x:$,.0f}<extra></extra>"
        )
        apply_custom_chart_theme(fig_fac, height=360)
        fig_fac.update_layout(coloraxis_colorbar=dict(title="Part %", thickness=12, len=0.8))
        st.plotly_chart(fig_fac, use_container_width=True)
        
    with col_t5_2:
        render_chart_card(
            title="💎 Wealth Tier Realization Matrix",
            subtitle="Constituent volume, donors, participation %, and share of funds raised",
            badge_text="Screening Matrix"
        )
        wealth_table = filtered_df.groupby('Wealth_Screening_Rating').agg(
            Alumni=('Constituent_ID', 'count'),
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Total_Raised=('Giving_Amount_FY26', 'sum')
        ).reindex(all_tiers).dropna().reset_index()
        
        wealth_table['Participation'] = (wealth_table['Donors'] / wealth_table['Alumni'] * 100).apply(lambda x: f"{x:.1f}%")
        wealth_table['Avg_Gift'] = (wealth_table['Total_Raised'] / wealth_table['Donors'].replace(0, np.nan)).apply(lambda x: f"${x:,.2f}")
        wealth_table['Share_of_Total'] = (wealth_table['Total_Raised'] / tot_rev_fy26 * 100).apply(lambda x: f"{x:.1f}%")
        wealth_table['Total_Raised'] = wealth_table['Total_Raised'].apply(lambda x: f"${x:,.2f}")
        
        st.dataframe(
            wealth_table[['Wealth_Screening_Rating', 'Alumni', 'Donors', 'Participation', 'Avg_Gift', 'Total_Raised', 'Share_of_Total']],
            hide_index=True,
            use_container_width=True
        )
        
    render_chart_card(
        title="🌍 Geographic Philanthropic Distribution",
        subtitle="Regional philanthropic revenue ($ CAD) and active participation rate",
        badge_text="Geography"
    )
    geo_df = filtered_df.groupby('Geographic_Region').agg(
        Alumni=('Constituent_ID', 'count'),
        Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
        Revenue=('Giving_Amount_FY26', 'sum')
    ).reset_index()
    geo_df['Participation'] = (geo_df['Donors'] / geo_df['Alumni']) * 100
    
    fig_geo = px.bar(
        geo_df,
        x='Geographic_Region',
        y='Revenue',
        color='Geographic_Region',
        color_discrete_sequence=['#ED1B2F', '#0F172A', '#2563EB', '#10B981'],
        text=geo_df.apply(lambda r: f"${r['Revenue']/1e6:.2f}M ({r['Participation']:.1f}% Part)", axis=1),
        labels={'Revenue': 'Total FY26 Revenue ($ CAD)', 'Geographic_Region': 'Region'}
    )
    fig_geo.update_traces(
        textposition='outside',
        hovertemplate="<b>%{x}</b><br>Revenue: %{y:$,.0f}<extra></extra>"
    )
    apply_custom_chart_theme(fig_geo, height=310)
    fig_geo.update_layout(showlegend=False)
    st.plotly_chart(fig_geo, use_container_width=True)


# =============================================================================
# 7. CORPORATE FOOTER
# =============================================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 12px; padding: 12px 0;">
    McDill University Advancement Analytics Platform | Built with Streamlit & Plotly | FY2026 Reporting Year
</div>
""", unsafe_allow_html=True)
