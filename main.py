import os
import subprocess
import shutil
import ftplib

os.system('cls')

from rich.console import Console
from rich.text import Text

console = Console()


MAX_SIZE = 500_000_000
TEMP_DIR = "./album/"
MODE = 1 # 0: 128k, 1: 256k
SAMPLE_RATES = {
    0: '128k',
    1: '256k'
}

songs = []
sizes = []
albumSize = 0

# create temp album file for storing converted songs
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)

os.mkdir(TEMP_DIR)

# make sure file path is usable
def sanitise(filename):
    if '"' in filename:
        return filename.split('"')[1].replace('"',"")
    elif "'" in filename:
        return filename.split("'")[1].replace("'","")
    else:
        return filename

def calculateOutputName(_input,counter=0):
    seperator = '/' if '/' in _input else '\\'
    
    a = _input.split(seperator)
    base = a[len(a)-1][:-1]
    return f"{counter}. {base}"


while True:
    for i in range(len(songs)):
        # Print in green
        text = Text.assemble((f"{songs[i].replace(TEMP_DIR,'')} : {sizes[i]} bytes", "green"))
        console.print(text)
    perc = round(((MAX_SIZE-albumSize)/MAX_SIZE) * 100,2)
    text = Text.assemble((f"bytes remainaing space on cart: {MAX_SIZE-albumSize}", "dark_orange3"),(f" - {perc}%",f"{'green' if perc >= 50 else 'red1'}"))
    console.print(text)
    print()
    print('Enter a blank line to end')
    filename = input(f"Please Drag file {len(songs)+1} here: ")
    if filename != "":
        if '.mp3' not in filename:
            os.system('cls')
            continue
        sanitised = sanitise(filename)
        if os.path.isfile(sanitised):
            text = Text.assemble(("Valid File Found", "green"))
            console.print(text) # Print in green
        output = calculateOutputName(filename,len(songs)+1)
        command = f'ffmpeg -i {filename} -map 0:a -acodec libmp3lame -ab {SAMPLE_RATES[MODE]} "{TEMP_DIR}{output}"'
        #print(command)
        
        text = Text.assemble(("Converting file to correct format...", "dodger_blue1"))
        console.print(text)
        subprocess.call(command, stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
        
        songs.append(f"{TEMP_DIR}{output}")
        sizes.append(os.path.getsize(f"{TEMP_DIR}{output}"))
        albumSize+=os.path.getsize(os.path.abspath(f"{TEMP_DIR}{output}"))

        os.system('cls')
    else:
        break
os.system('cls')
for i in range(len(songs)):
    # Print in green
    text = Text.assemble((f"{songs[i].replace(TEMP_DIR,'')} : {sizes[i]} bytes", "green"))
    console.print(text)
perc = round(((MAX_SIZE-albumSize)/MAX_SIZE) * 100,2)
text = Text.assemble((f"bytes remainaing space on cart: {MAX_SIZE-albumSize}", "dark_orange3"),(f" - {perc}%",f"{'green' if perc >= 50 else 'red1'}"))
console.print(text)

print()
cover = input("Please provide an album cover: ")
if cover != "":
    source = sanitise(cover)
    dest = f"{TEMP_DIR}{calculateOutputName(source+'-')}"
    shutil.copyfile(source,dest)
    songs.insert(0,dest)

print()
print()
text = Text.assemble(('PLEASE CONNECT TO THE PROGRAMMERS WIRELESS NETWORK', "red3"))
console.print(text)
text = Text.assemble(("press enter when you're ready", "green"))
console.print(text)
input()


text = Text.assemble(("connecting to programmer...", "deep_sky_blue1"))
console.print(text)

session = ftplib.FTP('192.168.0.4')

from rich.progress import track

print("Starting Upload, this may take a while depending on sound quantity and size")
for i in track(range(len(songs)), description="Uploading..."):
    with open(songs[i],'rb') as file:
        session.storbinary(f'STOR {songs[i].replace(TEMP_DIR,"")}',file)

session.quit()



shutil.rmtree(TEMP_DIR)
quit()
    