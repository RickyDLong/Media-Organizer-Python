#!/usr/bin/python3

import json
import re
import os
import os.path
import shutil
import fnmatch

movie_directory = ''
junk_files = ()
movie_files = ()
download_directory = ''
tv_directory = ''

#regex patterns
date_pattern = (r'([12][0-9]{3}).*')
tv_pattern = (r'([S-s]\d[0-9][E-e]\d[0-9]).*')

#setting up json.config
def load_config():
    global config, movie_directory, junk_files, movie_files, download_directory, tv_directory
    with open('config.json') as config_data:
        config = json.load(config_data)

    movie_directory = (config['movie_directory'])
    junk_files = tuple(config['junk_files'])
    download_directory = (config['download_directory'])
    movie_files = tuple(config['media_files'])
    tv_directory = (config['tv_directory'])
load_config()

#Function to move and rename television files
def move_tv_files(tv_directory, download_directory):
    print('----------MOVING TELEVISION SHOWS ----------')
    c = 0 #This sets the count to 0
    for dirpath, dirnames, filenames in os.walk(download_directory):
        for filename in filenames:
            #searches target directory to see if the file is already there
            if os.path.exists(os.path.join(tv_directory, filename)):
                print('FILE ALREADY EXISTS!')
            else:
                if filename.endswith(movie_files):
                    print('Changing ' +filename, 'to:')
                    #splits file name from file extension so that it can be renamed
                    title = list(os.path.splitext(filename))
                    #Removes periods and dashes from filename
                    title[0] = re.sub(r'\.|\_|\(|\)', '', title[0])
                    clean_title = (''.join(title))
                    #searches the [0] index (name) of the file for the regex pattern in tv_pattern
                    a = re.search(tv_pattern, clean_title, re.IGNORECASE)
                    clean_title = re.sub(tv_pattern, '', clean_title) + a.group(1)
                    #targeting filename for the rename
                    b = os.path.join(dirpath,filename)
                    d = os.path.join(dirpath,clean_title +title[1])
                    print(clean_title +title[1])
                    #renaming the file
                    os.rename(b, d)
                    print('_______________________________')
                    #Moves them from movie directory to tv directory
                    old_dir = os.path.join(dirpath, filename)
                    new_dir = os.path.join(tv_directory, filename)
                    shutil.move(old_dir, new_dir)
                    c += 1 #Counts out how many files are moved so that it can reflect in print statement
    print('{0} files have been moved to {1}\n'.format(c, movie_directory))
move_tv_files(tv_directory, download_directory)


#Function to move movies to proper folder
def move_files(movie_directory, download_directory, movie_files):
    print('----------MOVING MOVIE FILES ----------')
    c = 0
    for dirpath, dirnames, filenames in os.walk(download_directory):
        for filename in filenames:
            if os.path.exists(os.path.join(movie_directory, filename)):
                print('This file already exists in movie directory')
            else:
                if filename.endswith(movie_files):
                    old_dir = os.path.join(dirpath, filename)
                    new_dir = os.path.join(movie_directory, filename)
                    shutil.move(old_dir, new_dir)
                    c += 1
    print('{0} files have been moved to {1}\n'.format(c, movie_directory))
move_files(movie_directory, download_directory, movie_files)


# Searches for and corrects movie names to have proper format.
def fix_names(movie_directory):
    print('--------RENAMING MOVIE FILE(S):---------')
    c = 0
    for dirpath, dirnames, filenames in os.walk(movie_directory):
        for filename in filenames:
            #searching for movie files
            if filename.endswith(movie_files):
                print('Changing ' +filename, 'to:')
                #splitting filename from extension for rename
                title = list(os.path.splitext(filename))
                title[0] = re.sub(r'\.|\_|\(|\)', '', title[0])
                clean_title = (''.join(title))
                #applying regex pattern to filename
            try:
                a = re.search(date_pattern, clean_title)
                clean_title = re.sub(date_pattern, '', clean_title) + a.group(1)
                b = os.path.join(dirpath,filename)
                d = os.path.join(dirpath,clean_title +title[1])
                print(clean_title +title[1])
                #renaming file
                os.rename(b, d)
                c += 1
                print('_______________________________')
            except Exception as err:
                print('\n' +clean_title, ' does not fit the regex format\n''----------------------------------')
fix_names(movie_directory)
