import arxiv
import json
import os
import re

# Function to replace LaTeX equation delimiters
def format_latex(text):
    # Replace "$$ ... $$" with "\[ ... \]"
    text = re.sub(r'\$\$(.+?)\$\$', r'\\[\1\\]', text, flags=re.DOTALL)
    # Replace "$ ... $" with "\( ... \)"
    text = re.sub(r'\$(.+?)\$', r'\\(\1\\)', text, flags=re.DOTALL)
    # Replace double backslashes for JSON encoding
    return text

# Query term
query = "mathematical biology"

# Directory and filename to save the output
output_dir = "../assets/"  # Specify your desired directory
output_file = "articles.json"  # Specify your desired filename
output_path = os.path.join(output_dir, output_file)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Initialize the arXiv client
client = arxiv.Client()

# Define the search query
search = arxiv.Search(
    query=query,
    max_results=20,
    sort_by=arxiv.SortCriterion.Relevance
)

# Collect articles into a list
articles = []

for result in client.results(search):
    article_info = {
        'title': format_latex(result.title),
        'year': result.published.strftime("%B %Y"),  # Format the date
        'authors': ", ".join([str(author) for author in result.authors]),  # Convert authors to strings
        'abstract': format_latex(result.summary),
        'link': result.pdf_url
    }
    articles.append(article_info)

# Save articles to JSON file
with open(output_path, 'w', encoding='utf-8') as json_file:
    json.dump(articles, json_file, indent=4, ensure_ascii=False)