# -*- coding: utf8 -*-
import begin
from colorama import Fore, Back, Style, init
import musicbrainzngs as brainz
from mutagen.mp3 import MP3
import msvcrt
import os
from pygame import mixer
import random
import re
import time


_name = 'Smart Play!'
_version = "0.0.2"


init(autoreset=True)
brainz.set_useragent(_name, _version)


COLOR_COMBINATIONS = [
    Fore.WHITE + Back.CYAN,
    Fore.WHITE + Back.RED,
    Fore.GREEN + Back.BLUE + Style.BRIGHT,
    Fore.MAGENTA + Back.LIGHTGREEN_EX,
    Fore.LIGHTRED_EX + Back.LIGHTWHITE_EX,
]


def colorize_text(text):
    "Colorize printed text randomly"
    return random.choice(COLOR_COMBINATIONS) + text


class MusicInfo(object):
    def __init__(self, filename, filepath):
        self.filename = filename
        self.filepath = filepath
        self._length = None

    @property
    def length(self):
        if not self._length:
            self._length = MP3(self.complete_path).info.length
        return self._length

    @property
    def complete_path(self):
        return os.path.join(self.filepath, self.filename)

    def complement_info(self):
        self._get_info_from_brainz()

    def _get_info_from_brainz(self):
        results = brainz.search_works(alias=self._get_alias())
        try:
            work = results['work-list'][0]
            self.title = work.get('title', None)
            self.artists = [
                a['artist']['name']
                for a in work['artist-relation-list']
                if 'artist' in a]
        except Exception:
            self.title = None
            self.artists = []

    def _get_alias(self):
        title = self.filename
        start_number = re.match("([0-9])+", title)
        if start_number:
            title = title.replace(start_number.group(), "")
        return self.filename \
            .replace(".mp3", "") \
            .replace("-", " ") \
            .replace("_", " ") \
            .replace(".", " ") \
            .strip(" ")


def find_all_songs(path):
    "Finds all MP3 songs under a folder (and its subfolders)"
    all_songs = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".mp3"):
                all_songs.append(
                    MusicInfo(
                        filename=f,
                        filepath=root))
    return all_songs


def select_song(all_songs):
    "Select one of the songs randomly"
    return random.choice(all_songs)


def play_song(music_info):
    mixer.init()
    mixer.music.load(music_info.complete_path)
    mixer.music.play()


def pause_music():
    mixer.music.pause()


def unpause_music():
    mixer.music.unpause()


def print_info(music_info):
    music_info.complement_info()
    if music_info.title:
        print(colorize_text("Music title is " + music_info.title))
    for a in music_info.artists:
        print(colorize_text("* " + a))


def wait_for_command_or_timeout(seconds):
    'Wait for a valid command or timeout until finishes'
    start_time = time.time()
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().upper()
            if key == b'N':
                break
            elif key == b'P':
                pause_music()
            elif key == b'C':
                unpause_music()
            elif key == b'Q':
                exit()
        elif time.time() - start_time > seconds:
            break
        time.sleep(0.5)


@begin.start
def main(folder: "Music folder"):
    print(colorize_text("{} V{}".format(_name, _version)))
    print(colorize_text("[N]ext  [P]ause  [C]ontinue  [Q]uit"))
    all_songs = find_all_songs(folder)
    while True:
        song = select_song(all_songs)
        print(colorize_text("Playing '{}'".format(song.filename)))
        play_song(song)
        wait_for_command_or_timeout(song.length)
