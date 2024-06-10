import uuid
import playsound
#import speech_recognition as sr
from gtts import gTTS
import openai
import subprocess
import os
import platform
import pyttsx3
import pygame
# ------------------------------ OPENAI API -------------------------------
# Define the API endpoint and your API key
API_URL = "https://api.openai.com/v1/engines/davinci-codex/completions"
LANG = "es"
# Set OpenAI API key
# API_KEY = "YOUR-API-KEY"
# openai.api_key = API_KEY
pygame.init()

# ------------------------------ FUNCTIONS -------------------------------
def open_app(prompt): # Open an app
    for app in osApps:
        if app in prompt:
            responder(f'Abriendo {osApps[app][1]}')
            subprocess.Popen(
                osApps[app][0], 
                shell=True, 
                start_new_session=True
            )
            return True
    return False

def close_app(prompt): # Close an app
    for app in osApps:
        if app in prompt:
            responder(f'Cerrando {osApps[app][1]}')
            if OS == 'Linux':
                command = f'killall {osApps[app][1]}'
            else:
                command = f'taskkill /IM {osApps[app][1]}.exe /F'
            subprocess.Popen(
                command,
                shell=True,
                start_new_session=True,
            )
            return True
    return False

def search_web(prompt): # Search the web
    try:
        search_query = prompt.replace('search'+' ', "").replace('busca'+' ', "")
        search_query = "https://www.google.com/search?q=" + search_query
        responder(f'Buscando')
        if OS == 'Linux':
            command = f'xdg-open "{search_query}"'
        else:
            command = f'start {search_query}'
        subprocess.Popen(
            command,
            shell=True,
            start_new_session=True,
        )
        return True
    except Exception as e:
        print("Error:", e)
        return False

def gpt(prompt): # Chat with GPT-3
    prompt = prompt.replace("chat", "")
    prompt = prompt + " responde en menos de 40 palabras"
    try:
        chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
            ],
        )
        respuesta = gTTS(text=chat['choices'][0]['message']['content'], lang=LANG, slow=False)
        archivo = f'{str(uuid.uuid4())}.mp3'
        respuesta.save(archivo)
        playsound.playsound(archivo)
        os.remove(archivo)
        return True
    except Exception as e:
        print("Error:", e)
        return False

def jujutsu(prompt): # Play a song
    if OS == 'Linux':
        command = f'totem ~/Desktop/Trabajos/Sistemas/IA/Virtual_Asistant/specialz.mp3'
    else:
        command = f'start ~/Desktop/Trabajos/Sistemas/IA/Virtual_Asistant/specialz.mp3'
    subprocess.Popen(
        command,
        shell=True,
        start_new_session=True,
    )

    return True

def exit(prompt): # Exit the program
    pygame.quit()
    if OS == "Windows":
        command = 'taskkill /IM python.exe /F'
    else:
        command = 'killall python'
    subprocess.Popen(
        command,
        shell=True,
        start_new_session=True,
        )
    return True

def responder(texto):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(texto)
    engine.runAndWait()

# ----------------------------- DICCTIONARIES -----------------------------
comandos = { # Dictionary with the commands by language
    "English": {
        "open": open_app,
        "close": close_app,
        "search": search_web,
        "break it down": jujutsu,
        "kill yourself": exit,
        "chat": gpt,
        },
    "Spanish": {
        "abre": open_app,
        "termina": close_app,
        "busca": search_web,
        "rompe lo": jujutsu,
        "muerete": exit,
        "chat": gpt,
        },
    }
 
apps = { # Dictionary with the apps by OS
    'Linux':{
        'visual studio':['code', 'code'],
        'steam':['flatpak run com.valvesoftware.Steam', 'steam'],
        'music':['totem', 'totem'],
        'spotify':['flatpak run com.spotify.Client', 'spotify'],
    },
    'Windows':{
        'visual studio':['code', 'Code'],
        'panel de control':['control', 'Control'],
        'reproductor':['wmplayer', 'Wmplayer'],
        'word':['winword', 'Winword'],
        'excel':['excel', 'Excel'],
        'powerpoint':['powerpnt', 'Powerpnt'],
        'calculadora':['calc', 'Calc'],
        'notepad':['notepad', 'Notepad'],
        'navegador':['brave', 'Brave'],
        'archivos':['explorer', 'Explorer'],
    },
}

OS = platform.system() # Linux or Windows or Mac
osApps = apps[OS] # Dictionary with the apps for the current OS



