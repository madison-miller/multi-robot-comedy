"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
"""
import os
import csv

#to process any special delimters we put in the script file
import re

from urllib3.filepost import writer

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './49050.json'
import eyed3
from google.cloud import texttospeech

g = open("testFile.txt", "r")
Orig = g.read()
Oline = (Orig.split('\n'))
mp3counter = 1
lengthCounter = 0


'''
this function will replace special character sequences in a text line with
the equivalent SSML and returns the modified line

Right now it only recognizes <br/> being equivalent to <break time="3s"/>
To add more sequences, add them to the dictionary
'''
def replace_special_chars_with_ssml(line):
    special_character_ssml_dict = {
            r"(\<br\/\>)": '<break time="3s"/>', #this regex matches <br/>
            }

    for special_char, ssml_string  in special_character_ssml_dict.items():
        (modified_line, no_of_replacements) = re.subn(special_char, ssml_string, line)
        print("Made %s replacements. \n Line is now: %s" 
                % (no_of_replacements, modified_line)
            )

    return modified_line

# Instantiates a client
client = texttospeech.TextToSpeechClient()

with open('gestureFile.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for i in Oline:

        Oword = (i.split(' '))
        textMP3 = []
        emp = 0
        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        if Oword[0] == '1:':
            if Oword[1] == "*":
                # Low Speed, High Pitch
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=0.85,
                    volume_gain_db=16)
                textMP3 = i[5:len(i)]
                emp = 1
            elif Oword[1] == "**":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=0.85,
                    volume_gain_db=-2)
                textMP3 = i[6:len(i)]
                emp = 2
            elif Oword[1] == "***":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=1.3,
                    volume_gain_db=16)
                textMP3 = i[7:len(i)]
                emp = 3
            elif Oword[1] == "****":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=1.3,
                    volume_gain_db=-2)
                textMP3 = i[8:len(i)]
                emp = 4
            elif Oword[len(Oword) - 1] == "?":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                textMP3 = i[3:len(i)]
                emp = 5
            else:
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                emp = 0
                textMP3 = i[3:len(i)]
        elif Oword[0] == '2:':
            if Oword[1] == "*":
                #Low Speed, High Pitch
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=0.85,
                    volume_gain_db=16)
                textMP3 = i[5:len(i)]
                emp = 1
            elif Oword[1] == "**":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=0.85,
                    volume_gain_db=-2)
                textMP3 = i[6:len(i)]
                emp = 2
            elif Oword[1] == "***":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=1.3,
                    volume_gain_db=16)
                textMP3 = i[7:len(i)]
                emp = 3
            elif Oword[1] == "****":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3,
                    speaking_rate=1.3,
                    volume_gain_db=-2)
                textMP3 = i[8:len(i)]
                emp = 4
            elif Oword[len(Oword) - 1] == "?":
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                textMP3 = i[3:len(i)]
                emp = 5
            # elif Oword[1] == "<br>":
            #     synthesis_input = texttospeech.types.SynthesisInput(break="1s")
            else:
                voice = texttospeech.types.VoiceSelectionParams(
                    language_code='en-US',
                    ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
                audio_config = texttospeech.types.AudioConfig(
                    audio_encoding=texttospeech.enums.AudioEncoding.MP3)
                emp = 0
                textMP3 = i[3:len(i)]


        #replace special chars with ssml in the line
        textMP3 = replace_special_chars_with_ssml(textMP3);

        #make textmp3 look like SSML
        textMP3 = "<speak> %s </speak>" % (textMP3)

        # Select the type of audio file you want returned
        # audio_config = texttospeech.types.AudioConfig(
        #     audio_encoding=texttospeech.enums.AudioEncoding.MP3)

        # Set the text input to be synthesized in SSML format
        synthesis_input = texttospeech.types.SynthesisInput(ssml=textMP3)

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(synthesis_input, voice, audio_config)

        audioFile = str(mp3counter) + '.mp3'
        # print(audioFile)
        # The response's audio_content is binary.
        audioFile = str(mp3counter) + '.mp3'
        with open(audioFile, 'wb') as out:
            # Write the response to the output file.
            out.write(response.audio_content)
            print('Audio content written to ' + audioFile)

        duration = int(eyed3.load(audioFile).info.time_secs)
        print(duration)

        # Gets the number WITHOUT semicolon
        number = Oword[0]


        writer.writerow([lengthCounter, number[0], emp, textMP3])
        mp3counter = int(mp3counter) + 1
        lengthCounter = int(lengthCounter) + duration
        # lengthCounter = round(lengthCounter, 2)
