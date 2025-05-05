from prefect import task, flow
import pandas as pd
import os

# Import functions from your modules
from check_robots import check_robots
from scraping import download_airline_reviews
from processing import consolidate_reviews
from storage import save_reviews_to_file, read_and_print_reviews, load_reviews_df
from nlp import nlp_pipeline, create_sentiment_dataframes, analyse_verification_status,\
                calculate_sentiment_percentage,analyse_delays
from visualisations import generate_word_clouds, plot_sentiment_counts, plot_polarity_subjectivity, \
                         plot_sentiment_by_airline, plot_average_rating_by_airline, plot_delay_keywords
from topic_modelling import preprocess_for_topic_modelling, apply_lda_model, visualise_lda_topics


# Wrap key steps as Prefect tasks
os.makedirs("data", exist_ok=True)

# Prefect Tasks

@task
def task_check_robots() -> str:
    """Task: Check robots.txt and return its content."""
    return check_robots()

@task
def task_download_reviews() -> None:
    """Task: Download HTML pages for all airlines."""
    download_airline_reviews()

@task
def task_consolidate_reviews() -> list:
    """Task: Consolidate reviews from the downloaded HTML files."""
    return consolidate_reviews()

@task
def task_save_reviews(reviews: list) -> None:
    """Task: Save the consolidated reviews to a text file."""
    save_reviews_to_file(reviews, filename="all_reviews.txt")  # 'data/' prefix is handled in storage.py

@task
def task_load_reviews_df() -> pd.DataFrame:
    """Task: Load the saved reviews into a DataFrame."""
    return load_reviews_df("data/all_reviews.txt")

@task
def task_apply_nlp(df: pd.DataFrame) -> pd.DataFrame:
    """Task: Clean the review text and apply sentiment analysis."""
    return nlp_pipeline(df, review_column="Review_Text")

@task
def task_create_sentiment_dataframes(df: pd.DataFrame) -> tuple:
    """Task: Create separate DataFrames for each sentiment category."""
    return create_sentiment_dataframes(df)

@task
def task_calculate_sentiment_percentage(df_positive: pd.DataFrame, df_negative: pd.DataFrame,
                                        df_neutral: pd.DataFrame, df: pd.DataFrame) -> None:
    """Task: Calculate sentiment percentages."""
    calculate_sentiment_percentage(df_positive, df_negative, df_neutral, df)

@task
def task_analyse_verification(df: pd.DataFrame) -> None:
    """Task: Analyse the verification status of reviews."""
    analyse_verification_status(df)

@task
def task_analyse_delays(df: pd.DataFrame) -> pd.DataFrame:
    """Task: Identify keywords relating to delays and cancellations in negative reviews."""
    return analyse_delays(df)    

@task
def task_visualisation(df_positive: pd.DataFrame, df_negative: pd.DataFrame,
                             df_neutral: pd.DataFrame, df: pd.DataFrame) -> None:
    """Task: Visualise sentiment analysis results."""
    generate_word_clouds(df_positive, df_negative, df_neutral)
    plot_polarity_subjectivity(df)
    plot_sentiment_counts(df)
    plot_sentiment_by_airline(df)
    plot_average_rating_by_airline(df)
    delay_keywords_df = task_analyse_delays(df_negative)
    plot_delay_keywords(delay_keywords_df)

@task
def task_topic_modelling(df: pd.DataFrame) -> None:
    """Task: Perform topic modelling on the cleaned reviews."""
    dictionary, corpus = preprocess_for_topic_modelling(df)
    lda_model = apply_lda_model(corpus, dictionary, num_topics=5)
    visualise_lda_topics(lda_model, corpus, dictionary)


# Prefect Flow

@flow
def main_flow() -> None:
    """
    Main Prefect flow for scraping, processing and analysing airline reviews.

    Steps
    ------
    1. Check site permissions
    2. Download HTML pages for reviews
    3. Extract and consolidate reviews
    4. Save and reload as a DataFrame
    5. Apply NLP and sentiment analysis
    6. Analyse delay keywords
    7. Visualise results
    8. Perform topic modelling

    """
    # Step 1: Check robots.txt
    task_check_robots()

    # Step 2: Download reviews
    task_download_reviews()

    # Step 3: Consolidate reviews
    reviews = task_consolidate_reviews()
    task_save_reviews(reviews)

    # Step 4: Load reviews into a DataFrame
    read_and_print_reviews("data/all_reviews.txt")
    df = task_load_reviews_df()

    # Step 5: Apply NLP and sentiment analysis
    df_processed = task_apply_nlp(df)
    task_analyse_verification(df_processed)
    df_positive, df_negative, df_neutral = task_create_sentiment_dataframes(df_processed)

    # Step 6: Analyse delay keywords
    delay_keywords_df = task_analyse_delays(df_negative)

    # Step 7: Visualise results
    task_visualisation(df_positive, df_negative, df_neutral, df_processed)

    # Step 8: Perform topic modelling
    task_topic_modelling(df_processed)

    # Print delay keywords DataFrame for debugging
    print(delay_keywords_df)


# Entry point
if __name__ == "__main__":
    main_flow()