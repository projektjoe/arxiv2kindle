from bs4 import BeautifulSoup
import os
import shutil
import zipfile

from converter.html_elems import get_mimetype, get_container_xml, get_package_opf, get_epub_css, get_common_itr_css, \
    get_chapter_content, get_title_page, table_of_contents
id_to_section = {}
def remove_numbers_spaces_special_chars(input_string):
    # Remove numbers, spaces, special characters, and convert to lowercase
    result = ''.join(e for e in input_string if e.isalpha()).lower()
    return result
def section_needs_math(soup):
    return len(soup.find_all('math'))
def add_name_to_annotation_xml(soup):
    ann_elems = soup.find_all('annotation-xml')
    for ann_elem in ann_elems:
        if 'xmlns' not in ann_elem.attrs:
            ann_elem['name'] = "contentequiv"
    return soup
def add_xmlns_to_math_elements(soup):
    math_elements = soup.find_all('math')
    for math_elem in math_elements:
        if 'xmlns' not in math_elem.attrs:
            math_elem['xmlns'] = "http://www.w3.org/1998/Math/MathML"
    return soup

def add_xmlns_to_svg_elements(soup):
    svg_elements = soup.find_all('svg')
    for svg_elem in svg_elements:
        if 'xmlns' not in svg_elem.attrs:
            svg_elem['xmlns'] = "http://www.w3.org/1998/Math/MathML"
    return soup

def remove_merror(soup):
    merror_elems = soup.find_all('merror')
    for merror_elem in merror_elems:
        merror_elem.decompose()
    return soup

def modify_hrefs(soup):
    ann_elems = soup.find_all('a')
    for ann_elem in ann_elems:
        if 'href' in ann_elem.attrs:
            if 'http' in ann_elem['href']:
                continue
            try:
                section = id_to_section[ann_elem['href'].replace('#', '')]
            except KeyError:
                continue
            ann_elem['href'] = ann_elem['href'].replace('#', f'{section}.xhtml#')
            # ann_elem['epub:type'] = "noteref"
    return soup

def handle_images(soup):
    for img in soup.find_all('img'):
        if 'ar5iv' in img['src']:
            img.decompose()
        img['src'] = os.path.join('../images/', os.path.basename(img['src']))
    return soup

def remove_latex_errors(soup):
    for elem in soup.find_all():
        if 'ltx_ERROR' in elem.get('class', []):
            elem.decompose()
    return soup
def remove_styling(soup):
    elements_with_style = soup.find_all(style=True)
    for element in elements_with_style:
        del element['style']
    return soup

preprocessing = [add_name_to_annotation_xml,
                 add_xmlns_to_math_elements,
                 add_xmlns_to_svg_elements,
                 remove_merror,
                 modify_hrefs,
                 handle_images,
                 remove_latex_errors,
                 remove_styling]
def get_section_title(child):
    if 'ltx_abstract' in child.get('class', []):
        return 'Abstract'
    for child_child in child.children:
        if child_child.name == 'h2':
            section_title = child_child.text
            return section_title
    return ''


def extract_title(article):
    out = ""
    elem = article.find_all(class_='ltx_title_document')
    if elem and len(elem):
        out = elem[0].string
        out = ' '.join(word.capitalize() for word in out.split())  # capitalize
    return out
def extract_all_references(article):
    for child in article.children:
        if child.name:  # Check if child is a tag and not a NavigableString
            section_title = remove_numbers_spaces_special_chars(get_section_title(child))
            try:
                id_to_section[child['id']] = section_title
            except:
                pass
            # loop on all children of child and get all values of the key id
            for element in child.find_all(id=True):
                id_to_section[element['id']] = section_title

    return id_to_section

def process_html_file(html):
    data = {
        "title": '',
        "sections": [] # section title to HTML
    }
    soup = BeautifulSoup(html, 'html.parser')

    article = soup.find_all('article')[0]

    # data['title'] = extract_title(article)
    id_to_section = extract_all_references(article)
    # Loop through all children of the 'article' tag
    for child in article.children:
        if child.name:  # Check if child is a tag and not a NavigableString
            classes = child.get('class', [])
            if 'ltx_section' in classes  or 'ltx_bibliography' in classes or 'ltx_abstract' in classes or 'ltx_appendix' in classes:
                section_title = get_section_title(child)

                new_html = BeautifulSoup(get_chapter_content(section_title), 'html')

                for pre in preprocessing:
                    child = pre(child)


                new_html.body.append(child)


                data['sections'].append({'title': section_title,
                                         'title_raw': remove_numbers_spaces_special_chars(section_title),
                                        'content': str(new_html),
                                        'needs_math': section_needs_math(new_html)})

    return data

def read_file(file_path):
    data = ''
    with open(file_path, 'r') as f:
        data = f.read()
    return data
def save_file(filepath, content):
    with open(filepath, "w") as f:
        f.write(content)

def setup_directories(book_dir, EPUB_dir, meta_dir, css_dir, img_dir, xhtml_dir):
    shutil.rmtree(book_dir, ignore_errors=True)
    os.makedirs(book_dir, exist_ok=True)
    os.makedirs(EPUB_dir)
    os.makedirs(meta_dir)
    os.makedirs(css_dir)
    os.makedirs(img_dir)
    os.makedirs(xhtml_dir)

def save_files(book_dir, meta_dir, EPUB_dir, css_dir, img_dir, xhtml_dir, data, images):
    save_file(os.path.join(book_dir, 'mimetype'), get_mimetype())
    save_file(os.path.join(meta_dir, 'container.xml'), get_container_xml())
    save_file(os.path.join(EPUB_dir, 'package.opf'), get_package_opf((data['title']), data['author'], data['sections'], images))

    save_file(os.path.join(css_dir, 'commonltr.css'), get_common_itr_css())
    save_file(os.path.join(css_dir, 'epub.css'), get_epub_css())

    for section in data['sections']:
        xhtml_filename = f"{(section['title_raw'])}.xhtml"
        save_file(os.path.join(xhtml_dir, xhtml_filename), section['content'])

    for img_id, img_content in images.items():
        img_path = os.path.join(img_dir, os.path.basename(img_id))
        with open(img_path, 'wb') as f:
            f.write(img_content)

def create_epub(book_dir, output_epub):
    with zipfile.ZipFile(output_epub, 'w') as zipf:
        for foldername, _, filenames in os.walk(book_dir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                zipf.write(file_path, arcname=os.path.relpath(file_path, book_dir))

def html_to_epub(website_data, title, author= 'Unknown', output_epub='book.epub'):
    html_content, images = website_data
    book_dir = 'tmp'
    data = process_html_file(html_content)
    data['title'] = title
    data['author'] = author
    data['sections'] = [{
                    'title': 'titlepage',
                    'title_raw': 'titlepage',
                    'content': get_title_page(data['title'], ''),
                    'needs_math': False
                 },
                {
                    'title': 'nav',
                    'title_raw':'nav',
                    'content': table_of_contents(data['sections']),
                    'needs_math': False
                }] + data['sections']

    EPUB_dir = os.path.join(book_dir, 'EPUB')
    meta_dir = os.path.join(book_dir, 'META-INF')
    css_dir = os.path.join(EPUB_dir, 'css')
    img_dir = os.path.join(EPUB_dir, 'images')
    xhtml_dir = os.path.join(EPUB_dir, 'xhtml')
    # Setup directories
    setup_directories(book_dir, EPUB_dir, meta_dir, css_dir, img_dir, xhtml_dir)
    save_files(book_dir, meta_dir, EPUB_dir, css_dir, img_dir, xhtml_dir, data, images)

    # Create EPUB file
    create_epub(book_dir, data['title'] + '.epub')

    shutil.rmtree(book_dir, ignore_errors=True)



