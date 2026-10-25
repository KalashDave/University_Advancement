"""
McGill University Advancement - Raw CRM Data Generator
Script: generate_raw_crm_data.py
Target Output: mcgill_advancement_raw_crm.csv (30,000 constituent records)

Description:
Simulates a merged raw database extract from Salesforce CRM, Salesforce Marketing Cloud,
Eventbrite/AlumnForce, and Google Analytics 4 (GA4) at the close of Fiscal Year 2026
(McGill Fiscal Year: May 1, 2025 – April 30, 2026; McGill24: March 11, 2026).

Zero summary KPIs or calculated percentage scores are output.
All columns represent realistic raw database fields with natural latent statistical
correlations for downstream feature engineering and predictive modeling.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Set master reproducible seed
np.random.seed(42)

def generate_mcgill_advancement_data(n_records: int = 30000) -> pd.DataFrame:
    """
    Generates a realistic raw constituent extract of 30,000 alumni records.
    """
    print(f"Starting constituent generation for N={n_records:,} records...")

    # =========================================================================
    # 1. CONSTITUENT DEMOGRAPHICS & EDUCATION (CRM CORE)
    # =========================================================================
    print("1/5 Generating Constituent Demographics & Education...")
    
    # Constituent_ID: Unique 7-digit string ID 'MCG-1000001' to 'MCG-1030000'
    constituent_ids = [f"MCG-{1000001 + i}" for i in range(n_records)]

    # Class_Year: Integer graduation year between 1965 and 2025.
    # Weight slightly toward grads from 1995 to 2025.
    all_years = np.arange(1965, 2026)
    year_weights = np.zeros(len(all_years))
    for i, y in enumerate(all_years):
        if y < 1995:
            year_weights[i] = 1.0 + 1.2 * (y - 1965) / 29.0
        else:
            year_weights[i] = 2.8 + 3.2 * (y - 1995) / 30.0
    year_weights /= year_weights.sum()
    class_year = np.random.choice(all_years, size=n_records, p=year_weights)

    # Primary_Degree_Type: Undergraduate 68%, Masters 22%, PhD 5%, MD/JD 5%
    degree_types_list = ['Undergraduate', 'Masters', 'PhD', 'MD/JD']
    degree_probs = [0.68, 0.22, 0.05, 0.05]
    degree_counts = np.random.multinomial(n_records, degree_probs)
    
    primary_degree_type = []
    for deg, cnt in zip(degree_types_list, degree_counts):
        primary_degree_type.extend([deg] * cnt)
    primary_degree_type = np.random.permutation(np.array(primary_degree_type, dtype=object))

    # Primary_Faculty:
    # Target proportions:
    # Arts 24%, Science 20%, Management 15%, Engineering 14%, Medicine 10%, Education 7%, Law 5%, AES 5%
    # Rule: MD/JD degrees map strictly to Medicine or Law.
    fac_targets = {
        'Faculty of Arts': int(round(n_records * 0.24)),
        'Faculty of Science': int(round(n_records * 0.20)),
        'Desautels Faculty of Management': int(round(n_records * 0.15)),
        'Faculty of Engineering': int(round(n_records * 0.14)),
        'Faculty of Medicine and Health Sciences': int(round(n_records * 0.10)),
        'Faculty of Education': int(round(n_records * 0.07)),
        'Faculty of Law': int(round(n_records * 0.05)),
        'Faculty of Agricultural and Environmental Sciences': int(round(n_records * 0.05))
    }

    primary_faculty = np.empty(n_records, dtype=object)
    mdjd_mask = (primary_degree_type == 'MD/JD')
    n_mdjd = mdjd_mask.sum()

    # Split MD/JD into ~66% Medicine (MD) and ~34% Law (JD)
    n_md = int(round(n_mdjd * 0.66))
    n_jd = n_mdjd - n_md
    mdjd_facs = ['Faculty of Medicine and Health Sciences'] * n_md + ['Faculty of Law'] * n_jd
    np.random.shuffle(mdjd_facs)
    primary_faculty[mdjd_mask] = mdjd_facs

    # Remaining faculty seats for non-MD/JD degrees
    rem_targets = fac_targets.copy()
    rem_targets['Faculty of Medicine and Health Sciences'] -= n_md
    rem_targets['Faculty of Law'] -= n_jd

    non_mdjd_pool = []
    for fac, cnt in rem_targets.items():
        non_mdjd_pool.extend([fac] * cnt)

    non_mdjd_mask = ~mdjd_mask
    n_non_mdjd = non_mdjd_mask.sum()
    if len(non_mdjd_pool) < n_non_mdjd:
        non_mdjd_pool.extend(['Faculty of Arts'] * (n_non_mdjd - len(non_mdjd_pool)))
    elif len(non_mdjd_pool) > n_non_mdjd:
        non_mdjd_pool = non_mdjd_pool[:n_non_mdjd]

    np.random.shuffle(non_mdjd_pool)
    primary_faculty[non_mdjd_mask] = non_mdjd_pool

    # Birth_Year: Class_Year - 22 plus random offset (-2 to +6 years)
    # Higher degrees take longer to complete
    birth_year = np.empty(n_records, dtype=int)
    for i in range(n_records):
        deg = primary_degree_type[i]
        if deg == 'Undergraduate':
            offset = np.random.randint(-2, 3) # -2 to +2
        elif deg == 'Masters':
            offset = np.random.randint(0, 5)   # 0 to +4
        elif deg == 'PhD':
            offset = np.random.randint(2, 7)   # +2 to +6
        else: # MD/JD
            offset = np.random.randint(1, 6)   # +1 to +5
        birth_year[i] = class_year[i] - 22 + offset

    # Gender: 'F' 52%, 'M' 45%, 'X' 1%, None/missing 2%
    gender_choices = ['F', 'M', 'X', None]
    gender_probs = [0.52, 0.45, 0.01, 0.02]
    gender = np.random.choice(gender_choices, size=n_records, p=gender_probs)

    # Country_of_Residence: Canada 67%, US 18%, UK 4%, France 3%, Hong Kong 2%, Other International 6%
    country_choices = ['Canada', 'United States', 'United Kingdom', 'France', 'Hong Kong', 'Other International']
    country_probs = [0.67, 0.18, 0.04, 0.03, 0.02, 0.06]
    country_of_residence = np.random.choice(country_choices, size=n_records, p=country_probs)

    # Province_State:
    # If Canada: QC (65%), ON (22%), BC (8%), AB (5%)
    # If US: NY (30%), CA (25%), MA (16%), IL (10%), DC (10%), TX (9%)
    # If outside North America: None
    province_state = np.empty(n_records, dtype=object)
    canada_mask = (country_of_residence == 'Canada')
    province_state[canada_mask] = np.random.choice(
        ['QC', 'ON', 'BC', 'AB'],
        size=canada_mask.sum(),
        p=[0.65, 0.22, 0.08, 0.05]
    )

    us_mask = (country_of_residence == 'United States')
    province_state[us_mask] = np.random.choice(
        ['NY', 'CA', 'MA', 'IL', 'DC', 'TX'],
        size=us_mask.sum(),
        p=[0.30, 0.25, 0.16, 0.10, 0.10, 0.09]
    )
    province_state[~canada_mask & ~us_mask] = None

    # Preferred_Language: 'EN' 78%, 'FR' 22%, with higher 'FR' weight when Province_State == 'QC'
    preferred_language = np.empty(n_records, dtype=object)
    qc_mask = (province_state == 'QC')
    france_mask = (country_of_residence == 'France')
    other_geo_mask = (~qc_mask) & (~france_mask)

    # Calibrated so overall population FR rate is ~22%
    preferred_language[qc_mask] = np.random.choice(['FR', 'EN'], size=qc_mask.sum(), p=[0.35, 0.65])
    preferred_language[france_mask] = np.random.choice(['FR', 'EN'], size=france_mask.sum(), p=[0.85, 0.15])
    preferred_language[other_geo_mask] = np.random.choice(['FR', 'EN'], size=other_geo_mask.sum(), p=[0.08, 0.92])

    # Wealth_Screening_Rating:
    # Tier 1: $100k+ (1%), Tier 2: $25k-$99k (4%), Tier 3: $5k-$24k (12%),
    # Tier 4: $1k-$4.9k (28%), Tier 5: Under $1k (40%), Unrated (15%)
    # Correlate higher tiers with older grads and Management/Medicine/Law/Engineering.
    fac_wealth_weights = {
        'Faculty of Medicine and Health Sciences': 1.85,
        'Faculty of Law': 1.75,
        'Desautels Faculty of Management': 1.65,
        'Faculty of Engineering': 1.35,
        'Faculty of Science': 1.00,
        'Faculty of Arts': 0.88,
        'Faculty of Agricultural and Environmental Sciences': 0.85,
        'Faculty of Education': 0.80
    }
    fac_w_arr = np.array([fac_wealth_weights[f] for f in primary_faculty])
    years_since_grad = 2026 - class_year
    age_factor = years_since_grad / 60.0

    # Young grads have higher unrated probability in prospect research
    p_unrated_raw = 0.04 + 0.23 * ((class_year - 1965) / 60.0) ** 1.6
    p_unrated_raw = p_unrated_raw * (0.15 / p_unrated_raw.mean())
    p_unrated = np.clip(p_unrated_raw, 0.02, 0.45)
    unrated_mask = np.random.rand(n_records) < p_unrated

    # Ensure exactly 15% (4,500) unrated
    n_target_unrated = int(round(n_records * 0.15))
    current_unrated = unrated_mask.sum()
    if current_unrated < n_target_unrated:
        candidates = np.where(~unrated_mask)[0]
        p_c = p_unrated[candidates] / p_unrated[candidates].sum()
        add_idx = np.random.choice(candidates, size=n_target_unrated - current_unrated, replace=False, p=p_c)
        unrated_mask[add_idx] = True
    elif current_unrated > n_target_unrated:
        candidates = np.where(unrated_mask)[0]
        p_c = (1.0 - p_unrated[candidates]) / (1.0 - p_unrated[candidates]).sum()
        rem_idx = np.random.choice(candidates, size=current_unrated - n_target_unrated, replace=False, p=p_c)
        unrated_mask[rem_idx] = False

    # Score among rated constituents
    latent_wealth_score = 0.42 * age_factor + 0.38 * (fac_w_arr / 1.85) + 0.20 * np.random.normal(0, 0.15, size=n_records)
    rated_indices = np.where(~unrated_mask)[0]
    sorted_rated = rated_indices[np.argsort(-latent_wealth_score[rated_indices])]

    wealth_screening_rating = np.empty(n_records, dtype=object)
    wealth_screening_rating[unrated_mask] = 'Unrated'

    # Exactly 1% (300), 4% (1200), 12% (3600), 28% (8400), 40% (12000)
    wealth_screening_rating[sorted_rated[:300]] = 'Tier 1: $100k+'
    wealth_screening_rating[sorted_rated[300:1500]] = 'Tier 2: $25k-$99k'
    wealth_screening_rating[sorted_rated[1500:5100]] = 'Tier 3: $5k-$24k'
    wealth_screening_rating[sorted_rated[5100:13500]] = 'Tier 4: $1k-$4.9k'
    wealth_screening_rating[sorted_rated[13500:]] = 'Tier 5: Under $1k'

    # =========================================================================
    # 2. DIGITAL & MARKETING CLOUD RAW LOGS (FY26)
    # =========================================================================
    print("2/5 Generating Digital & Marketing Cloud Logs (FY26)...")

    # Has_Valid_Email: Binary integer (1 for 92%, 0 for 8%)
    # Older grads slightly more likely to have bounced email
    p_valid_email = 0.94 - 0.05 * (years_since_grad / 60.0)
    p_valid_email = p_valid_email * (0.92 / p_valid_email.mean())
    has_valid_email = (np.random.rand(n_records) < p_valid_email).astype(int)

    # Email_Opt_Out_Flag: Binary integer.
    # If Has_Valid_Email == 0, set to 1. Otherwise ~14% opted out.
    email_opt_out_flag = np.zeros(n_records, dtype=int)
    email_opt_out_flag[has_valid_email == 0] = 1
    valid_email_mask = (has_valid_email == 1)
    email_opt_out_flag[valid_email_mask] = (np.random.rand(valid_email_mask.sum()) < 0.14).astype(int)

    # Emails_Delivered_FY26: Integer. Must be 0 if Has_Valid_Email == 0 or Email_Opt_Out_Flag == 1.
    # Otherwise integer between 8 and 32.
    can_deliver_email = (has_valid_email == 1) & (email_opt_out_flag == 0)
    emails_delivered = np.zeros(n_records, dtype=int)
    emails_delivered[can_deliver_email] = np.clip(
        np.round(np.random.normal(20.0, 5.0, size=can_deliver_email.sum())).astype(int),
        8, 32
    )

    # Latent digital engagement factor for correlated activity
    base_digital_affinity = np.random.beta(2.5, 4.0, size=n_records)

    # Emails_Opened_FY26: Integer between 0 and Emails_Delivered_FY26.
    # Beta-Binomial draw so average open rates hover around 28%, higher for engaged alumni.
    p_open_individual = np.clip(
        base_digital_affinity * 0.40 + np.random.beta(2.2, 5.5, size=n_records) * 0.25,
        0.02, 0.85
    )
    # Calibrate mean to ~28%
    p_open_individual = p_open_individual * (0.28 / p_open_individual.mean())
    p_open_individual = np.clip(p_open_individual, 0.01, 0.95)

    emails_opened = np.zeros(n_records, dtype=int)
    emails_opened[can_deliver_email] = np.random.binomial(
        emails_delivered[can_deliver_email],
        p_open_individual[can_deliver_email]
    )

    # Emails_Clicked_FY26: Integer between 0 and Emails_Opened_FY26 (typically 0 to 40% of opened).
    emails_clicked = np.zeros(n_records, dtype=int)
    has_opened_mask = (emails_opened > 0)
    p_click_individual = np.clip(
        np.random.beta(1.8, 8.0, size=has_opened_mask.sum()) * 0.40,
        0.0, 0.40
    )
    emails_clicked[has_opened_mask] = np.random.binomial(
        emails_opened[has_opened_mask],
        p_click_individual
    )

    # GA4_Giving_Page_Views_FY26: Integer (0 to 18) tracking web sessions. Strongly correlated with Emails_Clicked_FY26.
    ga4_page_views = np.zeros(n_records, dtype=int)
    clicked_mask = (emails_clicked > 0)
    # Clicks trigger web sessions
    ga4_page_views[clicked_mask] = np.clip(
        np.random.poisson(1.0 + 1.25 * emails_clicked[clicked_mask]),
        0, 18
    )
    # Small fraction of non-clickers visit giving site directly (organic / social traffic)
    non_clicked_traffic = (~clicked_mask) & (np.random.rand(n_records) < 0.055)
    ga4_page_views[non_clicked_traffic] = np.random.choice([1, 2, 3], size=non_clicked_traffic.sum(), p=[0.75, 0.20, 0.05])

    # McGill_Connect_Registered: Binary (1 or 0). ~18% registered (skewed toward alumni graduating after 2005).
    p_connect = np.where(class_year > 2005, 0.27, 0.08)
    p_connect = p_connect * (0.18 / p_connect.mean())
    mcgill_connect_registered = (np.random.rand(n_records) < p_connect).astype(int)

    # McGill_Connect_Logins_FY26: Integer. 0 if McGill_Connect_Registered == 0, otherwise Poisson draw (0 to 25).
    mcgill_connect_logins = np.zeros(n_records, dtype=int)
    connect_mask = (mcgill_connect_registered == 1)
    mcgill_connect_logins[connect_mask] = np.clip(
        np.random.poisson(3.8, size=connect_mask.sum()),
        0, 25
    )

    # =========================================================================
    # 3. EXPERIENTIAL (EVENTS) & VOLUNTEER LOGS
    # =========================================================================
    print("3/5 Generating Experiential Events & Volunteer Logs...")

    # Regional affinity flag
    is_local_geo = np.isin(province_state, ['QC', 'ON', 'NY', 'MA'])

    # Lifetime_Events_Attended: Integer (0 to 45). Higher for older alumni and those living in QC, ON, NY, or MA.
    # Zero-inflated: ~55% zero
    lifetime_events_prob = 0.25 + 0.32 * age_factor + 0.16 * is_local_geo
    has_lifetime_events = np.random.rand(n_records) < lifetime_events_prob
    lifetime_events_attended = np.zeros(n_records, dtype=int)
    event_lambda = (1.5 + 4.5 * age_factor[has_lifetime_events]) * np.where(is_local_geo[has_lifetime_events], 1.7, 0.7)
    lifetime_events_attended[has_lifetime_events] = np.clip(
        1 + np.random.negative_binomial(2, 2.0 / (2.0 + event_lambda)),
        1, 45
    )

    # Events_Registered_FY26: Integer (0 to 6). Around 26% of alumni register for at least 1 event in FY26.
    reg_propensity = 0.10 + 0.14 * is_local_geo + 0.18 * (lifetime_events_attended > 0) + 0.10 * base_digital_affinity
    q_reg = np.quantile(reg_propensity + np.random.normal(0, 0.05, size=n_records), 0.74)
    registered_mask = (reg_propensity + np.random.normal(0, 0.05, size=n_records)) >= q_reg

    events_registered = np.zeros(n_records, dtype=int)
    events_registered[registered_mask] = np.clip(
        1 + np.random.poisson(0.75, size=registered_mask.sum()),
        1, 6
    )

    # Events_Attended_FY26: Integer between 0 and Events_Registered_FY26 (accounting for ~20% no-show drop-off).
    events_attended = np.zeros(n_records, dtype=int)
    events_attended[registered_mask] = np.random.binomial(
        events_registered[registered_mask],
        0.80
    )

    # Attended_Homecoming_FY26: Binary (1 or 0). Can only be 1 if Events_Attended_FY26 >= 1.
    # Higher likelihood if 2026 - Class_Year is a 5-year reunion multiple (5, 10, 15, 20, 25, etc.).
    attended_homecoming = np.zeros(n_records, dtype=int)
    attended_any_mask = (events_attended >= 1)
    is_reunion_year = ((2026 - class_year) % 5 == 0)
    p_homecoming = np.where(is_reunion_year[attended_any_mask], 0.65, 0.20)
    attended_homecoming[attended_any_mask] = np.random.binomial(1, p_homecoming)

    # Is_Active_Volunteer_FY26: Binary (1 or 0). ~5.5% of alumni serve as mentor, board member, class agent, or McGill24 ambassador.
    vol_propensity = 0.02 + 0.06 * (events_attended > 0) + 0.05 * mcgill_connect_registered + 0.03 * is_local_geo
    q_vol = np.quantile(vol_propensity + np.random.normal(0, 0.02, size=n_records), 0.945) # top 5.5%
    is_active_volunteer = (vol_propensity + np.random.normal(0, 0.02, size=n_records) >= q_vol).astype(int)

    # Volunteer_Hours_Logged_FY26: Float. 0.0 if Is_Active_Volunteer_FY26 == 0, otherwise sampled from realistic hours (2.0 to 65.0).
    volunteer_hours_logged = np.zeros(n_records, dtype=float)
    vol_mask = (is_active_volunteer == 1)
    raw_vol_hours = np.random.gamma(shape=3.2, scale=5.2, size=vol_mask.sum()) + 2.0
    volunteer_hours_logged[vol_mask] = np.round(np.clip(raw_vol_hours, 2.0, 65.0), 1)

    # Alumni_Survey_Completed_FY26: Binary (1 or 0). ~11% completed the annual alumni attitude survey.
    survey_propensity = 0.05 + 0.08 * (emails_opened > 0) + 0.07 * (events_attended > 0) + 0.06 * is_active_volunteer
    q_survey = np.quantile(survey_propensity + np.random.normal(0, 0.03, size=n_records), 0.89)
    alumni_survey_completed = (survey_propensity + np.random.normal(0, 0.03, size=n_records) >= q_survey).astype(int)

    # =========================================================================
    # 4. SOLICITATION & CAMPAIGN OUTREACH (FY26)
    # =========================================================================
    print("4/5 Generating Solicitation & Campaign Outreach (FY26)...")

    # Primary_Solicitation_Channel_FY26:
    # Targets: Email_Digital 55%, Direct_Mail_Letter 18%, Phonathon_Student_Caller 12%,
    # Crowdfunding_McGill24 10%, No_Solicitation 5%.
    # Rule: If Email_Opt_Out_Flag == 1, do not assign 'Email_Digital'.
    primary_solicitation_channel = np.empty(n_records, dtype=object)
    opt_out_indices = np.where(email_opt_out_flag == 1)[0]
    opt_in_indices = np.where(email_opt_out_flag == 0)[0]

    # Non-digital channels relative distribution: 18%, 12%, 10%, 5% (sum = 45%)
    non_email_weights = np.array([0.18, 0.12, 0.10, 0.05]) / 0.45
    non_email_channels = ['Direct_Mail_Letter', 'Phonathon_Student_Caller', 'Crowdfunding_McGill24', 'No_Solicitation']

    # Assign non-email channels to all opted out constituents
    primary_solicitation_channel[opt_out_indices] = np.random.choice(
        non_email_channels,
        size=len(opt_out_indices),
        p=non_email_weights
    )

    # Exactly 55% (16,500) assigned to Email_Digital from opted in pool
    n_target_email_digital = int(round(n_records * 0.55))
    email_digital_chosen = np.random.choice(opt_in_indices, size=n_target_email_digital, replace=False)
    primary_solicitation_channel[email_digital_chosen] = 'Email_Digital'

    # Remaining opted in constituents receive other channels
    rem_opt_in = np.setdiff1d(opt_in_indices, email_digital_chosen)
    primary_solicitation_channel[rem_opt_in] = np.random.choice(
        non_email_channels,
        size=len(rem_opt_in),
        p=non_email_weights
    )

    # Direct_Mail_Pieces_Sent_FY26: Integer (0 to 4). Higher for alumni over age 45 and prior donors.
    is_over_45 = (2026 - birth_year) >= 45
    direct_mail_pieces = np.zeros(n_records, dtype=int)
    is_dm_channel = (primary_solicitation_channel == 'Direct_Mail_Letter')

    # If Direct Mail is primary solicitation channel:
    direct_mail_pieces[is_dm_channel] = np.random.choice([1, 2, 3, 4], size=is_dm_channel.sum(), p=[0.25, 0.40, 0.25, 0.10])
    # Other channels: older alumni or prior prospects may receive annual appeal piece
    dm_secondary = (~is_dm_channel) & is_over_45 & (np.random.rand(n_records) < 0.28)
    direct_mail_pieces[dm_secondary] = np.random.choice([1, 2], size=dm_secondary.sum(), p=[0.80, 0.20])

    # Phonathon_Calls_Completed_FY26: Integer (0 to 3).
    phonathon_calls = np.zeros(n_records, dtype=int)
    is_phone_channel = (primary_solicitation_channel == 'Phonathon_Student_Caller')
    phonathon_calls[is_phone_channel] = np.random.choice([1, 2, 3], size=is_phone_channel.sum(), p=[0.45, 0.35, 0.20])
    # Very small random secondary completed calls for others
    phone_secondary = (~is_phone_channel) & (np.random.rand(n_records) < 0.02)
    phonathon_calls[phone_secondary] = 1

    # Marketing_Outreach_Cost_FY26: Float rounded to 2 decimals.
    # $0.08 per email delivered + $3.75 per direct mail piece + $6.50 per phonathon call + $0.50 if GA4 > 0
    marketing_cost = (
        emails_delivered * 0.08 +
        direct_mail_pieces * 3.75 +
        phonathon_calls * 6.50 +
        np.where(ga4_page_views > 0, 0.50, 0.0)
    )
    marketing_outreach_cost = np.round(marketing_cost, 2)

    # =========================================================================
    # 5. MULTI-YEAR PHILANTHROPIC & TRANSACTION HISTORY (CRM GIFT TABLES)
    # =========================================================================
    print("5/5 Modeling Multi-Year Giving History & Latent Propensity...")

    # Numeric score for wealth tier
    wealth_tier_score_map = {
        'Tier 1: $100k+': 3.0,
        'Tier 2: $25k-$99k': 2.2,
        'Tier 3: $5k-$24k': 1.4,
        'Tier 4: $1k-$4.9k': 0.7,
        'Tier 5: Under $1k': 0.0,
        'Unrated': 0.1
    }
    w_num = np.array([wealth_tier_score_map[t] for t in wealth_screening_rating])

    # Latent propensity score for giving
    # Driven by Wealth_Screening_Rating, age, Lifetime_Events_Attended,
    # Events_Attended_FY26, Emails_Clicked_FY26, GA4_Giving_Page_Views_FY26, and Is_Active_Volunteer_FY26
    latent_propensity = (
        0.35 * w_num +
        0.22 * age_factor +
        0.18 * np.log1p(lifetime_events_attended) +
        0.16 * np.log1p(events_attended) +
        0.12 * np.log1p(emails_clicked) +
        0.08 * np.log1p(ga4_page_views) +
        0.25 * is_active_volunteer +
        np.random.normal(0, 0.35, size=n_records)
    )

    # Helper function to sample Pareto gift amounts
    def sample_pareto_gift(wealth_tier: str, gift_count: int) -> float:
        params = {
            'Tier 1: $100k+': (1500.0, 1.15, 25000.0),
            'Tier 2: $25k-$99k': (500.0, 1.25, 25000.0),
            'Tier 3: $5k-$24k': (150.0, 1.35, 12000.0),
            'Tier 4: $1k-$4.9k': (50.0, 1.50, 4500.0),
            'Tier 5: Under $1k': (20.0, 1.80, 950.0),
            'Unrated': (25.0, 1.70, 1500.0)
        }
        x_min, alpha, x_max = params[wealth_tier]
        if gift_count >= 6: # Sustainer
            monthly_options = np.array([5.0, 10.0, 15.0, 20.0, 25.0, 35.0, 50.0, 75.0, 100.0, 150.0, 200.0, 250.0, 500.0])
            if 'Tier 1' in wealth_tier or 'Tier 2' in wealth_tier:
                p_m = (monthly_options >= 50.0)
            elif 'Tier 3' in wealth_tier:
                p_m = (monthly_options >= 20.0) & (monthly_options <= 200.0)
            else:
                p_m = (monthly_options <= 50.0)
            p_weights = p_m.astype(float) / p_m.sum()
            m_amt = np.random.choice(monthly_options, p=p_weights)
            return float(min(max(m_amt * gift_count, 20.0), 25000.0))
        else:
            u = np.random.uniform(0.001, 0.999)
            val = x_min / ((1.0 - u) ** (1.0 / alpha))
            val = min(max(val, 20.0), x_max)
            if gift_count > 1:
                val *= (1.0 + 0.35 * (gift_count - 1))
            return float(min(max(val, 20.0), 25000.0))

    # --- Lifetime_Gift_Count_Prior_To_FY24 & Amount ---
    # ~62% of alumni should have 0 gifts prior to FY24 (38% have >= 1 gifts)
    q_prior = np.quantile(latent_propensity, 0.62)
    prior_donor_mask = (latent_propensity >= q_prior)

    lifetime_gift_count_prior = np.zeros(n_records, dtype=int)
    prior_lambda = 1.2 + 3.8 * age_factor[prior_donor_mask] + 2.8 * w_num[prior_donor_mask]
    counts_prior = 1 + np.random.poisson(prior_lambda)
    lifetime_gift_count_prior[prior_donor_mask] = np.clip(counts_prior, 1, 50)

    tier_base_mean = {
        'Tier 1: $100k+': 8.5,
        'Tier 2: $25k-$99k': 7.5,
        'Tier 3: $5k-$24k': 6.5,
        'Tier 4: $1k-$4.9k': 5.5,
        'Tier 5: Under $1k': 4.5,
        'Unrated': 4.8
    }
    lifetime_giving_amount_prior = np.zeros(n_records, dtype=float)
    for t, mu in tier_base_mean.items():
        t_mask = prior_donor_mask & (wealth_screening_rating == t)
        if t_mask.sum() > 0:
            c = lifetime_gift_count_prior[t_mask]
            amounts = np.exp(np.random.normal(mu, 0.70, size=t_mask.sum())) * np.sqrt(c)
            amounts = np.clip(amounts, 20.0 * c, 250000.0)
            lifetime_giving_amount_prior[t_mask] = np.round(amounts, 2)

    # --- Gift_Count_FY24 & Giving_Amount_FY24 ---
    # ~13% of alumni donate in FY24
    score_fy24 = latent_propensity + 1.25 * prior_donor_mask
    q_fy24 = np.quantile(score_fy24, 0.87)
    donor_fy24_mask = (score_fy24 >= q_fy24)

    gift_count_fy24 = np.zeros(n_records, dtype=int)
    giving_amount_fy24 = np.zeros(n_records, dtype=float)
    fy24_indices = np.where(donor_fy24_mask)[0]

    for idx in fy24_indices:
        # ~20% sustainer in FY24
        is_sust = (np.random.rand() < 0.20)
        c = 12 if is_sust else np.random.choice([1, 2, 3, 4, 5], p=[0.70, 0.18, 0.07, 0.03, 0.02])
        gift_count_fy24[idx] = c
        giving_amount_fy24[idx] = np.round(sample_pareto_gift(wealth_screening_rating[idx], c), 2)

    # --- Gift_Count_FY25 & Giving_Amount_FY25 ---
    # ~62% of FY24 donors donate again in FY25, plus lapsed/first-time donors (~14% overall FY25 donor rate)
    retain_score_fy25 = latent_propensity[donor_fy24_mask] + np.random.normal(0, 0.45, size=donor_fy24_mask.sum())
    q_retain_25 = np.quantile(retain_score_fy25, 0.38) # top 62%
    retained_fy25_idx = fy24_indices[retain_score_fy25 >= q_retain_25]

    n_target_fy25 = int(round(n_records * 0.14)) # 4,200
    n_needed_fy25 = n_target_fy25 - len(retained_fy25_idx)

    non_fy24_mask = ~donor_fy24_mask
    score_non_fy24 = latent_propensity[non_fy24_mask] + 1.1 * prior_donor_mask[non_fy24_mask]
    q_new_fy25 = np.quantile(score_non_fy24, 1.0 - (n_needed_fy25 / non_fy24_mask.sum()))
    new_fy25_idx = np.where(non_fy24_mask)[0][score_non_fy24 >= q_new_fy25]

    donor_fy25_mask = np.zeros(n_records, dtype=bool)
    donor_fy25_mask[retained_fy25_idx] = True
    donor_fy25_mask[new_fy25_idx] = True

    gift_count_fy25 = np.zeros(n_records, dtype=int)
    giving_amount_fy25 = np.zeros(n_records, dtype=float)

    # Retained donors anchored near FY24 giving
    for idx in retained_fy25_idx:
        prev_count = gift_count_fy24[idx]
        prev_amt = giving_amount_fy24[idx]
        is_sust = (prev_count >= 6) if (np.random.rand() < 0.85) else (np.random.rand() < 0.15)
        c = 12 if is_sust else np.random.choice([1, 2, 3, 4, 5], p=[0.70, 0.18, 0.07, 0.03, 0.02])
        gift_count_fy25[idx] = c
        # Anchor near FY24
        amt = prev_amt * np.random.uniform(0.90, 1.15)
        giving_amount_fy25[idx] = np.round(min(max(amt, 20.0), 25000.0), 2)

    # New / reactivated donors in FY25
    for idx in new_fy25_idx:
        is_sust = (np.random.rand() < 0.20)
        c = 12 if is_sust else np.random.choice([1, 2, 3, 4, 5], p=[0.70, 0.18, 0.07, 0.03, 0.02])
        gift_count_fy25[idx] = c
        giving_amount_fy25[idx] = np.round(sample_pareto_gift(wealth_screening_rating[idx], c), 2)

    # --- Gift_Count_FY26 & Giving_Amount_FY26 ---
    # Overall FY26 donor rate: 14-16% (targeting ~15.0%)
    # FY25-to-FY26 retention rate: 60-65% (targeting ~62.5%)
    # Lapsed reactivation rate: 10-12% (targeting ~11.0%)
    fy25_indices = np.where(donor_fy25_mask)[0]
    score_retain_fy26 = (
        latent_propensity[donor_fy25_mask] +
        0.30 * np.log1p(events_attended[donor_fy25_mask]) +
        0.20 * np.log1p(emails_clicked[donor_fy25_mask]) +
        0.15 * np.log1p(ga4_page_views[donor_fy25_mask]) +
        0.25 * is_active_volunteer[donor_fy25_mask] +
        np.random.normal(0, 0.35, size=len(fy25_indices))
    )
    # Retention ~62.5%
    q_retain_26 = np.quantile(score_retain_fy26, 0.375)
    retained_fy26_idx = fy25_indices[score_retain_fy26 >= q_retain_26]

    # Lapsed pool: gave in FY24 or prior, but NOT in FY25
    gave_prior_all = prior_donor_mask | donor_fy24_mask
    lapsed_mask = gave_prior_all & (~donor_fy25_mask)
    lapsed_indices = np.where(lapsed_mask)[0]

    score_lapsed_26 = (
        latent_propensity[lapsed_mask] +
        0.35 * np.log1p(events_attended[lapsed_mask]) +
        0.25 * np.log1p(emails_clicked[lapsed_mask]) +
        0.20 * np.log1p(ga4_page_views[lapsed_mask]) +
        0.25 * is_active_volunteer[lapsed_mask] +
        np.random.normal(0, 0.35, size=len(lapsed_indices))
    )
    # Lapsed reactivation ~11.0%
    q_lapsed_26 = np.quantile(score_lapsed_26, 0.89)
    reactivated_fy26_idx = lapsed_indices[score_lapsed_26 >= q_lapsed_26]

    # First-timers from never-givers
    never_gave_mask = (~gave_prior_all) & (~donor_fy25_mask)
    never_indices = np.where(never_gave_mask)[0]

    n_target_fy26 = int(round(n_records * 0.150)) # 4,500 total
    n_needed_first_timers = n_target_fy26 - len(retained_fy26_idx) - len(reactivated_fy26_idx)

    score_never_26 = (
        latent_propensity[never_gave_mask] +
        0.40 * np.log1p(events_attended[never_gave_mask]) +
        0.30 * np.log1p(emails_clicked[never_gave_mask]) +
        0.20 * np.log1p(ga4_page_views[never_gave_mask]) +
        0.30 * is_active_volunteer[never_gave_mask] +
        np.random.normal(0, 0.35, size=len(never_indices))
    )
    q_never_26 = np.quantile(score_never_26, 1.0 - (n_needed_first_timers / len(never_indices)))
    first_timers_fy26_idx = never_indices[score_never_26 >= q_never_26]

    all_fy26_donor_indices = np.concatenate([retained_fy26_idx, reactivated_fy26_idx, first_timers_fy26_idx])
    donor_fy26_mask = np.zeros(n_records, dtype=bool)
    donor_fy26_mask[all_fy26_donor_indices] = True

    gift_count_fy26 = np.zeros(n_records, dtype=int)
    giving_amount_fy26 = np.zeros(n_records, dtype=float)

    # Sustainer requirement: "around 22-25% of active FY26 donors"
    # Set to 1 if Gift_Count_FY26 >= 6
    n_active_fy26 = len(all_fy26_donor_indices)
    n_target_sustainers = int(round(n_active_fy26 * 0.235)) # ~23.5%
    sustainer_chosen = np.random.choice(all_fy26_donor_indices, size=n_target_sustainers, replace=False)
    sustainer_set = set(sustainer_chosen)

    # Giving_Amount_FY26 for Repeat Donors:
    # ~35% upgrade by 15-60%, ~45% same amount, ~20% slightly less
    retained_set = set(retained_fy26_idx)
    for idx in all_fy26_donor_indices:
        is_sust = (idx in sustainer_set)
        if is_sust:
            c = 12 if (np.random.rand() < 0.82) else np.random.randint(6, 12)
        else:
            c = np.random.choice([1, 2, 3, 4, 5], p=[0.70, 0.19, 0.06, 0.03, 0.02])
        gift_count_fy26[idx] = c

        if idx in retained_set:
            prev_amt = giving_amount_fy25[idx]
            roll = np.random.rand()
            if roll < 0.35: # Upgrade by 15-60%
                amt = prev_amt * np.random.uniform(1.15, 1.60)
            elif roll < 0.80: # Exact same
                amt = prev_amt
            else: # Slightly less (down by 5-30%)
                amt = prev_amt * np.random.uniform(0.70, 0.95)
            giving_amount_fy26[idx] = np.round(min(max(amt, 20.0), 25000.0), 2)
        else:
            giving_amount_fy26[idx] = np.round(sample_pareto_gift(wealth_screening_rating[idx], c), 2)

    # Is_Monthly_Sustainer_FY26: Binary (1 or 0). Set to 1 if Gift_Count_FY26 >= 6
    is_monthly_sustainer_fy26 = (gift_count_fy26 >= 6).astype(int)

    # McGill24_Gift_Amount_FY26: Float. 0.0 if Giving_Amount_FY26 == 0.
    # Around 40% of FY26 donors give part or all of their FY26 gift on McGill24
    # (especially those with high Emails_Clicked_FY26 or GA4_Giving_Page_Views_FY26).
    # Must be less than or equal to Giving_Amount_FY26.
    mcgill24_gift_amount_fy26 = np.zeros(n_records, dtype=float)
    mcgill24_propensity = (
        0.35 * (primary_solicitation_channel[all_fy26_donor_indices] == 'Crowdfunding_McGill24') +
        0.30 * np.log1p(emails_clicked[all_fy26_donor_indices]) +
        0.25 * np.log1p(ga4_page_views[all_fy26_donor_indices]) +
        np.random.normal(0, 0.35, size=n_active_fy26)
    )
    n_target_mcgill24 = int(round(n_active_fy26 * 0.40)) # exactly 40% of active donors
    mcgill24_chosen_idx = all_fy26_donor_indices[np.argsort(-mcgill24_propensity)[:n_target_mcgill24]]

    for idx in mcgill24_chosen_idx:
        tot_giving = giving_amount_fy26[idx]
        c = gift_count_fy26[idx]
        if c == 1:
            # Single gift in FY26: 75% gave entire gift on McGill24, 25% gave portion
            if np.random.rand() < 0.75:
                mcgill24_amt = tot_giving
            else:
                mcgill24_amt = np.round(tot_giving * np.random.uniform(0.50, 0.90), 2)
        else:
            # Multiple gifts: McGill24 is one of their gifts
            mcgill24_amt = np.round(min(tot_giving, max(20.0, tot_giving / c)), 2)
        
        mcgill24_gift_amount_fy26[idx] = min(tot_giving, max(20.0, mcgill24_amt))

    # --- Last_Gift_Date & Last_Gift_Designation ---
    # Helper to generate random dates
    def sample_dates_in_range(start_str: str, end_str: str, size: int) -> list:
        start = datetime.strptime(start_str, "%Y-%m-%d")
        end = datetime.strptime(end_str, "%Y-%m-%d")
        delta = (end - start).days
        offsets = np.random.randint(0, delta + 1, size=size)
        return [(start + timedelta(days=int(d))).strftime("%Y-%m-%d") for d in offsets]

    last_gift_date = np.empty(n_records, dtype=object)
    last_gift_date[:] = None

    # Condition 1: FY26 Donors
    fy26_donor_mask = (giving_amount_fy26 > 0)
    for idx in np.where(fy26_donor_mask)[0]:
        if mcgill24_gift_amount_fy26[idx] > 0 and (np.random.rand() < 0.78):
            # McGill24 2026 was Wednesday, March 11, 2026
            last_gift_date[idx] = "2026-03-11"
        else:
            last_gift_date[idx] = sample_dates_in_range("2025-05-01", "2026-04-30", 1)[0]

    # Condition 2: FY25 Donors (who did not give in FY26)
    fy25_only_mask = (~fy26_donor_mask) & (giving_amount_fy25 > 0)
    n_fy25_only = fy25_only_mask.sum()
    if n_fy25_only > 0:
        last_gift_date[fy25_only_mask] = sample_dates_in_range("2024-05-01", "2025-04-30", n_fy25_only)

    # Condition 3: FY24 Donors (who did not give in FY25 or FY26)
    fy24_only_mask = (~fy26_donor_mask) & (~fy25_only_mask) & (giving_amount_fy24 > 0)
    n_fy24_only = fy24_only_mask.sum()
    if n_fy24_only > 0:
        last_gift_date[fy24_only_mask] = sample_dates_in_range("2023-05-01", "2024-04-30", n_fy24_only)

    # Condition 4: Prior Donors (who did not give in FY24, FY25, or FY26)
    prior_only_mask = (~fy26_donor_mask) & (~fy25_only_mask) & (~fy24_only_mask) & (lifetime_gift_count_prior > 0)
    n_prior_only = prior_only_mask.sum()
    if n_prior_only > 0:
        last_gift_date[prior_only_mask] = sample_dates_in_range("2010-05-01", "2023-04-30", n_prior_only)

    # Non-donors remain None

    # Last_Gift_Designation:
    # The McGill Fund (Unrestricted) 38%, Student Scholarships & Bursaries 26%,
    # Faculty Priority Fund 18%, Research & Discovery 10%, Varsity Athletics 8%
    last_gift_designation = np.empty(n_records, dtype=object)
    last_gift_designation[:] = None

    all_ever_donors_mask = (last_gift_date != None)
    n_ever_donors = all_ever_donors_mask.sum()
    designation_choices = [
        'The McGill Fund (Unrestricted)',
        'Student Scholarships & Bursaries',
        'Faculty Priority Fund',
        'Research & Discovery',
        'Varsity Athletics & Martlets/Redbirds'
    ]
    designation_probs = [0.38, 0.26, 0.18, 0.10, 0.08]
    last_gift_designation[all_ever_donors_mask] = np.random.choice(
        designation_choices,
        size=n_ever_donors,
        p=designation_probs
    )

    # =========================================================================
    # ASSEMBLE DATAFRAME IN STRICT SCHEMA ORDER
    # =========================================================================
    df = pd.DataFrame({
        # 1. Constituent Demographics & Education
        'Constituent_ID': constituent_ids,
        'Class_Year': class_year,
        'Birth_Year': birth_year,
        'Gender': gender,
        'Primary_Degree_Type': primary_degree_type,
        'Primary_Faculty': primary_faculty,
        'Country_of_Residence': country_of_residence,
        'Province_State': province_state,
        'Preferred_Language': preferred_language,
        'Wealth_Screening_Rating': wealth_screening_rating,

        # 2. Digital & Marketing Cloud Logs
        'Has_Valid_Email': has_valid_email,
        'Email_Opt_Out_Flag': email_opt_out_flag,
        'Emails_Delivered_FY26': emails_delivered,
        'Emails_Opened_FY26': emails_opened,
        'Emails_Clicked_FY26': emails_clicked,
        'GA4_Giving_Page_Views_FY26': ga4_page_views,
        'McGill_Connect_Registered': mcgill_connect_registered,
        'McGill_Connect_Logins_FY26': mcgill_connect_logins,

        # 3. Experiential Events & Volunteer Logs
        'Lifetime_Events_Attended': lifetime_events_attended,
        'Events_Registered_FY26': events_registered,
        'Events_Attended_FY26': events_attended,
        'Attended_Homecoming_FY26': attended_homecoming,
        'Is_Active_Volunteer_FY26': is_active_volunteer,
        'Volunteer_Hours_Logged_FY26': volunteer_hours_logged,
        'Alumni_Survey_Completed_FY26': alumni_survey_completed,

        # 4. Solicitation & Campaign Outreach
        'Primary_Solicitation_Channel_FY26': primary_solicitation_channel,
        'Direct_Mail_Pieces_Sent_FY26': direct_mail_pieces,
        'Phonathon_Calls_Completed_FY26': phonathon_calls,
        'Marketing_Outreach_Cost_FY26': marketing_outreach_cost,

        # 5. Multi-Year Philanthropic & Transaction History
        'Lifetime_Gift_Count_Prior_To_FY24': lifetime_gift_count_prior,
        'Lifetime_Giving_Amount_Prior_To_FY24': lifetime_giving_amount_prior,
        'Gift_Count_FY24': gift_count_fy24,
        'Giving_Amount_FY24': giving_amount_fy24,
        'Gift_Count_FY25': gift_count_fy25,
        'Giving_Amount_FY25': giving_amount_fy25,
        'Gift_Count_FY26': gift_count_fy26,
        'Giving_Amount_FY26': giving_amount_fy26,
        'McGill24_Gift_Amount_FY26': mcgill24_gift_amount_fy26,
        'Is_Monthly_Sustainer_FY26': is_monthly_sustainer_fy26,
        'Last_Gift_Date': last_gift_date,
        'Last_Gift_Designation': last_gift_designation
    })

    return df


def validate_data_integrity(df: pd.DataFrame) -> None:
    """
    Enforces strict logical constraints so that zero impossible rows exist.
    """
    print("\n" + "=" * 65)
    print("RUNNING RIGOROUS DATA INTEGRITY & SANITY CHECKS")
    print("=" * 65)

    n = len(df)
    assert n == 30000, f"Expected 30,000 rows, got {n}"
    assert df['Constituent_ID'].nunique() == 30000, "Constituent_ID must be unique"
    assert df['Constituent_ID'].iloc[0] == 'MCG-1000001'
    assert df['Constituent_ID'].iloc[-1] == 'MCG-1030000'
    print("[PASS] Row count and Constituent_ID sequence strictly verified.")

    # Class Year & Birth Year checks
    assert ((df['Class_Year'] >= 1965) & (df['Class_Year'] <= 2025)).all(), "Class_Year out of bounds"
    diff = df['Birth_Year'] - (df['Class_Year'] - 22)
    assert ((diff >= -2) & (diff <= 6)).all(), "Birth_Year offset out of [-2, 6] range"
    print("[PASS] Class_Year and Birth_Year bounds verified.")

    # Degree & Faculty checks
    mdjd_facs = df.loc[df['Primary_Degree_Type'] == 'MD/JD', 'Primary_Faculty'].unique()
    assert set(mdjd_facs).issubset({'Faculty of Medicine and Health Sciences', 'Faculty of Law'}), \
        f"MD/JD mapped to invalid faculty: {mdjd_facs}"
    print("[PASS] MD/JD degrees strictly mapped to Medicine or Law.")

    # Geo null checks
    non_na_countries = ~df['Country_of_Residence'].isin(['Canada', 'United States'])
    assert df.loc[non_na_countries, 'Province_State'].isna().all(), \
        "Province_State must be null outside Canada and US"
    print("[PASS] Geo consistency and Province_State nullability verified.")

    # Email and marketing delivery checks
    no_email = (df['Has_Valid_Email'] == 0)
    assert (df.loc[no_email, 'Email_Opt_Out_Flag'] == 1).all(), \
        "Email_Opt_Out_Flag must be 1 if Has_Valid_Email == 0"
    cannot_deliver = (df['Has_Valid_Email'] == 0) | (df['Email_Opt_Out_Flag'] == 1)
    assert (df.loc[cannot_deliver, 'Emails_Delivered_FY26'] == 0).all(), \
        "Emails_Delivered_FY26 must be 0 when email is invalid or opted out"
    assert ((df['Emails_Opened_FY26'] >= 0) & (df['Emails_Opened_FY26'] <= df['Emails_Delivered_FY26'])).all(), \
        "Emails_Opened_FY26 cannot exceed Emails_Delivered_FY26"
    assert ((df['Emails_Clicked_FY26'] >= 0) & (df['Emails_Clicked_FY26'] <= df['Emails_Opened_FY26'])).all(), \
        "Emails_Clicked_FY26 cannot exceed Emails_Opened_FY26"
    print("[PASS] Email marketing pipeline constraints strictly hold.")

    # GA4 & Connect checks
    assert ((df['GA4_Giving_Page_Views_FY26'] >= 0) & (df['GA4_Giving_Page_Views_FY26'] <= 18)).all()
    no_connect = (df['McGill_Connect_Registered'] == 0)
    assert (df.loc[no_connect, 'McGill_Connect_Logins_FY26'] == 0).all()
    print("[PASS] GA4 page views and McGill Connect login constraints hold.")

    # Events and Volunteer checks
    assert ((df['Events_Attended_FY26'] >= 0) & (df['Events_Attended_FY26'] <= df['Events_Registered_FY26'])).all(), \
        "Events_Attended_FY26 cannot exceed Events_Registered_FY26"
    no_events_attended = (df['Events_Attended_FY26'] == 0)
    assert (df.loc[no_events_attended, 'Attended_Homecoming_FY26'] == 0).all(), \
        "Attended_Homecoming_FY26 can only be 1 if Events_Attended_FY26 >= 1"
    not_vol = (df['Is_Active_Volunteer_FY26'] == 0)
    assert (df.loc[not_vol, 'Volunteer_Hours_Logged_FY26'] == 0.0).all(), \
        "Volunteer_Hours_Logged_FY26 must be 0 for non-volunteers"
    is_vol = (df['Is_Active_Volunteer_FY26'] == 1)
    assert ((df.loc[is_vol, 'Volunteer_Hours_Logged_FY26'] >= 2.0) & (df.loc[is_vol, 'Volunteer_Hours_Logged_FY26'] <= 65.0)).all(), \
        "Volunteer_Hours_Logged_FY26 out of [2.0, 65.0] range"
    print("[PASS] Event attendance, Homecoming, and Volunteer hours verified.")

    # Solicitation channel & Marketing cost checks
    opted_out = (df['Email_Opt_Out_Flag'] == 1)
    assert (df.loc[opted_out, 'Primary_Solicitation_Channel_FY26'] != 'Email_Digital').all(), \
        "Opted-out constituents cannot be assigned Email_Digital"
    
    expected_cost = np.round(
        df['Emails_Delivered_FY26'] * 0.08 +
        df['Direct_Mail_Pieces_Sent_FY26'] * 3.75 +
        df['Phonathon_Calls_Completed_FY26'] * 6.50 +
        np.where(df['GA4_Giving_Page_Views_FY26'] > 0, 0.50, 0.0),
        2
    )
    diff_cost = np.abs(df['Marketing_Outreach_Cost_FY26'] - expected_cost)
    assert (diff_cost < 0.001).all(), "Marketing_Outreach_Cost_FY26 calculation mismatch"
    print("[PASS] Solicitation channels and exact Outreach Cost formula verified.")

    # Multi-Year Giving consistency
    for yr in ['FY24', 'FY25', 'FY26']:
        cnt_col = f'Gift_Count_{yr}'
        amt_col = f'Giving_Amount_{yr}'
        zero_cnt = (df[cnt_col] == 0)
        assert (df.loc[zero_cnt, amt_col] == 0.0).all(), f"{amt_col} must be 0.0 if {cnt_col} == 0"
        pos_cnt = (df[cnt_col] > 0)
        assert (df.loc[pos_cnt, amt_col] >= 20.0).all(), f"{amt_col} must be >= $20 if {cnt_col} > 0"
        assert (df.loc[pos_cnt, amt_col] <= 25000.0).all(), f"{amt_col} exceeds $25,000"

    # Prior giving
    assert (df.loc[df['Lifetime_Gift_Count_Prior_To_FY24'] == 0, 'Lifetime_Giving_Amount_Prior_To_FY24'] == 0.0).all()
    assert (df.loc[df['Lifetime_Gift_Count_Prior_To_FY24'] > 0, 'Lifetime_Giving_Amount_Prior_To_FY24'] > 0.0).all()

    # McGill24 giving
    assert (df['McGill24_Gift_Amount_FY26'] <= df['Giving_Amount_FY26'] + 1e-5).all(), \
        "McGill24_Gift_Amount_FY26 cannot exceed Giving_Amount_FY26"
    assert (df.loc[df['Giving_Amount_FY26'] == 0.0, 'McGill24_Gift_Amount_FY26'] == 0.0).all()

    # Monthly sustainer
    sust_expected = (df['Gift_Count_FY26'] >= 6).astype(int)
    assert (df['Is_Monthly_Sustainer_FY26'] == sust_expected).all(), \
        "Is_Monthly_Sustainer_FY26 must match Gift_Count_FY26 >= 6"

    # Last Gift Date & Designation nullability
    never_gave = (
        (df['Lifetime_Gift_Count_Prior_To_FY24'] == 0) &
        (df['Gift_Count_FY24'] == 0) &
        (df['Gift_Count_FY25'] == 0) &
        (df['Gift_Count_FY26'] == 0)
    )
    assert df.loc[never_gave, 'Last_Gift_Date'].isna().all(), "Non-donors must have null Last_Gift_Date"
    assert df.loc[never_gave, 'Last_Gift_Designation'].isna().all(), "Non-donors must have null Last_Gift_Designation"
    assert df.loc[~never_gave, 'Last_Gift_Date'].notna().all(), "Donors must have valid Last_Gift_Date"
    assert df.loc[~never_gave, 'Last_Gift_Designation'].notna().all(), "Donors must have valid Last_Gift_Designation"
    print("[PASS] Philanthropic consistency, sustaining rules, and donor/non-donor dates verified.")
    print("ALL INTEGRITY CHECKS PASSED PERFECTLY!\n")


def print_schema_summary(df: pd.DataFrame, output_path: str) -> None:
    """
    Prints a clean schema check and summary statistics as required.
    """
    print("=" * 65)
    print("MCGILL UNIVERSITY ADVANCEMENT - CRM RAW EXTRACT SCHEMA CHECK")
    print("=" * 65)
    print(f"File Output Path : {output_path}")
    print(f"Total Rows       : {len(df):,}")
    print(f"Total Columns    : {len(df.columns)}")
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    mem_usage_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    print(f"File Size on Disk: {file_size_mb:.2f} MB")
    print(f"In-Memory Usage  : {mem_usage_mb:.2f} MB")
    print("-" * 65)

    print(f"{'#':<3} {'Column Name':<38} {'Dtype':<10} {'Nulls':<7} {'Null %':<7}")
    print("-" * 65)
    for idx, col in enumerate(df.columns, 1):
        null_count = df[col].isna().sum()
        null_pct = (null_count / len(df)) * 100.0
        dtype_str = str(df[col].dtype)
        print(f"{idx:<3} {col:<38} {dtype_str:<10} {null_count:<7} {null_pct:>5.1f}%")

    print("-" * 65)
    print("KEY ADVANCEMENT BENCHMARKS & CORRELATION AUDIT")
    print("-" * 65)
    print(f"Undergraduate / Graduate Split : {(df['Primary_Degree_Type'] == 'Undergraduate').mean():.1%} Undergrad | {(df['Primary_Degree_Type'] != 'Undergraduate').mean():.1%} Grad")
    print(f"Canada / US / Intl Split       : {(df['Country_of_Residence'] == 'Canada').mean():.1%} CA | {(df['Country_of_Residence'] == 'United States').mean():.1%} US | {(~df['Country_of_Residence'].isin(['Canada', 'United States'])).mean():.1%} Intl")
    print(f"Email Deliverability & Opt-In  : {df['Has_Valid_Email'].mean():.1%} valid email | {(df['Email_Opt_Out_Flag'] == 0).mean():.1%} opted in")
    
    deliv_mask = df['Emails_Delivered_FY26'] > 0
    open_rate = df.loc[deliv_mask, 'Emails_Opened_FY26'].sum() / df.loc[deliv_mask, 'Emails_Delivered_FY26'].sum()
    open_mask = df['Emails_Opened_FY26'] > 0
    click_rate = df.loc[open_mask, 'Emails_Clicked_FY26'].sum() / df.loc[open_mask, 'Emails_Opened_FY26'].sum()
    print(f"Email Open Rate (FY26)         : {open_rate:.1%} (target ~28%)")
    print(f"Email Click-to-Open Rate (FY26): {click_rate:.1%}")
    print(f"Event Registrations (FY26)     : {(df['Events_Registered_FY26'] > 0).mean():.1%} (target ~26%)")
    print(f"Active Volunteer Rate (FY26)   : {df['Is_Active_Volunteer_FY26'].mean():.1%} (target ~5.5%)")

    fy24_donors = df['Gift_Count_FY24'] > 0
    fy25_donors = df['Gift_Count_FY25'] > 0
    fy26_donors = df['Gift_Count_FY26'] > 0
    retention_24_to_25 = fy25_donors[fy24_donors].mean()
    retention_25_to_26 = fy26_donors[fy25_donors].mean()
    
    gave_prior_all = (df['Lifetime_Gift_Count_Prior_To_FY24'] > 0) | fy24_donors
    lapsed_mask = gave_prior_all & (~fy25_donors)
    reactivation_rate = fy26_donors[lapsed_mask].mean()
    sustainer_rate = df.loc[fy26_donors, 'Is_Monthly_Sustainer_FY26'].mean()
    mcgill24_rate = (df.loc[fy26_donors, 'McGill24_Gift_Amount_FY26'] > 0).mean()

    print(f"FY24 Donor Rate                : {fy24_donors.mean():.1%} (target ~13%)")
    print(f"FY25 Donor Rate                : {fy25_donors.mean():.1%} (target ~14%)")
    print(f"FY24 -> FY25 Retention Rate    : {retention_24_to_25:.1%} (target ~62%)")
    print(f"FY26 Donor Rate                : {fy26_donors.mean():.1%} (target 14-16%)")
    print(f"FY25 -> FY26 Retention Rate    : {retention_25_to_26:.1%} (target 60-65%)")
    print(f"Lapsed Reactivation Rate (FY26): {reactivation_rate:.1%} (target 10-12%)")
    print(f"Monthly Sustainers (in FY26)   : {sustainer_rate:.1%} (target 22-25%)")
    print(f"McGill24 Donors (in FY26)      : {mcgill24_rate:.1%} (target ~40%)")
    print(f"Total FY26 Philanthropic Raised: ${df['Giving_Amount_FY26'].sum():,.2f}")
    print(f"Total McGill24 FY26 Raised     : ${df['McGill24_Gift_Amount_FY26'].sum():,.2f}")
    print("=" * 65 + "\n")


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_csv = os.path.join(script_dir, "mcgill_advancement_raw_crm.csv")

    df = generate_mcgill_advancement_data(n_records=30000)
    validate_data_integrity(df)
    
    print(f"Exporting raw CSV to {output_csv}...")
    df.to_csv(output_csv, index=False)
    print("Export complete.")

    print_schema_summary(df, output_csv)
