# University Advancement & Alumni Analytics (McGill University)

A raw operational constituent extract and synthetic data generation pipeline simulating 30,000 alumni records for **McGill University Advancement**. 

This repository models a consolidated enterprise database extract merged across **Salesforce CRM**, **Salesforce Marketing Cloud**, **Eventbrite / AlumnForce**, and **Google Analytics 4 (GA4)** at the close of McGill Fiscal Year 2026 (FY26: May 1, 2025 – April 30, 2026; McGill24: March 11, 2026).

---

## Key Highlights & Design Principles

- **Zero Pre-Calculated KPIs**: In accordance with enterprise raw data lake architectures, this dataset contains **no** aggregated summary scores, pre-computed retention rates, or calculated percentage fields (such as open rates or RFM scores). It represents the raw operational state of record tables.
- **Realistic Latent Correlations**: The records are synthesized using realistic statistical distributions (Pareto curves for gift amounts, Beta-Binomial models for email open/click engagement, Poisson and Negative Binomial distributions for event attendance and web sessions, and latent logistic propensity models) to ensure authentic relationships for predictive modeling and feature engineering.
- **Zero Impossible Rows**: Strict database integrity constraints and business logic rules are enforced, ensuring 100% data validity across demographics, event attendance, marketing channels, and multi-year giving histories.

---

## Data Schema & Dictionary (41 Columns)

The extract contains 30,000 rows across five functional database domains:

### 1. Constituent Demographics & Education (CRM Core)
- `Constituent_ID`: Unique 7-digit identifier (`MCG-1000001` to `MCG-1030000`).
- `Class_Year`: Graduation year (1965–2025, weighted toward recent cohorts 1995–2025).
- `Birth_Year`: Birth year calculated from degree type and graduation timing (`Class_Year - 22 + offset`).
- `Gender`: Constituent gender identity (`F` 52%, `M` 45%, `X` 1%, `None`/missing 2%).
- `Primary_Degree_Type`: Highest/primary degree earned (`Undergraduate` 68%, `Masters` 22%, `PhD` 5%, `MD/JD` 5%).
- `Primary_Faculty`: McGill academic faculty (`Faculty of Arts`, `Faculty of Science`, `Desautels Faculty of Management`, `Faculty of Engineering`, `Faculty of Medicine and Health Sciences`, `Faculty of Education`, `Faculty of Law`, `Faculty of Agricultural and Environmental Sciences`). *Strict constraint: MD/JD degrees map solely to Medicine or Law.*
- `Country_of_Residence`: Geographic country (`Canada` 67%, `United States` 18%, `United Kingdom` 4%, `France` 3%, `Hong Kong` 2%, `Other International` 6%).
- `Province_State`: Canadian province (`QC`, `ON`, `BC`, `AB`) or US state (`NY`, `CA`, `MA`, `IL`, `DC`, `TX`); `None` for international constituents outside North America.
- `Preferred_Language`: Official language preference (`EN` 78%, `FR` 22%, with higher Francophone representation in Quebec).
- `Wealth_Screening_Rating`: Prospect research capacity tier (`Tier 1: $100k+`, `Tier 2: $25k-$99k`, `Tier 3: $5k-$24k`, `Tier 4: $1k-$4.9k`, `Tier 5: Under $1k`, `Unrated`). Correlated with age, career duration, and high-earning faculties.

### 2. Digital & Marketing Cloud Logs (FY26)
- `Has_Valid_Email`: Deliverable email address flag (`1` for 92%, `0` for 8%).
- `Email_Opt_Out_Flag`: CASL/CAN-SPAM unsubscribe status (`1` if opted out or invalid email; `0` if opted in).
- `Emails_Delivered_FY26`: Count of mass emails successfully delivered in FY26 ($0$ if opted out / invalid, otherwise $8$ to $32$).
- `Emails_Opened_FY26`: Count of emails opened ($0 \le \text{Opened} \le \text{Delivered}$; population average ~28%).
- `Emails_Clicked_FY26`: Count of emails with link clicks ($0 \le \text{Clicked} \le \text{Opened}$).
- `GA4_Giving_Page_Views_FY26`: Web tracking sessions on giving.mcgill.ca and mcgill24.ca ($0$ to $18$, correlated with email clicks).
- `McGill_Connect_Registered`: Registration status on McGill Connect alumni mentorship platform (`1` or `0`).
- `McGill_Connect_Logins_FY26`: Annual logins on McGill Connect platform ($0$ if unregistered, otherwise Poisson draw up to $25$).

### 3. Experiential Events & Volunteer Logs
- `Lifetime_Events_Attended`: Total historical alumni events attended ($0$ to $45$).
- `Events_Registered_FY26`: Events registered during FY26 ($0$ to $6$).
- `Events_Attended_FY26`: Events actually attended during FY26 ($0 \le \text{Attended} \le \text{Registered}$, modeling no-show drop-off).
- `Attended_Homecoming_FY26`: Participation in McGill Homecoming / Reunion ($1$ only if attended events in FY26; elevated on 5-year reunion multiples).
- `Is_Active_Volunteer_FY26`: Active volunteer flag (mentor, reunion committee, McGill24 ambassador).
- `Volunteer_Hours_Logged_FY26`: Recorded service hours ($0.0$ if inactive, otherwise $2.0$ to $65.0$).
- `Alumni_Survey_Completed_FY26`: Response to annual alumni survey (`1` or `0`).

### 4. Solicitation & Campaign Outreach (FY26)
- `Primary_Solicitation_Channel_FY26`: Main solicitation channel (`Email_Digital`, `Direct_Mail_Letter`, `Phonathon_Student_Caller`, `Crowdfunding_McGill24`, `No_Solicitation`). *Opted-out alumni never receive `Email_Digital`.*
- `Direct_Mail_Pieces_Sent_FY26`: Count of physical mail appeals sent ($0$ to $4$).
- `Phonathon_Calls_Completed_FY26`: Completed student phonathon call sessions ($0$ to $3$).
- `Marketing_Outreach_Cost_FY26`: Exact operational solicitation cost incurred:
  $$\text{Delivered} \times \$0.08 + \text{Mail} \times \$3.75 + \text{Calls} \times \$6.50 + (\text{GA4} > 0 \ ?\ \$0.50 : \$0.00)$$

### 5. Multi-Year Philanthropic & Transaction History (CRM Gift Tables)
- `Lifetime_Gift_Count_Prior_To_FY24`: Gifts recorded prior to May 1, 2023 (~62% zero; $1$ to $50$ for donors).
- `Lifetime_Giving_Amount_Prior_To_FY24`: Total cumulative giving amount prior to FY24 ($0.0$ if count is $0$, otherwise log-normal).
- `Gift_Count_FY24` & `Giving_Amount_FY24`: Giving activity in FY24 (~13% donor rate; Pareto curve from $\$20$ to $\$25,000$).
- `Gift_Count_FY25` & `Giving_Amount_FY25`: Giving activity in FY25 (~14% donor rate; ~62% retention from FY24).
- `Gift_Count_FY26` & `Giving_Amount_FY26`: Giving activity in FY26 (~15% donor rate; 60–65% retention from FY25; 10–12% lapsed reactivation).
- `McGill24_Gift_Amount_FY26`: Giving recorded on McGill24 Giving Day ($0.0$ if non-donor; $\le \text{Giving\_Amount\_FY26}$).
- `Is_Monthly_Sustainer_FY26`: Recurring monthly giver flag (`1` iff `Gift_Count_FY26 >= 6`, representing ~23.5% of FY26 donors).
- `Last_Gift_Date`: ISO date string (`YYYY-MM-DD`) of most recent donation; `None` for non-donors. (McGill24 gifts concentrated on `2026-03-11`).
- `Last_Gift_Designation`: Designated philanthropic allocation (`The McGill Fund (Unrestricted)`, `Student Scholarships & Bursaries`, `Faculty Priority Fund`, `Research & Discovery`, `Varsity Athletics & Martlets/Redbirds`); `None` for non-donors.

---

## Quick Start & Execution

### Prerequisites
- Python 3.10+
- `numpy`
- `pandas`

### Installation & Execution
```bash
# Clone the repository
git clone https://github.com/KalashDave/University_Advancement.git
cd University_Advancement

# Install dependencies
pip install numpy pandas

# Run the raw data generator
python generate_raw_crm_data.py
```

The script will validate all assertions and generate `mcgill_advancement_raw_crm.csv` in the local directory.
