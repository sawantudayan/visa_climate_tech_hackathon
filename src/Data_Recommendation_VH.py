import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel files for both datasets
file_path_dataset1 = file_path_dataset2 = "Enter the Path to the dataset"  # Make sure the path is correct


df_dataset1 = pd.read_excel(file_path_dataset1, sheet_name='2_Card data')
df_dataset2 = pd.read_excel(file_path_dataset2, sheet_name='3_Open banking data')


# Display the first few rows of each dataset to understand the data structure
print("Dataset 1:")
print(df_dataset1.head())

print("\nDataset 2:")
print(df_dataset2.head())





# Convert date columns to datetime for both datasets
df_dataset1['cpd_dt'] = pd.to_datetime(df_dataset1['cpd_dt'])
df_dataset2['Value.dates.booked'] = pd.to_datetime(df_dataset2['Value.dates.booked'])

# Fill missing values in both datasets
df_dataset1.fillna(0, inplace=True)
df_dataset2.fillna(0, inplace=True)

# Trend Analysis

# 1. Time-Based Trends
# Monthly trends based on 'cpd_mnth_id' from dataset 1
monthly_trends_dataset1 = df_dataset1.groupby('cpd_mnth_id').size().reset_index(name='Transaction_Count')

# Daily trends based on 'cpd_dt' from dataset 1
daily_trends_dataset1 = df_dataset1.groupby('cpd_dt').size().reset_index(name='Transaction_Count')

# Monthly trends based on 'Value.dates.booked' from dataset 2
monthly_trends_dataset2 = df_dataset2.groupby(df_dataset2['Value.dates.booked'].dt.to_period('M')).size().reset_index(name='Transaction_Count')

# Daily trends based on 'Value.dates.booked' from dataset 2
daily_trends_dataset2 = df_dataset2.groupby(df_dataset2['Value.dates.booked'].dt.date).size().reset_index(name='Transaction_Count')


# 2. Category-Based Trends

# Trends by 'mrch_catg_rlup_nm' from dataset 1
category_trends_dataset1 = df_dataset1.groupby('mrch_catg_rlup_nm').size().reset_index(name='Transaction_Count')

# Trends by 'mrch_catg_rlup_nm2' from dataset 2
category_trends_dataset2 = df_dataset2.groupby('mrch_catg_rlup_nm2').size().reset_index(name='Transaction_Count')



# 3. Cluster and Merchant Trends
# Trends by 'cluster_name_adjusted' from both datasets
cluster_trends_dataset1 = df_dataset1.groupby('cluster_name_adjusted').size().reset_index(name='Transaction_Count')
cluster_trends_dataset2 = df_dataset2.groupby('cluster_name_adjusted').size().reset_index(name='Transaction_Count')

# Optionally, visualize the trends using matplotlib or seaborn

# Recommendation Algorithms

# Create user-item matrix for collaborative filtering using dataset 1
user_item_matrix_dataset1 = df_dataset1.pivot_table(index='cpd_mnth_id', columns='mrch_catg_rlup_nm', values='Value.amount', aggfunc='sum', fill_value=0)

# Collaborative Filtering using Cosine Similarity for dataset 1
cosine_sim_dataset1 = cosine_similarity(user_item_matrix_dataset1)
user_sim_matrix_dataset1 = pd.DataFrame(cosine_sim_dataset1, index=user_item_matrix_dataset1.index, columns=user_item_matrix_dataset1.index)

def get_collaborative_recommendations(user_id, user_sim_matrix, user_item_matrix, n_recommendations=5):
    similar_users = user_sim_matrix[user_id].sort_values(ascending=False).index[1:]
    similar_user_items = user_item_matrix.loc[similar_users]
    item_scores = similar_user_items.sum().sort_values(ascending=False)
    recommendations = item_scores.index[:n_recommendations]
    return recommendations

# Create user-item matrix for collaborative filtering using dataset 2
# Modify this based on the structure of dataset 2
user_item_matrix_dataset2 = df_dataset2.pivot_table(index='Value.accountId', columns='Category', values='amount', aggfunc='sum', fill_value=0)

# Collaborative Filtering using Cosine Similarity for dataset 2
cosine_sim_dataset2 = cosine_similarity(user_item_matrix_dataset2)
user_sim_matrix_dataset2 = pd.DataFrame(cosine_sim_dataset2, index=user_item_matrix_dataset2.index, columns=user_item_matrix_dataset2.index)

# Content-Based Filtering for dataset 2
# Modify this based on the features available in dataset 2
item_features_dataset2 = df_dataset2[['mrch_catg_rlup_nm2', 'Value.amount.currencyCode', 'amount', 'Category']]
item_features_dataset2 = pd.get_dummies(item_features_dataset2)

# Calculate cosine similarity between items for dataset 2
item_cosine_sim_dataset2 = cosine_similarity(item_features_dataset2)
item_sim_matrix_dataset2 = pd.DataFrame(item_cosine_sim_dataset2, index=item_features_dataset2.index, columns=item_features_dataset2.index)

def get_content_based_recommendations(item_id, item_sim_matrix, n_recommendations=5):
    similar_items = item_sim_matrix[item_id].sort_values(ascending=False).index[1:n_recommendations+1]
    return similar_items

# Hybrid Recommendation Approach for dataset 2
def get_hybrid_recommendations(user_id, user_sim_matrix, user_item_matrix, item_sim_matrix, n_recommendations=5):
    collaborative_recs = get_collaborative_recommendations(user_id, user_sim_matrix, user_item_matrix, n_recommendations)
    hybrid_recs = []
    for item_id in collaborative_recs:
        content_recs = get_content_based_recommendations(item_id, item_sim_matrix, n_recommendations)
        hybrid_recs.extend(content_recs)
    hybrid_recs = list(set(hybrid_recs))  # Remove duplicates
    return hybrid_recs[:n_recommendations]

# Example usage for dataset 1
user_id = 123  # Replace with actual user ID
collaborative_recs_dataset1 = get_collaborative_recommendations(user_id, user_sim_matrix_dataset1, user_item_matrix_dataset1)
print("Collaborative Recommendations (Dataset 1):", collaborative_recs_dataset1)

# Example usage for dataset 2
user_id = 'user_123'  # Replace with actual user ID from dataset 2
hybrid_recs_dataset2 = get_hybrid_recommendations(user_id, user_sim_matrix_dataset2, user_item_matrix_dataset2, item_sim_matrix_dataset2)
print("Hybrid Recommendations (Dataset 2):", hybrid_recs_dataset2)
