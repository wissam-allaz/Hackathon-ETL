import pandas as pd
import re

def clean_text(df):
    df_cleaned = df.copy()
    df_cleaned.columns = df_cleaned.columns.str.lower()
    str_columns = df_cleaned.select_dtypes(include='object').columns
    
    for col in str_columns:
        df_cleaned[col] = df_cleaned[col].str.lower().str.replace(' ', '_')
    
    return df_cleaned

def clean_col_names(df, column):

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

def drop_nulls_and_duplicates(df, column):
    df_cleaned = df.copy()
    df_cleaned = df_cleaned.dropna(subset=[column]).copy()
    df_cleaned = df_cleaned.drop_duplicates(subset=[column]).copy()
    df_cleaned.reset_index(drop=True, inplace=True)
    
    return df_cleaned


def create_id_column(df, col, new_id_col):
    unique_names = df[col].unique()
    app_id_mapping = {name: idx + 1 for idx, name in enumerate(unique_names)}
    df[new_id_col] = df[col].map(app_id_mapping)
    cols = [new_id_col] + [col for col in df.columns if col not in [new_id_col]]
    df = df[cols]
    return df

def convert_int(number, characters):
    try:
        for char in characters:
            number = number.replace(char, '')
        return int(float(number))  
    except ValueError:
        return None  

def convert_column_to_int(df, column_name, characters):
    df[column_name] = df[column_name].apply(lambda x: convert_int(x, characters))
    return df


def convert_float(number, characters):
    try:
        for char in characters:
            number = number.replace(char, '')
        return float(number)
    except ValueError:
        return float('nan')

def convert_column_to_float(df, column_name, characters):
    df[column_name] = df[column_name].apply(lambda x: convert_float(x, characters))
    return df


def convert_int_with_suffix(number):
    try:
        number = number.strip().lower()
        
        if 'm' in number:
            number = number.replace('m', '')
            return int(float(number) * 1_000_000)  
        elif 'k' in number:
            number = number.replace('k', '')
            return int(float(number) * 1_000)  
        else:
            return int(float(number)) 
    except ValueError:
        return None 

def convert_column_to_int_suffix(df, column_name):
    df[column_name] = df[column_name].apply(lambda x: convert_int_with_suffix(x))
    return df

def map_type_in_place(df, type_col):
    type_mapping = {'free': 0, 'paid': 1}
    df[type_col] = df[type_col].map(type_mapping)


def normalize_and_encode_ratings(df,column_name):    
    rating_labels = {
        'unrated': 0,
        'everyone': 1,
        'everyone_10+': 2,
        'teen': 3,
        'mature_17+': 4,
        'adults_only_18+': 5
    }
    df['content_rating_label'] = df[column_name].map(rating_labels).fillna(-1)
    df['content_rating_label']=df['content_rating_label'].astype('int')
    return df

def clean_date(date_str):
    try:
        cleaned_date = date_str.replace('_', ' ').replace(',', '')
        return pd.to_datetime(cleaned_date, format='%B %d %Y', errors='coerce')
    except Exception as e:
        print(f"Error processing date: {date_str} - {e}")
        return pd.NaT 
    

def transform_playstore(df):
    df_cleaned_text = clean_text(df)
    df_cleaned_names = clean_col_names(df_cleaned_text,'app')
    df_unique_apps = drop_nulls_and_duplicates(df_cleaned_names, 'app')
    df_unique_apps = df_unique_apps.drop(df_unique_apps[df_unique_apps['category'] == '1.9'].index)
    df_unique_apps = df_unique_apps.reset_index(drop=True)
    df_cleaned_categories = clean_col_names(df_unique_apps, 'category')
    df_unique_cat = create_id_column(df_cleaned_categories,'category', 'category_id')
    df_cleaned_genres = clean_col_names(df_unique_apps, 'genres')
    df_unique_subcategory = create_id_column(df_cleaned_genres,'genres', 'genres_id')
    average_rating = df_unique_subcategory['rating'].mean()
    df_unique_subcategory['rating'] = df_unique_subcategory['rating'].fillna(average_rating)
    df_unique_subcategory['rating'] = df_unique_subcategory['rating'].round(1)
    df_reviews_to_int = convert_column_to_int(df_unique_subcategory, 'reviews', [])
    df_installs_to_int = convert_column_to_int(df_reviews_to_int, 'installs', [',', '+'])
    df_installs_to_int = df_installs_to_int.drop(df_installs_to_int[df_installs_to_int['size'] == 'varies_with_device'].index)
    df_size_to_int = convert_column_to_int_suffix(df_installs_to_int,'size')
    map_type_in_place(df_size_to_int, 'type')
    df_size_to_int.drop(df_size_to_int[df_size_to_int['type'] == '0'].index, inplace=True)
    df_cleaned_price = convert_column_to_float(df_size_to_int, 'price', ['$'])
    df_normalized_rating = normalize_and_encode_ratings(df_cleaned_price, 'content rating')
    df_normalized_rating['last updated'] = df_normalized_rating['last updated'].apply(clean_date)
    df_final = create_id_column(df_normalized_rating,'app', 'app_id')
    return df_final
