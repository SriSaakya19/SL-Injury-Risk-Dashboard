import streamlit as st
import pandas as pd

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
    # Ikkada Total_Balls kuda accept chesthundi
    if 'workload' in col.lower() or 'load' in col.lower() or 'balls' in col.lower():
        workload_col = col

# Columns dorikaya check
if not player_col or not workload_col:
    st.error(f"❌ CSV lo 'Player' and 'Workload/Total_Balls' columns undali. Nuvvu unna columns: {list(df.columns)}")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")
players = st.sidebar.multiselect("Player select cheyyi", df[player_col].unique(), default=df[player_col].unique()[:3])

if not players:
    st.warning("Oka player aina select cheyyi")
    st.stop()

filtered_df = df[df[player_col].isin(players)]

# Main Dashboard
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Player Data")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    st.subheader("📈 Workload Trend")
    if date_col:
        chart_data = filtered_df.pivot_table(index=date_col, columns=player_col, values=workload_col)
        st.line_chart(chart_data)
    else:
        chart_data = filtered_df.groupby(player_col)[workload_col].sum()
        st.bar_chart(chart_data)

# Risk Alert
st.subheader("⚠️ Injury Risk Alert")
threshold = 100  # nuvvu ee number marchukovachu
high_risk = filtered_df[filtered_df[workload_col] > threshold]

if not high_risk.empty:
    st.warning(f"⚠️ {len(high_risk)} records lo high workload > {threshold} kanipinchindi")
    st.dataframe(high_risk[[player_col, workload_col]])
else:
    st.success("✅ All players are in safe workload zone")

st.markdown("---")
st.caption("Built with Streamlit for SL Cricket Team")