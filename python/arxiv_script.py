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

years_ago = 10
years_ago_datetime = (datetime.now() - timedelta(days=years_ago*365)).strftime('%Y%m%d')
today = datetime.now().strftime('%Y%m%d')

date_filter = f"submittedDate:[{years_ago_datetime} TO {today}]"

query = f"({' OR '.join(keywords)}) AND ({categories}) AND {date_filter}"

# Output Directory and filename
output_dir = "./assets/"  
output_file = "articles.json"  
output_path = os.path.join(output_dir, output_file)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# ArXiv client
client = arxiv.Client()

# Search query
search = arxiv.Search(
    query=query,
    max_results=20,
    sort_by=arxiv.SortCriterion.Relevance,
)

# Articles
articles = []

for result in client.results(search):
    article_info = {
        'title': format_latex(result.title),
        'year': result.published.strftime("%B %Y"),  # Format the date
        'date': result.published.strftime("%Y-%m-%d"), # for sorting
        'authors': ", ".join([str(author) for author in result.authors]),  # Convert authors to strings
        'abstract': format_latex(result.summary),
        'link': result.pdf_url
    }
    articles.append(article_info)

# Sort articles by the formatted date in descending order
sorted_articles = sorted(articles, key=lambda x: x['date'], reverse=True)

# Save articles to JSON file
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(sorted_articles, json_file, indent=4, ensure_ascii=False)