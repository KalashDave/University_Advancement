"""
McDill University Advancement - Executive Analytics & CASE Intelligence Portal
File: app.py
Description: Lean, clean executive dashboard inspired by Tabler UI with minimal text,
             interactive tooltips, prominent dropdown module navigation, and high-impact visual cards.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# =============================================================================
# 1. PAGE CONFIGURATION & TABLER-STYLE MODERN DESIGN SYSTEM
# =============================================================================
st.set_page_config(
    page_title="McDill Advancement Dashboard | FY26",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Tabler UI Clean Modern CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B;
    }
    
    /* Tabler Clean Canvas Background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Top Navigation Bar */
    .tabler-navbar {
        background: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        padding: 14px 24px;
        margin: -4rem -4rem 1.5rem -4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    
    .tabler-brand {
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .tabler-logo-icon {
        width: 36px;
        height: 36px;
        background: #ED1B2F;
        color: #FFFFFF;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 2px 6px rgba(237, 27, 47, 0.25);
    }
    
    .tabler-brand-text {
        font-size: 17px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
    }
    
    .tabler-brand-sub {
        font-size: 11px;
        font-weight: 500;
        color: #64748B;
    }
    
    .tabler-nav-badge {
        background: #F1F5F9;
        color: #475569;
        border: 1px solid #E2E8F0;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    
    .live-dot {
        width: 7px;
        height: 7px;
        background: #10B981;
        border-radius: 50%;
        display: inline-block;
    }
    
    /* Prominent Module Switcher */
    .nav-selector-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 20px;
        box-shadow: 0 1px 4px rgba(15, 23, 42, 0.03);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
    }
    
    .nav-selector-label {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    
    /* Clean Dashboard Title Bar */
    .dashboard-title-row {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-bottom: 16px;
    }
    
    .dashboard-title {
        font-size: 22px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        margin: 0;
    }
    
    .dashboard-subtitle {
        font-size: 12px;
        color: #64748B;
        margin: 2px 0 0 0;
    }
    
    /* =========================================================================
       TABLER-STYLE KPI CARDS (CLEAN & MINIMAL)
       ========================================================================= */
    .tabler-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 98px;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    
    .tabler-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 14px rgba(15, 23, 42, 0.06);
    }
    
    .tabler-card-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .tabler-card-value {
        font-size: 24px;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin: 4px 0 2px 0;
    }
    
    .tabler-card-label {
        font-size: 12px;
        font-weight: 500;
        color: #64748B;
    }
    
    .tabler-delta {
        font-size: 11px;
        font-weight: 700;
        display: inline-flex;
        align-items: center;
        gap: 2px;
    }
    
    .tabler-delta.up { color: #10B981; }
    .tabler-delta.down { color: #EF4444; }
    .tabler-delta.neutral { color: #64748B; }
    
    /* Interactive Hover Tooltip (Optional Info) */
    .tooltip-box {
        position: relative;
        display: inline-block;
        cursor: pointer;
    }
    
    .tooltip-icon {
        width: 17px;
        height: 17px;
        border-radius: 50%;
        background: #F1F5F9;
        color: #94A3B8;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: 800;
        transition: all 0.15s ease;
        user-select: none;
    }
    
    .tooltip-box:hover .tooltip-icon {
        background: #0F172A;
        color: #FFFFFF;
    }
    
    .tooltip-dropdown {
        visibility: hidden;
        opacity: 0;
        width: 240px;
        background: #0F172A;
        color: #F8FAFC;
        text-align: left;
        border-radius: 8px;
        padding: 10px 12px;
        font-size: 11px;
        line-height: 1.45;
        position: absolute;
        z-index: 9999;
        top: 24px;
        right: 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.35);
        border: 1px solid #334155;
        transition: opacity 0.2s ease, transform 0.2s ease;
        transform: translateY(-4px);
        pointer-events: none;
    }
    
    .tooltip-box:hover .tooltip-dropdown {
        visibility: visible;
        opacity: 1;
        transform: translateY(0);
    }
    
    /* Visual Container Cards */
    .tabler-visual-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px 18px 12px 18px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03);
        margin-bottom: 18px;
    }
    
    .tabler-visual-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        border-bottom: 1px solid #F1F5F9;
        padding-bottom: 8px;
    }
    
    .tabler-visual-title {
        font-size: 13px;
        font-weight: 700;
        color: #0F172A;
    }
    
    .tabler-badge-small {
        font-size: 10px;
        font-weight: 700;
        padding: 2px 6px;
        border-radius: 4px;
        background: #F1F5F9;
        color: #475569;
    }

    /* Lean Table Styling */
    .tabler-activity-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 12px;
    }
    
    .tabler-activity-table th {
        text-align: left;
        color: #64748B;
        font-weight: 600;
        padding: 8px 10px;
        border-bottom: 1px solid #E2E8F0;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    .tabler-activity-table td {
        padding: 10px 10px;
        border-bottom: 1px solid #F1F5F9;
        color: #1E293B;
    }
    
    .tabler-activity-table tr:last-child td {
        border-bottom: none;
    }

    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# =============================================================================
# 2. DATA CACHING & FAST AGGREGATION
# =============================================================================
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
    
    # Aliases
    df['Last_Gift_Designation'] = df['Last_Gift_Designation'].replace({
        'The McGill Fund (Unrestricted)': 'The McDill Fund (Unrestricted)'
    })
    df['Display_Channel'] = df['Primary_Solicitation_Channel_FY26'].replace({
        'Crowdfunding_McGill24': 'Crowdfunding_McDill24'
    })
    
    return df


df_master = load_and_preprocess_advancement_data()


# =============================================================================
# 3. REUSABLE TABLER KPI CARD & PLOTLY THEMING
# =============================================================================
def render_tabler_kpi(value: str, label: str, delta: str = "", delta_type: str = "up",
                      tooltip_def: str = "", tooltip_bench: str = ""):
    """Renders a clean Tabler-style KPI card with optional hover tooltip."""
    delta_icon = "▲" if delta_type == "up" else ("▼" if delta_type == "down" else "•")
    delta_html = f'<span class="tabler-delta {delta_type}">{delta_icon} {delta}</span>' if delta else ''
    
    tooltip_html = ""
    if tooltip_def or tooltip_bench:
        tooltip_html = f"""
        <div class="tooltip-box">
            <div class="tooltip-icon">ℹ</div>
            <div class="tooltip-dropdown">
                <div style="font-weight:700; color:#FFFFFF; margin-bottom:4px;">{label}</div>
                <div style="color:#CBD5E1; margin-bottom:4px;">{tooltip_def}</div>
                <div style="color:#93C5FD; font-size:10px; border-top:1px solid #334155; padding-top:4px;"><b>Benchmark:</b> {tooltip_bench}</div>
            </div>
        </div>
        """
    
    st.markdown(f"""
    <div class="tabler-card">
        <div class="tabler-card-top">
            <span class="tabler-card-label">{label}</span>
            <div style="display: flex; align-items: center; gap: 8px;">
                {delta_html}
                {tooltip_html}
            </div>
        </div>
        <div class="tabler-card-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def apply_tabler_theme(fig, height=300):
    """Applies sleek Tabler UI styling to Plotly figures."""
    fig.update_layout(
        font=dict(family="Inter, -apple-system, sans-serif", size=11, color="#334155"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=40, r=25, t=15, b=30),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=11,
            font_color="#FFFFFF",
            font_family="Inter, sans-serif",
            bordercolor="#334155"
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#64748B"))
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#64748B"))
    return fig


# =============================================================================
# 4. SIDEBAR (COMPACT FILTERS)
# =============================================================================
with st.sidebar:
    st.markdown("### 🔍 Filters")
    all_faculties = sorted(df_master['Primary_Faculty'].unique().tolist())
    selected_faculties = st.multiselect("Faculty", options=all_faculties, default=all_faculties)
    
    cohort_options = ['All Cohorts', 'Young Alumni (<10 yrs)', 'Mid-Career (10-25 yrs)', 'Senior Alumni (25+ yrs)']
    quick_cohort = st.selectbox("Cohort", options=cohort_options, index=0)
    
    all_regions = ['Quebec', 'Rest of Canada', 'United States', 'International']
    selected_regions = st.multiselect("Region", options=all_regions, default=all_regions)
    
    all_tiers = ['Tier 1: $100k+', 'Tier 2: $25k-$99k', 'Tier 3: $5k-$24k', 'Tier 4: $1k-$4.9k', 'Tier 5: Under $1k', 'Unrated']
    selected_tiers = st.multiselect("Wealth Tier", options=all_tiers, default=all_tiers)
    
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
    st.warning("No records match active filters.")
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
# 5. TOP NAVBAR & PROMINENT MODULE SELECTOR
# =============================================================================
# Clean Tabler Top Navbar
st.markdown(f"""
<div class="tabler-navbar">
    <div class="tabler-brand">
        <div class="tabler-logo-icon">🎓</div>
        <div>
            <div class="tabler-brand-text">McDill University</div>
            <div class="tabler-brand-sub">Advancement Analytics</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <span class="tabler-nav-badge">
            <span class="live-dot"></span> FY26 Certified Close
        </span>
        <span class="tabler-nav-badge">
            {n_filtered:,} Records Active
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Prominent Module Selector (Big & Prominent Dropdown)
col_nav_left, col_nav_right = st.columns([1.8, 1.2])
with col_nav_left:
    selected_module = st.selectbox(
        "SELECT ADVANCEMENT INTELLIGENCE MODULE:",
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
with col_nav_right:
    st.markdown(f"""
    <div style="text-align: right; padding-top: 24px; font-size: 12px; color: #64748B;">
        Current Scope: <b>${tot_rev_fy26/1e6:.2f}M Raised</b> • <b>{donors_fy26:,} Donors</b>
    </div>
    """, unsafe_allow_html=True)


# =============================================================================
# VIEW 1: EXECUTIVE OVERVIEW (LANDING PAGE - TABLER UI INSPIRATION)
# =============================================================================
if selected_module == "📊 Executive Overview (Landing Dashboard)":
    
    st.markdown("""
    <div class="dashboard-title-row">
        <div>
            <h1 class="dashboard-title">Dashboard</h1>
            <p class="dashboard-subtitle">Executive overview of university philanthropic performance, donor participation, and engagement metrics.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 6 Top-Line KPI Cards (Exactly like the Tabler screenshot)
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    
    with k1:
        render_tabler_kpi(
            value=f"${tot_rev_fy26/1e6:.2f}M",
            label="Total Revenue",
            delta="+14%",
            delta_type="up",
            tooltip_def="Cumulative booked commitments across all funds in FY26.",
            tooltip_bench="U15 Benchmark: $3.0M – $6.5M"
        )
    with k2:
        render_tabler_kpi(
            value=f"{donors_fy26:,}",
            label="Active Donors",
            delta="+7%",
            delta_type="up",
            tooltip_def="Unique alumni making at least one gift in FY26.",
            tooltip_bench="Target: 4,000 – 4,800 donors"
        )
    with k3:
        render_tabler_kpi(
            value=f"{part_rate:.1f}%",
            label="Participation",
            delta="+1%",
            delta_type="up",
            tooltip_def="Percentage of addressable alumni who contributed.",
            tooltip_bench="CASE U15 Average: 8%–12%"
        )
    with k4:
        render_tabler_kpi(
            value=f"{retention_rate:.1f}%",
            label="Retention Rate",
            delta="+3%",
            delta_type="up",
            tooltip_def="Repeat donors from FY25 renewing in FY26.",
            tooltip_bench="CASE National Standard: 60%–65%"
        )
    with k5:
        render_tabler_kpi(
            value=f"${avg_gift:,.0f}",
            label="Average Gift",
            delta="+5%",
            delta_type="up",
            tooltip_def="Total revenue divided by active donor count.",
            tooltip_bench="Average Gift Target: $700 – $850"
        )
    with k6:
        render_tabler_kpi(
            value=f"{roi_mult:.1f}x",
            label="Marketing ROI",
            delta="+2%",
            delta_type="up",
            tooltip_def="Dollars raised per dollar of outreach cost.",
            tooltip_bench="AFP Standard: > 6.7x (cost < $0.15/dollar)"
        )
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    
    # Main Dashboard Visual Grid (Left 60%, Right 40% matching Tabler layout)
    grid_left, grid_right = st.columns([1.25, 0.75])
    
    with grid_left:
        # Development / Revenue Activity Card
        st.markdown("""
        <div class="tabler-visual-card">
            <div class="tabler-visual-header">
                <span class="tabler-visual-title">Development Activity (FY24 – FY26)</span>
                <span class="tabler-badge-small">Revenue & Donors</span>
            </div>
        """, unsafe_allow_html=True)
        
        my_df = pd.DataFrame({
            'Year': ['FY2024', 'FY2025', 'FY2026'],
            'Revenue': [tot_rev_fy24, tot_rev_fy25, tot_rev_fy26],
            'Donors': [(filtered_df['Gift_Count_FY24'] > 0).sum(), donors_fy25, donors_fy26]
        })
        
        # Smooth area chart like "Purchases" in Tabler image
        fig_area = go.Figure()
        fig_area.add_trace(go.Scatter(
            x=my_df['Year'],
            y=my_df['Revenue'],
            mode='lines+markers',
            name='Revenue ($)',
            line=dict(color='#206BC4', width=3, shape='spline'),
            fill='tozeroy',
            fillcolor='rgba(32, 107, 196, 0.08)',
            marker=dict(size=7, color='#206BC4'),
            hovertemplate="<b>%{x}</b><br>Revenue: %{y:$,.0f}<extra></extra>"
        ))
        apply_tabler_theme(fig_area, height=220)
        fig_area.update_layout(yaxis=dict(tickformat='$,.0s', showgrid=True))
        st.plotly_chart(fig_area, use_container_width=True)
        
        # Compact Activity Table underneath (like user/commit table in image)
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        fac_summary = filtered_df.groupby('Primary_Faculty').agg(
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Raised=('Giving_Amount_FY26', 'sum')
        ).reset_index().sort_values(by='Raised', ascending=False).head(4)
        
        table_html = """
        <table class="tabler-activity-table">
            <thead>
                <tr>
                    <th>Academic Faculty</th>
                    <th>Donors</th>
                    <th>Commitments</th>
                    <th>Share</th>
                </tr>
            </thead>
            <tbody>
        """
        for _, row in fac_summary.iterrows():
            share = (row['Raised'] / tot_rev_fy26 * 100) if tot_rev_fy26 > 0 else 0
            table_html += f"""
                <tr>
                    <td><b>{row['Primary_Faculty']}</b></td>
                    <td>{row['Donors']:,}</td>
                    <td>${row['Raised']:,.0f}</td>
                    <td><span style="color:#206BC4; font-weight:600;">{share:.1f}%</span></td>
                </tr>
            """
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with grid_right:
        # Donut Chart 1: Designation Allocation (like green 37%/63% donut in image)
        st.markdown("""
        <div class="tabler-visual-card">
            <div class="tabler-visual-header">
                <span class="tabler-visual-title">Gift Designation Share</span>
                <span class="tabler-badge-small">Allocation</span>
            </div>
        """, unsafe_allow_html=True)
        
        desig_df = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].groupby('Last_Gift_Designation')['Giving_Amount_FY26'].sum().reset_index()
        fig_d1 = px.pie(
            desig_df,
            names='Last_Gift_Designation',
            values='Giving_Amount_FY26',
            hole=0.62,
            color_discrete_sequence=['#2FB344', '#206BC4', '#4299E1', '#F59F00', '#D63939']
        )
        fig_d1.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="<b>%{label}</b><br>%{value:$,.0f} (%{percent})<extra></extra>"
        )
        fig_d1.update_layout(
            height=180,
            margin=dict(l=10, r=10, t=5, b=5),
            showlegend=False
        )
        st.plotly_chart(fig_d1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Donut Chart 2: CASE Engagement (like the blue multi-slice donut in image)
        st.markdown("""
        <div class="tabler-visual-card">
            <div class="tabler-visual-header">
                <span class="tabler-visual-title">CASE 4-Pillar Engagement</span>
                <span class="tabler-badge-small">AEM Modes</span>
            </div>
        """, unsafe_allow_html=True)
        
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
                '0 Modes': '#CBD5E1',
                '1 Mode': '#93C5FD',
                '2 Modes': '#206BC4',
                '3 Modes': '#2FB344',
                '4 Modes': '#D63939'
            }
        )
        fig_d2.update_traces(
            textposition='inside',
            textinfo='percent',
            hovertemplate="<b>%{label}</b><br>%{value:,} Alumni (%{percent})<extra></extra>"
        )
        fig_d2.update_layout(
            height=180,
            margin=dict(l=10, r=10, t=5, b=5),
            showlegend=False
        )
        st.plotly_chart(fig_d2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Bottom Row: 3 Secondary KPI Cards (like image bottom: New Feedbacks, Today profit, Users online)
    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    
    mcdill24_rev = filtered_df['McGill24_Gift_Amount_FY26'].sum()
    sustainers_cnt = (filtered_df['Is_Monthly_Sustainer_FY26'] == 1).sum()
    target_goal = 4000000.0
    pct_goal = (tot_rev_fy26 / target_goal * 100)
    
    with b1:
        render_tabler_kpi(
            value=f"${mcdill24_rev/1e3:,.0f}K",
            label="McDill24 Giving Day",
            delta=f"{(mcdill24_rev/tot_rev_fy26*100):.1f}% Share",
            delta_type="neutral",
            tooltip_def="Dollars mobilized during the 24-hour campaign.",
            tooltip_bench="CASE Benchmark: 15%–25% of annual revenue"
        )
    with b2:
        render_tabler_kpi(
            value=f"{sustainers_cnt:,}",
            label="Monthly Sustainers",
            delta=f"{(sustainers_cnt/donors_fy26*100):.1f}% Donors",
            delta_type="up",
            tooltip_def="Donors giving recurring monthly gifts.",
            tooltip_bench="Target: 20%–25% of active donors"
        )
    with b3:
        render_tabler_kpi(
            value=f"{pct_goal:.1f}%",
            label="Campaign Pace ($4.0M Goal)",
            delta=f"${(target_goal - tot_rev_fy26)/1e3:,.0f}K to go",
            delta_type="up",
            tooltip_def="Progress toward FY26 stretch commitment goal.",
            tooltip_bench="On track for 100% close"
        )


# =============================================================================
# VIEW 2: PHILANTHROPIC HEALTH & REVENUE
# =============================================================================
elif selected_module == "🏛️ Philanthropic Health & Revenue":
    st.markdown("""
    <div class="dashboard-title-row">
        <div>
            <h1 class="dashboard-title">Philanthropic Health & Commitments</h1>
            <p class="dashboard-subtitle">Multi-year philanthropic velocity, Pareto gift size dispersion, and campaign urgency.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    p1, p2, p3 = st.columns(3)
    mcdill24_rev = filtered_df['McGill24_Gift_Amount_FY26'].sum()
    with p1:
        render_tabler_kpi(
            value=f"${tot_rev_fy26:,.0f}",
            label="FY26 Total Commitments",
            delta="+14.2% YoY",
            delta_type="up",
            tooltip_def="Total gifts received across all funds in FY26.",
            tooltip_bench="U15 Target: $3.0M – $6.5M"
        )
    with p2:
        render_tabler_kpi(
            value=f"${avg_gift:,.2f}",
            label="Average Gift Yield",
            delta="Median: $150",
            delta_type="neutral",
            tooltip_def="Revenue divided by donor count.",
            tooltip_bench="U15 Avg: $600 – $850"
        )
    with p3:
        render_tabler_kpi(
            value=f"${mcdill24_rev:,.0f}",
            label="McDill24 Campaign",
            delta=f"{(mcdill24_rev/tot_rev_fy26*100):.1f}% Share",
            delta_type="up",
            tooltip_def="Annual 24-hour giving day total.",
            tooltip_bench="CASE Benchmark: 15% – 25%"
        )
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Multi-Year Trajectory (FY24–FY26)</span></div>', unsafe_allow_html=True)
        fig_traj = go.Figure()
        fig_traj.add_trace(go.Bar(
            x=['FY24', 'FY25', 'FY26'],
            y=[tot_rev_fy24, tot_rev_fy25, tot_rev_fy26],
            name='Revenue ($)',
            marker_color='#206BC4',
            text=[f"${tot_rev_fy24/1e6:.2f}M", f"${tot_rev_fy25/1e6:.2f}M", f"${tot_rev_fy26/1e6:.2f}M"],
            textposition='outside'
        ))
        apply_tabler_theme(fig_traj, height=280)
        st.plotly_chart(fig_traj, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c2:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Giving Tier Dispersion (Pareto)</span></div>', unsafe_allow_html=True)
        tier_agg = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].copy()
        tier_agg['Tier'] = pd.cut(
            tier_agg['Giving_Amount_FY26'],
            bins=[-np.inf, 100, 500, 2500, 10000, np.inf],
            labels=['<$100', '$100-$499', '$500-$2.4k', '$2.5k-$9.9k', '$10k+']
        )
        t_data = tier_agg.groupby('Tier', observed=True)['Giving_Amount_FY26'].sum().reset_index()
        fig_tier = px.bar(t_data, x='Tier', y='Giving_Amount_FY26', color='Giving_Amount_FY26', color_continuous_scale='Blues')
        apply_tabler_theme(fig_tier, height=280)
        fig_tier.update_layout(coloraxis_showscale=False, yaxis=dict(title='Total Raised ($)'))
        st.plotly_chart(fig_tier, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# VIEW 3: DONOR LIFECYCLE & RETENTION FUNNEL
# =============================================================================
elif selected_module == "🔄 Donor Lifecycle & Retention Funnel":
    st.markdown("""
    <div class="dashboard-title-row">
        <div>
            <h1 class="dashboard-title">Donor Lifecycle & Retention</h1>
            <p class="dashboard-subtitle">Constituent retention, lapsed donor win-backs, first-time acquisition, and recurring sustainers.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
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
        render_tabler_kpi(value=f"{retention_rate:.1f}%", label="Consecutive Retention", delta="+2.5%", delta_type="up", tooltip_bench="CASE: 60%–65%")
    with l2:
        render_tabler_kpi(value=f"{react_rate:.1f}%", label="Lapsed Reactivation", delta=f"{reactivated:,} Donors", delta_type="up", tooltip_bench="CASE: 10%–12%")
    with l3:
        render_tabler_kpi(value=f"{acq_rate:.1f}%", label="New Acquisition", delta=f"{acquired:,} First-Time", delta_type="neutral", tooltip_bench="Benchmark: 3%–6%")
    with l4:
        render_tabler_kpi(value=f"{(sustainers/donors_fy26*100):.1f}%", label="Monthly Sustainers", delta=f"{sustainers:,} Donors", delta_type="up", tooltip_bench="Target: 20%–25%")

    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Donor Migration Flow (FY25 ➔ FY26)</span></div>', unsafe_allow_html=True)
    
    lybunt = ((filtered_df['Donated_FY25'] == 1) & (filtered_df['Donated_FY26'] == 0)).sum()
    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            pad=16, thickness=16,
            label=[f"FY25 Donors ({donors_fy25:,})", f"Prior Lapsed ({n_lapsed:,})", f"Never Gave ({n_never:,})",
                   f"Retained ({retained_25_26:,})", f"LYBUNT ({lybunt:,})", f"Reactivated ({reactivated:,})",
                   f"Dormant ({n_lapsed-reactivated:,})", f"Acquired ({acquired:,})", f"Unacquired ({n_never-acquired:,})"],
            color=["#0F172A", "#F59E0B", "#94A3B8", "#10B981", "#EF4444", "#206BC4", "#CBD5E1", "#ED1B2F", "#E2E8F0"]
        ),
        link=dict(
            source=[0, 0, 1, 1, 2, 2],
            target=[3, 4, 5, 6, 7, 8],
            value=[retained_25_26, lybunt, reactivated, n_lapsed-reactivated, acquired, n_never-acquired],
            color=["rgba(16,185,129,0.35)", "rgba(239,68,68,0.35)", "rgba(32,107,196,0.35)", "rgba(203,213,225,0.35)", "rgba(237,27,47,0.35)", "rgba(226,232,240,0.35)"]
        )
    ))
    fig_sankey.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Inter", size=11))
    st.plotly_chart(fig_sankey, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# VIEW 4: MARKETING EFFICIENCY & CHANNELS
# =============================================================================
elif selected_module == "📈 Marketing Efficiency & Channels":
    st.markdown("""
    <div class="dashboard-title-row">
        <div>
            <h1 class="dashboard-title">Marketing Efficiency & Digital Funnel</h1>
            <p class="dashboard-subtitle">Cost per dollar raised, channel ROI multiplier, and digital conversion rates.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    cpdr = (tot_cost / tot_rev_fy26) if tot_rev_fy26 > 0 else 0.0
    open_rate = (filtered_df['Emails_Opened_FY26'].sum() / filtered_df['Emails_Delivered_FY26'].sum() * 100) if filtered_df['Emails_Delivered_FY26'].sum() > 0 else 0.0
    web_donors = ((filtered_df['GA4_Giving_Page_Views_FY26'] > 0) & (filtered_df['Donated_FY26'] == 1)).sum()
    web_visitors = (filtered_df['GA4_Giving_Page_Views_FY26'] > 0).sum()
    web_conv = (web_donors / web_visitors * 100) if web_visitors > 0 else 0.0
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        render_tabler_kpi(value=f"${cpdr:.4f}", label="Cost per $ Raised", delta="AFP Standard < $0.15", delta_type="up", tooltip_bench="AFP Standard: < $0.15")
    with m2:
        render_tabler_kpi(value=f"{roi_mult:.1f}x", label="Marketing ROI", delta="Total Spend: " + f"${tot_cost:,.0f}", delta_type="up")
    with m3:
        render_tabler_kpi(value=f"{open_rate:.1f}%", label="Email Open Rate", delta="Higher Ed Avg ~28%", delta_type="neutral")
    with m4:
        render_tabler_kpi(value=f"{web_conv:.1f}%", label="GA4 Giving Conversion", delta=f"{web_donors:,} Donors", delta_type="up")
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Channel Conversion Rate (%)</span></div>', unsafe_allow_html=True)
        chan_df = filtered_df.groupby('Display_Channel').agg(
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Total=('Constituent_ID', 'count')
        ).reset_index()
        chan_df['Conv'] = chan_df['Donors'] / chan_df['Total'] * 100
        fig_c = px.bar(chan_df, x='Display_Channel', y='Conv', color='Conv', color_continuous_scale='Blues', text=chan_df['Conv'].apply(lambda x: f"{x:.1f}%"))
        fig_c.update_traces(textposition='outside')
        apply_tabler_theme(fig_c, height=270)
        fig_c.update_layout(coloraxis_showscale=False, yaxis=dict(title='Conversion (%)'))
        st.plotly_chart(fig_c, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_m2:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Digital Giving Funnel</span></div>', unsafe_allow_html=True)
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
            marker=dict(color=["#0F172A", "#206BC4", "#4299E1", "#F59F00", "#10B981"])
        ))
        fig_fun.update_layout(height=270, margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Inter", size=10))
        st.plotly_chart(fig_fun, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# VIEW 5: CASE 4-PILLAR ENGAGEMENT (AEM)
# =============================================================================
elif selected_module == "🤝 CASE 4-Pillar Engagement (AEM)":
    st.markdown("""
    <div class="dashboard-title-row">
        <div>
            <h1 class="dashboard-title">CASE 4-Pillar Engagement</h1>
            <p class="dashboard-subtitle">Global Alumni Engagement Metrics (AEM): Philanthropic, Experiential, Volunteer, and Communication.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    events_att = (filtered_df['Events_Attended_FY26'] > 0).sum()
    event_rate = (events_att / n_filtered * 100) if n_filtered > 0 else 0.0
    show_rate = (filtered_df['Events_Attended_FY26'].sum() / filtered_df['Events_Registered_FY26'].sum() * 100) if filtered_df['Events_Registered_FY26'].sum() > 0 else 0.0
    multi_pillar = (filtered_df['CASE_Pillar_Count'] >= 2).sum()
    volunteers = (filtered_df['Is_Active_Volunteer_FY26'] == 1).sum()
    
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        render_tabler_kpi(value=f"{event_rate:.1f}%", label="Event Attendance", delta=f"{events_att:,} Alumni", delta_type="up", tooltip_bench="CASE Experiential: 10%–15%")
    with e2:
        render_tabler_kpi(value=f"{show_rate:.1f}%", label="Ticket Show Rate", delta="Realized Attendees", delta_type="neutral", tooltip_bench="Benchmark: 55%–65%")
    with e3:
        render_tabler_kpi(value=f"{(multi_pillar/n_filtered*100):.1f}%", label="2+ CASE Modes", delta="43.7% Giving Rate", delta_type="up", tooltip_bench="Lift Law: 2+ modes 9x higher giving")
    with e4:
        render_tabler_kpi(value=f"{(volunteers/n_filtered*100):.1f}%", label="Active Volunteers", delta=f"{volunteers:,} Leaders", delta_type="up", tooltip_bench="Target: 4%–7%")
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    c_e1, c_e2 = st.columns(2)
    with c_e1:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">CASE Engagement Modes vs. Giving Rate (%)</span></div>', unsafe_allow_html=True)
        aem_df = filtered_df.groupby('CASE_Pillar_Count').agg(
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Total=('Constituent_ID', 'count')
        ).reset_index()
        aem_df['Giving_Rate'] = aem_df['Donors'] / aem_df['Total'] * 100
        fig_lift = px.bar(aem_df, x='CASE_Pillar_Count', y='Giving_Rate', color='CASE_Pillar_Count', color_continuous_scale='Blues', text=aem_df['Giving_Rate'].apply(lambda x: f"{x:.1f}%"))
        fig_lift.update_traces(textposition='outside')
        apply_tabler_theme(fig_lift, height=270)
        fig_lift.update_layout(coloraxis_showscale=False, yaxis=dict(title='Giving Rate (%)'))
        st.plotly_chart(fig_lift, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_e2:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Homecoming Milestone Spikes</span></div>', unsafe_allow_html=True)
        years = filtered_df.groupby('Years_Since_Grad')['Attended_Homecoming_FY26'].mean().reset_index()
        years['Rate'] = years['Attended_Homecoming_FY26'] * 100
        fig_home = px.line(years, x='Years_Since_Grad', y='Rate', markers=True)
        fig_home.update_traces(line=dict(color='#ED1B2F', width=2), marker=dict(size=4))
        apply_tabler_theme(fig_home, height=270)
        fig_home.update_layout(yaxis=dict(title='Homecoming Rate (%)'))
        st.plotly_chart(fig_home, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# VIEW 6: PROSPECT CAPACITY & FACULTY INTELLIGENCE
# =============================================================================
elif selected_module == "💎 Prospect Capacity & Faculty Intelligence":
    st.markdown("""
    <div class="dashboard-title-row">
        <div>
            <h1 class="dashboard-title">Prospect Capacity & Faculty Intelligence</h1>
            <p class="dashboard-subtitle">Wealth screening realization, major gift potential, and faculty benchmarking.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    t1_t2_rev = filtered_df[filtered_df['Wealth_Screening_Rating'].isin(['Tier 1: $100k+', 'Tier 2: $25k-$99k'])]['Giving_Amount_FY26'].sum()
    t1_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 1: $100k+']
    t1_conv = ((t1_df['Gift_Count_FY26'] > 0).sum() / len(t1_df) * 100) if len(t1_df) > 0 else 0.0
    t2_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 2: $25k-$99k']
    t2_conv = ((t2_df['Gift_Count_FY26'] > 0).sum() / len(t2_df) * 100) if len(t2_df) > 0 else 0.0
    
    w1, w2, w3 = st.columns(3)
    with w1:
        render_tabler_kpi(value=f"${t1_t2_rev/1e6:.2f}M", label="Top Tier Giving", delta=f"{(t1_t2_rev/tot_rev_fy26*100):.1f}% Total Funds", delta_type="up", tooltip_bench="Tiers 1 & 2 generate > 68% of commitments")
    with w2:
        render_tabler_kpi(value=f"{t1_conv:.1f}%", label="Tier 1 ($100k+) Conv", delta=f"{len(t1_df):,} Prospects", delta_type="up", tooltip_bench="Target: > 60% participation")
    with w3:
        render_tabler_kpi(value=f"{t2_conv:.1f}%", label="Tier 2 ($25k-$99k) Conv", delta=f"{len(t2_df):,} Prospects", delta_type="up", tooltip_bench="Target: > 45% participation")
        
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
    c_f1, c_f2 = st.columns([1.1, 0.9])
    with c_f1:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Faculty Commitments ($ CAD)</span></div>', unsafe_allow_html=True)
        fac_league = filtered_df.groupby('Primary_Faculty')['Giving_Amount_FY26'].sum().reset_index().sort_values(by='Giving_Amount_FY26', ascending=True)
        fig_fl = px.bar(fac_league, x='Giving_Amount_FY26', y='Primary_Faculty', orientation='h', color='Giving_Amount_FY26', color_continuous_scale='Blues')
        apply_tabler_theme(fig_fl, height=310)
        fig_fl.update_layout(coloraxis_showscale=False, yaxis=dict(title=''))
        st.plotly_chart(fig_fl, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with c_f2:
        st.markdown('<div class="tabler-visual-card"><div class="tabler-visual-header"><span class="tabler-visual-title">Wealth Screening Matrix</span></div>', unsafe_allow_html=True)
        w_matrix = filtered_df.groupby('Wealth_Screening_Rating').agg(
            Alumni=('Constituent_ID', 'count'),
            Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
            Raised=('Giving_Amount_FY26', 'sum')
        ).reset_index()
        w_matrix['Part %'] = (w_matrix['Donors'] / w_matrix['Alumni'] * 100).apply(lambda x: f"{x:.1f}%")
        w_matrix['Raised'] = w_matrix['Raised'].apply(lambda x: f"${x/1e3:,.0f}k")
        st.dataframe(w_matrix[['Wealth_Screening_Rating', 'Alumni', 'Part %', 'Raised']], hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# =============================================================================
# 7. MINIMAL FOOTER
# =============================================================================
st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 11px; padding: 24px 0 12px 0;">
    McDill University Advancement Analytics • Lean Executive Dashboard • FY2026 Reporting Year
</div>
""", unsafe_allow_html=True)
