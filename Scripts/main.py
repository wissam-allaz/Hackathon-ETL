import pandas as pd
from transform_reviews import transform_reviews
from transform_playstore import transform_playstore


df_reviews = pd.read_csv('csv/googleplaystore_user_reviews.csv')
df_playstore = pd.read_csv('csv/googleplaystore.csv')


df_transformed_reviews = transform_reviews(df_reviews)
df_transformed_reviews.to_csv('transformed_reviews.csv', index=False)

print("Data transformation complete. Transformed data saved to 'transformed_reviews.csv'.")


df_transformed_playstore = transform_playstore(df_playstore)
df_transformed_reviews.to_csv('transformed_playstore.csv', index=False)

print("Data transformation complete. Transformed data saved to 'transformed_reviews.csv'.")

