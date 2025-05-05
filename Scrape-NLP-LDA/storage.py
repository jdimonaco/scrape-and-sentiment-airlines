import os
from typing import List
import pandas as pd 

# Save reviews to a file
def save_reviews_to_file(reviews: List[List[str]], filename: str = "all_reviews.txt") -> None:
  """
    Saves a list of airline reviews to a file, allowing the user to scrape and analyse reviews offline.
    Uses 'with' statement for proper file clousure and resource management.

    Steps
    -------
    - File Opening: Opens the 'all_reviews.txt'.
    - Header Writing: Creater a header for columns "Airline Name | Title | Rating | Review Text"
    - Data Writing:Iterates over the list of reviews and writes each review as a row, separating values with a pipe.
    - Loops through each review.
    - Extract Data:
        - If the review has the expected format (4 elements):
            - Extracts airline, title, rating, and review text.
            - Split the review text column to separate the review and the review verification.
            - If successful, assigns the verification status; otherwise, marks as "Not Verified".
        - If the review format is unexpected, prints a message and skips it.
    - Write the file on the expected format

    Parameters
    ----------
    reviews : A list where each review is represented as a list of strings.
    filename : The name of the file where all reviews will be saved.

    Returns
    -------
    None

    Example Usage
    -------------
    save_reviews_to_file(reviews= reviews, filename= 'all_reviews.txt')
    """

  with open(filename, "w", encoding="utf-8") as file:
    file.write("Airline Name | Title | Rating | Verified | Review_Text\n")
    file.write("\n")

    for review in reviews:
        # Handle reviews with 4 elements (missing 'verified')
        if len(review) == 4:
            airline, title, rating, review_text = review

            # Split review_text by '|' to extract verified and review_text
            split_review = review_text.split("|", 1)

            # Handle cases where split might not result in two elements
            if len(split_review) == 2:
                verified, review_text = split_review
                verified = verified.strip() # Remove leading/trailing spaces
                review_text = review_text.strip() # Remove leading/trailing spaces
            else:
                verified = "Not Verified"  # Or any default value you prefer

        else:
            print(f"Skipping review with unexpected format: {review}")
            continue  # Skip this review and continue to the next

        # Write to file
        file.write(f"{airline} | {title} | {rating} | {verified} | {review_text}\n")
    

# Reads the saved reviews file and prints the reviews
def read_and_print_reviews(filename: str = "all_reviews.txt"):
  """
    Reads and prints the contents of a saved airline reviews file.
    Verifies data storage and provides a quick review of extracted reviews.

    Steps
    -------
    - Open File: Opens 'all_reviews.txt' file in read mode.
    - Read Content: Reads the content.
    - Print: Displays the content.

    Parameters
    ----------
    filename : The name of the file to read

    Returns
    -------
    None

    Example Usage
    -------------
    read_and_print_reviews(filename= 'all_reviews.txt')
    """
  with open("all_reviews.txt", "r", encoding="utf-8") as file:
      content = file.read()
      print(content)


# Load reviews data
def load_reviews_df(file_path: str = "all_reviews.txt") -> pd.DataFrame:
    """
    Loads reviews from a text file.

    Steps
    -------
    - Open the txt file originated from the scraping code,with the specific format "|" as the delimiter.
    - Skip the header.
    - Strip spaces from the columns.

    Parameters
    ----------
    file_path : The path to the reviews text file with all reviews


    Returns
    -------
    A DataFrame containing the reviews data


    Example Usage
    -------------
    data = load_reviews_df(file_path= 'all_reviews.txt')
    """
    df = pd.read_csv("all_reviews.txt", sep="|", encoding="utf-8", skiprows=[1])
    df.columns = df.columns.str.strip()

    return df

