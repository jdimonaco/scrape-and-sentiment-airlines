import re
import string
from typing import List, Tuple
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')

# Data Cleaning 

# Global stopwords set
STOPWORDS = set(stopwords.words('english'))

# Remove Stop Words
def cleaning_stopwords(text: str) -> str:
    """Remove common stopwords from the text."""
    return " ".join([word for word in text.split() if word.lower() not in STOPWORDS])

# Remove Punctuation
def cleaning_punctuations(text: str) -> str:
    """Remove punctuation characters from the text."""
    return text.translate(str.maketrans('', '', string.punctuation))

# Remove Repeating Characters
def cleaning_repeating_chars(text: str) -> str:
    """Reduce repeated characters (e.g., 'soooo' becomes 'so')."""
    return re.sub(r'(.)\1+', r'\1', text)

# Remove URLs
def cleaning_urls(text: str) -> str:
    """Remove URLs from the text."""
    return re.sub(r'https?://\S+|www\.\S+', '', text)

# Remove Numbers
def cleaning_numbers(text: str) -> str:
    """Remove numbers from the text."""
    return re.sub(r'\d+', '', text)

# Remove Short words
def remove_short_words(text: str) -> str:
    """Remove words that are 2 characters or fewer."""
    return " ".join(word for word in text.split() if len(word) > 2)

# Tokenize Text
def tokenize_text(text: str) -> List[str]:
    """Tokenize the text using TweetTokenizer."""
    tokenizer = TweetTokenizer()
    return tokenizer.tokenize(text)

# Apply Stemming
def apply_stemming(tokens: List[str]) -> List[str]:
    """Apply stemming to a list of tokens."""
    stemmer = PorterStemmer()
    return [stemmer.stem(token) for token in tokens]

# Apply Lemmatization
def apply_lemmatization(tokens: List[str]) -> List[str]:
    """Apply lemmatization to a list of tokens."""
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(token) for token in tokens]

# Apply each step of text preprocessing
def process_tokens(text: str) -> str:
    """
    Tokenizes the text, then applies stemming and lemmatization
    Returns the processed text as a single string

    Steps
    -----
    - Tokenize the input text using the 'tokenize_text' function.
    - Apply stemming to the tokens using the 'apply_stemming' function.
    - Apply lemmatization to the tokens using the 'apply_lemmatization' function.
    - Join the processed tokens into a single string and return it.

    Parameters
    ----------
    The text to be processed

    Returns
    -------
    The text as a single string with tokens that have been stemmed and lemmatized
    """
    tokens = tokenize_text(text)
    tokens = apply_stemming(tokens)
    tokens = apply_lemmatization(tokens)
    return " ".join(tokens)

# Apply each step of text cleaning, including preprocessing
def full_cleaning(text: str) -> str:
    """
    Applies a sequence of cleaning steps to the text

    Steps
    -----
      - Remove stopwords.
      - Remove punctuation.
      - Remove repeating characters.
      - Remove URLs.
      - Remove numbers.
      - Remove very short words.
      - Tokenize, then apply stemming and lemmatization.
    Returns the fully cleaned text.

    Parameters
    ----------
    The  text to be fully cleaned

    Returns
    -------
    The cleaned text
    """
    text = cleaning_stopwords(text)
    text = cleaning_punctuations(text)
    text = cleaning_repeating_chars(text)
    text = cleaning_urls(text)
    text = cleaning_numbers(text)
    text = remove_short_words(text)
    text = process_tokens(text)
    return text

# Sentiment Analysis 

# Get Subjectivity Score
def get_subjectivity(text: str) -> float:
    """
    Returns the subjectivity score of the text using TextBlob
    These are the personal opinions, feelings, and beliefs of the
    individual who created the text.
    """
    return TextBlob(text).sentiment.subjectivity

# Get Polarity Score
def get_polarity(text: str) -> float:
    """
    Returns the polarity score of the text using TextBlob
    This is a measure of how positive or negative the text is
    """
    return TextBlob(text).sentiment.polarity

# Get Sentiment Label
def get_sentiment_label(score: float) -> str:
    """Classifies sentiment based on polarity score"""
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

# NLP Pipeline
def nlp_pipeline(df: pd.DataFrame, review_column: str = "Review_Text") -> pd.DataFrame:
    """
    This function ensure the whole pipeline is applied to the reviews

    Steps
    -------
    - Calls the full_cleaning function to clean the review text, tokenizes and processes tokens (stemming and lemmatization).
    - Calls the get_subjectivity function to compute the subjectivity of the text.
    - Calls the get_polarity function to compute the polarity of the text.
    - Classifies the sentiment.

    Parameters
    ----------
    The input DataFrame containing review data

    Returns
    -------
    The original DataFrame with new columns

    Example Usage
    -------------
    processed_data = nlp_pipeline(data= data, review_column='Review_Text')
    """
    df["Clean_Review"] = df[review_column].apply(full_cleaning)
    df["Subjectivity"] = df["Clean_Review"].apply(get_subjectivity)
    df["Polarity"] = df["Clean_Review"].apply(get_polarity)
    df["Sentiment"] = df["Polarity"].apply(get_sentiment_label)
    return df

# Create DataFrames for Positive, Negative, and Neutral Reviews
def create_sentiment_dataframes(df: pd.DataFrame):
    """Create separate DataFrames for positive, negative, and neutral reviews."""
    df_positive = df[df['Sentiment'] == 'Positive']
    df_negative = df[df['Sentiment'] == 'Negative']
    df_neutral = df[df['Sentiment'] == 'Neutral']
    return df_positive, df_negative, df_neutral

# Calculate and Display Sentiment Percentages
def calculate_sentiment_percentage(df_positive: pd.DataFrame, df_negative: pd.DataFrame, df_neutral: pd.DataFrame, df: pd.DataFrame) -> None:
    """Calculate and display the percentage of positive, negative, and neutral reviews."""
    positive_percentage = round((df_positive.shape[0] / df.shape[0]) * 100, 1)
    negative_percentage = round((df_negative.shape[0] / df.shape[0]) * 100, 1)
    neutral_percentage = round((df_neutral.shape[0] / df.shape[0]) * 100, 1)
    
    print(f"Positive Reviews: {positive_percentage}%")
    print(f"Negative Reviews: {negative_percentage}%")
    print(f"Neutral Reviews: {neutral_percentage}%")

# Analyse Verification Status
def analyse_verification_status(data: pd.DataFrame) -> None:
    """
    Analyses the verification status of reviews and prints the distribution.

    Steps
    -----
    - Calculate the total number of reviews.
    - Count the number of verified and non-verified reviews.
    - Calculate the percentage of verified and non-verified reviews.
    - Print the verification status.
    - Check non-verified reviews among negative sentiment

    Parameters
    ----------
    The DataFrame containing the reviews

    Returns
    -------
    None

    Example Usage
    -------------
    analyse_verification_status(processed_data)
    """
    total_reviews = len(data)
    verified_reviews = data['Verified'].value_counts().get('✅ Trip Verified', 0)
    non_verified_reviews = data['Verified'].value_counts().get('Not Verified', 0)
    verified_percentage = round((verified_reviews / total_reviews) * 100, 1)
    non_verified_percentage = round((non_verified_reviews / total_reviews) * 100, 1)
    
    print("\nVerification Status Distribution:")
    print(f"Total Reviews: {total_reviews}")
    print(f"Verified Reviews: {verified_reviews} ({verified_percentage}%)")
    print(f"Non-Verified Reviews: {non_verified_reviews} ({non_verified_percentage}%)")
    
    negative_reviews = data[data['Sentiment'] == 'Negative']
    negative_non_verified = negative_reviews[negative_reviews['Verified'] == 'Not Verified']
    negative_non_verified_percentage = round((len(negative_non_verified) / len(negative_reviews)) * 100, 1)
    
    print("\nNon-Verified Reviews Among Negative Sentiment:")
    print(f"Total Negative Reviews: {len(negative_reviews)}")
    print(f"Non-Verified Negative Reviews: {len(negative_non_verified)} ({negative_non_verified_percentage}%)")
    
# Analyse Delays
def analyse_delays(data):
    """
    Analyses delays and cancellations within the review data,
    focusing on negative sentiment and counting delay keywords per airline.

    Steps
    -----
        - Define a list of keywords.
        - Filter the DataFrame to include only reviews with negative sentiment.
        - Create a dictionary to store the count of delay keywords for each airline.
        - Iterate through the negative reviews and count the delay keywords for each airline.
        - Update the dictionary with the keyword counts.
        - Convert the dictionary into a DataFrame with airlines and their delay keyword counts.

    Parameters
    ----------
     The DataFrame containing processed reviews.

    Returns
    -------
    A DataFrame with airlines and their delay keyword counts.

    Example Usage
    -------------
    analyse_data(data= data)
    """
    delay_keywords = ["delay", "delayed", "late", "cancellation", "cancelled"]
    df_negative = data[data['Sentiment'] == 'Negative']

    airline_keyword_counts = {}

    for index, row in df_negative.iterrows():
        airline = row['Airline Name']
        review_text = row['Clean_Review'].lower()

        keyword_count = sum(1 for keyword in delay_keywords if keyword in review_text.split())

        airline_keyword_counts.setdefault(airline, 0)  
        airline_keyword_counts[airline] += keyword_count

    result_df = pd.DataFrame(list(airline_keyword_counts.items()), columns=['Airline Name', 'Delay_Keyword_Count'])

    return result_df
        


