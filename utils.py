import requests
from bs4 import BeautifulSoup
import unicodedata
import re

def get_sentences(url):
        try:
                html_content = requests.get(url).text
        except requests.exceptions.RequestException as e:
                return None

        soup = BeautifulSoup(html_content, "html.parser")
        texts = soup.find_all('p')
        if not texts:
                return None

        p_tag_list = []
        for text in texts:
                p_tag_list.append(text.get_text())

        p_tag_str = " ".join(p_tag_list)
        p_tag_str = unicodedata.normalize("NFKD", p_tag_str)
        p_tag_str = p_tag_str.replace("\n", "")
        p_tag_str = p_tag_str.replace("...", ".")
        p_tag_str = p_tag_str.replace("\t", ".")
        p_tag_str = p_tag_str.replace("\r", ".")
        p_tag_str = re.sub(' +', ' ', p_tag_str)
        p_tag_str = re.sub(r'\.{2,}', '. ', p_tag_str)

        return p_tag_str