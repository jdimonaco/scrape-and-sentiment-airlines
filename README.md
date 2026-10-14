✈️ **Airline Review Sentiment & Delay Analysis**

📌 **Project Overview**

This project explores how passenger reviews can reveal patterns in airline performance and customer satisfaction. Using web scraping and natural language processing (NLP), it extracts and analyses online airline reviews to identify common issues such as delays, cancellations, and poor service.

By examining passenger sentiment and feedback, the project aims to provide insights into the recurring challenges faced by travellers and to highlight differences in performance across airlines.

🎯 **Objectives**

- Identify airlines known for reliable operational performance.

- Leverage sentiment data to assess airline service quality.

- Extract delay-related themes and keywords from passenger reviews.


📦 **Scope**

- Collect public reviews via web scraping from the Airline Quality Reviews website.

- Process and analyse review content using NLP techniques.

- Perform sentiment classification, delay keyword detection, and topic modelling.

- Visualise insights to highlight airline performance strengths and weaknesses.


💡 **Value of the Project**

- Understand common causes of airline service issues from a passenger perspective.

- Identify patterns in delays, cancellations, and customer dissatisfaction.

- Highlight differences in airline performance using real-world feedback.

- Provide data-driven insights for researchers, policy makers, or frequent flyers.

- Support transparency and accountability in the aviation industry.


🔍**Data Sources**

- Primary Source: Airline passenger reviews scraped from AirlineQuality.com.

- While direct cargo customer feedback is limited, passenger reviews provide actionable insights into airline reliability, punctuality, and service quality.

⚙️ **Project Workflow**

1. **Data Collection**
- Web scraping using requests and BeautifulSoup to gather public reviews.

2. **Data Processing**
- Text cleaning: stopword and punctuation removal, tokenisation, stemming and lemmatisation (used for word clouds and topic modelling).

- Sentiment analysis using TextBlob on the original review text to classify reviews (positive, negative, neutral).

- Delay-related keyword extraction and frequency analysis.

- Extraction of polarity and subjectivity scores.

3. **Visualisations**
- Word clouds of frequently used terms.

- Sentiment distribution plots by airline.

- Delay keyword frequency comparison across airlines.

- Average rating and sentiment plots by airline.

- LDA topic modelling to surface common themes in the reviews.

4. **Results & Insights**

Based on 60 reviews (the 10 reviews on each of 6 airlines' first review page):

- 73% of reviews were positive and 27% negative.

- Qatar Airways had the highest average rating (8.4/10) and the most positive sentiment; Emirates and Lufthansa had the lowest average rating (3.7/10), and half of Emirates' reviews were negative.

- Delay and cancellation keywords in negative reviews were most frequent for American Airlines (5 mentions), followed by Lufthansa (3) and Emirates (2).

- 80% of reviews were verified trips; 44% of the negative reviews came from non-verified reviewers.

- Topic modelling grouped the reviews around seat comfort and cabin class, onboard service, and boarding and service issues.

- With 10 reviews per airline, these findings are indicative rather than conclusive.

📊 **Future Work**
- Integrate additional sources (e.g., TripAdvisor) to reduce bias and validate trends.

- Upgrade sentiment analysis with transformer-based models (e.g., BERT, GPT) for more accurate tone detection.

- Automate scraping and NLP pipeline for near real-time monitoring.

- Deploy insights in a dashboard format for airline partner performance tracking.

▶️ **How to Run**

Clone the repository:
git clone https://github.com/jdimonaco/scrape-and-sentiment-airlines.git
cd scrape-and-sentiment-airlines

Move into the project folder and install requirements:
cd Scrape-NLP-LDA
pip install -r requirements.txt

Run the full analysis pipeline:
python main.py

✅ **Ethical Considerations**
- This project adheres to responsible and ethical data collection and analysis practices:

- Website Terms Reviewed: The Airline Quality website’s robots.txt and terms of service were checked prior to scraping to ensure compliance with ethical scraping guidelines.

- No PII Collected: Personally identifiable information (e.g., passenger names or locations) was intentionally excluded from scraping and analysis to protect user privacy.

- Data Minimisation: Only review text and general metadata (e.g., airline name, star rating) were extracted to serve the analytical purpose.

- Non-Commercial Use: This is a research-only project with no intent to monetise or republish any data.

- Responsible Disclosure: The project maintainer is open to addressing concerns from data owners. If an issue arises, it will be reviewed and resolved promptly.

⚠️ **Disclaimer**
This repository is intended solely for academic and research purposes. It is not affiliated with or endorsed by any airline or review platform.

All data was collected from publicly available sources.

No attempt has been made to distribute or monetise any scraped data.

All trademarks and content belong to their respective owners.

If you are a data owner and have concerns about the use of your content, please contact the project maintainer to address the issue.

