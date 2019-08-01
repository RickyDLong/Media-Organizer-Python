#! /usr/bin/python3
'''
Directories can be edited in config.json...
This will remove any unwanted file types from root.
It will then look into the source folder to check if new movies have been added and if so, move them
to root. It will then proceed to clean up empty subfolders in both directories
'''

import os
import os.path
import shutil
import json
import time

movie_directory = ''
junk_files = ()
movie_files = ()
download_directory = ''

def load_config():
    global config, movie_directory, junk_files, movie_files, download_directory
    with open('config.json') as config_data:
        config = json.load(config_data)

    movie_directory = (config['movie_directory'])
    junk_files = tuple(config['junk_files'])
    download_directory = (config['download_directory'])
    movie_files = tuple(config['media_files'])

load_config()


#Searches through movie_directory and deletes file extensions contained in junk_files
def remove_trash_files(movie_directory, junk_files):
    print('----------REMOVING UNWANTED FILES----------\n')
    c = 0
    for dirpath, dirnames, filenames in os.walk(movie_directory, topdown = False):
        for filename in filenames:
            if filename.endswith(junk_files):
                 os.remove(os.path.join(dirpath, filename))
                 c += 1
    print("{0} non-movie file(s) removed from the Movie Database.\n".format(c))
remove_trash_files(movie_directory, junk_files)

#Searches download_directory and subfolders for file types that contain movie_files and moves them to movie_directory
def move_files(movie_directory, download_directory, junk_files):
    print('----------MOVING FILES ----------')
    c = 0
    for dirpath, dirnames, filenames in os.walk(download_directory):
        for filename in filenames:
            if os.path.exists(os.path.join(movie_directory, filename)):
                print('This file already exists in movie directory')
            else:
                    old_dir = os.path.join(dirpath, filename)
                    new_dir = os.path.join(movie_directory, filename)
                    shutil.move(old_dir, new_dir)
                    c += 1
    print('{0} files have been moved to {1}\n'.format(c, movie_directory))
move_files(movie_directory, download_directory, movie_files)


#Deletes left-over empty subfolders
def remove_empty_folders(movie_directory):
    print('----------Deleting Sub-Folders----------\n')
    c = 0
    for dirpath, dirnames, filenames in os.walk(movie_directory, topdown=False):
        if filenames: continue
        try:
            os.rmdir(dirpath)
            c += 1
        except OSError as ex:
            print('Error: ', ex)

remove_empty_folders(movie_directory)

#Deletes left-over empty subfolders inside download_directory
def remove_empty_folders2(download_directory):
    for (dirpath, dirnames, filenames) in os.walk(download_directory):
        if filenames: continue
        try:
            os.rmdir(dirpath)
        except OSError as ex:
            print('Error: ', ex)

remove_empty_folders2(download_directory)
print('----------DONE-----------\n')
