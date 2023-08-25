from google.cloud import texttospeech
import os


def convert_to_mp3(input_dir, output_dir):
    # Create a client
    client = texttospeech.TextToSpeechClient()

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if not filename.endswith(".txt"):
            continue
        mp3_filename = filename.replace('.txt', '.mp3')
        with open(os.path.join(input_dir, filename), 'r', encoding='utf-8') as file:
            text = file.read()
            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Build the voice request, select the language code, name of the voice, and the SSML gender
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-US",
                name="en-US-Wavenet-D",  # Example of a specific voice name
                ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
            )

            # Select the type of audio file you want
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            # Perform the text-to-speech request
            response = client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )

            mp3_path = os.path.join(output_dir, mp3_filename)
            print(f'Converting {filename} to {mp3_path}...', end='', flush=True)
            with open(mp3_path, "wb") as out:
                out.write(response.audio_content)
            print(' done.')
