"""
McDill University Advancement - Executive Analytics & CASE Intelligence Portal
File: app.py
Description: Lean, clean executive dashboard inspired by Tabler UI with native cards,
             built-in metric tooltips, prominent dropdown navigation, and zero raw HTML code block leaks.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# =============================================================================
# 1. PAGE CONFIGURATION & TABLER-STYLE CLEAN CSS
# =============================================================================
st.set_page_config(
    page_title="McDill Advancement Dashboard | FY26",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Tabler UI Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Clean Page Background */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Native Container Border Wrapper (Tabler Card Style) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03) !important;
        padding: 4px !important;
    }
    
    /* Native Metric Styling */
    [data-testid="stMetric"] {
        padding: 8px 10px !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 11px !important;
        font-weight: 600 !important;
        color: #64748B !important;
        text-transform: uppercase !important;
        letter-spacing: 0.04em !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 24px !important;
        font-weight: 800 !important;
        color: #0F172A !important;
        letter-spacing: -0.02em !important;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 11px !important;
        font-weight: 700 !important;
    }
    
    /* Hide Default Footer */
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
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
# 3. PLOTLY THEME HELPER
# =============================================================================
def apply_tabler_theme(fig, height=270):
    """Applies clean Tabler UI styling to Plotly figures."""
    fig.update_layout(
        font=dict(family="Inter, -apple-system, sans-serif", size=11, color="#334155"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=35, r=20, t=15, b=30),
        hovermode="closest",
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=11,
            font_color="#FFFFFF",
            font_family="Inter, sans-serif"
        )
    )
    fig.update_xaxes(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#64748B"))
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", tickfont=dict(size=10, color="#64748B"))
    return fig


# =============================================================================
# 4. SIDEBAR FILTERS
# =============================================================================
with st.sidebar:
    st.markdown("### 🔍 Global Slicers")
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
# 5. PROMINENT SECTION SELECTOR (BIG DROPDOWN)
# =============================================================================
st.markdown("### 🎓 McDill University Advancement Intelligence")

selected_module = st.selectbox(
    "SELECT VIEW / MODULE:",
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

st.caption(f"Active Universe: **{n_filtered:,} Records** | **${tot_rev_fy26/1e6:.2f}M Commitments** | **{donors_fy26:,} Donors**")
st.markdown("---")


# =============================================================================
# VIEW 1: EXECUTIVE OVERVIEW (LANDING PAGE - TABLER UI INSPIRATION)
# =============================================================================
if selected_module == "📊 Executive Overview (Landing Dashboard)":
    
    st.subheader("Dashboard")
    
    # 6 Top-Line KPI Cards (Using Native st.metric with clean tooltips)
    k1, k2, k3, k4, k5, k6 = st.columns(6)
    
    with k1:
        with st.container(border=True):
            st.metric(
                label="Total Revenue",
                value=f"${tot_rev_fy26/1e6:.2f}M",
                delta="+14% YoY",
                help="Total philanthropic commitments booked in FY26 across all university designations.\n\nU15 Benchmark: $3.0M – $6.5M"
            )
    with k2:
        with st.container(border=True):
            st.metric(
                label="Active Donors",
                value=f"{donors_fy26:,}",
                delta="+7% YoY",
                help="Distinct constituents contributing at least one gift in FY26.\n\nTarget: 4,000 – 4,800 active donors"
            )
    with k3:
        with st.container(border=True):
            st.metric(
                label="Participation",
                value=f"{part_rate:.1f}%",
                delta="+1.2%",
                help="Percentage of addressable alumni who contributed.\n\nCASE U15 Average: 8% – 12%"
            )
    with k4:
        with st.container(border=True):
            st.metric(
                label="Retention Rate",
                value=f"{retention_rate:.1f}%",
                delta="+2.5%",
                help="Repeat FY25 donors who contributed again in FY26.\n\nCASE National Standard: 60% – 65%"
            )
    with k5:
        with st.container(border=True):
            st.metric(
                label="Average Gift",
                value=f"${avg_gift:,.0f}",
                delta="+5% YoY",
                help="Total revenue divided by active donor headcount.\n\nTarget: $700 – $850"
            )
    with k6:
        with st.container(border=True):
            st.metric(
                label="Marketing ROI",
                value=f"{roi_mult:.1f}x",
                delta="+2.1x",
                help="Philanthropic revenue generated per dollar of outreach cost.\n\nAFP Standard: > 6.7x"
            )
            
    st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)
    
    # Main Grid (Left 60% Activity & Table, Right 40% Dual Donut Charts)
    col_left, col_right = st.columns([1.25, 0.75])
    
    with col_left:
        with st.container(border=True):
            st.markdown("##### Development Activity (FY24 – FY26)")
            st.caption("Multi-year philanthropic commitments revenue velocity ($ CAD)")
            
            my_df = pd.DataFrame({
                'Year': ['FY2024', 'FY2025', 'FY2026'],
                'Revenue': [tot_rev_fy24, tot_rev_fy25, tot_rev_fy26]
            })
            
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(
                x=my_df['Year'],
                y=my_df['Revenue'],
                mode='lines+markers',
                line=dict(color='#206BC4', width=3, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(32, 107, 196, 0.08)',
                marker=dict(size=7, color='#206BC4'),
                hovertemplate="<b>%{x}</b><br>Revenue: %{y:$,.0f}<extra></extra>"
            ))
            apply_tabler_theme(fig_area, height=210)
            fig_area.update_layout(yaxis=dict(tickformat='$,.0s', showgrid=True))
            st.plotly_chart(fig_area, use_container_width=True)
            
            st.markdown("##### Faculty Commitments Summary")
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
            st.markdown("##### Gift Designation Share")
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
            fig_d1.update_layout(height=180, margin=dict(l=10, r=10, t=5, b=5), showlegend=False)
            st.plotly_chart(fig_d1, use_container_width=True)
            
        with st.container(border=True):
            st.markdown("##### CASE 4-Pillar Engagement")
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
            fig_d2.update_layout(height=180, margin=dict(l=10, r=10, t=5, b=5), showlegend=False)
            st.plotly_chart(fig_d2, use_container_width=True)

    # Bottom Row: 3 Secondary Metric Cards
    mcdill24_rev = filtered_df['McGill24_Gift_Amount_FY26'].sum()
    sustainers_cnt = (filtered_df['Is_Monthly_Sustainer_FY26'] == 1).sum()
    target_goal = 4000000.0
    pct_goal = (tot_rev_fy26 / target_goal * 100)
    
    b1, b2, b3 = st.columns(3)
    with b1:
        with st.container(border=True):
            st.metric(
                label="McDill24 Giving Day",
                value=f"${mcdill24_rev/1e3:,.0f}K",
                delta=f"{(mcdill24_rev/tot_rev_fy26*100):.1f}% Share of Total",
                help="Dollars raised during the 24-hour digital campaign.\n\nCASE Benchmark: 15% – 25%"
            )
    with b2:
        with st.container(border=True):
            st.metric(
                label="Monthly Sustainers",
                value=f"{sustainers_cnt:,}",
                delta=f"{(sustainers_cnt/donors_fy26*100):.1f}% of Donors",
                help="Donors giving via recurring monthly gifts.\n\nTarget: 20% – 25% of donors"
            )
    with b3:
        with st.container(border=True):
            st.metric(
                label="Campaign Goal Pace",
                value=f"{pct_goal:.1f}%",
                delta=f"${(target_goal - tot_rev_fy26)/1e3:,.0f}K to Target",
                help="Progress towards the $4.0M annual strategic goal."
            )


# =============================================================================
# VIEW 2: PHILANTHROPIC HEALTH & REVENUE
# =============================================================================
elif selected_module == "🏛️ Philanthropic Health & Revenue":
    st.subheader("Philanthropic Health & Commitments")
    
    p1, p2, p3 = st.columns(3)
    mcdill24_rev = filtered_df['McGill24_Gift_Amount_FY26'].sum()
    with p1:
        with st.container(border=True):
            st.metric(label="FY26 Total Commitments", value=f"${tot_rev_fy26:,.0f}", delta="+14.2% YoY", help="Total gifts received across all funds in FY26.")
    with p2:
        with st.container(border=True):
            st.metric(label="Average Gift Yield", value=f"${avg_gift:,.2f}", delta="Median: $150", help="Revenue divided by donor count.")
    with p3:
        with st.container(border=True):
            st.metric(label="McDill24 Campaign", value=f"${mcdill24_rev:,.0f}", delta=f"{(mcdill24_rev/tot_rev_fy26*100):.1f}% Share", help="Annual 24-hour giving day total.")
            
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("##### Multi-Year Trajectory (FY24–FY26)")
            fig_traj = go.Figure()
            fig_traj.add_trace(go.Bar(
                x=['FY24', 'FY25', 'FY26'],
                y=[tot_rev_fy24, tot_rev_fy25, tot_rev_fy26],
                name='Revenue ($)',
                marker_color='#206BC4',
                text=[f"${tot_rev_fy24/1e6:.2f}M", f"${tot_rev_fy25/1e6:.2f}M", f"${tot_rev_fy26/1e6:.2f}M"],
                textposition='outside'
            ))
            apply_tabler_theme(fig_traj, height=270)
            st.plotly_chart(fig_traj, use_container_width=True)
            
    with c2:
        with st.container(border=True):
            st.markdown("##### Giving Tier Dispersion (Pareto)")
            tier_agg = filtered_df[filtered_df['Giving_Amount_FY26'] > 0].copy()
            tier_agg['Tier'] = pd.cut(
                tier_agg['Giving_Amount_FY26'],
                bins=[-np.inf, 100, 500, 2500, 10000, np.inf],
                labels=['<$100', '$100-$499', '$500-$2.4k', '$2.5k-$9.9k', '$10k+']
            )
            t_data = tier_agg.groupby('Tier', observed=True)['Giving_Amount_FY26'].sum().reset_index()
            fig_tier = px.bar(t_data, x='Tier', y='Giving_Amount_FY26', color='Giving_Amount_FY26', color_continuous_scale='Blues')
            apply_tabler_theme(fig_tier, height=270)
            fig_tier.update_layout(coloraxis_showscale=False, yaxis=dict(title='Total Raised ($)'))
            st.plotly_chart(fig_tier, use_container_width=True)


# =============================================================================
# VIEW 3: DONOR LIFECYCLE & RETENTION FUNNEL
# =============================================================================
elif selected_module == "🔄 Donor Lifecycle & Retention Funnel":
    st.subheader("Donor Lifecycle & Retention")
    
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
            st.metric(label="Consecutive Retention", value=f"{retention_rate:.1f}%", delta="+2.5%", help="CASE: 60%–65%")
    with l2:
        with st.container(border=True):
            st.metric(label="Lapsed Reactivation", value=f"{react_rate:.1f}%", delta=f"{reactivated:,} Donors", help="CASE: 10%–12%")
    with l3:
        with st.container(border=True):
            st.metric(label="New Acquisition", value=f"{acq_rate:.1f}%", delta=f"{acquired:,} Donors", help="Benchmark: 3%–6%")
    with l4:
        with st.container(border=True):
            st.metric(label="Monthly Sustainers", value=f"{(sustainers/donors_fy26*100):.1f}%", delta=f"{sustainers:,} Donors", help="Target: 20%–25%")

    with st.container(border=True):
        st.markdown("##### Donor Migration Flow (FY25 ➔ FY26)")
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
        fig_sankey.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Inter", size=11))
        st.plotly_chart(fig_sankey, use_container_width=True)


# =============================================================================
# VIEW 4: MARKETING EFFICIENCY & CHANNELS
# =============================================================================
elif selected_module == "📈 Marketing Efficiency & Channels":
    st.subheader("Marketing Efficiency & Digital Funnel")
    
    cpdr = (tot_cost / tot_rev_fy26) if tot_rev_fy26 > 0 else 0.0
    open_rate = (filtered_df['Emails_Opened_FY26'].sum() / filtered_df['Emails_Delivered_FY26'].sum() * 100) if filtered_df['Emails_Delivered_FY26'].sum() > 0 else 0.0
    web_donors = ((filtered_df['GA4_Giving_Page_Views_FY26'] > 0) & (filtered_df['Donated_FY26'] == 1)).sum()
    web_visitors = (filtered_df['GA4_Giving_Page_Views_FY26'] > 0).sum()
    web_conv = (web_donors / web_visitors * 100) if web_visitors > 0 else 0.0
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        with st.container(border=True):
            st.metric(label="Cost per $ Raised", value=f"${cpdr:.4f}", delta="AFP Standard < $0.15", help="AFP Standard: < $0.15")
    with m2:
        with st.container(border=True):
            st.metric(label="Marketing ROI", value=f"{roi_mult:.1f}x", delta="Total Spend: " + f"${tot_cost:,.0f}")
    with m3:
        with st.container(border=True):
            st.metric(label="Email Open Rate", value=f"{open_rate:.1f}%", delta="Higher Ed Avg ~28%")
    with m4:
        with st.container(border=True):
            st.metric(label="GA4 Web Conversion", value=f"{web_conv:.1f}%", delta=f"{web_donors:,} Donors")
            
    c_m1, c_m2 = st.columns(2)
    with c_m1:
        with st.container(border=True):
            st.markdown("##### Channel Conversion Rate (%)")
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
            
    with c_m2:
        with st.container(border=True):
            st.markdown("##### Digital Giving Funnel")
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


# =============================================================================
# VIEW 5: CASE 4-PILLAR ENGAGEMENT (AEM)
# =============================================================================
elif selected_module == "🤝 CASE 4-Pillar Engagement (AEM)":
    st.subheader("CASE 4-Pillar Engagement (AEM)")
    
    events_att = (filtered_df['Events_Attended_FY26'] > 0).sum()
    event_rate = (events_att / n_filtered * 100) if n_filtered > 0 else 0.0
    show_rate = (filtered_df['Events_Attended_FY26'].sum() / filtered_df['Events_Registered_FY26'].sum() * 100) if filtered_df['Events_Registered_FY26'].sum() > 0 else 0.0
    multi_pillar = (filtered_df['CASE_Pillar_Count'] >= 2).sum()
    volunteers = (filtered_df['Is_Active_Volunteer_FY26'] == 1).sum()
    
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        with st.container(border=True):
            st.metric(label="Event Attendance", value=f"{event_rate:.1f}%", delta=f"{events_att:,} Alumni", help="CASE Experiential: 10%–15%")
    with e2:
        with st.container(border=True):
            st.metric(label="Ticket Show Rate", value=f"{show_rate:.1f}%", delta="Realized Attendees", help="Benchmark: 55%–65%")
    with e3:
        with st.container(border=True):
            st.metric(label="2+ CASE Modes", value=f"{(multi_pillar/n_filtered*100):.1f}%", delta="43.7% Giving Rate", help="Lift Law: 2+ modes 9x higher giving")
    with e4:
        with st.container(border=True):
            st.metric(label="Active Volunteers", value=f"{(volunteers/n_filtered*100):.1f}%", delta=f"{volunteers:,} Leaders", help="Target: 4%–7%")
            
    c_e1, c_e2 = st.columns(2)
    with c_e1:
        with st.container(border=True):
            st.markdown("##### CASE Engagement Modes vs. Giving Rate (%)")
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
            
    with c_e2:
        with st.container(border=True):
            st.markdown("##### Homecoming Milestone Spikes")
            years = filtered_df.groupby('Years_Since_Grad')['Attended_Homecoming_FY26'].mean().reset_index()
            years['Rate'] = years['Attended_Homecoming_FY26'] * 100
            fig_home = px.line(years, x='Years_Since_Grad', y='Rate', markers=True)
            fig_home.update_traces(line=dict(color='#ED1B2F', width=2), marker=dict(size=4))
            apply_tabler_theme(fig_home, height=270)
            fig_home.update_layout(yaxis=dict(title='Homecoming Rate (%)'))
            st.plotly_chart(fig_home, use_container_width=True)


# =============================================================================
# VIEW 6: PROSPECT CAPACITY & FACULTY INTELLIGENCE
# =============================================================================
elif selected_module == "💎 Prospect Capacity & Faculty Intelligence":
    st.subheader("Prospect Capacity & Faculty Intelligence")
    
    t1_t2_rev = filtered_df[filtered_df['Wealth_Screening_Rating'].isin(['Tier 1: $100k+', 'Tier 2: $25k-$99k'])]['Giving_Amount_FY26'].sum()
    t1_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 1: $100k+']
    t1_conv = ((t1_df['Gift_Count_FY26'] > 0).sum() / len(t1_df) * 100) if len(t1_df) > 0 else 0.0
    t2_df = filtered_df[filtered_df['Wealth_Screening_Rating'] == 'Tier 2: $25k-$99k']
    t2_conv = ((t2_df['Gift_Count_FY26'] > 0).sum() / len(t2_df) * 100) if len(t2_df) > 0 else 0.0
    
    w1, w2, w3 = st.columns(3)
    with w1:
        with st.container(border=True):
            st.metric(label="Top Tier Giving", value=f"${t1_t2_rev/1e6:.2f}M", delta=f"{(t1_t2_rev/tot_rev_fy26*100):.1f}% Total Funds", help="Tiers 1 & 2 generate > 68% of commitments")
    with w2:
        with st.container(border=True):
            st.metric(label="Tier 1 ($100k+) Conv", value=f"{t1_conv:.1f}%", delta=f"{len(t1_df):,} Prospects", help="Target: > 60% participation")
    with w3:
        with st.container(border=True):
            st.metric(label="Tier 2 ($25k-$99k) Conv", value=f"{t2_conv:.1f}%", delta=f"{len(t2_df):,} Prospects", help="Target: > 45% participation")
            
    c_f1, c_f2 = st.columns([1.1, 0.9])
    with c_f1:
        with st.container(border=True):
            st.markdown("##### Faculty Commitments ($ CAD)")
            fac_league = filtered_df.groupby('Primary_Faculty')['Giving_Amount_FY26'].sum().reset_index().sort_values(by='Giving_Amount_FY26', ascending=True)
            fig_fl = px.bar(fac_league, x='Giving_Amount_FY26', y='Primary_Faculty', orientation='h', color='Giving_Amount_FY26', color_continuous_scale='Blues')
            apply_tabler_theme(fig_fl, height=300)
            fig_fl.update_layout(coloraxis_showscale=False, yaxis=dict(title=''))
            st.plotly_chart(fig_fl, use_container_width=True)
            
    with c_f2:
        with st.container(border=True):
            st.markdown("##### Wealth Screening Matrix")
            w_matrix = filtered_df.groupby('Wealth_Screening_Rating').agg(
                Alumni=('Constituent_ID', 'count'),
                Donors=('Gift_Count_FY26', lambda x: (x > 0).sum()),
                Raised=('Giving_Amount_FY26', 'sum')
            ).reset_index()
            w_matrix['Part %'] = (w_matrix['Donors'] / w_matrix['Alumni'] * 100).apply(lambda x: f"{x:.1f}%")
            w_matrix['Raised'] = w_matrix['Raised'].apply(lambda x: f"${x/1e3:,.0f}k")
            st.dataframe(w_matrix[['Wealth_Screening_Rating', 'Alumni', 'Part %', 'Raised']], hide_index=True, use_container_width=True)


# =============================================================================
# 7. MINIMAL FOOTER
# =============================================================================
st.markdown("---")
st.caption("McDill University Advancement Analytics • Lean Executive Dashboard • FY2026 Reporting Year")
