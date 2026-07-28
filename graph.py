import pandas as pd
import matplotlib.pyplot as plt

# 1. Injury risk report ni chaduvudam
df = pd.read_csv(r"C:\Users\user\Desktop\SL_Injury_Project\data\injury_risk_report.csv")

# 2. Top 10 High Risk players ni teeskundam
top10 = df.head(10)

# 3. Bar graph create cheddam
plt.figure(figsize=(10,6))
plt.bar(top10['player'], top10['Risk_Score'], color='red')

plt.title('Top 10 Players - Injury Risk Score', fontsize=14, fontweight='bold')
plt.xlabel('Player Name')
plt.ylabel('Risk Score')
plt.xticks(rotation=45, ha='right')  # names tilted ga
plt.tight_layout()

# 4. Save cheyyadam
plt.savefig(r"C:\Users\user\Desktop\SL_Injury_Project\data\risk_graph.png")
plt.show()

print("✅ Graph saved as risk_graph.png")