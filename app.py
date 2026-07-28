import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="SL Injury Risk Dashboard", layout="wide")
st.title("🏏 Sri Lanka Cricket - Injury Risk Dashboard")
st.markdown("---")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/player_workload.csv')
        # Columns lo space teesi, proper case ki marchadam
        df.columns = df.columns.str.strip().str.title()
        return df
    except FileNotFoundError:
        st.error("❌ 'data/player_workload.csv' file dorakaledu. GitHub lo 'data' folder unda check cheyyi.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Debug: CSV lo em columns unnayo chupiddam
st.info(f"CSV lo dorikina columns: {list(df.columns)}")

# Column names auto detect cheddam
player_col = None
date_col = None  
workload_col = None

for col in df.columns:
    if 'player' in col.lower() or 'name' in col.lower():
        player_col = col
    if 'date' in col.lower():
        date_col = col
    if 'workload' in col.lower() or 'load' in col.lower():
        workload_col = col

# Columns dorikaya check
if not player_col or not workload_col:
    st.error(f"❌ CSV lo 'Player' and 'Workload' columns undali. Nuvvu unna columns: {list(df.columns)}")
    st.stop()

# Sidebar
st.sidebar.header("Filters")
players = st.sidebar.multiselect("Player select cheyyi", df[player_col].unique(), default=df[player_col].unique()[:3])

filtered_df = df[df[player_col].isin(players)]

# Main Dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Player Data")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    st.subheader("📈 Workload Trend")
    if date_col:
        for player in players:
            player_data = filtered_df[filtered_df[player_col] == player]
            chart_data = player_data.set_index(date_col)[workload_col]
            st.line_chart(chart_data)
    else:
        st.bar_chart(filtered_df.set_index(player_col)[workload_col])

# Risk Alert
st.subheader("⚠️ Injury Risk Alert")
if workload_col:
    high_risk = filtered_df[filtered_df[workload_col] > 100]  # 100 threshold - nuvvu marchukovachu
    if not high_risk.empty:
        st.warning(f"⚠️ {len(high_risk)} records lo high workload kanipinchindi")
    else:
        st.success("✅ All players are in safe workload zone")

st.markdown("---")
st.caption("Built with Streamlit for SL Cricket Team")