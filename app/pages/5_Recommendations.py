"""
Strategic Recommendations Page for Bellabeat.
Data-driven marketing and product roadmap presented for Bellabeat executive leadership,
specifically Chief Creative Officer Urška Sršen and the marketing analytics team.
"""

import sys
from pathlib import Path
import streamlit as st

# Add app root to path for imports
app_dir = Path(__file__).resolve().parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from utils import apply_custom_css

st.set_page_config(page_title="Recommendations | Bellabeat Analytics", page_icon="💡", layout="wide")
apply_custom_css()

# Header Section
st.title("💡 Strategic Recommendations & Marketing Playbook")
st.markdown(
    """
    **Prepared for:** Urška Sršen (Chief Creative Officer & Co-Founder) and Bellabeat Marketing Leadership  
    **Objective:** Translate empirical non-Bellabeat smart device usage patterns into actionable marketing campaigns, 
    app feature enhancements, and hardware positioning for Bellabeat's product ecosystem (*Leaf*, *Time*, and *Bellabeat App*).
    """
)
st.markdown("---")

# Strategic KPI Summary Row
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">Activity Deficit</div>
            <div class="metric-value">8,280</div>
            <div class="metric-sub">Avg steps vs. 10k CDC target (-17.2%)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">Sedentary Dominance</div>
            <div class="metric-value">993 min</div>
            <div class="metric-sub">~16.5 hrs / 81.3% of waking time</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">Sleep Tracking Gap</div>
            <div class="metric-value">72.7%</div>
            <div class="metric-sub">24 of 33 logged sleep; 6.99h avg duration</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with k4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-title">Weekend Drop-Off</div>
            <div class="metric-value">-1,192</div>
            <div class="metric-sub">Step gap: Tuesday (8,861) vs Sunday (7,669)</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Recommendation 1
# -----------------------------------------------------------------------------
with st.container():
    st.subheader("1. Automated Non-Wear Detection & Data Quality Safeguards")
    st.caption("Ecosystem Area: Bellabeat Hardware Sensors & Mobile Data Pipeline")

    col_rec1_left, col_rec1_right = st.columns([1, 1])
    with col_rec1_left:
        st.markdown(
            """
            **🔍 Key Finding:**  
            Across the 940 daily tracking records, **79 days (8.4%)** recorded a full 1,440 sedentary minutes with zero steps—indicating the tracker was placed on a nightstand or desk while the software continued registering full-day sedentary activity.
            
            **💡 Strategic Recommendation:**  
            Incorporate automated capacitive or optical wear-detection logic within the Bellabeat app firmware. When device removal is detected, the app should suspend sedentary minute accumulation and flag unmonitored windows instead of skewing activity metrics. Pair this with polite, smart push prompts (e.g., *"Did you take off your Leaf? Tap to log charging time"*).
            """
        )
    with col_rec1_right:
        st.markdown(
            """
            **📈 Business & Marketing Rationale:**  
            Inaccurate data erodes consumer trust. When a user sees a report claiming they were "sedentary for 24 hours," they lose confidence in the device's algorithmic precision. Clean data reporting protects Bellabeat's brand reputation for premium wellness analytics, eliminates false wellness penalties in the app, and provides genuine wear-compliance data for health insights.
            """
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# Recommendation 2
# -----------------------------------------------------------------------------
with st.container():
    st.subheader("2. Proactive Habit Nudges for the 'Moderate' Majority")
    st.caption("Ecosystem Area: Bellabeat Mobile App Notifications & Daily Coaching")

    col_rec2_left, col_rec2_right = st.columns([1, 1])
    with col_rec2_left:
        st.markdown(
            """
            **🔍 Key Finding:**  
            The cohort averaged **8,280 daily steps**, falling short of the CDC-recommended 10,000-step baseline. User segmentation reveals that **57.6% (19 of 33 users)** fall into the Moderate tier (5,000–9,999 steps), averaging **7,856 steps/day**, while sedentary time accounts for **81.3% (~993 minutes)** of the daily tracked cycle.
            
            **💡 Strategic Recommendation:**  
            Rather than blasting generic 10,000-step ultimatums that discourage everyday users, Bellabeat should program contextual micro-nudges timed around observed sedentary plateaus. Specifically, prompt users during the mid-afternoon work slump (1:00 PM – 4:00 PM) with achievable 250-step walking prompts, quick desk stretches, or hydration check-ins paired with the *Bellabeat Spring* smart bottle.
            """
        )
    with col_rec2_right:
        st.markdown(
            """
            **📈 Business & Marketing Rationale:**  
            Bellabeat’s brand equity is built on accessible, holistic women's wellness, not aggressive athletic competition. The 19 Moderate users represent the highest-conversion opportunity: helping them bridge a realistic **~2,144-step gap** (from their 7,856 daily average to the 10,000-step benchmark) via micro-habits builds sustained self-efficacy, boosts Daily Active Users (DAU), and fuels subscription retention for Bellabeat Membership coaching programs.
            """
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# Recommendation 3
# -----------------------------------------------------------------------------
with st.container():
    st.subheader("3. Frictionless Sleep Tracking Adoption & Wind-Down Coaching")
    st.caption("Ecosystem Area: Bellabeat Leaf Hardware Positioning & Membership Content")

    col_rec3_left, col_rec3_right = st.columns([1, 1])
    with col_rec3_left:
        st.markdown(
            """
            **🔍 Key Finding:**  
            Only **24 of 33 participants (72.7%)** logged any sleep data, revealing that over a quarter of consumers abandoned nighttime tracking. Furthermore, among active sleep loggers, average sleep was **6.99 hours** (below the 7–9 hour restorative threshold), and participants spent an average of **39 minutes awake in bed** overall (averaging 42.5 minutes across participant means) before falling asleep or getting up.
            
            **💡 Strategic Recommendation:**  
            Position the versatile *Bellabeat Leaf* (worn as a clip on sleepwear or a lightweight necklace) as the superior, jewelry-grade alternative to bulky rubber smartwatches that disrupt sleep. In the app, incentivize nighttime wear through gamified bedtime consistency streaks and offer tailored wind-down audio content—such as guided breathwork and bedtime meditations—to address the 39-to-43 minute sleep latency gap.
            """
        )
    with col_rec3_right:
        st.markdown(
            """
            **📈 Business & Marketing Rationale:**  
            Sleep duration directly governs women's hormonal health, menstrual cycle regularity, and daytime energy. Driving sleep tracking compliance from 72% toward 95%+ provides the longitudinal sleep architecture needed to deliver Bellabeat’s signature cycle-synced wellness recommendations, establishing an unmatched competitive moat against Fitbit and Apple.
            """
        )

st.markdown("---")

# -----------------------------------------------------------------------------
# Recommendation 4
# -----------------------------------------------------------------------------
with st.container():
    st.subheader("4. 'Sunday Reset' Weekend Momentum & Activity Preservation")
    st.caption("Ecosystem Area: Bellabeat Marketing Campaigns & Social Community Programs")

    col_rec4_left, col_rec4_right = st.columns([1, 1])
    with col_rec4_left:
        st.markdown(
            """
            **🔍 Key Finding:**  
            Physical activity peaks on **Tuesday (8,861 steps)** and Saturday, but plunges to a weekly trough on **Sunday (7,669 steps)**—representing a sharp **1,192-step drop** that corresponds directly with lower daily calorie expenditure and prolonged sedentary lounging.
            
            **💡 Strategic Recommendation:**  
            Launch a branded **"Sunday Reset"** campaign across the Bellabeat app and social media. Deliver motivational notifications on Friday afternoons encouraging weekend movement goals, and offer light, non-intimidating Sunday wellness activities—such as restorative nature walks, stroller strolls, or gentle restorative yoga sessions—designed to keep movement consistent without feeling like a chore.
            """
        )
    with col_rec4_right:
        st.markdown(
            """
            **📈 Business & Marketing Rationale:**  
            Habit decay disproportionately strikes on unstructured weekends. By actively guiding users through Sunday with gentle, restorative self-care content, Bellabeat flattens the weekly churn curve, keeps users engaged going into Monday, and reinforces its positioning as an empathetic lifestyle companion rather than a rigid fitness tracker.
            """
        )

st.markdown("---")

# Strategic Action Matrix
st.subheader("📋 Executive Strategic Action Matrix")
st.markdown(
    """
    | # | Strategic Initiative | Target User Segment | Ecosystem Touchpoint | Primary Success Metric |
    | :-: | :--- | :--- | :--- | :--- |
    | **1** | **Automated Non-Wear Safeguards** | All Active Users | Device Firmware & Data Sync | Reduction in false 1,440-minute sedentary records (<1%) |
    | **2** | **Midday Sedentary Micro-Nudges** | Moderate Segment (57.6%) | Bellabeat App & Spring Bottle | Shift Moderate cohort steps toward 10k (+15% step volume) |
    | **3** | **Frictionless Sleep & Wind-Down** | Non-Sleep Loggers (27.3%) | *Leaf* Jewelry + Audio Library | Sleep logging adoption from 72.7% to 90%+; lower bed latency |
    | **4** | **Sunday Reset Campaign** | Weekend Slump Users | Social Media + App Push Prompts | Narrow the 1,192-step Tuesday-to-Sunday weekend deficit |
    """
)
