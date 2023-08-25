import os
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom


def generate_podcast_feed(book_title, mp3_dir, text_chapters_dir, base_url):
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    title = SubElement(channel, "title")
    title.text = book_title

    link = SubElement(channel, "link")
    link.text = base_url

    description = SubElement(channel, "description")
    description.text = f"A TTS-generated audiobook of {book_title}"

    for filename in os.listdir(mp3_dir):
        if not filename.endswith(".mp3"):
            continue
        chapter_number = filename.split('_')[1].split('.')[0]
        text_filename = filename.replace('.mp3', '.txt')
        with open(os.path.join(text_chapters_dir, text_filename), 'r', encoding='utf-8') as file:
            chapter_title = file.readline().strip().replace("Chapter ", "")
        mp3_url = os.path.join(base_url, filename)

        item = SubElement(channel, "item")
        item_title = SubElement(item, "title")
        item_title.text = f"Chapter {chapter_number}: {chapter_title}"

        item_link = SubElement(item, "link")
        item_link.text = mp3_url

        enclosure = SubElement(item, "enclosure", url=mp3_url, type="audio/mpeg")

        item_description = SubElement(item, "description")
        item_description.text = f"{book_title} - {chapter_title}"

    xml_str = minidom.parseString(tostring(rss)).toprettyxml(indent="   ")
    with open("feed.xml", "w", encoding='utf-8') as f:
        f.write(xml_str)


