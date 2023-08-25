import os

import ebooklib
from ebooklib import epub


def extract_cover(epub_path, cover_path):
    output_path = os.path.dirname(cover_path)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    book = epub.read_epub(epub_path)

    # Look for cover image
    for item in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        if 'cover' in item.get_name().lower():
            cover_image_data = item.get_content()

            # Write the cover image to the output path
            with open(cover_path, 'wb') as img_file:
                img_file.write(cover_image_data)
            print(f"Cover image extracted to {output_path}")
            return

    print("Cover image not found.")
