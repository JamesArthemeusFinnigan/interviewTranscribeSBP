__author__ = "Your Name"
__version__ = "0.1.0"
__license__ = "MIT"


def main():
    import whisper_timestamped as whisper
    import os
    from datetime import datetime as d
    import time
    import json
    import random
    from datetime import datetime as dt
    import wave
    import contextlib
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
    print("  __                            _  _       _   _  __ ")
    print(" (_ _|_  _. ._ _|_ o ._   _    |_ |_ |\/| |_) |_ /__ ")
    print(" __) |_ (_| |   |_ | | | (_|   |  |  |  | |   |_ \_| ")
    print("                          _|                         ")
    print("")
    print("*************************************")
    print("FFMPEG is now converting your file to a .wav file")
    print("*************************************")
    start = dt.now()

    cmd = "ffmpeg -i "+str(file)+" -c:a libmp3lame -q:a 8 .backend/output.mp3"

    os.system(cmd)

    usingFile = '.backend/output.mp3'
    import soundfile as sf
    f = sf.SoundFile(usingFile)
    frames = f.frames
    sampleRate = f.samplerate
    duration = frames / sampleRate

    print("  __                                      ___  __  _   _  _  ")
    print(" (_ _|_  _. ._ _|_ o ._   _    \    / |_|  |  (_  |_) |_ |_) ")
    print(" __) |_ (_| |   |_ | | | (_|    \/\/  | | _|_ __) |   |_ | \ ")
    print("                          _|                                 ")
    print("")
    print("*************************************")
    print("Whisper is now transcribing your file")
    print("*************IMPORTANT*************")
    print("Please do not close the program until the transcription is complete")
    audio = whisper.load_audio(".backend/output.mp3")
    modelChoice = input("Which model would you like to use? (medium/large): ")
    match modelChoice:
        case "medium":
            model = whisper.load_model('medium', device='cpu')
        case "large":
            model = whisper.load_model('large', device='cpu')
        case other:
            print("Please enter a valid model and relaunch the program")
            exit()
    timestamps = input(
        "How many seconds apart should timestamps be set? (Please enter time in SECONDS): ")
    fileName = input(
        "What would you like to name the file? (Please do not include file extension): ")
    result = whisper.transcribe(model, audio)
    with open(jsonname, "w") as fp:
        json.dump(result, fp)
    os.remove(usingFile)
    with open(jsonname, "r") as json_file:
        word_dict = json.load(json_file)
    TS = 0
    nextTS = TS + int(timestamps)
    textString = ""
    for segment in word_dict["segments"]:
        i = 0
        for word in segment["words"]:
            print(word)
            if word["start"] >= nextTS:
                hours = int(nextTS // 3600)
                minutes = int((nextTS % 3600) // 60)
                seconds = int(nextTS % 60)
                TS_Formatted = "[{:0>2}:{:0>2}:{:0>2}]".format(
                    hours, minutes, seconds)
                textString += " "
                textString += TS_Formatted
                textString += " "
                textString += word["text"]
                TS = nextTS
                nextTS = TS + int(timestamps)
            elif i != 0:
                if word["start"] >= segment["words"][i-1]["end"]+0.5:
                    textString += "\n"
                    textString += word["text"]
                else:
                    textString += " "
                    textString += word["text"]
            else:
                textString += " "
                textString += word["text"]
            i += 1
    with open(fileName, "w") as text_file:
        text_file.write(textString)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
