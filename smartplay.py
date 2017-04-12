# -*- coding: utf8 -*-
import begin
from colorama import Fore, Back, init, Style
from mutagen.mp3 import MP3
import os
from pygame import mixer
import random
import time


init(autoreset=True)


COLOR_COMBINATIONS = [
    Fore.WHITE + Back.CYAN,
    Fore.RED + Back.WHITE,
    Fore.GREEN + Back.BLUE,
    Fore.MAGENTA + Back.LIGHTGREEN_EX,
]


def colorize_text(text):
    return random.choice(COLOR_COMBINATIONS) + text


def find_all_songs(path):
    all_songs = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".mp3"):
                all_songs.append((f, root + "\\" + f))
    return all_songs


def select_song(all_songs):
    return random.choice(all_songs)


def play_song(song_name):
    mixer.init()
    mixer.music.load(song_name)
    mixer.music.play()
    time.sleep(_get_mp3_length(song_name))


def _get_mp3_length(song_name):
    return MP3(song_name).info.length


@begin.start
def main(path):
    "Plays a random song from this folder"
    print(Fore.WHITE + Back.CYAN + "Smart Play! V0.0.1")
    all_songs = find_all_songs(path)
    while True:
        song = select_song(all_songs)
        print(colorize_text("Playing {}".format(song[0])))
        play_song(song[1])
