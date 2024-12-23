import requests
from bs4 import BeautifulSoup
import json
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def fetch_article_details(doi_link):
    """
    Fetch the abstract and posted date from the article's detail page, preserving HTML formatting.
    """
    try:
        response = requests.get(doi_link)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.warning(f"Error fetching details for {doi_link}: {e}")
        return {"abstract": "N/A", "posted_date": "N/A"}

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract abstract
    abstract_html = " ".join(
        p.text.strip() for p in soup.select("div.section.abstract p")
    ) or "N/A"

    # Extract posted date
    posted_date_section = soup.find("div", class_="pane-content", string=lambda text: text and "Posted" in text)
    posted_date = (
        posted_date_section.text
            .replace("\n","")
            .replace("\xa0", " ")
            .replace("Posted", "").strip(". ")
        if posted_date_section else "N/A"
    )

    return {"abstract": abstract_html, "posted_date": posted_date}


def scrape_biorxiv_search(query, subjects, start_date, end_date, num_results=10):
    """
    Scrape bioRxiv search results and save them to a JSON file.
    """
    
    # Format URL-encoded request
    base_url = "https://www.biorxiv.org/search/"
    formatted_query = query.replace(" ", "%20")
    formatted_subjects = "%2C".join(subjects).replace(" ", "%20")
    search_url = (
        f"{base_url}{formatted_query}%20jcode%3Abiorxiv%20subject_collection_code%3A{formatted_subjects}"
        f"%20limit_from%3A{start_date}%20limit_to%3A{end_date}%20numresults%3A{num_results}%20sort%3Arelevance-rank%20format_result%3Astandard"
    )

    # Send GET request to bioRxiv
    try:
        response = requests.get(search_url)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching search results: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("span.highwire-cite-title")

    results = {}
    for article in articles:
        try:
            # Extract title
            title = article.text.strip() or "N/A"

            # Extract link to the article
            link_tag = article.find("a", href=True)
            link = link_tag["href"] if link_tag else "N/A"
            pdf_link = f"https://www.biorxiv.org{link}.full.pdf"

            # Extract DOI 
            metadata = article.find_next("div", class_="highwire-cite-metadata")
            doi_tag = metadata.find("span", class_="highwire-cite-metadata-doi") if metadata else None
            doi = doi_tag.text.split("doi:")[-1].strip() if doi_tag else "N/A"
            

            # Extract authors
            authors_tag = article.find_next("div", class_="highwire-cite-authors")
            authors = authors_tag.text.strip() if authors_tag else "N/A"
            

            # Use DOI as a unique key to avoid duplicates
            if doi not in results:
                
                article_details = fetch_article_details(doi)
                
                results[doi] = {
                    "title": title,
                    "authors": authors,
                    "doi": doi,
                    "pdf_link": pdf_link,
                    "abstract": article_details["abstract"],
                    "posted": article_details["posted_date"]
                }
                
        except Exception as e:
            logging.warning(f"Error parsing article data: {e}")
            continue

    return [results[key] for key in results.keys()]

def get_monthly_date_ranges(past_year=True):
    """Generate monthly date ranges for the past year."""
    end_date = datetime.today().replace(day=1) if past_year else datetime.today()
    start_date = end_date - timedelta(days=365)

    date_ranges = []
    current_date = start_date

    while current_date < end_date:
        month_start = current_date.replace(day=1)
        next_month = month_start + timedelta(days=31)
        month_end = (next_month - timedelta(days=next_month.day)).date()
        date_ranges.append((month_start.date(), month_end))
        current_date = next_month

    return date_ranges

def fetch_monthly_articles(query, subjects, results_per_month=3):
    """Fetch articles for each month in the past year."""
    date_ranges = get_monthly_date_ranges()
    all_articles = []

    for start_date, end_date in date_ranges:
        logging.info(f"Fetching articles for {start_date} to {end_date}...")
        articles = scrape_biorxiv_search(query, subjects, str(start_date), str(end_date), num_results=results_per_month)
        all_articles.extend(articles)

    return all_articles

def save_articles_to_json(articles, output_path):
    """Save articles to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(articles, json_file, indent=4, ensure_ascii=False)

    logging.info(f"Results saved to {output_path}")
    
# Parameters

scopes=[
    # "Animal Behavior and Cognition",   
    "Biochemistry",
    "Bioengineering",  
    "Bioinformatics",  
    "Biophysics",  
    "Cancer Biology",  
    "Cell Biology",
    # "Developmental Biology",   
    # "Ecology", 
    # "Evolutionary Biology",
    "Genetics",
    "Genomics",
    "Immunology",  
    # "Microbiology",
    "Molecular Biology",   
    "Neuroscience",
    # "Paleontology",
    "Pathology",   
    "Pharmacology and Toxicology", 
    "Physiology",  
    # "Plant Biology",   
    "Scientific Communication and Education",  
    "Synthetic Biology",   
    "Systems Biology", 
    # "Zoology", 
]
query = "mathematical model OR dynamical systems OR systems biology OR sensitivity analysis OR machine learning"
subjects = scopes
results_per_month = 3
output_path = "./assets/biorxiv.json"

articles = fetch_monthly_articles(query, subjects, results_per_month=results_per_month)

if articles:
    print(f"Found {len(articles)} unique articles from the past year. Results saved.")
    save_articles_to_json(articles, output_path)
else:
    print("No articles found.")