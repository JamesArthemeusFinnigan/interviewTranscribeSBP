import whisper
import os
from datetime import datetime as d
import time
import json
import random

# ******TRANSFORMING AUDIO TO TEXT******

timestamp = str(random.randint(0, 10000000000))
textname = "Output/transcription" + str(timestamp) + ".txt"
jsonname = ".backend/dump" + str(timestamp) + ".json"
file = input("Please insert file here: ")
file = file[:-1]


cmd = "ffmpeg -i "+str(file)+" -c:a libmp3lame -q:a 8 .backend/output.wav"

os.system(cmd)

usingFile = '.backend/output.wav'

model = whisper.load_model('medium')
result = model.transcribe(usingFile, verbose=True)


# ******WRITING TO FILE, DELETING UNUSED AUDIO FILE******

with open(jsonname, "w") as fp:
    json.dump(result, fp)

os.remove(usingFile)


# ******READING FROM FILE******

with open(jsonname, "r") as fp:
    data = json.load(fp)
with open(textname, "w") as fp:
    fp.write("")

# *****PARSING DATA******
i = 0
toBeAdded = ''
os.remove(textname)

# for segment in data['segments']:
#     continuing = True
#     if continuing == True:
#         print(segment['end'])
#         print(data['segments'][i+1]['start'])


for segment in data['segments']:
    if segment["text"][-1] == "." or segment["text"][-1] == "?" or segment["text"][-1] == "!":
        toBeAdded += segment['text']
        print(toBeAdded)
        with open(textname, "a") as fp:
            fp.write(toBeAdded)
            fp.write('\n')
            toBeAdded = ''
    else:
        toBeAdded += segment['text']
        toBeAdded += ' '
