from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.parse import urljoin, urlparse
import pandas as pd
import utils

def remove_unwanted_links(links, extensions):
    # Remove links that end with unwanted extensions
    return [link for link in links if not any(link.endswith(ext) for ext in extensions)]

def process_links(parent_links, extensions):
    child_links = []
    parent_sentences = []

    for plink in parent_links:
        try:
            req = Request(plink)
            html_page = urlopen(req)
            soup = BeautifulSoup(html_page, "lxml")

            # Extract sentences from the parent link
            parent_sentences_str = utils.get_sentences(plink)
            parent_sentences.append(parent_sentences_str)

            child_link_temp = []

            # Find all links in the current parent page
            for link in soup.findAll('a'):
                href = link.get('href')
                if href and href.strip():
                    full_url = urljoin(plink, href)
                    # Only add the link if it is a valid full URL
                    if urlparse(full_url).netloc:
                        child_link_temp.append(full_url)

            # Remove unwanted links and ensure there are no duplicates
            child_link_temp = remove_unwanted_links(child_link_temp, extensions)
            child_links.append(list(set(child_link_temp)))

        except Exception as e:
            print(f"Error opening the page: {plink}")
            print(f"Error message: {e}")

    return child_links, parent_sentences

def process_child_links(child_links):
    child_sentences = []
    for chlink_group in child_links:
        for subchlink in chlink_group:
            # Extract sentences from each child link
            child_sentences_str = utils.get_sentences(subchlink)
            child_sentences.append(child_sentences_str)
    return child_sentences

def scrape_links():
    # Read the parent links from the CSV file
    df = pd.read_csv('csv_links.csv')
    parent_links = df['Website'].tolist()
    extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg']

    # Process the parent links to get child links and parent sentences
    child_links, parent_sentences = process_links(parent_links, extensions)
    # Process the child links to get child sentences
    child_sentences = process_child_links(child_links)

    return parent_links, child_links, parent_sentences, child_sentences
