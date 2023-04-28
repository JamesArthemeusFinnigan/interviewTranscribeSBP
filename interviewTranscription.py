import whisper
import os
from datetime import datetime as d
import time
import json
import random
from datetime import datetime as dt

#             ___  __  _   _  _         _     _   _  _
#  \    / |_|  |  (_  |_) |_ |_)   |_| |_ |  |_) |_ |_)
#   \/\/  | | _|_ __) |   |_ | \   | | |_ |_ |   |_ | \
#                _   _
#  |_         | | \ / \
#  |_) \/   \_| |_/ \_/
#      /

# ******TRANSFORMING AUDIO TO TEXT******
print("  __                                _     _   _  _  ")
print(" (_ _|_  _. ._ _|_ o ._   _    |_| |_ |  |_) |_ |_) ")
print(" __) |_ (_| |   |_ | | | (_|   | | |_ |_ |   |_ | \ ")
print("                          _|                        ")

timestamp = str(random.randint(0, 10000000000))
textname = "Output/transcription" + str(timestamp) + ".txt"
jsonname = ".backend/dump" + str(timestamp) + ".json"
print("")
file = input("Please insert file here: ")
file = file[:-1]
print("  __                            _  _       _   _  __ ")
print(" (_ _|_  _. ._ _|_ o ._   _    |_ |_ |\/| |_) |_ /__ ")
print(" __) |_ (_| |   |_ | | | (_|   |  |  |  | |   |_ \_| ")
print("                          _|                         ")
print("")
print("*************************************")
print("FFMPEG is now converting your file to a .wav file")
print("*************************************")
start = dt.now()

cmd = "ffmpeg -i "+str(file)+" -c:a libmp3lame -q:a 8 .backend/output.wav"

os.system(cmd)

usingFile = '.backend/output.wav'

print("  __                                      ___  __  _   _  _  ")
print(" (_ _|_  _. ._ _|_ o ._   _    \    / |_|  |  (_  |_) |_ |_) ")
print(" __) |_ (_| |   |_ | | | (_|    \/\/  | | _|_ __) |   |_ | \ ")
print("                          _|                                 ")
print("")
print("*************************************")
print("Whisper is now transcribing your file")
print("*************IMPORTANT*************")
print("Please do not close the program until the transcription is complete")
verbosity = input(
    "Would you like to see the transcription as it is happening? (y/n): ")
print("*************IMPORTANT*************")
print("*************************************")

model = whisper.load_model('medium')
match verbosity:
    case "y":
        result = model.transcribe(usingFile, verbose=True)
    case "n":
        result = model.transcribe(usingFile, verbose=False)


# ******WRITING TO FILE, DELETING UNUSED AUDIO FILE******

with open(jsonname, "w") as fp:
    json.dump(result, fp)

os.remove(usingFile)

print("  __                            _       _   __  _  _  ")
print(" (_ _|_  _. ._ _|_ o ._   _    |_) /\  |_) (_  |_ |_) ")
print(" __) |_ (_| |   |_ | | | (_|   |  /--\ | \ __) |_ | \ ")
print("                          _|                          ")
print("")
print("*************************************")
print("Whisper has finished transcribing your file. The Raw file is saved in the .backend folder")
print("*************************************")
print("")
print("***********IMPORTANT***********")
nameChoice = input("Would you like to set a name for the final file? (y/n): ")
match nameChoice:
    case "y":
        textnameAdd = input("Please enter the name you would like to use: ")
        textname = "Output/" + textnameAdd + ".txt"
parsingOptions = input(
    "Would you like to segment the output for chatGPT? (y/n): ")
print("***********IMPORTANT***********")
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

match parsingOptions:
    case "n":

        for segment in data['segments']:
            if segment["text"][-1] == "." or segment["text"][-1] == "?" or segment["text"][-1] == "!":
                toBeAdded += segment['text']
                with open(textname, "a") as fp:
                    fp.write(toBeAdded)
                    fp.write('\n')
                toBeAdded = ''
            else:
                toBeAdded += segment['text']

    case "y":
        ln1 = "\n\n"
        ln2 = "*******************************"
        ln3 = "NEXT SEGMENT FOR GPT"
        ln4 = "*******************************"
        ln5 = "\n\n"
        charCount = 0
        for segment in data['segments']:
            charCount += len(segment['text'])
            if segment["text"][-1] == "." or segment["text"][-1] == "?" or segment["text"][-1] == "!":
                toBeAdded += segment['text']
                with open(textname, "a") as fp:
                    fp.write(toBeAdded)
                    fp.write('\n')
                toBeAdded = ''
                if charCount > 3000:
                    with open(textname, "a") as fp:
                        fp.write(ln1)
                        fp.write(ln2)
                        fp.write(ln3)
                        fp.write(ln4)
                        fp.write(ln5)
                    charCount = 0
            else:
                charCount += len(segment['text'])
                toBeAdded += segment['text']


end = dt.now()

tdelta = end - start
print("  _ ___      ___  __      _  _  ")
print(" |_  |  |\ |  |  (_  |_| |_ | \ ")
print(" |  _|_ | \| _|_ __) | | |_ |_/ ")
print("                                ")
print("")
print("*************************************")
print("Your file has been transcribed and saved in the Output folder. Transcription took " +
      str(tdelta) + " seconds")
print("*************************************")
