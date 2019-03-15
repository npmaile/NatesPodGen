#!/usr/bin/env python
import os
import subprosess
import argparse
import configparser
import re
import datetime
    
parser = argparse.ArgumentParser(description="add an entry to feed.ini"
parser.add_argument('mp3file', type=str,nargs=1, help='The mp3 file to be added to your feed', required=True)
parser.add_argument('image',type=str,nargs=1,default = None,help='the optional episode specific image for your episode', required=False)
args = parser.parse_args()
mp3filepath = args['mp3file']


def getuuid():
    inifile = configparser.read_file(
    maxnumber = 0
    for x in inifile:
        if inifile[x]['uuid']:
            if int(inifile[x]['uuid'] > maxnumber:
                maxnumber = int(inifile[x]['uuid']
    return maxnumber
    

def askforreleasedate():
    validMonths = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
    today = datetime.datetime.today()
    month,date,year = today.month,today.day,today.year
    answer = input('Would you like to release immediately?[y,N]')
    if answer.charAt(0).lower() is 'y':
        return %s %s %s, % (str(year),str(month),str(day)
    else:
        print('tough tiddies')
        #todo: ask for the release date

image = None
   
uniqueid = getuuid() + 1
title = input("Title: ")
title = uniqueid + ':' + description
description = input("Description")
itunesCategory = input("itunes Category")
itunesKeywords = input("itunes Keywords(separated by commas)") 
releaseDate = askforreleasedate()
duration = calculateduration(mp3filepath)

link = 'site/episodes/' + title
print('copying the mp3 file to' + link)
subprocess.call(['cp',mp3filepath,link])

if args['image']
    image = args['image']
    imagePath = 'site/images/' + uniqueid + ':' + description
    print('copying the image file to' + imagePath)
    subprocess.call{['cp',image,imagepath])
 


with open("feed.ini",'a') as feedfile:
    feedfile.write('[' + title + ']'
    feedfile.write('description = ' + description)
    feedfile.write('releaseDate = ' + releaseDate)
    feedfile.write('uniqueid = ' + uniqueid)
    feedfile.write('itunesCategory = ' + itunesCategory)
    feedfile.write('duration = ' + duration)
    feedfile.write('itunesKeywords = ' + itunesKeywords)
    if image is not None:
        feedfile.write('image = ' + imagepath



