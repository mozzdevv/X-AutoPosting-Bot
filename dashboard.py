import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="X AutoBot Dashboard", layout="wide")

LOG_FILE = "bot_activity.json"
HISTORY_FILE = "posted_history.json"

st.title("🤖 X AutoBot Dashboard")
st.caption("Monitoring @SaasSexy98662")

col1, col2 = st.columns(2)

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

# --- Stats ---
history = load_data(HISTORY_FILE)
logs = load_data(LOG_FILE)

# Scheduler State
scheduler_state = {}
if os.path.exists("scheduler_state.json"):
    with open("scheduler_state.json", "r") as f:
        scheduler_state = json.load(f)

total_posted = len(history)

with col1:
    st.metric("Total Posts", total_posted)
    if scheduler_state.get("next_run"):
        next_dt = datetime.fromisoformat(scheduler_state["next_run"])
        st.info(f"⏰ Next Post Attempt: **{next_dt.strftime('%H:%M:%S')}**")

with col2:
    recent_rejections = len([l for l in logs[:20] if l.get('status') == 'rejected'])
    st.metric("Recent Rejection Rate", f"{(recent_rejections/20)*100:.0f}%" if logs else "0%")

st.divider()

# --- Activity Log ---
st.subheader("📋 Activity Log")

if logs:
    df_logs = pd.DataFrame(logs)
    
    # Reorder columns primarily
    cols = ['timestamp', 'type', 'status', 'score', 'reason', 'content']
    # Filter only existing cols
    cols = [c for c in cols if c in df_logs.columns]
    
    st.dataframe(df_logs[cols], use_container_width=True)
else:
    st.info("No activity logs found yet. Run the bot to see data.")

st.divider()

# --- Posted History ---
st.subheader("✅ Posted History")
if history:
    # Reverse to show newest first
    for item in reversed(history[-10:]):
        with st.container():
            st.markdown(f"**{item.get('timestamp', '')}** ({item.get('type')})")
            st.code(item.get('content'))
else:
    st.text("No posts yet.")
    
# --- Manual Trigger ---
st.sidebar.header("Controls")
if st.sidebar.button("Refresh Data"):
    st.rerun()

st.sidebar.info("To run the bot manually, use the terminal: `python main_bot.py`")
