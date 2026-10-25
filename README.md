# McDill University Advancement Intelligence & CASE Analytics Portal

**Live Application Demo:** [https://mcdill-advancement-analytics.onrender.com](https://mcdill-advancement-analytics.onrender.com)

---

## 1. Project Title, Overview & Live Demo

**McDill University Advancement Intelligence** is an enterprise-grade institutional analytics and decision-support portal engineered for university executives, advancement vice-presidents, annual giving directors, and major gift officers. 

### The Core Business Problem
Higher education institutions face increasing pressure to optimize fundraising operations, justify marketing expenditures, and transition from anecdotal outreach to data-driven constituent engagement. In typical advancement divisions, data is siloed across disparate platforms:
* Core CRM databases (Salesforce, Ellucian Advance) containing demographic and academic degree history.
* Digital marketing systems (Salesforce Marketing Cloud) capturing email delivery, opens, and click-through rates.
* Web analytics engines (Google Analytics 4) recording high-intent online giving portal visits.
* Event and community platforms (Eventbrite, AlumnForce) tracking reunion attendance and alumni network logins.
* Financial ledgers recording multi-year gift transactions, recurring monthly pledges, and annual giving day totals.

Without a unified intelligence layer, leadership cannot accurately measure the Cost to Raise a Dollar (CRD), evaluate alumni retention trajectories across cohorts, or benchmark engagement against recognized standards such as the Council for Advancement and Support of Education (CASE) Alumni Engagement Metrics (AEM).

### How This Platform Solves It
This portal bridges the gap between raw atomic database extracts and executive decision-making. Ingesting an enterprise dataset of 30,000 constituent records across 41 raw database fields, it executes real-time feature engineering, lifecycle segmentation, and statistical attribution. The application provides an interactive, dark-mode analytics suite that helps institutional advancement teams:
1. Track multi-year revenue velocity ($ CAD) and monitor progress toward campaign milestones.
2. Quantify marketing return on investment across digital, direct mail, and phonathon channels.
3. Diagnose donor attrition patterns (LYBUNT/SYBUNT) and measure lapsed donor reactivation rates.
4. Operationalize the 4-pillar CASE AEM framework across Philanthropic, Experiential, Volunteer, and Communication touchpoints.
5. Identify high-capacity alumni prospects in Top Wealth Screening Tiers ($100k+ capacity) for major gift cultivation.

---

## 2. Tech Stack & Architecture Summary

The repository is built using an enterprise Python analytics stack optimized for high performance, interactive data visualization, and cloud containerization.

| Layer | Technologies & Libraries | Role & Implementation Details |
| :--- | :--- | :--- |
| **Data Engineering & Synthesis** | Python 3.11, NumPy, Pandas | Deterministic generation of 30,000 constituent records with 41 raw database attributes, Pareto gift distributions, and automated data integrity assertion suites. |
| **Analytics & UI Engine** | Streamlit (>=1.35.0) | High-contrast Executive Midnight interface, multi-select global slicers, in-memory caching via `@st.cache_data`, and custom responsive CSS component containers. |
| **Data Visualization** | Plotly Express, Plotly Graph Objects (>=5.18.0) | 2x2 grid suites per module, interactive hover cards, multi-year trend trajectories, Pareto concentration charts, and demographic distributions. |
| **Predictive Analytics & ML** | Scikit-Learn (>=1.3.0), NumPy | Latent behavioral propensity modeling, feature engineering, wealth screening capacity scoring, and leakage-free prospect prioritization. |
| **Containerization & Cloud Ops** | Docker, Render PaaS, Linux / Debian Slim | Multi-stage Docker containerization with layer caching, curl healthchecks, dynamic `$PORT` binding, and Render Blueprint infrastructure-as-code automation. |

---

## 3. Repository File Structure & Component Guide

```text
University_Advancement/
├── .streamlit/
│   └── config.toml                  # Streamlit server flags & Executive Midnight theme palette
├── Dockerfile                       # Multi-stage production container configuration
├── .dockerignore                    # Excluded files for streamlined Docker build context
├── render.yaml                      # Render Blueprint infrastructure-as-code deployment spec
├── requirements.txt                 # Pinned Python package dependencies
├── generate_raw_crm_data.py         # 30,000 constituent raw CRM data synthesis engine
├── mcgill_advancement_raw_crm.csv   # Synthesized raw constituent database extract (41 columns)
├── app.py                           # Main Streamlit dashboard application (6 strategic modules)
└── README.md                        # Enterprise project documentation and architecture guide
```

### Component Breakdown
* **`app.py`**: The central application script. Contains the executive dark theme CSS, data preprocessing routines, global filtering engine, KPI calculation logic, and six specialized analytical views.
* **`generate_raw_crm_data.py`**: The data synthesis script. Simulates realistic, non-random alumni constituent profiles using statistical distributions, latent behavioral propensity equations, and integrity assertion checks.
* **`mcgill_advancement_raw_crm.csv`**: The 41-column, 30,000-row constituent dataset produced by the simulation script. Contains atomic CRM records without pre-aggregated summaries.
* **`Dockerfile`**: Defines the Debian-based container image. Uses Python 3.11-slim, implements Docker layer caching for dependencies, installs healthcheck utilities, and dynamically binds to the host port.
* **`render.yaml`**: Infrastructure-as-code specification for deploying the Docker container directly to Render Free Tier web services.
* **`.streamlit/config.toml`**: Configures the base dark mode, McDill Crimson primary accent (`#ED1B2F`), slate card backgrounds (`#1E293B`), and headless server settings.
* **`requirements.txt`**: Specifies exact library versions required for repeatable environments across local machines and cloud containers.

---

## 4. Dataset & Data Simulation Methodology

The underlying dataset (`mcgill_advancement_raw_crm.csv`) models a comprehensive constituent extract at the close of Fiscal Year 2026 (May 1, 2025 to April 30, 2026). It contains **30,000 constituent records** and **41 raw database columns** spanning five core functional domains:

1. **Constituent Demographics & Education (10 columns):** `Constituent_ID`, `Class_Year`, `Birth_Year`, `Gender`, `Primary_Degree_Type`, `Primary_Faculty`, `Country_of_Residence`, `Province_State`, `Preferred_Language`, `Wealth_Screening_Rating`.
2. **Digital & Marketing Cloud Logs (8 columns):** `Has_Valid_Email`, `Email_Opt_Out_Flag`, `Emails_Delivered_FY26`, `Emails_Opened_FY26`, `Emails_Clicked_FY26`, `GA4_Giving_Page_Views_FY26`, `McGill_Connect_Registered`, `McGill_Connect_Logins_FY26`.
3. **Experiential Events & Volunteer Logs (7 columns):** `Lifetime_Events_Attended`, `Events_Registered_FY26`, `Events_Attended_FY26`, `Attended_Homecoming_FY26`, `Is_Active_Volunteer_FY26`, `Volunteer_Hours_Logged_FY26`, `Alumni_Survey_Completed_FY26`.
4. **Solicitation & Campaign Outreach (4 columns):** `Primary_Solicitation_Channel_FY26`, `Direct_Mail_Pieces_Sent_FY26`, `Phonathon_Calls_Completed_FY26`, `Marketing_Outreach_Cost_FY26`.
5. **Multi-Year Philanthropic History (12 columns):** `Lifetime_Gift_Count_Prior_To_FY24`, `Lifetime_Giving_Amount_Prior_To_FY24`, `Gift_Count_FY24`, `Giving_Amount_FY24`, `Gift_Count_FY25`, `Giving_Amount_FY25`, `Gift_Count_FY26`, `Giving_Amount_FY26`, `McGill24_Gift_Amount_FY26`, `Is_Monthly_Sustainer_FY26`, `Last_Gift_Date`, `Last_Gift_Designation`.

### Statistical Distributions & Behavioral Realism
Rather than populating records with uniform random numbers, the data generator enforces human behavioral correlations and domain rules:
* **Heavy-Tailed Giving Amounts (Pareto Distribution):** Gift sizes follow a Pareto power-law distribution where shape parameter alpha (1.15 to 1.80) scales inversely with wealth capacity. Major gift tiers capture the vast majority of philanthropic dollars.
* **Email Engagement Funnel (Beta-Binomial Process):** Email open rates hover around 28%, and click-through rates range from 0% to 40% of opened emails, reflecting real-world marketing engagement.
* **Web Intent Signals (Poisson Process):** GA4 online giving page views (0 to 18) are directly tied to email click events, with organic search accounting for minor background visits.
* **Event Attendance & No-Show Factor:** Event attendance applies an 80% realization rate (20% no-show drop-off) against registered seats. Homecoming attendance spikes for alumni celebrating 5-year reunion milestones (5th, 10th, 15th, 20th, 25th reunions).
* **Strict Logical Boundaries (Zero Impossible Rows):** Unsubscribed constituents never receive digital emails. Non-volunteers log exactly zero volunteer hours. Non-donors have null gift dates. Geographic states are null outside North America.

---

## 5. Dashboard Architecture & User Experience

The web application is structured with intuitive navigation and global filtering controls:

```text
[ Sidebar Global Slicers: Faculty | Cohort | Region | Wealth Tier ]
                                ↓
        [ Header: McDill University Advancement Analytics ]
                                ↓
    [ Module Selector: 6 Strategic Advancement Views ]
                                ↓
       [ Module Banner: Scope, Objectives & CASE Pillars ]
                                ↓
       [ Aligned Strategic KPI Metric Cards with Tooltips ]
                                ↓
         [ 2x2 Distinct Plotly Visualization Suites ]
                                ↓
 [ Interactive 41-Column CRM Dataset Snapshot (Landing Page Only) ]
```

### Global Slicers & Filtering
All filters reside in the collapsible left sidebar and default to "All" options:
* **Academic Faculty:** Multiselect supporting Arts, Science, Desautels Management, Engineering, Medicine, Education, Law, and Agricultural & Environmental Sciences.
* **Cohort Selector:** Multiselect grouping alumni into Young Alumni (<10 yrs), Mid-Career (10-25 yrs), and Senior Alumni (25+ yrs).
* **Geographic Region:** Multiselect filtering by Quebec, Rest of Canada, United States, and International regions.
* **Wealth Capacity Tier:** Multiselect isolating Tier 1 ($100k+), Tier 2 ($25k-$99k), Tier 3 ($5k-$24k), Tier 4 ($1k-$4.9k), Tier 5 (Under $1k), and Unrated records.

### Detailed Overview of the 6 Dashboard Modules

#### View 1: Executive Overview (Landing Dashboard)
* **Purpose:** Single-pane institutional briefing for the President, Provost, and Vice-President of Advancement.
* **Primary KPI Cards:** Total Revenue ($ CAD), Active Donors, Alumni Participation Rate (%), Donor Retention Rate (%), Average Gift Yield ($ CAD), Marketing ROI Multiple.
* **Secondary Aligned Cards:** McDill24 Giving Day Revenue ($ CAD), Monthly Sustainers (Count and Share), Campaign Goal Pace ($100M Goal).
* **Visualizations:** Class Year graduation timeline distribution, Generational age breakdown (Silent to Gen Z), Gender identity share, and Global geographic footprint.
* **Dataset Snapshot:** Interactive HTML preview of the underlying CRM extract with custom hover tooltips detailing every column definition.

#### View 2: Philanthropic Health & Revenue
* **Purpose:** Financial auditing of fundraising yield, giving tier concentration, and revenue velocity.
* **KPIs:** FY26 Total Commitments, Average Gift Yield, McDill24 Campaign Contribution.
* **Visualizations (2x2 Grid):**
  1. *Multi-Year Commitments Trajectory (FY24 to FY26):* Assesses year-over-year fundraising growth.
  2. *Giving Amount Tier Concentration (Pareto Dispersion):* Breaks down dollars by gift bracket (<$100 to $10k+).
  3. *Monthly Giving Seasonality Trend:* Tracks calendar peaks around year-end tax deadlines and Giving Day.
  4. *Average Gift Yield by Academic Faculty:* Ranks academic divisions by average donation size.

#### View 3: Donor Lifecycle & Retention Funnel
* **Purpose:** Evaluates constituent migration dynamics across consecutive renewal, attrition risk, and reactivation.
* **KPIs:** Consecutive Retention Rate (FY25 to FY26), Lapsed Reactivation Rate, First-Time Donor Acquisition Rate, Monthly Sustainer Penetration.
* **Visualizations (2x2 Grid):**
  1. *Three-Year Longitudinal Donor Trajectory:* Compares active donor population counts across FY24, FY25, and FY26.
  2. *Constituent Lifecycle Stage Segmentation:* Classifies the universe into Donors, Lapsed prospects, and Never-Givers.
  3. *Donor Retention Benchmarks:* Contrasts consecutive retention and reactivation rates against CASE standards.
  4. *Monthly Sustainer Growth & Impact:* Evaluates the revenue contribution of recurring monthly donors versus one-time donors.

#### View 4: Marketing Efficiency & Channels
* **Purpose:** Analyzes the economic return of solicitation channels and tracks digital giving funnel conversion.
* **KPIs:** Cost per Dollar Raised (CPDR), Marketing ROI Multiple, Email Open Rate (%), GA4 Online Giving Portal Conversion Rate (%).
* **Visualizations (2x2 Grid):**
  1. *Philanthropic Revenue by Solicitation Channel:* Compares dollars raised via Digital, Direct Mail, Phonathon, and McDill24.
  2. *Channel Conversion Rate (%):* Measures donor conversion efficiency across channels.
  3. *Marketing Outreach Cost vs. Revenue:* Evaluates direct outreach expenditure against total dollars raised.
  4. *Net ROI Multiple by Channel:* Ranks solicitation channels by return on marketing investment.

#### View 5: CASE 4-Pillar Engagement (AEM)
* **Purpose:** Operationalizes the Council for Advancement and Support of Education framework across all four recognized dimensions.
* **Pillar Definitions:** Philanthropic (financial contributions), Experiential (event and reunion attendance), Volunteer (boards, mentoring, and ambassadorship), Communication (email opens and portal logins).
* **KPIs:** Event Attendance Rate (Experiential), Ticket Show Rate (Realized Attendance), 2+ CASE Modes Multi-Modal Share, Active Volunteers Count.
* **Visualizations (2x2 Grid):**
  1. *CASE 4-Pillar Constituent Penetration Rates:* Compares participation across all four dimensions.
  2. *Multi-Pillar Constituent Breadth:* Illustrates constituent overlap across 0, 1, 2, 3, or all 4 engagement pillars.
  3. *Experiential Attendance by Graduation Cohort:* Analyzes event participation differences between Young, Mid-Career, and Senior alumni.
  4. *Communication Engagement across Academic Faculties:* Ranks faculties by digital open and login rates.

#### View 6: Prospect Capacity & Faculty Intelligence
* **Purpose:** Equips major gift officers and faculty development directors with wealth screening insights and prioritized prospect pipelines.
* **KPIs:** Top Tier Giving ($100k+ Tier 1 & Tier 2 Totals), Tier 1 ($100k+) Conversion Rate, Tier 2 ($25k-$99k) Conversion Rate.
* **Visualizations (2x2 Grid):**
  1. *Faculty Commitments ($ CAD):* Ranks academic divisions by total philanthropic commitments secured.
  2. *Wealth Capacity Tier Conversion Rates (%):* Evaluates giving rates across wealth screening brackets.
  3. *Wealth Screening Matrix:* Cross-tabulates alumni counts, donor totals, participation rates, and dollars raised per tier.
  4. *Major Gift Pipeline ($25k+ Capacity) by Faculty:* Identifies major gift opportunity pools across academic divisions.

---

## 6. KPI Framework & Methodology

The table below provides a complete reference for all strategic performance indicators calculated across the portal:

| Strategic Pillar | Metric Name | Business Definition | Underlying Calculation Formula | Benchmark / Target |
| :--- | :--- | :--- | :--- | :--- |
| **Financial Health** | Total Philanthropic Revenue | Total dollars committed in FY26 across all university accounts. | `Sum(Giving_Amount_FY26)` | Annual target: $3.0M to $6.5M |
| **Financial Health** | Cost per Dollar Raised (CPDR) | Direct outreach expense incurred to secure one dollar of revenue. | `Sum(Marketing_Outreach_Cost_FY26) / Sum(Giving_Amount_FY26)` | CASE standard: < $0.20 (Ideal < $0.10) |
| **Financial Health** | Marketing ROI Multiple | Ratio of philanthropic dollars generated per marketing dollar spent. | `Sum(Giving_Amount_FY26) / Sum(Marketing_Outreach_Cost_FY26)` | Association of Fundraising Professionals: > 6.7x |
| **Financial Health** | McDill24 Giving Day Total | Commitments secured during the 24-hour university blitz. | `Sum(McGill24_Gift_Amount_FY26)` | Target: > 18% of annual revenue |
| **Lifecycle & Pipeline** | Active Donors | Unique constituents making at least one gift during the fiscal year. | `Count(Constituent_ID where Gift_Count_FY26 > 0)` | Target: 4,000 to 4,800 donors |
| **Lifecycle & Pipeline** | Alumni Participation Rate | Proportion of addressable alumni who contributed financially in FY26. | `(Active Donors / Total Filtered Population) * 100` | U15 Canadian Peer Median: 8% to 12% |
| **Lifecycle & Pipeline** | Consecutive Donor Retention | Percentage of prior-year (FY25) donors renewing their gift in FY26. | `(Donated_FY25 & Donated_FY26 Donors / Donated_FY25 Donors) * 100` | CASE National Average: 60% to 65% |
| **Lifecycle & Pipeline** | Lapsed Reactivation Rate | Percentage of inactive prior donors who resumed giving in FY26. | `(Donated_FY26 & Gave_Prior & ~Donated_FY25) / Lapsed Pool * 100` | CASE Benchmark: 10% to 12% |
| **Lifecycle & Pipeline** | Monthly Sustainer Share | Share of active donors enrolled in automated recurring giving. | `(Count where Is_Monthly_Sustainer_FY26 == 1 / Active Donors) * 100` | Higher Ed Target: 20% to 25% |
| **Marketing Efficiency**| Email Open Rate | Proportion of delivered advancement marketing emails opened. | `Sum(Emails_Opened_FY26) / Sum(Emails_Delivered_FY26) * 100` | Industry Average: ~28% |
| **Marketing Efficiency**| GA4 Portal Conversion Rate | Share of giving page visitors who completed a gift transaction. | `(Visitors with Pageviews & Donated_FY26 / Total Visitors) * 100` | Non-profit E-Commerce: 15% to 22% |
| **CASE AEM Framework**| Experiential Pillar Rate | Share of alumni participating in at least one university event. | `(Count where Events_Attended_FY26 > 0 / Total Population) * 100` | CASE Standard: 10% to 15% |
| **CASE AEM Framework**| Ticket Show Realization | Percentage of event registrants who attended the scheduled event. | `Sum(Events_Attended_FY26) / Sum(Events_Registered_FY26) * 100` | Industry Standard: 55% to 65% |
| **CASE AEM Framework**| Multi-Modal Engagement Lift| Share of alumni active in two or more of the 4 CASE dimensions. | `(Count where CASE_Pillar_Count >= 2 / Total Population) * 100` | Multi-modal alumni show 9x giving lift |
| **Major Gifts** | Tier 1 Capacity Conversion | Participation rate among prospects rated with $100k+ wealth capacity. | `(Tier 1 Donors / Total Tier 1 Prospects) * 100` | Major Gift Goal: > 60% participation |

---

## 7. Machine Learning Pipeline & Propensity Simulator

### Predictive Objective & Target Variable
The predictive analytics engine models **Giving Propensity ($P(\text{Donation} = 1)$)**, defined as the likelihood that an addressable constituent completes a donation in the current reporting fiscal year (`Gift_Count_FY26 > 0`).

### Feature Selection & Preventing Data Leakage
To prevent data leakage, all post-decision transaction features and contemporaneous campaign outcomes are strictly excluded from the feature space:
* **Excluded Target-Leaking Columns:** `Gift_Count_FY26`, `Giving_Amount_FY26`, `McGill24_Gift_Amount_FY26`, `Is_Monthly_Sustainer_FY26`, and `Last_Gift_Date`.
* **Included Historical & Behavioral Predictors:**
  1. *Demographic Indicators:* Years since graduation (`2026 - Class_Year`), academic degree type, faculty wealth multiplier, and geographic region.
  2. *Capacity Ratings:* Wealth screening tier score mapped on a numerical capacity scale (Tier 1 = 3.0, Tier 2 = 2.2, Tier 3 = 1.4, Tier 4 = 0.7, Tier 5 = 0.0, Unrated = 0.1).
  3. *Digital Engagement Signals:* Log-transformed email click count (`np.log1p(Emails_Clicked_FY26)`), digital affinity score, and GA4 giving portal pageviews (`np.log1p(GA4_Giving_Page_Views_FY26)`).
  4. *Experiential & Leadership Attributes:* Log-transformed lifetime event attendance, FY26 event attendance count, and active volunteer status (`Is_Active_Volunteer_FY26`).
  5. *Longitudinal Donor History:* Cumulative prior gift counts and multi-year giving flags (`Gift_Count_FY24`, `Giving_Amount_FY24`, and `Gave_Prior`).

### Latent Propensity Formula
The behavioral generation and downstream propensity scoring use a multi-factor equation calibrated against historical giving patterns:

```text
Latent_Score = 0.35 * Wealth_Score 
             + 0.22 * Age_Factor 
             + 0.18 * ln(1 + Lifetime_Events) 
             + 0.16 * ln(1 + FY26_Events) 
             + 0.12 * ln(1 + Email_Clicks) 
             + 0.08 * ln(1 + GA4_Pageviews) 
             + 0.25 * Volunteer_Flag 
             + Gaussian_Noise(0, 0.35)
```

Constituents are segmented into priority deciles based on calculated propensity. High-propensity constituents with high wealth screening ratings who have not yet donated represent prime discovery prospects for major gift discovery and targeted annual fund appeals.

---

## 8. Local Setup & Docker Usage Instructions

### Prerequisites
* Python 3.11 or higher
* Git
* Docker Desktop (optional, for containerized execution)

### Option A: Local Python Virtual Environment

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/KalashDave/University_Advancement.git
   cd University_Advancement
   ```

2. **Create and Activate a Virtual Environment:**
   * On macOS / Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   * On Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Regenerate the CRM Dataset (Optional):**
   ```bash
   python generate_raw_crm_data.py
   ```
   *Running this script executes 30,000 constituent simulations, validates all integrity assertions, and refreshes `mcgill_advancement_raw_crm.csv`.*

5. **Launch the Streamlit Application:**
   ```bash
   streamlit run app.py
   ```
   *Open your browser and navigate to `http://localhost:8501` to view the portal.*

---

### Option B: Docker Container Execution

1. **Build the Docker Image:**
   ```bash
   docker build -t mcdill-advancement-analytics:latest .
   ```

2. **Run the Container Locally:**
   ```bash
   docker run -d --name mcdill_dashboard -p 8501:8501 mcdill-advancement-analytics:latest
   ```

3. **Access the Containerized Portal:**
   * Open `http://localhost:8501` in your browser.
   * To inspect container logs:
     ```bash
     docker logs -f mcdill_dashboard
     ```
   * To stop the container:
     ```bash
     docker stop mcdill_dashboard && docker rm mcdill_dashboard
     ```

---

## 9. Author & Contact

**Kalash Dave**  
* GitHub: [https://github.com/KalashDave](https://github.com/KalashDave)  
* Project Repository: [https://github.com/KalashDave/University_Advancement](https://github.com/KalashDave/University_Advancement)
