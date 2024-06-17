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
