import streamlit as st
import pandas as pd

st.set_page_config(page_title="SL Injury Predictor", layout="wide")
st.title("🏏 Sri Lanka Cricket - Injury Risk Dashboard")

# Load data
df = pd.read_csv('../data/player_workload.csv')

# Add dummy risk for demo - tarvata model predictions tho replace cheddam
df['Risk'] = ['High' if x > df['Total_Balls'].mean() else 'Low' for x in df['Total_Balls']]

st.subheader("Player Workload & Risk")
st.dataframe(df.sort_values('Total_Balls', ascending=False).head(20))

st.subheader("Risk Distribution")
st.bar_chart(df['Risk'].value_counts())

st.success("Dashboard is running!")