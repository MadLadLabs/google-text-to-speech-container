import os
import glob
import yaml
from dataclasses import dataclass
from typing import List
from google.cloud import texttospeech

INPUT_ROOT_PATH = '/input'

@dataclass
class SpeechSynthesisConfig:
    language_code: str
    ssml_voice_gender: str
    texts: List[str]
    ssmls: List[str]
    pitch: float
    voice_name: str

def string_gender_to_texttospeech_enum(text):
    if text == 'male':
        return texttospeech.SsmlVoiceGender.MALE
    if text == 'female':
        return texttospeech.SsmlVoiceGender.FEMALE
    if text == 'neutral':
        return texttospeech.SsmlVoiceGender.NEUTRAL
    raise Exception(f'Unknown gender: "{text}"')


if __name__ == '__main__':
    if os.path.exists(f'{INPUT_ROOT_PATH}'):
        print('Running in batch mode')

        for filepath in glob.glob(f'{INPUT_ROOT_PATH}/*.yml'):
            filename = os.path.splitext(os.path.basename(filepath))[0]
            with open(filepath) as speech_synthesis_config_file:
                speech_synthesis_config_dict = yaml.load(speech_synthesis_config_file, Loader=yaml.FullLoader)

                speech_synthesis_config = SpeechSynthesisConfig(**speech_synthesis_config_dict)

                client = texttospeech.TextToSpeechClient()
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.MP3,
                    pitch=speech_synthesis_config.pitch
                    )
                voice = texttospeech.VoiceSelectionParams(
                    language_code=speech_synthesis_config.language_code,
                    name=speech_synthesis_config.voice_name
                    # ssml_gender=string_gender_to_texttospeech_enum(speech_synthesis_config.ssml_voice_gender)
                )

                for i, text in enumerate(speech_synthesis_config.texts):
                    synthesis_input = texttospeech.SynthesisInput(text=text)
                    response = client.synthesize_speech(
                        input=synthesis_input, voice=voice, audio_config=audio_config
                    )

                    output_filename = f'{filename}_text_{i}.mp3'

                    with open(f'{INPUT_ROOT_PATH}/{output_filename}', 'wb') as out:
                        out.write(response.audio_content)

                for i, ssml in enumerate(speech_synthesis_config.ssmls):
                    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
                    response = client.synthesize_speech(
                        input=synthesis_input, voice=voice, audio_config=audio_config
                    )

                    output_filename = f'{filename}_ssml_{i}.mp3'

                    with open(f'{INPUT_ROOT_PATH}/{output_filename}', 'wb') as out:
                        out.write(response.audio_content)

                
