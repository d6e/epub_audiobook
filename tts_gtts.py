from gtts import gTTS
import os


def convert_to_mp3(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue
        mp3_filename = filename.replace('.txt', '.mp3')
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            tts = gTTS(text=text, lang='en')
            mp3_path = os.path.join(output_dir, mp3_filename)
            print(f'Converting {filename} to {mp3_path}...', end='', flush=True)
            tts.save(mp3_path)
            print(' done.')


