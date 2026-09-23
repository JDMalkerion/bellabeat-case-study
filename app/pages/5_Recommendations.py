"""
Strategic Recommendations Page for Bellabeat.
Placeholder for Day 3 marketing copy, business recommendations, and product features.
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

st.title("💡 Strategic Recommendations & Marketing Playbook")
st.markdown(
    "Data-driven business recommendations for Bellabeat executives, marketing leadership, and product teams."
)
st.markdown("---")

st.info("📌 **Day 3 Strategic Roadmap Placeholder**: The full executive copy, tactical messaging, and product rollout roadmap will be drafted during Day 3.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎯 1. Target Audience & Growth Strategy")
    st.markdown(
        """
        - **Target the Moderate Segment (57.6% of Cohort)**:
          - *Placeholder*: Tailor messaging around realistic incremental progress rather than extreme athletic feats.
        - **Weekend Activity Dropoff Interventions**:
          - *Placeholder*: Design Friday afternoon motivational prompts to maintain consistency over the weekend.
        - **Empowering Women's Holistic Health**:
          - *Placeholder*: Connect cycle-tracking insights with daily activity and recovery suggestions.
        """
    )

    st.subheader("⏱️ 2. Inactive Time & Sedentary Habit Interventions")
    st.markdown(
        """
        - **Smart Sedentary Alerts (Combatting the 16.5-Hour Sedentary Day)**:
          - *Placeholder*: Gentle vibration or mobile nudge after 50 continuous minutes of daytime inactivity.
        - **Micro-Movement Breaks**:
          - *Placeholder*: Quick 2-to-3 minute desk stretches and posture check-ins.
        """
    )

with col2:
    st.subheader("🌙 3. Sleep Latency & Bedtime Wind-Down")
    st.markdown(
        """
        - **Addressing the 39-Minute Awake-in-Bed Gap**:
          - *Placeholder*: In-app guided breathwork, evening journaling, and progressive muscle relaxation.
        - **Bedtime Consistency Rewards**:
          - *Placeholder*: Streak gamification for hitting target sleep onset times.
        """
    )

    st.subheader("⌚ 4. Device Wear Compliance & Ecosystem Positioning")
    st.markdown(
        """
        - **Preventing Tracker Abandonment (8.4% Non-Wear Days)**:
          - *Placeholder*: Battery recharge reminders and discreet clip/jewelry wear options (Bellabeat Leaf).
        - **Subscription & Premium Monetization**:
          - *Placeholder*: Personalized wellness reports connecting sleep, stress, and physical exertion.
        """
    )
