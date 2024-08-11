import pandas as pd
from transform_reviews import transform_reviews, assign_unique_ids
from transform_playstore import transform_playstore

# Load the data
df_reviews = pd.read_csv('csv/googleplaystore_user_reviews.csv')
df_playstore = pd.read_csv('csv/googleplaystore.csv')

# Transform the reviews and playstore DataFrames
df_transformed_reviews = transform_reviews(df_reviews)
df_transformed_playstore = transform_playstore(df_playstore)

# Drop 'app_id' columns from both DataFrames if they exist
if 'app_id' in df_transformed_reviews:
    df_transformed_reviews = df_transformed_reviews.drop(columns=['app_id'])

if 'app_id' in df_transformed_playstore:
    df_transformed_playstore = df_transformed_playstore.drop(columns=['app_id'])


df_combined = df_transformed_reviews.merge(df_transformed_playstore, on='app', how='outer')


df_combined = assign_unique_ids(df_combined, id_column_name='app_id', col='app')

df_transformed_reviews.to_csv('transformed_csv/transformed_reviews.csv', index=False)
df_transformed_playstore.to_csv('transformed_csv/transformed_playstore.csv', index=False)
df_combined.to_csv('transformed_csv/combined_playstore_reviews.csv', index=False)

print("Data transformation complete. Transformed data saved to 'transformed_reviews.csv', 'transformed_playstore.csv', and 'combined_playstore_reviews.csv'.")
