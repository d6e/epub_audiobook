import os

from extract_ebook import extract_chapters
from make_rss import generate_podcast_feed
from tts_gtts import convert_to_mp3


def main():
    epub_path = 'epubs/Serious_Weakness.epub'
    book_name = os.path.splitext(os.path.basename(epub_path))[0]

    # Extract the epub chapters to text files
    text_dir = f"text_chapters/{book_name}/chapters"
    extract_chapters(epub_path, text_dir)

    # Convert the text files to mp3 files
    episodes_dir = f'audio/{book_name}/episodes'  # The directory where you want to save the MP3 files
    # convert_to_mp3(text_dir, episodes_dir)

    # Generate podcast feed
    base_url = 'http://yourdomain.com/path/to/mp3s'  # Base URL where the MP3 files are hosted
    generate_podcast_feed(book_name, episodes_dir, text_dir, base_url)


if __name__ == '__main__':
    main()
