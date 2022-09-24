'''
Notes:
    - for the word detection part i need to check constantly if the word is being said. I.e i need to create a listener who converts that what is said live to 0
    - I need first create an listener 
    - for testing purposes it is better to use first the microphone of the laptop
    - I first reimplement the basic virtual assistant and then I will advance it with my own models
    - i just use a conda environment for running my code
    - i need to think how I can use an ai model for 
pyttsx3  
SpeechRecognition 
'''

# wake word detection --> Speech to text --> Conversational AI

from distutils import text_file
import speech_recognition as sr
import pyttsx3
import requests
import config

condition = False

# takes the input from the microphone and converts it to text
def takeInput(condition):
    listener = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            print(command)
            command = command.lower()
            # wake word detection - only if input contains certain word it goes in the loop
            if "alexa" in command:
                conversationalAi(command)
            elif condition == True:
                conversationalAi(command)
    except:
        pass


def conversationalAi(text):
    headers = {
        'Authorization': config.key,
    }
    json_data = {
        'model': 'text-davinci-002',
        'prompt': (text),
        'temperature': 0.7,
        'max_tokens': 100,
    }
    response = requests.post(
        'https://api.openai.com/v1/completions', headers=headers, json=json_data)
    text = response.json()['choices'][0]['text']
    textToSpeech(text)

# converts the text to speech


def textToSpeech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    takeInput(condition=True)


if __name__ == "__main__":
    takeInput(False)
    # textToSpeech()
