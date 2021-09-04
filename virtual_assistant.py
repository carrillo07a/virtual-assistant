import speech_recognition as sr
import pyttsx3
import pywhatkit
import urllib.request
import json
import datetime
import wikipedia

# Name Assistant
name_assistant = 'siri'

# Help to turn off the program
status = 1

# Listener
listener = sr.Recognizer()
engine = pyttsx3.init()

# Get voices
voices = engine.getProperty('voices')
engine.setProperty('volume', 0.9)


# Audio output
def talk(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    status = 1

    try:
        # Activate microphone
        with sr.Microphone() as source:
            # Get the audio
            print("Listening....")
            listener.adjust_for_ambient_noise(source, duration=0.1)
            voice = listener.listen(source)

            # Convert audio to text
            recognize = listener.recognize_google(voice, language='es-ES')
            recognize = recognize.lower()

            # Replace name assistant
            if name_assistant in recognize:
                recognize = recognize.replace(name_assistant, '')
                status = run(recognize)

    except sr.RequestError as e:
        print("No Result; {0}".format(e))
    except sr.UnknownValueError as e:
        pass

    return status


def run(recognize):
    status = 1
    # All actions
    if 'reproduce' in recognize:
        play = recognize.replace('reproduce', '')
        talk('Reproduciendo' + play)
        pywhatkit.playonyt(play)
    elif 'hora' in recognize:
        hours = datetime.datetime.now().strftime('%I:%M %p')
        talk('Son las ' + hours)
    elif 'busca' in recognize:
        search = recognize.replace('busca', '')
        wikipedia.set_lang("es")
        summary = wikipedia.summary(search, sentences=1)
        talk(str(summary))
    elif 'gracias' in recognize or 'es todo' in recognize:
        talk('Espero haberte ayudado')
    elif 'exit' in recognize or 'salir' in recognize:
        status = 0
        talk('Hasta luego')
    else:
        talk("Por favor vuelve a intentarlo, no reconozco: " + recognize)
    return status


while status:
    status = listen()
