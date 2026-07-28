import pandas as pd

# 1. Manam create chesina workload file ni chaduvudam
df = pd.read_csv(r"C:\Users\user\Desktop\SL_Injury_Project\data\player_workload.csv")

# 2. Risk Score calculate cheddam
df['Risk_Score'] = df['Total_Balls'] / 100

# 3. Risk Level categorize cheddam
def get_risk_level(score):
    if score < 5:
        return 'Low'
    elif score < 15:
        return 'Medium'
    else:
        return 'High'

df['Risk_Level'] = df['Risk_Score'].apply(get_risk_level)

# 4. Ekkuva risk unna vallani top lo pettadam
df = df.sort_values('Risk_Score', ascending=False)

# 5. Nitish unda leda check cheddam
print("\n--- ALL PLAYERS IN DATA ---")
for player in df['player'].unique():
    if 'Nitish' in player or 'Reddy' in player:
        print("Found:", player)
print("---------------------------\n")

# 6. Save cheyyadam
df.to_csv(r"C:\Users\user\Desktop\SL_Injury_Project\data\injury_risk_report.csv", index=False)

print("✅ Injury Risk Report Ready!")
print(df.head(10))