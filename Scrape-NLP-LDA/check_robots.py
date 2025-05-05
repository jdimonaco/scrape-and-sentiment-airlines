import requests

# Check rules for web scraping
def check_robots() -> str:
  """
  Check rules for web scraping, ensuring compliance with ethical web scraping practices.

  Steps
  -------
  - Define a URL
  - Sends an HTTP GET request to the defined URL
  - Prints the HTTP status code and reason
  - Stores the response text
  - Prints the response

  Returns
  -------
  String with the list of what is allowed or disallowed

  Example Usage
  -------------
  check_robots()

  """
  url = "https://www.airlinequality.com/robots.txt"
  response = requests.get(url)
  print(f"{response.status_code} {response.reason}")
  text = response.text
  print(text)

check_robots()
