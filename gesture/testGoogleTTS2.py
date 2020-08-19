"""Synthesizes speech from the input string of text or ssml.
Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
import csv
import math

#to process any special delimters we put in the script file
import re

from urllib3.filepost import writer

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './neural-guard-255602-842fb8103266.json'

import eyed3
from google.cloud import texttospeech
from sentiment import create_gesture_output

OUTPUT_FILE = "./GestureFile.csv"

inputFile = input('Enter file name: ')
g = open(inputFile, "r")
whole_script = g.read()
lines_of_script = (whole_script.split('\n'))
mp3counter = 1
lengthCounter = 0

# Instantiates a client
client = texttospeech.TextToSpeechClient()

'''
Looks for breaks in the form "(1.5br)" and replaces it with the ssml substitute
@param: line - takes a line from the script
@return: a modified line that replaces the form "(1br)" and puts it into ssml
'''
def ssml_break(line):
    replacements = 0

    modified_line = line
    while ((modified_line.find('br)')) != -1):
        inline_break = modified_line[modified_line.find('('):modified_line.find('br)')+3]
        
        break_time = '<break time="' + inline_break[1:-3] + 's"/>'
        
        modified_line = modified_line.replace(inline_break, break_time, 1)
        
        print("Replacement Made!")
        replacements += 1

    if (replacements > 0):
        return modified_line

    print("No Replacement Made!")
    return line

with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['gesture_number', 'time', 'speaker', 'additional', 'dialogue'])
    for single_line in lines_of_script:

        words_in_line = (single_line.split(' '))
        textMP3 = []
        emp = 0
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        if words_in_line[0] == '1:':
            # '1:' means Male voice
            speaker = 1
            voice = texttospeech.VoiceSelectionParams(
                language_code='en-US',
                ssml_gender=texttospeech.SsmlVoiceGender.MALE)
        elif words_in_line[0] == '2:':
            # '2:' means a Female voice
            speaker = 2
            voice = texttospeech.VoiceSelectionParams(
                language_code='en-US',
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
            
        #Number of asterisks decide speed and volume
        asterisk_count = single_line.count('*')

        if asterisk_count == 1: 
            # Low Speed, High Pitch
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.85)
            emp = 1
        elif asterisk_count == 2:
            # Low Speed, Low Pitch
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.85)
            emp = 2
        elif asterisk_count == 3:
            # High Speed, High Pitch
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.3)
            emp = 3
        elif asterisk_count == 4:
            # High Speed, Low Pitch
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.3)
            emp = 4
        else:
            # Normal Speed/Pitch
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3)
            emp = 0

        #sets special case if line is question
        if single_line.count('?') != 0:
            emp = 5

        #Removes characters that are used as special designators from lines
        textMP3 = single_line.replace("*", "")
        textMP3 = textMP3.replace("1:", "")
        textMP3 = textMP3.replace("2:", "")

        #makes it so that there is only one space between each word
        textMP3 = " ".join(textMP3.split())

        print(textMP3)

        #replace special chars with ssml in the line
        textMP3 = ssml_break(textMP3);

        #make textmp3 look like SSML
        textMP3 = "<speak> %s </speak>" % (textMP3)

        # Set the text input to be synthesized in SSML format
        synthesis_input = texttospeech.SynthesisInput(ssml=textMP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            request={'input': synthesis_input, 'voice': voice, 'audio_config': audio_config})

        audioFile = str(mp3counter) + '.mp3'
        
        # if emp == 1:
        #     audioFile = str(mp3counter) + '*.mp3'
        # if emp == 2:
        #     audioFile = str(mp3counter) + '**.mp3'
        # if emp == 3:
        #     audioFile = str(mp3counter) + '***.mp3'
        # if emp == 4:
        #     audioFile = str(mp3counter) + '****.mp3'

        # The response's audio_content is binary.
        with open(audioFile, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to ' + audioFile)

        duration = int(eyed3.load(audioFile).info.time_secs)

        print(duration)

        writer.writerow([mp3counter, duration, speaker, emp, textMP3])
        mp3counter = int(mp3counter) + 1
        #lengthCounter = int(lengthCounter) + duration

create_gesture_output(OUTPUT_FILE)
