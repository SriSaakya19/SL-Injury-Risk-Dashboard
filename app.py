import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="SL Cricket Injury Dashboard", 
    page_icon="🏏",
    layout="wide"
)

st.title("🏏 Sri Lanka Cricket - Injury Risk Dashboard")
st.markdown("Monitor player workload and prevent injuries with data-driven insights")

@st.cache_data
def load_data():
    df = pd.read_csv('data/player_workload.csv')
    df.columns = df.columns.str.strip().str.title()
    return df

df = load_data()

player_col = None
workload_col = None
for col in df.columns:
    if 'player' in col.lower() or 'name' in col.lower():
        player_col = col
    if 'workload' in col.lower() or 'load' in col.lower() or 'balls' in col.lower():
        workload_col = col

# Key Metrics
st.subheader("Key Stats")
col1, col2, col3 = st.columns(3)
col1.metric("Total Players", df[player_col].nunique())
col2.metric("Total Records", len(df))
col3.metric("High Risk Records", len(df[df[workload_col] > 100]))

st.markdown("---")

# Sidebar
st.sidebar.header("Filters")
players = st.sidebar.multiselect("Select Players", df[player_col].unique(), default=df[player_col].unique()[:3])
filtered_df = df[df[player_col].isin(players)]

# Main Dashboard
col1, col2 = st.columns(2)
with col1:
    st.subheader("📊 Player Data")
    st.dataframe(filtered_df, use_container_width=True)

with col2:
    st.subheader("📈 Workload per Player")
    chart_data = filtered_df.groupby(player_col)[workload_col].sum()
    fig, ax = plt.subplots()
    colors = ['red' if x > 100 else '#1f77b4' for x in chart_data]
    ax.bar(chart_data.index, chart_data.values, color=colors)
    ax.set_ylabel('Total Balls Bowled')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

# Risk Alert
st.subheader("⚠️ Injury Risk Alert")
threshold = 100
high_risk = filtered_df[filtered_df[workload_col] > threshold]
if not high_risk.empty:
    st.warning(f"⚠️ {len(high_risk)} records found with high workload > {threshold}")
    st.dataframe(high_risk)
else:
    st.success("✅ All players are in safe workload zone")

st.markdown("---")

# About Section
with st.expander("About This Dashboard"):
    st.write("""
    **Purpose**: This dashboard helps Sri Lanka Cricket coaching staff monitor player workload to reduce injury risk.
    
    **How it works**: 
    - Red bars indicate players with workload > 100 balls - high injury risk
    - Use filters to focus on specific players
    - Review risk alerts to take preventive action
    
    **Built by**: SAKYA using Python, Pandas, Streamlit
    """)

st.caption("Built for SL Cricket Team | Deployed on Streamlit Cloud")