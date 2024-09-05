# Overview
This project is an ETL (Extract, Transform, Load) pipeline developed for a hackathon project. It uses Python to extract, transform, and combine data from the Playstore dataset and Playstore reviews dataset. The combined dataset is provided in the transformed_csv folder for further use by the web development team.

## Features
Modularized ETL process with individual scripts for Playstore data (transform_playstore.py) and Playstore reviews data (transform_reviews.py).
Combines Playstore and Playstore reviews datasets into a unified dataset stored as combined_playstore_reviews.csv.
Structured CSV outputs for both transformed Playstore and reviews data.

## Scripts
main.py: Entry point to run the ETL pipeline, orchestrating the extraction, transformation, and loading steps.
transform_playstore.py: Handles extraction and transformation of Playstore dataset (googleplaystore.csv).
transform_reviews.py: Handles extraction and transformation of Playstore reviews dataset (googleplaystore_user_reviews.csv).

## Datasets
csv/googleplaystore.csv: Raw Playstore dataset.
csv/googleplaystore_user_reviews.csv: Raw Playstore reviews dataset.
transformed_csv/: Contains the cleaned and transformed Playstore, reviews, and combined datasets.

## Requirements
Python 3.x
Pandas library (for data processing)
