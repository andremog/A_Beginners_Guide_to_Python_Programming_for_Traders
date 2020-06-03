# A Beginners Guide to Python Programming for Traders
# Chapter 7 - RSI Edges Case Study
# Copy and paste this code into a jupyter notebook
# Hit ctl + enter to run

import talib as ta
import pandas as pd
import matplotlib.pyplot as plt

security = 'SPY'         # Security to inspect
rsi_lookback = 4         # Number of days for RSI Lookback
start_date='2003-01-01'
end_date='2020-05-29'

# Step 1 - Grab Data for the Security in Question
df = get_pricing(security, start_date, end_date, frequency='daily')

# Step 2 - Make a new column which calculates the RSI value for every day in our sample
df['rsi'] = ta.RSI(df['close_price'], rsi_lookback)
df.dropna(inplace=True)

# Step 3 - Make a new column displaying the future 3-day percent changes
df['future_3_day_close'] = df['close_price'].shift(-3)
df['future_3_day_pct_ch'] = df['future_3_day_close'].pct_change(3)
df.dropna(inplace=True)

# Step #4 - Use Boolean filtering to filter create buckets (new dataframes) using different RSI readings
all_days = df['future_3_day_pct_ch'].mean() * 100
bucket_1 = df[df['rsi']<=10]['future_3_day_pct_ch'].mean() * 100
bucket_2 = df[(df['rsi']>10) & (df['rsi']<=20)]['future_3_day_pct_ch'].mean() * 100
bucket_3 = df[(df['rsi']>20) & (df['rsi']<=30)]['future_3_day_pct_ch'].mean() * 100
bucket_4 = df[(df['rsi']>30) & (df['rsi']<=40)]['future_3_day_pct_ch'].mean() * 100
bucket_5 = df[(df['rsi']>40) & (df['rsi']<=50)]['future_3_day_pct_ch'].mean() * 100
bucket_6 = df[(df['rsi']>50) & (df['rsi']<=60)]['future_3_day_pct_ch'].mean() * 100
bucket_7 = df[(df['rsi']>60) & (df['rsi']<=70)]['future_3_day_pct_ch'].mean() * 100
bucket_8 = df[(df['rsi']>70) & (df['rsi']<=80)]['future_3_day_pct_ch'].mean() * 100
bucket_9 = df[(df['rsi']>80) & (df['rsi']<=90)]['future_3_day_pct_ch'].mean() * 100
bucket_10 = df[(df['rsi']>90)]['future_3_day_pct_ch'].mean() * 100

# Step #5 - Observe the future 3-day percent changes given the different RSI values
final_df = pd.DataFrame({'Average Future Percent Change':[all_days,bucket_1,bucket_2,bucket_3,bucket_4,
                                                          bucket_5,bucket_6,bucket_7,bucket_8,bucket_9,bucket_10]},
            index=['All Days','<10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','>90'])

ax = final_df.plot(kind='bar')
#plt.ylabel('Future Percent Change', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
vals = ax.get_yticks()/100
ax.set_yticklabels(['{:,.2%}'.format(y) for y in vals])
plt.legend(fontsize=15)
plt.suptitle('Average 3-day Future Percent Returns for Different RSI-'+ str(rsi_lookback) +' Buckets', fontsize=20)
plt.title(security + ": " + start_date + " - " + end_date, fontsize=20)
plt.grid(b=True, which='major', color='k', linestyle='-')
plt.grid(b=True, which='minor', color='r', linestyle='-', alpha=0.2)
plt.minorticks_on()
plt.show()
