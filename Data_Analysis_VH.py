import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


file_path = "Enter your csv path here"
data = pd.ExcelFile(file_path)


#print(data.sheet_names)

df = pd.read_excel(file_path, sheet_name='2_Card data')

#print(df.head())
#print(df.describe())

#print(df.isnull().sum())
df['cpd_dt'] = pd.to_datetime(df['cpd_dt'])


# Time-Based Trends : Monthly & Daily Trends
monthly_trends = df.groupby('cpd_mnth_id').size().reset_index(name='Transaction_Count')
daily_trends = df.groupby('cpd_dt').size().reset_index(name='Transaction_Count')



# Category-Based Trends - Merchant Category Code, Name
category_trends_code = df.groupby('mrch_catg_cd').size().reset_index(name='Transaction_Count')
category_trends_name = df.groupby('mrch_catg_rlup_nm').size().reset_index(name='Transaction_Count')


# Geographical Trends - City, Country
city_trends = df.groupby('city_name').size().reset_index(name='Transaction_Count')
country_trends = df.groupby('country_code').size().reset_index(name='Transaction_Count')


# Trends - Cluster & Merchant
cluster_trends = df.groupby('cluster_name_adjusted').size().reset_index(name='Transaction_Count')
merchant_trends = df.groupby('merchant').size().reset_index(name='Transaction_Count')


# Flag-Based Trends - CP, Domestic, Intraregion, Interregion
cp_flag_trends = df.groupby('cp_flag').size().reset_index(name='Transaction_Count')
domestic_flag_trends = df.groupby('domestic_flag').size().reset_index(name='Transaction_Count')
intraregion_flag_trends = df.groupby('intraregion_flag').size().reset_index(name='Transaction_Count')
interregion_flag_trends = df.groupby('interregion_flag').size().reset_index(name='Transaction_Count')



# Plot monthly trends
plt.figure(figsize=(10, 6))
sns.lineplot(x='cpd_mnth_id', y='Transaction_Count', data=monthly_trends)
plt.title('Monthly Transaction Trends')
plt.xlabel('Month')
plt.ylabel('Transaction Count')
plt.show()

# Plot daily trends
plt.figure(figsize=(10, 6))
sns.lineplot(x='cpd_dt', y='Transaction_Count', data=daily_trends)
plt.title('Daily Transaction Trends')
plt.xlabel('Date')
plt.ylabel('Transaction Count')
plt.show()