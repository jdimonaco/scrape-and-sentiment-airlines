import os
from typing import List
from scraping import scrape_reviews_from_file, airlines

# Processes airline reviews from local HTML files
def process_airline_reviews(airline: str) -> List[List[str]]:
    """
     Processes and extracts reviews for a single airline.

     Steps
      -------
      - Format Airline Name: Converts the airline name to lowercase and replaces spaces with hyphens
      - File Path Construction: Construct the file path based on the formatted name
      - Check File Existence:
          - If file exists → Calls 'scrape_reviews_from_file' to extract reviews
          - If not exists → Prints error message
      - Label and append each extracted review with the airline name


    Returns:
    --------
    It returns a list of reviews for that specific airline.

    Example Usage
    -------------
    airlines_reviews = process_airline_reviews(airline='British Airways')
    """
    formatted_airline = airline.lower().replace(" ", "-")
    
    file_path = "data/" + formatted_airline + ".html"
                
    airline_reviews = []

    if os.path.exists(file_path):
        print(f"Extracting reviews for {airline}")

        extracted_reviews = scrape_reviews_from_file(file_path)

        for review in extracted_reviews:
            airline_reviews.append([airline] + review)
        print(f"Found reviews for {airline}: {len(extracted_reviews)}")
    else:
        print(f"File not found for {airline}")

    return airline_reviews

# Consolidates reviews from all airlines into a single list
def consolidate_reviews() -> List[List[str]]:
    """
    Consolidates into a list all the individual reviews from airlines.

    Steps
    -------
    - Iterate Airlines: Loops through the list of airlines.
    - Process Reviews: Calls the 'process_airline_reviews' function for each airline to extract reviews.
    - Extend Reviews: Adds the extracted reviews to a main list.

    Returns
    -------
    A consolidated list of all reviews for every airline.

    Example Usage
    -------------
    all_reviews = consolidate_reviews()
    """
    all_reviews = []
    for airline in airlines:
        reviews = process_airline_reviews(airline)
        all_reviews.extend(reviews)
    return all_reviews