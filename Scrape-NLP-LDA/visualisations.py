import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud

# Generate Word Clouds for Sentiment
def generate_word_clouds(df_positive: pd.DataFrame, df_negative: pd.DataFrame, df_neutral: pd.DataFrame) -> None:
    """
    Generates and displays word clouds for positive, negative, and neutral reviews.
    """
    positive_reviews = ' '.join(df_positive['Clean_Review'])
    negative_reviews = ' '.join(df_negative['Clean_Review'])
    neutral_reviews = ' '.join(df_neutral['Clean_Review'])

    wordcloud_positive = WordCloud(width=800, height=500, random_state=42, max_font_size=100).generate(positive_reviews)
    wordcloud_negative = WordCloud(width=800, height=500, random_state=42, max_font_size=100).generate(negative_reviews)
    wordcloud_neutral = WordCloud(width=800, height=500, random_state=42, max_font_size=100).generate(neutral_reviews)

    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud_positive, interpolation='bilinear')
    plt.axis('off')
    plt.title("Positive Reviews Word Cloud")
    plt.show()

    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud_negative, interpolation='bilinear')
    plt.axis('off')
    plt.title("Negative Reviews Word Cloud")
    plt.show()

    plt.figure(figsize=(15, 8))
    plt.imshow(wordcloud_neutral, interpolation='bilinear')
    plt.axis('off')
    plt.title("Neutral Reviews Word Cloud")
    plt.show()

# Plot Polarity vs Subjectivity
def plot_polarity_subjectivity(df: pd.DataFrame) -> None:
    """Plot polarity vs subjectivity of the reviews."""
    plt.figure(figsize=(8,6))
    plt.scatter(df["Polarity"], df["Subjectivity"], color='blue')
    plt.title("Sentiment Analysis: Polarity vs Subjectivity")
    plt.xlabel("Polarity")
    plt.ylabel("Subjectivity")
    plt.show()

# Plot Sentiment Counts
def plot_sentiment_counts(df: pd.DataFrame) -> None:
    """Create a bar chart to visualise the sentiment distribution."""
    plt.figure(figsize=(8,6))
    df['Sentiment'].value_counts().plot(kind='bar')
    plt.title('Sentiment Av.nalysis')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.show()  
    
# Sentiment vs. Airline
def plot_sentiment_by_airline(data: pd.DataFrame):
    """Creates a boxplot of review polarity for each airline."""
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Airline Name', y='Polarity', data=data)
    plt.title('Sentiment Distribution by Airline')
    plt.xlabel('Airline')
    plt.ylabel('Polarity')
    plt.xticks(rotation=45, ha='right')
    plt.show()

# Calculate average rating for each airline (all reviews)
def plot_average_rating_by_airline(data: pd.DataFrame):
    """
    Computes average ratings overall and for negative reviews, then displays a grouped bar chart.
    """
    data = data.copy()
    data['Rating'] = pd.to_numeric(data['Rating'], errors='coerce')

    overall_ratings = data.groupby('Airline Name')['Rating'].mean().reset_index()
    overall_ratings['Rating_Type'] = 'Overall Average'

    negative_reviews = data[data['Sentiment'] == 'Negative']
    negative_ratings = negative_reviews.groupby('Airline Name')['Rating'].mean().reset_index()
    negative_ratings['Rating_Type'] = 'Negative Average'

    all_ratings = pd.concat([overall_ratings, negative_ratings])

    plt.figure(figsize=(12, 6))
    sns.barplot(x='Airline Name', y='Rating', hue='Rating_Type', data=all_ratings, palette={'Overall Average': 'blue', 'Negative Average': 'slategrey'})  # Specify palette
    plt.title('Average Rating vs. Negative Average Rating by Airline')
    plt.xlabel('Airline')
    plt.ylabel('Average Rating')
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Rating Type')
    plt.show()


# Create a bar plot
def plot_delay_keywords(delay_keywords_df: pd.DataFrame):
    """
    Plots a bar chart showing delay- and cancellation-related keyword counts by airline.
    """
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Airline Name', y='Delay_Keyword_Count', data=delay_keywords_df, color='blue')
    plt.title('Frequency of Delay-Related Keywords by Airline')
    plt.xlabel('Airline')
    plt.ylabel('Count of Delay Keywords')
    plt.xticks(rotation=45, ha='right')
    plt.show()