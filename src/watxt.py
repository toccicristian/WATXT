#   Este programa transcribe un mp3 inteligible en un txt
#   Copyright (C) 2023 Cristian Tocci
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

#   Contacto : toccicristian@hotmail.com / toccicristian@protonmail.ch


#watxt.py archivo.mp3 [longitud minima de silencio]


import shutil
import sys
import glob
from os.path import normpath, expanduser, isfile, isdir
from os import path
import os

import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

licencias = dict()
licencias['gplv3'] = """    watxt.py  Copyright (C) 2023  Cristian Tocci
    This program comes with ABSOLUTELY NO WARRANTY; for details press 'w'.
    This is free software, and you are welcome to redistribute it
    under certain conditions; See COPYING.odt file for further details.
"""

licencias['gplv3logo'] = """
+----------------------------------------------------------------------------------------------------+
|oooooooo+~~~+~~~~~~+~~~~~+~~~~+~~~~~~+~~~~+~~~~~~+~~+~~~~+~~~~~+~~~~+~~~~~~++~~+~~+~~~~~~:  ::::::~+|
|oooooooo :::::::::::::::::::::::::::::::::::::::::::~::::::::::::::::::::::::::::::::. ~~~++ooooo+:.|
|ooooooo~::::::~:::::::::::::::::::::::::::::::::::::+::::::::::::::::::::::::~~.~:~:~+oooooooooooo:.|
|ooooooo :~:~~~~~~~~~~+~::: +~~~~~~~~~~~~~::++ :::::~+~:::::::::::::::::::~...~:::~ooooooooooooooo~.+|
|oooooo~~:~oo~~~~~~~~~oo~:~+oo ~~~~~~.ooo.~oo+~::::.+o ::::::::::::::::~  .~::::+oo+~:   +ooooooo::+o|
|oooooo::.+o+~::::::~+oo : oo~::::::::oo~:~oo~::::: oo~:::::::::::::: ~ ~::::.++~ ~:::::.+oooo+~ ~ooo|
|ooooo+~:~oo~:::::::::::::~oo::::::::+oo :+oo~:::::~oo+.::::::::::.:~ ~:::::: .:::::::~~oooo+:~ +oooo|
|ooooo::~+o+.:::::::::::: oo+~:::::: oo~~:oo~::::::~ooo~::::::::.~~.::::::::::::::::~~+oooooo+~::oooo|
|oooo+~::oo~:::~:~:~~::::~oo~       ~oo::+oo.::::::~ooo+~::::: ~~.:::::::::::::::: ~+oooooooooo~~oooo|
|oooo~::+oo :::~   +oo::.ooo~~~~~~~~~:.: oo+:::::::~oooo~:::~~+:::::::::::::::: ~+++~~~~oooooo+.~oooo|
|ooo+.: oo~:::::::.oo+.:~oo~::::::::::::~oo:::::::::oooo+~::++~::::::::::::::~   .::::::ooooo~.~ooooo|
|ooo~::~oo::::::::~oo~:~+o+~::::::::::: oo+~:::::::.+ooo~.~o+:::::::::::::::::::::::: +oooo+: +oooooo|
|ooo.: oo+.~~~~~~ +oo.::oo~::::::::::::~oo~~~~~~~:::+oo~ +oo ::::::::::::::::::::.:~ooooo+: ~oooooooo|
|oo~::.~~~~~~~~~~~~~ ::~+~.::::::::::::~+~~~~~~~~~:::o~ +ooo:::::::::::::::::: ~+oooooo~::~oooooooooo|
|o+ :~   ~::::::::::::.  ~::::: ..:::::::::::::::::::~ ~oooo~~::::::::::~. ~~+oooooo+~::+oooooooooooo|
|o~~:~~: ~ :~~. ~~.::~~~~. ::.~~~~::~:: :~~.~::~~ ::::.oooooo+~~::::~~~~ooooooooo+~::~+oooooooooooooo|
|o::~~~~:::~~~ ~~~.:: ::~.~:~.~~~: ~~~ :~~~: ~~~~~:::: oooooooooooooooooooooo++~::~+ooooooooooooooooo|
|+:::~::::::~~::::::::~~:::~::~:::::::::::~::::~:::::::~ooooooooooooooooo++~::~~+oooooooooooooooooooo|
|::::::::::::::::::::::::::::::::::::::::::::::::::::::: ~oooooooooo+~~~::~~+oooooooooooooooooooooooo|
|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~:~~~~~:    ::::::::~~~ooooooooooooooooooooooooooooo|
+----------------------------------------------------------------------------------------------------+
"""

licencias['textow'] = """ 
    15. Disclaimer of Warranty.
    THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY 
    APPLICABLE LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT 
    HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM “AS IS” WITHOUT 
    WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT 
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A 
    PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE 
    OF THE PROGRAM IS WITH YOU. SHOULD THE PROGRAM PROVE DEFECTIVE, YOU 
    ASSUME THE COST OF ALL NECESSARY SERVICING, REPAIR OR CORRECTION.
    
    16. Limitation of Liability.
    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING 
    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR 
    CONVEYS THE PROGRAM AS PERMITTED ABOVE, BE LIABLE TO YOU FOR 
    DAMAGES, INCLUDING ANY GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL 
    DAMAGES ARISING OUT OF THE USE OR INABILITY TO USE THE PROGRAM 
    (INCLUDING BUT NOT LIMITED TO LOSS OF DATA OR DATA BEING RENDERED 
    INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD PARTIES OR A FAILURE OF 
    THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER 
    OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

    17. Interpretation of Sections 15 and 16.
    If the disclaimer of warranty and limitation of liability provided above 
    cannot be given local legal effect according to their terms, 
    reviewing courts shall apply local law that most closely approximates 
    an absolute waiver of all civil liability in connection with the Program, 
    unless a warranty or assumption of liability accompanies a copy of 
    the Program in return for a fee.
    """

ayuda = f"""
    {sys.argv[0]} transcribe un mp3 inteligible en un txt.

    SINTAXIS:
    {sys.argv[0]} archivo.mp3/.ogg

    {sys.argv[0]} -h/--help/--ayuda     imprime esta ayuda

    {sys.argv[0]} -g                    informacion de licencia
    {sys.argv[0]} -w                    mas detalles de licencia
    {sys.argv[0]} -l/--gplv3logo        Un lindo logo de la GPLV3 en ASCII
"""





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


if len(sys.argv) == 2 and sys.argv[1] in ['-h','--help','--ayuda']:
    print(f'{ayuda}')
    sys.exit()

if len(sys.argv) == 2 and sys.argv[1] == "-g":
    print(f"{licencias['gplv3']}")
    sys.exit()

if len(sys.argv) == 2 and sys.argv[1] == "-w":
    print(f"{licencias['textow']}")
    sys.exit()

if len(sys.argv) == 2 and sys.argv[1] in ["-l","--gplv3logo"]:
    print(f"{licencias['gplv3logo']}")
    sys.exit()

if len(sys.argv)<2 or not isfile(normpath(expanduser( str(sys.argv[1]).rstrip() ))):
    log("El archivo no existe.")
    print(f"{ayuda}")
    sys.exit()

INPUTFILE=normpath(expanduser( str(sys.argv[1]).rstrip() ))
FINALTRANSCRIPT_FILE='finaltranscript.txt'
AUDIO_FILE=f"{INPUTFILE}.wav"
SEPARADOR="========================================="

minsilencelen=500
if len(sys.argv)>2 and es_entero(sys.argv[2]):
    minsilencelen=int(sys.argv[2])


#Chequeo si la extension del archivo esta permitida:
extension_valida = False
extensiones_permitidas=['.mp3','.ogg']
for extension in extensiones_permitidas:
    if str(INPUTFILE).rstrip().endswith(extension):
        extension_valida = True

if not extension_valida:
    print("La extension del archivo no esta permitida. \nExtensiones permitidas:",end='',flush=True)
    for extension in extensiones_permitidas:
        print(extension, end='')
        print("")
        sys.exit()

#si la extension es ogg lo cargo con "from_ogg"
log("Generando archivo wav...")
if str(INPUTFILE).rstrip().endswith(".ogg"):
    sound = AudioSegment.from_ogg(INPUTFILE)

#si la extension es mp3 lo cargo con "from_mp3"
if str(INPUTFILE).rstrip().endswith(".mp3"):
    sound = AudioSegment.from_mp3(INPUTFILE)

#convierto el archivo cargado a wav
sound.export(f'{AUDIO_FILE}', format="wav")

#transcribo AUDIO_FILE
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


