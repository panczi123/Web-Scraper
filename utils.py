import requests
from bs4 import BeautifulSoup
import unicodedata
import re

def get_sentences(url):
    try:
        # Attempt to fetch the content of the URL
        html_content = requests.get(url).text
    except requests.exceptions.RequestException as e:
        return None

    # Parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")
    # Extract all paragraphs
    texts = soup.find_all('p')
    if not texts:
        return None

    p_tag_list = []
    for text in texts:
        # Append the text content of each paragraph to the list
        p_tag_list.append(text.get_text())

    # Join all paragraphs into a single string
    p_tag_str = " ".join(p_tag_list)
    # Normalize unicode characters
    p_tag_str = unicodedata.normalize("NFKD", p_tag_str)
    # Replace newline characters with a space
    p_tag_str = p_tag_str.replace("\n", "")
    # Replace ellipses with a period
    p_tag_str = p_tag_str.replace("...", ".")
    # Replace tab characters with a period
    p_tag_str = p_tag_str.replace("\t", ".")
    # Replace carriage returns with a period
    p_tag_str = p_tag_str.replace("\r", ".")
    # Replace multiple spaces with a single space
    p_tag_str = re.sub(' +', ' ', p_tag_str)
    # Replace multiple periods with a single period and a space
    p_tag_str = re.sub(r'\.{2,}', '. ', p_tag_str)

    return p_tag_str
