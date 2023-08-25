import ebooklib
from ebooklib import epub
import os
from bs4 import BeautifulSoup


def get_chapters(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() != ebooklib.ITEM_DOCUMENT:
            continue
        content = item.get_body_content().decode('utf-8')
        # Remove the table of contents
        if "contents" in content.lower() or "toc" in content.lower():
            continue
        # Exclude any chapters without content
        if is_empty(content):
            continue
        chapters.append(content)
    return chapters


def is_empty(chapter):
    soup = BeautifulSoup(chapter, 'html.parser')
    text = soup.get_text()
    return len(text.strip()) == 0


def write_chapters_to_files(chapters, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for idx, chapter in enumerate(chapters, start=1):
        soup = BeautifulSoup(chapter, 'html.parser')

        # Assuming that the chapter title is inside an <h1>, <h2>, etc. tag
        title_tag = soup.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        title_text = title_tag.get_text() if title_tag else f"Chapter {idx}"

        text = soup.get_text()
        text = text.replace('\xa0', ' ')  # Replace non-breaking spaces with regular spaces
        text = text.replace('​', '\n') # Remove weird character

        with open(os.path.join(output_dir, f'chapter_{idx}.txt'), 'w', encoding='utf-8') as file:
            file.write(f"{title_text}\n{text}")
        print(f'Chapter {idx} written to file')


def extract_chapters(epub_path, output_dir):
    chapters = get_chapters(epub_path)
    write_chapters_to_files(chapters, output_dir)
