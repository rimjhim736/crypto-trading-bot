# main.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set up folders
os.makedirs('outputs', exist_ok=True)

# Load datasets
trader_df = pd.read_csv('"C:\Users\gunji\OneDrive\Desktop\placement\data science internship\fear_greed_index.csv"')
sentiment_df = pd.read_csv('"C:\Users\gunji\OneDrive\Desktop\placement\data science internship\historical_data.csv"')

# Preview data
print("Trader Data Sample\n", trader_df.head())
print("\nSentiment Data Sample:\n", sentiment_df.head())

# Convert date/time columns
trader_df['time'] = pd.to_datetime(trader_df['time'], errors='coerce')
trader_df['date'] = trader_df['time'].dt.date

sentiment_df['Date'] = pd.to_datetime(sentiment_df['Date'], errors='coerce')
sentiment_df['date'] = sentiment_df['Date'].dt.date

# Merge on date
merged_df = pd.merge(trader_df, sentiment_df[['date', 'Classification']], on='date', how='inner')

# Basic info
print("\nMerged Data Sample:\n", merged_df[['account', 'execution price', 'size', 'side', 'leverage', 'closedPnL', 'Classification']].head())

# Save merged data
merged_df.to_csv("csv_files/merged_data.csv", index=False)

# 1. Profitability vs Sentiment
plt.figure(figsize=(8,6))
sns.boxplot(data=merged_df, x='Classification', y='closedPnL')
plt.title('Closed PnL vs Market Sentiment')
plt.savefig('outputs/closedPnL_vs_sentiment.png')
plt.close()

# 2. Leverage vs Sentiment
plt.figure(figsize=(8,6))
sns.boxplot(data=merged_df, x='Classification', y='leverage')
plt.title('Leverage vs Market Sentiment')
plt.savefig('outputs/leverage_vs_sentiment.png')
plt.close()

# 3. Trade Size vs Sentiment
plt.figure(figsize=(8,6))
sns.boxplot(data=merged_df, x='Classification', y='size')
plt.title('Trade Size vs Market Sentiment')
plt.savefig('outputs/size_vs_sentiment.png')
plt.close()

# 4. Trade Volume by Sentiment
volume_by_sentiment = merged_df.groupby('Classification')['size'].sum().reset_index()

plt.figure(figsize=(6,6))
sns.barplot(data=volume_by_sentiment, x='Classification', y='size')
plt.title('Total Trade Volume by Sentiment')
plt.ylabel('Total Size')
plt.savefig('outputs/volume_by_sentiment.png')
plt.close()

print("✅ Analysis complete! Charts saved in `outputs/` folder and merged CSV saved in `csv_files/`.")
