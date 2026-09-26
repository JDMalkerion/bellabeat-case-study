# Bellabeat Smart Device Usage Analysis

A full-stack data analytics case study analyzing consumer smart device habits to inform product strategy, digital marketing campaigns, and customer retention for Bellabeat's ecosystem of women's wellness products.


### Streamlit Link: (https://bellabeat-case-study-nx5rkmgiwytyxbrd6nxbpj.streamlit.app)
---

## Business Task

Bellabeat is a high-tech manufacturer of health-focused smart products designed specifically for women, including the Bellabeat app, the *Leaf* wellness tracker, the *Time* hybrid smartwatch, and the *Spring* smart water bottle. 

Urška Sršen (co-founder and Chief Creative Officer) and the executive leadership team requested an analysis of how consumers utilize non-Bellabeat smart devices (represented by public Fitbit tracker data) to identify behavioral trends, daily movement habits, sleep patterns, and device adherence. These insights will inform Bellabeat's marketing strategy, illuminate opportunities to drive engagement across the Bellabeat app and subscription coaching programs, and position Bellabeat's design-forward hardware against competitors in the global smart device market.

---

## Data Source and License

- **Source**: [FitBit Fitness Tracker Data](https://www.kaggle.com/datasets/arashnic/fitbit) hosted on Kaggle by Mobius.
- **License**: Creative Commons Dedicated to Public Domain ([CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/)).
- **Collection**: Sourced from 33 Amazon Mechanical Turk survey respondents between April 12, 2016 and May 12, 2016.
- **Discrepancies & Quality Caveats**:
  - **User Count Discrepancy**: The original case study brief and Kaggle dataset documentation specify "30 eligible Fitbit users." Rigorous database ingestion and verification revealed **33 distinct user IDs** across daily and hourly activity tracking tables.
  - **Absence of Demographics**: The dataset contains zero demographic variables—no gender, age, weight benchmarks, geographic region, or reproductive health indicators. Extrapolating findings from a general sample to Bellabeat's female-centric audience must be treated as proxy behavior.
  - **Unspecified Units**: Distance metrics (`TotalDistance`, `TrackerDistance`) do not define measurement units (miles vs. kilometers).
  - **Feature Sparsity & Tracking Drop-off**: Tracking adherence degrades significantly beyond basic step counts. While 33 participants recorded daily steps, only 24 logged sleep, 14 logged second-by-second heart rates, and just 8 logged weight (with body fat missing in 65 out of 67 weight logs).

---

## Tools Used

- **SQLite / SQL**: Primary relational database (`sql/bellabeat.db`). Designed normalized table schemas, implemented ISO 8601 date normalization, eliminated sleep log duplicates, flagged non-wear records, and engineered 8 reusable analytical views (`analysis_*`).
- **Python / pandas / NumPy**: Built an automated, idempotent ingestion pipeline (`src/db_setup.py`), rigorous multi-layer data verification scripts (`src/verify.py`, `src/verify_analysis.py`), and automated view-to-CSV export utilities (`src/export_analysis.py`).
- **Streamlit & Plotly**: Developed a multipage interactive web application (`app/`) complete with executive KPI scorecards, CDC step segmentation donuts, stacked activity-minute charts, sleep histograms, participant wear-compliance heatmaps, and a read-only SQL execution console.
- **Microsoft Power BI**: Built an executive-ready companion dashboard (`powerbi/bellabeat-dashboard.pbix`) delivering interactive visuals and drill-down capabilities for stakeholder presentations.

---

## Key Findings

- **Cohort Size and Coverage**: The dataset encompasses 33 distinct users over a 31-day window (2016-04-12 through 2016-05-12), comprising 940 daily activity records and 22,099 hourly tracking rows.
- **Step Deficit Against CDC Benchmark**: Participants averaged **8,280 daily steps** (weighted across all valid wear days), falling ~17.2% below the CDC-recommended benchmark of 10,000 steps per day. Across all valid tracked days, users achieved 10,000+ steps on only 21.1% of days.
- **User Activity Segmentation**: Classifying participants by average daily steps on valid wear days reveals three distinct groups:
  - **Moderate Active (5,000 – 9,999 steps/day)**: 19 users (57.6% of the cohort).
  - **Heavy Active (≥ 10,000 steps/day)**: 7 users (21.2% of the cohort).
  - **Light Active (< 5,000 steps/day)**: 7 users (21.2% of the cohort).  
  The overwhelming majority of users are moderate movers rather than intensive fitness enthusiasts.
- **Dominance of Sedentary Behavior**: Participants logged an average of **993 sedentary minutes per day** (~16.5 hours), accounting for **81.3%** of all tracked daytime activity. In contrast, lightly active minutes averaged 193 min/day (15.8%), fairly active minutes averaged 14 min/day (1.1%), and very active minutes averaged 21 min/day (1.8%).
- **Non-Wear Day Identification**: A total of **79 daily records** (8.4% of total daily logs) recorded 1,440 sedentary minutes with zero steps, indicating the device sat untouched on a surface for a full 24-hour cycle while accumulating default sedentary time. These records were flagged (`is_likely_nonwear = 1`) rather than deleted, preserving data integrity while isolating genuine wear metrics.
- **Sleep Quality and Adoption Gap**: Only **24 of 33 participants (72.7%)** ever recorded sleep data. Across 410 deduplicated sleep logs, average sleep duration was **6.99 hours** per night (419.5 minutes), falling slightly below the CDC healthy adult threshold of 7–9 hours. Participants averaged 458.6 minutes in bed, spending an average of **39.1 minutes awake in bed**, pointing to significant sleep latency and nighttime restlessness.
- **High Baseline Wear Compliance**: Overall wear adherence averaged **91.9%** across the 31-day observation window. 26 of 33 users maintained compliance rates of 80% or higher, showing high willingness to wear hardware consistently.
- **Weekly Activity Rhythm**: Movement peaked on **Tuesday (8,861 steps)** and Saturday (8,291 steps), while plunging to an aggregate low on **Sunday (7,669 steps)**—representing a steep **1,192-step drop** that mirrored a weekly low in caloric burn (2,263 kcal on Sunday vs. 2,356 kcal on Tuesday).
- **Diurnal Caloric Burn Patterns**: Hourly calorie expenditure followed a bimodal distribution with distinct peaks at lunch (12:00 PM – 2:00 PM) and post-work evening (5:00 PM – 7:00 PM), bounded by prolonged afternoon sedentary slumps.

---

## Limitations

- **Small, Non-Representative Sample**: 33 individuals recruited via Amazon Mechanical Turk is a small sample with inherent self-selection bias toward digital survey workers, limiting broad population generalizability.
- **Demographic Blindness**: The dataset completely lacks gender, age, health status, or occupation data. Because Bellabeat specifically engineers products for women's physiological cycles and reproductive health, general Fitbit findings serve as a baseline behavioral proxy rather than a direct female cohort study.
- **High Attrition on Non-Step Features**: Substantial data sparsity in optional features—sleep tracking (24/33), heart rate (14/33), and weight logging (8/33, with 5 users logging ≤2 times)—precludes multi-variable regression on heart-rate exertion or body composition.
- **Non-Wear Ambiguity**: While a full 1,440 sedentary minutes provides a clean proxy for whole-day non-wear, shorter off-wrist intervals (e.g., removing the tracker for 4–8 hours during charging or bathing) cannot be cleanly decoupled from genuine resting time without continuous heart-rate or capacitive sensor data.

---

## Recommendations

A high-level summary of strategic initiatives for Bellabeat leadership:

1. **Automated Non-Wear Safeguards**: Implement optical/capacitive skin-contact detection in device firmware to suspend sedentary time accumulation when unclipped or removed, preventing artificial 1,440-minute inactivity penalties and preserving user trust in Bellabeat wellness scores.
2. **Contextual Micro-Nudges for the Moderate Majority**: Focus product marketing on the 57.6% Moderate segment (5k–10k steps, averaging 7,856 steps/day) rather than extreme athletic messaging. Trigger gentle 250-step walking prompts or hydration check-ins during the identified 1:00 PM – 4:00 PM sedentary lull to help users bridge the ~2,144-step gap to the 10,000-step benchmark.
3. **Frictionless Sleep Tracking & Wind-Down Coaching**: Position the versatile *Bellabeat Leaf* (worn as a lightweight pajama clip or necklace) as the unobtrusive alternative to uncomfortable wristwatches to capture the 27.3% of users who abandon sleep tracking. Introduce in-app bedtime wind-down meditations and breathing exercises to reduce the 39-minute awake-in-bed latency gap.
4. **"Sunday Reset" Weekend Momentum Program**: Counteract the 1,192-step Tuesday-to-Sunday drop-off with a branded "Sunday Reset" campaign in the Bellabeat app—delivering restorative nature walk challenges, light yoga routines, and weekly habit check-ins to prevent weekend drop-off.

*For complete strategic breakdowns, ROI rationales, and the Executive Strategic Action Matrix, navigate to Page 5 of the Streamlit dashboard or explore the companion Power BI dashboard.*

---

## Project Structure

```text
bellabeat-case-study/
├── app/
│   ├── app.py                      # Streamlit multipage application entry point
│   ├── utils.py                    # SQLite connection, SQL parsers, and custom styling
│   └── pages/
│       ├── 1_Overview.py           # Executive KPIs, step timeline, and CDC segmentation
│       ├── 2_Activity.py           # Weekday steps, intensity stacked bars, hourly calories
│       ├── 3_Sleep_and_Wear.py     # Sleep distribution, adherence rates, sedentary heatmap
│       ├── 4_SQL_Analysis.py       # Live analytical view inspector & custom SQL terminal
│       └── 5_Recommendations.py    # Strategic marketing roadmap and action matrix
├── data/                           # Raw Fitbit CSV dataset (10 files; gitignored)
├── exports/                        # Analytical view CSV exports (8 files)
│   ├── analysis_activity_minutes.csv
│   ├── analysis_calories_by_weekday.csv
│   ├── analysis_hourly_calories.csv
│   ├── analysis_sedentary_by_participant.csv
│   ├── analysis_sleep_duration.csv
│   ├── analysis_user_segments.csv
│   ├── analysis_wear_engagement.csv
│   └── analysis_weekday_steps.csv
├── powerbi/
│   └── bellabeat-dashboard.pbix    # Microsoft Power BI companion report
├── sql/
│   ├── 01_schema.sql               # SQLite DDL table schemas with typed columns
│   ├── 02_cleaning.sql             # Deduplication and clean_ views with non-wear flag
│   ├── 03_analysis.sql             # 8 analytical views prefixed with analysis_
│   ├── bellabeat.db                # Cleaned SQLite database (gitignored)
│   └── cleaning_log.md             # Detailed data audit, row counts, and cleaning log
├── src/
│   ├── db_setup.py                 # SQLite database creation & ISO 8601 CSV ingestion
│   ├── verify.py                   # Data ingestion and schema validation script
│   ├── verify_analysis.py          # View validation and statistical check script
│   └── export_analysis.py          # Script exporting analytical views to CSV in exports/
├── video/                          # Project walkthrough presentation video (planned)
├── requirements.txt                # Python dependencies for dashboard and scripts
├── .gitignore                      # Git exclusion rules (DB, venv, data CSVs)
└── README.md                       # Comprehensive case study documentation
```

---

## Run Locally

### 1. Prerequisites
- Python 3.10+ installed
- Git installed

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/JDMalkerion/bellabeat-case-study.git
cd bellabeat-case-study

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Initialize SQLite Database
If `sql/bellabeat.db` is not present or needs regeneration, run the database setup script to ingest raw data from `data/` and apply schema and cleaning transformations:
```bash
python3 src/db_setup.py
```

### 4. Verify Analytical Views & Pipeline (Optional)
Run the automated verification suite to validate data integrity, view row counts, and statistical calculations:
```bash
python3 src/verify.py
python3 src/verify_analysis.py
```

### 5. Launch the Streamlit Dashboard
```bash
streamlit run app/app.py
```
Open your browser to `http://localhost:8501` to explore the interactive dashboard.
