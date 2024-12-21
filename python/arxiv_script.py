import json
import os
import re
import arxiv
from datetime import datetime, timedelta

# Function to replace LaTeX equation delimiters
def format_latex(text):
    # Replace "$$ ... $$" with "\[ ... \]"
    text = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', text, flags=re.DOTALL)
    # Replace "$ ... $" with "\( ... \)"
    text = re.sub(r'\$(.+?)\$', r'\\(\1\\)', text, flags=re.DOTALL)
    # Replace double backslashes for JSON encoding
    return text

# Query term
keywords = [
    "mathematical model",
    "machine learning",
    "dynamical systems",
    "mathematical biology",
#    "mathematics education", 
    "recreational mathematics", 
    "communication of mathematics"
]

categories = "cat:q-bio OR cat:cs.LG OR cat:math.DS OR math.AP OR math.CA OR math.HO"

today = datetime.now().strftime('%Y%m%d')

# Define time ranges
time_ranges = {
    "last_month": (datetime.now() - timedelta(days=30)).strftime('%Y%m%d'),
    "last_year": (datetime.now() - timedelta(days=365)).strftime('%Y%m%d'),
    "last_5_years": (datetime.now() - timedelta(days=5*365)).strftime('%Y%m%d'),
    "all_time": "19900101"  # Arbitrary early date for all-time search
}

# Output Directory and filename
output_dir = "./assets/"  
output_file = "articles.json"  
output_path = os.path.join(output_dir, output_file)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# ArXiv client
client = arxiv.Client()

# Function to fetch articles for a given time range
def fetch_articles(time_range_start, max_results):
    date_filter = f"submittedDate:[{time_range_start} TO {today}]"
    query = f"({' OR '.join(keywords)}) AND ({categories}) AND {date_filter}"
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    articles = []
    for result in client.results(search):
        article_info = {
            'title': format_latex(result.title),
            'year': result.published.strftime("%B %Y"),
            'date': result.published.strftime("%Y-%m-%d"),
            'authors': ", ".join([str(author) for author in result.authors]),
            'abstract': format_latex(result.summary),
            'link': result.pdf_url
        }
        articles.append(article_info)
    return articles

# Fetch articles for each time range
articles_by_range = {
    "last_month": fetch_articles(time_ranges["last_month"], 5),
    "last_year": fetch_articles(time_ranges["last_year"], 5),
    "last_5_years": fetch_articles(time_ranges["last_5_years"], 5),
    "all_time": fetch_articles(time_ranges["all_time"], 5)
}

# Save articles to JSON file
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(articles_by_range, json_file, indent=4, ensure_ascii=False)