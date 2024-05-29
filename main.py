import requests
from bs4 import BeautifulSoup

from converter.converter import html_to_epub


class NoAr5ivCache(Exception):
    pass
def download_html(url, file_name='download.html'):
    response = requests.get(url)

    if response.status_code == 200:
        # with open(file_name, 'wb') as f:
        #     f.write(response.content)
        return response.content
    else:
        raise NoAr5ivCache

def download_website_assets(url):
    html_content = download_html(url)
    if not html_content:
        return None
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img')
    images = {}
    for img in img_tags:
        img_url = img.get('src')
        if not img_url:
            continue
        if 'ar5iv' in img_url:
            continue
        img_url = requests.compat.urljoin(url, img_url)
        if not 'http' in img_url:
            continue
        img_response = requests.get(img_url)
        if img_response.status_code == 200:
            images[img_url] = img_response.content
    return html_content, images

def get_author(url):
    soup = BeautifulSoup(download_html(url), 'html.parser')
    authors_div = soup.find('div', class_='authors')

    # Get the first child a tag text
    try:
        if authors_div:
            authors = authors_div.find_all('a')
            first_author_last_name = authors[0].text.split(' ')[-1]
            if len(authors) > 1:
                return first_author_last_name + ' et al.'
            else:
                return first_author_last_name
    except:
        return 'Unknown'

def get_title(url):
    soup = BeautifulSoup(download_html(url), 'html.parser')
    title = soup.find('h1', class_='title').text
    return title.replace("Title:", '')

def convert_latex_source_to_xml(url):
    return ""

def arxiv_to_paper(arxiv_link):
    assert "arxiv" in arxiv_link

    title = get_title(arxiv_link)
    author = get_author(arxiv_link)
    html_content = ""
    try:
        website_data = download_website_assets("https://ar5iv.labs.arxiv.org/html/" + arxiv_link.split('/')[-1])
    # need to get images too
    except NoAr5ivCache:
        website_data = convert_latex_source_to_xml(arxiv_link)

    html_to_epub(website_data,title, author)


link = "https://arxiv.org/abs/2403.09611"
arxiv_to_paper(link)
