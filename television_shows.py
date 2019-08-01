#!/usr/bin/python3

import os
import shutil
import os.path
import re

def find_shows():
    tv_dir = ('E:\Videos\Media Database\Television Shows')
    for dirpath, dirnames, filenames in os.walk('e:/videos/media database', topdown = False):
        for filename in filenames:
            if re.search(r'[0-9][a-zA-Z][0-9][0-9]',filename,re.IGNORECASE):
                print('Television Episode Found: ' + filename)
'''
            else:
                try:
                    old_dir = os.path.join(dirpath, filename)
                    new_dir = os.path.join(tv_dir, filename)
                    shutil.move(old_dir, tv_dir)
                except OSError as ex:
                    print('Error: ', ex)
'''
find_shows()
