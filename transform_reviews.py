import pandas as pd
import re

def clean_text(df):
    df_cleaned = df.copy()
    df_cleaned.columns = df_cleaned.columns.str.lower()
    str_columns = df_cleaned.select_dtypes(include='object').columns
    
    for col in str_columns:
        df_cleaned[col] = df_cleaned[col].str.lower().str.replace(' ', '_')
    
    return df_cleaned
    

def drop_nulls_and_duplicates(df, column):
    df_cleaned = df.copy()
    df_cleaned = df_cleaned.dropna(subset=[column]).copy()
    df_cleaned = df_cleaned.drop_duplicates(subset=[column]).copy()
    df_cleaned.reset_index(drop=True, inplace=True)
    
    return df_cleaned

def calculate_average_sentiment(df):
    app_sentiment_averages = df.groupby('app').agg(
        avg_sentiment_polarity=('sentiment_polarity', 'mean'),
        avg_sentiment_subjectivity=('sentiment_subjectivity', 'mean')
    ).reset_index()
    
    return app_sentiment_averages

def merge_sentiment_averages(df, sentiment_averages):
    df_merged = df.merge(sentiment_averages, on='app', how='left')
    
    return df_merged

def assign_unique_ids(df, id_column_name, col):
    df[id_column_name] = df[col].factorize()[0] + 1
    
    return df

def clean_app_names(df, column):

    df_cleaned_names = df.copy()

    def clean_name(name):

        name = name.lower()
        name = name.replace('_', ' ')
        name = re.sub(r'\s+', ' ', name)
        name = re.sub(r'[^\w\s-]', '', name)
        name = name.strip()
        return name
    
    df_cleaned_names[column] = df_cleaned_names[column].apply(clean_name)
    
    return df_cleaned_names

def transform_reviews(df):
    df_cleaned = clean_text(df)

    df_unique_reviews = drop_nulls_and_duplicates(df_cleaned, column='translated_review')

    app_sentiment_averages = calculate_average_sentiment(df_unique_reviews)
    
    df_with_averages = merge_sentiment_averages(df_unique_reviews, app_sentiment_averages)
  
    df_unique_apps = drop_nulls_and_duplicates(df_with_averages, column='app')
    
    df_cleaned_names = clean_app_names(df_unique_apps, 'app')
    
    df_final = assign_unique_ids(df_cleaned_names,'app_id','app')

    return df_final
