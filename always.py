import speech_recognition as sr
from gpt_API import *

NAME = 'nanami' # Name of the VA

# Create a dictionary with the name and index of the microphones
microfonos = {}
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    microfonos[name] = index
r = sr.Recognizer()
# Use the microphone index that accompanies the "default" microphone in your
# sound settings
mic_index = microfonos['default']
mic = sr.Microphone(device_index=mic_index)

done = False
# ------------------------------ FUNCTIONS -------------------------------

def run_command(prompt): # Run the command from the transcription 
        comandos_lang = comandos['Spanish'] # Get the commands for the language
        for command, function in comandos_lang.items(): # Check if the transcription contains a command
            if command in prompt: 
                done = function(prompt) 
                if done: 
                    break

while True:
    try:
        with mic as source:
            audio = r.listen(source)
            try:
                activar = r.recognize_google(audio, language='es-ES')
            except sr.UnknownValueError:
                print("Lo siento, no pude entender eso. Por favor, intenta de nuevo.")
            activar = activar.lower()
            print(activar)
            done = False
            index = activar.find(NAME)
            if index != -1:
                activar = activar[index:]
                activar = activar.replace(NAME, "")
                print(activar)
                run_command(activar)
                if done:
                    print('Anything else?')
                else:
                    print("I didn't undertand that. Try again.")
    except:
        pass
