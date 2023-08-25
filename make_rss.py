import os
import eyed3
from urllib.parse import urljoin
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
import urllib.parse


def generate_podcast_feed(book_title, input_dir, output_dir, base_url, cover_image_url):
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    title = SubElement(channel, "title")
    title.text = book_title

    link = SubElement(channel, "link")
    link.text = base_url

    description = SubElement(channel, "description")
    description.text = f"A TTS-generated audiobook of {book_title}"

    image = SubElement(channel, "image")
    image_url = SubElement(image, "url")
    image_url.text = cover_image_url
    image_title = SubElement(image, "title")
    image_title.text = book_title
    image_link = SubElement(image, "link")
    image_link.text = base_url

    mp3_files = sorted(os.listdir(input_dir), key=lambda x: int(x.split('_')[1].split('.')[0]))

    for idx, mp3_filename in enumerate(mp3_files, start=1):
        if not mp3_filename.endswith('.mp3'):
            continue

        audiofile = eyed3.load(os.path.join(input_dir, mp3_filename))
        duration = int(audiofile.info.time_secs)

        text_filename = mp3_filename.replace('.mp3', '.txt')
        with open(os.path.join(output_dir, text_filename), 'r', encoding='utf-8') as file:
            chapter_title = file.readline().strip()

        mp3_url = base_url + "/" + mp3_filename

        item = SubElement(channel, "item")
        item_title = SubElement(item, "title")
        item_title.text = chapter_title

        item_link = SubElement(item, "link")
        item_link.text = mp3_url

        SubElement(item, "enclosure", url=mp3_url, type="audio/mpeg", length=str(duration))

        item_description = SubElement(item, "description")
        item_description.text = f"{book_title} - {chapter_title}"

    xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="   ")
    filename = "feed.xml"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(xml_str)
    print(f"Podcast feed for '{book_title}' created here: '{filename}'")

