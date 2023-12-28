
#pitsydub3.py archivo.mp3 [longitud minima de silencio]

import shutil
import sys
import glob
from os.path import normpath, expanduser, isfile, isdir
from os import path
import os

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


def log(s='', file="log.txt", end='\n'):
    with open(file,'a') as ar:
        ar.write(s+"\n")

    print(s,end=end, flush=True)
    return None;


def es_entero(n):
    try:
        int(n)
        return True
    except ValueError:
        return False



if len(sys.argv)<2 or not isfile(normpath(expanduser( str(sys.argv[1]).rstrip() ))):
    log("El archivo no existe.")
    sys.exit()

INPUTFILE=normpath(expanduser( str(sys.argv[1]).rstrip() ))
FINALTRANSCRIPT_FILE='finaltranscript.txt'
AUDIO_FILE=f"{INPUTFILE}.wav"
SEPARADOR="========================================="

minsilencelen=500
if len(sys.argv)>2 and es_entero(sys.argv[2]):
    minsilencelen=int(sys.argv[2])


#convertir mp3 a wav
log("Generando archivo wav...")
sound = AudioSegment.from_mp3(INPUTFILE)
sound.export(f'{AUDIO_FILE}', format="wav")

#transcribe audio file
sound = AudioSegment.from_wav(AUDIO_FILE)

log("Dividiendo en chunks (esto puede tardar): ", end='')
#print("Dividiendo en chunks...")
chunks = split_on_silence(sound,
    #esto es segun como sea el audio
    min_silence_len = minsilencelen,
    silence_thresh = sound.dBFS-14,
    #mantenemos el silencio por 1 segundo
    keep_silence=500,
    )

folder_name = "audio-chunks"
if not isdir(folder_name):
    os.mkdir(folder_name)

#ESTABLECEMOS EL RECONOCEDOR DE HABLA COMO r
r = sr.Recognizer()

whole_text = ""
#procesamos cada trozo
for i, audio_chunk in enumerate(chunks, start=1):
    #exportamos el trozo del audio y lo guardamos enumerado
    log(f"chunk{str(i).zfill(4)}.wav ", end="")
    chunk_filename = os.path.join(folder_name, f"chunk{str(i).zfill(4)}.wav")
    audio_chunk.export(chunk_filename, format="wav")

log(f"\n{SEPARADOR}\nTranscribiendo:")
for chunk_filename in sorted(glob.glob(os.path.join(folder_name, "*.wav"))):
    #reconocemos el trozo de audio
    with sr.AudioFile(chunk_filename) as source:
        audio_listened = r.record(source)
        # lo intentamos convertir en texto
        try:
            text = r.recognize_google(audio_listened, language="es-AR")
        except sr.UnknownValueError as e:
            log(f" ***Error: {str(e)}*** ",end='')
        else:
            text = f"{text.capitalize()}. "
            log(f"{text}",end=' ')
            whole_text += text

log(f"\n{SEPARADOR}\nGuardando en archivo {FINALTRANSCRIPT_FILE}")
with open(FINALTRANSCRIPT_FILE, 'a') as ar:
    ar.write(f"{whole_text}\n")

log(f"\nEliminando archivos temporales")
shutil.rmtree(folder_name)
os.remove(AUDIO_FILE)


