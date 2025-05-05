import requests
import os
from bs4 import BeautifulSoup
import time
from typing import List

# List of specific airlines
airlines = [ "British Airways", "Lufthansa", "Emirates", "Qatar", "Singapore Airlines",
            "American Airlines"]

# Defining the url of the site
base_url = "https://www.airlinequality.com/airline-reviews/{airline}/"

# Download and save HTML files for individual airline review pages
def download_airline_reviews() -> None:
    """
    Downloads the HTML content of individual airline review pages and saves them locally.

    Steps
    -------
    - Format Airline Name: Converts the airline name to lowercase and replaces spaces with hyphens.
    - Construct URL: Inserts the formatted airline name into the base URL.
    - Send HTTP Requesst: Sends a GET request to download the HTML content.
    - Check response:
      -  If request is successful (code == 200) → Saves the HTML content named after the formatted airline.
      -  If not successful → Prints error message and the status code.

    This refined approach targets individual review pages rather than extracting reviews from a single aggregated page,
    ensuring accurate data collection for each airline.

    Returns
    -------
    None

    Example Usage
    -------------
    download_airline_reviews()
    """

    for airline in airlines:
        formatted_airline = airline.lower().replace(" ", "-")
        url = base_url.replace("{airline}", formatted_airline)

        response = requests.get(url)
        if response.status_code == 200:
            print(f"Downloading HTML for {airline}")

            with open(f"data/{formatted_airline}.html", "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"HTML file saved for {airline}")
        else:
            print(f"Failed to retrieve HTML for {airline} (Status code: {response.status_code})")

# Scrape reviews from the extracted file
def scrape_reviews_from_file(file_path: str, max_reviews: int = 20) -> List[List[str]]:
    """
   Extracts airline reviews from an HTML file.
    A 5-second delay is introduced between iterations to comply with ethical web scraping practices.

    Steps
    -------
    - Open the specified HTML file with UTF-8 encoding.
    - Parse the file's content using BeautifulSoup.
    - Finds all <article> tags with class 'comp_media-review-rated'.
    - For each review (up to 'max_reviews'):
        - Extracts the title from <h2> tag, or return "No Title" if missing..
        - Extracts the rating (first character from a <div> with class "rating-10", or "No Rating").
        - Extract the review text from the <div> with class "text_content" (or "No Review").
    - Append the extracted data into a list.

    Parameters
    ----------
    file_path : The path to the HTML file.
    max_reviews : Maximum number of reviews to extract.

    Returns
    -------
    A list of reviews, where each review is a list: [Airline Name, title, rating, review_text].

    Example Usage
    -------------
    reviews = scrape_reviews_from_file(file_path='british-airways.html', max_reviews=20)
    """
    reviews = []

    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        articles = soup.find_all("article", class_="comp_media-review-rated")

        for article in articles[:max_reviews]:
            time.sleep(5)

            title_element = article.find("h2")
            title = title_element.text if title_element else "No Title"

            rating_element = article.find("div", class_="rating-10")
            rating = rating_element.text.strip()[0] if rating_element and rating_element.text.strip() else "No Rating"

            review_text_element = article.find("div", class_="text_content")
            review_text = review_text_element.text if review_text_element else "No Review"

            reviews.append([title, rating, review_text])
    return reviews

