__author__ = "Jason Dieter Oesch"
__version__ = "1.1.0"
__license__ = "MIT"

import whisper
import os
from datetime import datetime as d
import time
import json
import random
from datetime import datetime as dt


class ffmpegHP():
    def convertToWav(file):
        print("  __                            _  _       _   _  __ ")
        print(" (_ _|_  _. ._ _|_ o ._   _    |_ |_ |\/| |_) |_ /__ ")
        print(" __) |_ (_| |   |_ | | | (_|   |  |  |  | |   |_ \_| ")
        print("                          _|                         ")
        print("")
        print("*************************************")
        print("FFMPEG is now converting your file to a .wav file")
        print("*************************************")
        start = dt.now()

        cmd = "ffmpeg -i "+str(file) + \
            " -c:a libmp3lame -q:a 8 .backend/output.wav"

        os.system(cmd)


class whisperHP:

    def __init__(self, jsonname, usingFile):
        self.jsonname = jsonname
        self.usingFile = usingFile

    def main(self):
        print("  __                                      ___  __  _   _  _  ")
        print(" (_ _|_  _. ._ _|_ o ._   _    \    / |_|  |  (_  |_) |_ |_) ")
        print(" __) |_ (_| |   |_ | | | (_|    \/\/  | | _|_ __) |   |_ | \ ")
        print("                          _|                                 ")
        print("")
        print("*************************************")
        print("Whisper is now transcribing your file")
        print("*************IMPORTANT*************")
        print("Please do not close the program until the transcription is complete")
        modelChoice = whisperHP.modelChoice()
        verbosityChoice = whisperHP.verbosity()
        model = whisper.load_model(modelChoice)
        self.result = model.transcribe(
            self.usingFile, verbose=verbosityChoice)
        whisperHP.writeToJson(self)

    def modelChoice():
        modelChoice = input(
            "Which model would you like to use? (medium/large): ")
        # if modelChoice != "medium" or modelChoice != "large":
        #     "Please enter a valid model and relaunch the program"
        #     exit()
        return modelChoice

    def verbosity():
        verbosity = input(
            "Would you like to see the transcription as it is happening? (y/n): ")
        match verbosity:
            case "y":
                return True
            case "n":
                return False

    def writeToJson(self):
        with open(self.jsonname, "w") as fp:
            json.dump(self.result, fp)


def main():

    start = dt.now()

    #             ___  __  _   _  _         _     _   _  _
    #  \    / |_|  |  (_  |_) |_ |_)   |_| |_ |  |_) |_ |_)
    #   \/\/  | | _|_ __) |   |_ | \   | | |_ |_ |   |_ | \
    #                _   _
    #  |_         | | \ / \
    #  |_) \/   \_| |_/ \_/
    #      /
    print("  __                                _     _   _  _  ")
    print(" (_ _|_  _. ._ _|_ o ._   _    |_| |_ |  |_) |_ |_) ")
    print(" __) |_ (_| |   |_ | | | (_|   | | |_ |_ |   |_ | \ ")
    print("                          _|                        ")

    timestamp = str(random.randint(0, 10000000000))
    textname = "Output/transcription" + str(timestamp) + ".txt"
    jsonname = ".backend/dump" + str(timestamp) + ".json"
    with open(jsonname, "w") as fp:
        fp.write("")
    print("")
    file = input("Please insert file here: ")
    file = file[:-1]
    ffmpegHP.convertToWav(file)

    usingFile = '.backend/output.wav'

    transcript = whisperHP(jsonname, usingFile)
    transcript.main()

    # # ******WRITING TO FILE, DELETING UNUSED AUDIO FILE******

    # with open(jsonname, "w") as fp:
    #     json.dump(result, fp)

    os.remove(usingFile)
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


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
