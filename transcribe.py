import pyaudio
import wave
import threading
#import keyboard
from pynput import keyboard
import whisper
from gpt_API import *
import playsound
from os import system
import speech_recognition as sr

from PyQt6 import QtWidgets, QtCore, QtGui
import sys

import subprocess

# ------------------------------ AUDIO RECORDER -------------------------------
class AudioRecorder:
    def __init__(self, filename="sound.wav"):
        self.filename = filename
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.chunk = 1024
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.done = False
        self.lang = "English"
        self.model = "base"
        self.transcription = ""
        self.translations = {
            "en": {
                "recording": "🔴 Recording",
                "stopped": "🔄 Stopped recording",
                "tutorial": "To begin or end a recording, press alt+l",
                "transcription": "🗣️",
                "language": "The language is currently set to: ",
            },
            "es": {
                "recording": "🔴 Grabando",
                "stopped": "🔄 Deteniendo",
                "tutorial": "Para comenzar o detener una grabación, presione alt+l",
                "transcription": "🗣️",
                "language": "El idioma actual es: ",
            },
        }
        self.trans = self.translations['en']
        playsound.playsound('ready.mp3')

    def set_lang(self, lang): # Set the language of the VA
        for key, value in langs.items():
            if lang in key:
                self.lang = value[0]
                self.trans = self.translations[value[1]]
                break
        return True

    def toggle_recording(self): # Start or stop the recording 
        self.is_recording = not self.is_recording 
        if self.is_recording: 
            system("clear")
            self.frames = []
            print(self.trans['recording'])
            threading.Thread(target=self.record).start() # Set a thread to record the audio
        else:
            print(self.trans['stopped'])

    def record(self): # Record the audio
        stream=self.audio.open( # Set the audio stream
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            frames_per_buffer=self.chunk,
            input=True
        )
        while self.is_recording: 
            data = stream.read(self.chunk)
            self.frames.append(data)

        stream.stop_stream()
        stream.close()
        self.save_audio()

    def transcribe_audio(self): # Transcribe the audio
        options = {
            "language":self.lang,
            "task":"transcribe",
        }
        self.set_model()
        result = self.whisp_model.transcribe(self.filename, **options)
        return result["text"]
    
    def save_audio(self): # Save the audio and transcribe it
        with wave.open(self.filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
        self.done = False
        self.transcription = self.transcribe_audio().lower()
        for blank in blanks: # Remove the blanks from the transcription
            self.transcription = self.transcription.replace(blank, "")
        self.run_command(self.transcription)  # Run the command from the transcription
        if self.done:
            print('Anything else?') # Success message
            responder('listo')
        else:
            print("I didn't undertand that. Try again.") # Error message
    
    def set_model(self): # Set the model to transcribe the audio
        self.whisp_model = whisper.load_model(self.model)

    def run_command(self, prompt): # Run the command from the transcription
        for lang in langs.keys(): # Check if the transcription contains a language
            if lang in prompt:  
                prompt = prompt.replace(lang, "")
                self.done = self.set_lang(lang) # Set the language of the VA
                change_gui_lang() # Change the language of the GUI
        comandos_lang = comandos[self.lang] # Get the commands for the language
        for command, function in comandos_lang.items(): # Check if the transcription contains a command
            if command in prompt: 
                self.done = function(prompt) 
                if self.done: 
                    break

# ------------------------------ AUDIO TOOLS -------------------------------
blanks = [',', '.'] # List of characters to remove from the transcription

langs = { # List of languages and their codes
    'spanish': ['Spanish', 'es'],
    'english': ['English', 'en'],
    'español': ['Spanish', 'es'],
    'inglés': ['English', 'en'],
    'ingles': ['English', 'en'],
    }

def set_hotkey(record='<alt>+l', toggle = '<alt>+k'): # Set the hotkey to start and stop the recording
    def hotkey_thread():
        with keyboard.GlobalHotKeys({
            record: toggle_button_text,
            toggle: toggle_on,
        }) as h:
            h.join()
    threading.Thread(target=hotkey_thread).start() # Set a thread to use the hotkey

# ------------------------------ GUI TOOLS --------------------------------
font = QtGui.QFont('Monocraft', 20)

guiLangs = { # List of languages and their codes
    'Spanish':['Español', 'Grabar', 'Enviar', 'Detener', 'Salir', 'muerete'],
    'English':['English', 'Record', 'Send', 'Stop', 'Exit', 'kill yourself'],
    }

is_always = False

def change_gui_lang(): # Change the language of the GUI
    recorder.set_lang(guiLangs[recorder.lang][0])

def toggle_button_text(): # Change the text of the button and start/stop the recording
    recorder.toggle_recording()
    if recorder.is_recording:
        voice.setStyleSheet('background-color: green; border-radius: 30px')
    else:
        voice.setStyleSheet('background-color: white; border-radius: 30px')

def toggle_on():
    global is_always
    is_always = not is_always
    if is_always:
        icon_toggle_on = QtGui.QIcon('ia/toggleon.png')
        toggle.setStyleSheet('background-color: white; border-radius: 30px')
    else:
        icon_toggle_on = QtGui.QIcon('ia/toggleoff.png')
        toggle.setStyleSheet('background-color: white; border-radius: 30px')
    toggle.setIcon(icon_toggle_on)
    subprocess.Popen(
        "gnome-terminal -- bash -c '~/toggle.sh; exec bash'",
        shell=True,
        start_new_session=True
    )
    
def send_prompt(): # Send the prompt to the VA
    recorder.run_command(textField.text().lower())
    textField.setText('')

def close_va(): # Close the VA
    recorder.run_command(guiLangs[recorder.lang][5])
    sys.exit()

# --------------------------------- MAIN -----------------------------------
recorder = AudioRecorder() 
set_hotkey()

# Create the GUI
mainApp = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setWindowTitle('Virtual Assistant')
window.setGeometry(1000, 300, 700, 380)

# Set the style of the GUI
style = QtWidgets.QStyleFactory.create('Fusion')
mainApp.setStyle(style)

# Create the button to start the speech recognition
voice = QtWidgets.QPushButton(window)
voice.setStyleSheet('background-color: white; border-radius: 30px;')
icon_voice = QtGui.QIcon('micro.png') 
voice.setIcon(icon_voice)
voice.setIconSize(QtCore.QSize(50, 50))  # Set the size of the icon
voice.setGeometry(QtCore.QRect(50, 150, 200, 60))
voice.setFont(font)
voice.clicked.connect(toggle_button_text)

# Create the button to send the prompt via text
text = QtWidgets.QPushButton(window)
text.setStyleSheet('background-color: white; border-radius: 30px;')
icon_text = QtGui.QIcon('ia/send.png') 
text.setIcon(icon_text)
text.setIconSize(QtCore.QSize(50, 50))  # Set the size of the icon
text.setGeometry(QtCore.QRect(50, 250, 200, 60))
text.setFont(font)
text.clicked.connect(send_prompt)

# Create a text field to send a prompt
textField = QtWidgets.QLineEdit(window)
textField.setGeometry(QtCore.QRect(50, 50, 600, 60))
textField.setFont(font)

# Create a toggle voice recognition button
toggle = QtWidgets.QPushButton(window)
toggle.setStyleSheet('background-color: white; border-radius: 30px;')
icon_toggle = QtGui.QIcon('ia/toggleoff.png')
toggle.setIcon(icon_toggle)
toggle.setIconSize(QtCore.QSize(50, 50))  # Set the size of the icon
toggle.setGeometry(QtCore.QRect(450, 150, 200, 60))
toggle.setFont(font)
toggle.clicked.connect(toggle_on)

# Create the button to close the program
Exit = QtWidgets.QPushButton(window)
Exit.setStyleSheet('background-color: red; border-radius: 30px;')
icon_exit = QtGui.QIcon('ia/off.png')
Exit.setIcon(icon_exit)
Exit.setIconSize(QtCore.QSize(50, 50))  # Set the size of the icon
Exit.setGeometry(QtCore.QRect(450, 250, 200, 60))
Exit.setFont(font)
Exit.clicked.connect(close_va)

# Show the GUI and close the program when the GUI is closed
window.show()
sys.exit(mainApp.exec())