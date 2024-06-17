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
#print(monthly_trends)


daily_trends = df.groupby('cpd_dt').size().reset_index(name='Transaction_Count')
#print(daily_trends)


# Category-Based Trends - Merchant Category Code, Name

category_trends_code = df.groupby('mrch_catg_cd').size().reset_index(name='Transaction_Count')
#print(category_trends_code)

category_trends_name = df.groupby('mrch_catg_rlup_nm').size().reset_index(name='Transaction_Count')
#print(category_trends_name)


# Geographical Trends - City, Country

city_trends = df.groupby('city_name').size().reset_index(name='Transaction_Count')
#print(city_trends)

country_trends = df.groupby('country_code').size().reset_index(name='Transaction_Count')
#print(country_trends)


# Trends - Cluster & Merchant

cluster_trends = df.groupby('cluster_name_adjusted').size().reset_index(name='Transaction_Count')
#print(cluster_trends)

merchant_trends = df.groupby('merchant').size().reset_index(name='Transaction_Count')
#print(merchant_trends)


# Flag-Based Trends - CP, Domestic, Intraregion, Interregion

cp_flag_trends = df.groupby('cp_flag').size().reset_index(name='Transaction_Count')
#print(cp_flag_trends)

domestic_flag_trends = df.groupby('domestic_flag').size().reset_index(name='Transaction_Count')
#print(domestic_flag_trends)

intraregion_flag_trends = df.groupby('intraregion_flag').size().reset_index(name='Transaction_Count')
#print(intraregion_flag_trends)

interregion_flag_trends = df.groupby('interregion_flag').size().reset_index(name='Transaction_Count')
#print(interregion_flag_trends)


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