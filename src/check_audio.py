import sys
import os
import json
import time
from playsound import playsound
import multiprocessing
from mutagen.mp3 import MP3

if len(sys.argv) != 3:
    print("Usage script " + sys.argv[0] + " arg1-audio files" + " arg2-json file")
    quit()


def play_audio(fn):
    audio = MP3(fn)
    t = audio.info.length
    proc = multiprocessing.Process(target=playsound, args=(fn,))
    proc.start()
    time.sleep(t)
    proc.terminate()


def repeat(fn):
    while True:
        listen_again = input("Would you like to listen again 'y/n'? ")
        if listen_again == "y":
            play_audio(fn)
        elif listen_again == "n":
            break
        else:
            print("Please type 'y' or 'n'")


def write_in_file(fn, json_file):
    while True:
        status = input("Is it noisy or clean (n/c)? ")
        if status == "n" or status == "N" or status == "c" or status == "C":
            json_dict = {fn: status}
            json_string = json.dumps(json_dict)
            json_file.writelines(json_string + ',' + '\n')
            break
        else:
            print("Please type [N]oisy or [C]lear")


def start_process():
    json_file = open(sys.argv[2], "w")
    json_file.write('[')
    if os.path.isdir(sys.argv[1]):
        for fn in os.listdir(sys.argv[1]):
            os.chdir(sys.argv[1])
            if fn.endswith('.mp3'):
                play_audio(fn)
                repeat(fn)
                write_in_file(fn, json_file)
    elif os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.mp3'):
        os.chdir(os.path.dirname(sys.argv[1]))
        play_audio(os.path.basename(sys.argv[1]))
        repeat(os.path.basename(sys.argv[1]))
        write_in_file(os.path.basename(sys.argv[1]), json_file)
    else:
        print("Please give a valid mp3 audio file or directory")
        quit()

    json_file.write(']')
    json_file.close()
    os.chdir('..')
    print("Generated results at: " + sys.argv[2])


if __name__ == '__main__':
    start_process()
