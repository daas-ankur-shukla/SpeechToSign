import io
import re
import sys
# importing google speech API
from google.cloud import speech
from google.cloud import translate
from google.cloud.speech import enums
from google.cloud.speech import types
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from SpeechToText.streamInput import MicrophoneStream

# Import the base64 encoding library.
import base64

# Pass the audio data to an encoding function.
def encode_audio(audio):
  # audio_content = audio.read()
  return base64.b64encode(audio)

# Create your views here.

def toText(speech_chunk, src_lang='en'):
    # printing information for sanility check
    print("source language {}".format(src_lang))
    print(speech_chunk)
    # print("target language {}".format(trgt_lang))

    # # Audio recording parameters
    # RATE = 16000
    # CHUNK = int(RATE / 10)  # 100ms
    #
    # client = speech.SpeechClient()
    # config = types.RecognitionConfig(
    #     encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    #     sample_rate_hertz=RATE,
    #     language_code=src_lang)
    # streaming_config = types.StreamingRecognitionConfig(
    #     config=config,
    #     interim_results=True)
    #
    # content= encode_audio(speech_chunk)
    # # with MicrophoneStream(RATE, CHUNK) as stream:
    # #     audio_generator = stream.generator()
    # requests = types.StreamingRecognizeRequest(audio_content=content)
    #                 # for content in audio_generator)
    #
    # responses = client.streaming_recognize(streaming_config, requests)
    #
    # num_chars_printed = 0
    # for response in responses:
    #     if not response.results:
    #         continue
    #
    #     # The `results` list is consecutive. For streaming, we only care about
    #     # the first result being considered, since once it's `is_final`, it
    #     # moves on to considering the next utterance.
    #     result = response.results[0]
    #     if not result.alternatives:
    #         continue
    #
    #     # Display the transcription of the top alternative.
    #     transcript = result.alternatives[0].transcript
    #
    #     # Display interim results, but with a carriage return at the end of the
    #     # line, so subsequent lines will overwrite them.
    #     #
    #     # If the previous result was longer than this one, we need to print
    #     # some extra spaces to overwrite the previous result
    #     overwrite_chars = ' ' * (num_chars_printed - len(transcript))
    #
    #     if not result.is_final:
    #         sys.stdout.write(transcript + overwrite_chars + '\r')
    #         sys.stdout.flush()
    #
    #         num_chars_printed = len(transcript)
    #
    #     else:
    #         text=transcript + overwrite_chars
    #         num_chars_printed = 0
    #         # printing text output
    #         print('Text output '+text)
    #         transciptionResponse={'text':text}
    #         return transciptionResponse
    with io.open('F:\\audio.raw', 'rb') as audio_file:
        content = audio_file.read()

    client = speech.SpeechClient()
    audio = types.RecognitionAudio(content=encode_audio(speech_chunk))
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    text=[]
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        text.append(result.alternatives[0].transcript)

    print(response)
    return JsonResponse(text, safe=False)
