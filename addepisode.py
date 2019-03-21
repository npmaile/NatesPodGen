#!/usr/bin/env python3
import os
import subprocess
import argparse
import configparser
import re
import datetime
    
parser = argparse.ArgumentParser(description="add an entry to feed.ini")
parser.add_argument('mp3file', type=str , nargs=1 , help='The mp3 file to be added to your feed')
parser.add_argument('-i','--image',type=str,nargs=1,default = None ,help='the optional episode specific image for your episode')
args = parser.parse_args()
mp3filepath = args['mp3file']

def calclength(mp3file):
    answer = input('what is the length of your mp3 audio file?(HH:MM:SS)'
            while not re.match('[1-9]2:[1-9]2:[1-9]2',answer):
                answer = input('Please put it in the correct format')##todo generate this instead of asking for it because I'm a good programmer, Damnit!

def getuuid():
    inifile = configparser.read_file('feed.ini')
    maxnumber = 0
    for x in inifile.sections():
        if inifile[x]['uuid'] is not None:
            if int(inifile[x]['uuid']) > maxnumber:
                maxnumber = int(inifile[x]['uuid'])

    return maxnumber
    

def askforreleasedate():
    validMonths = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
    today = datetime.datetime.today()
    month,date,year = today.month,today.day,today.year
    answer = input('Would you like to release immediately?[y,N]')
    if answer.charAt(0).lower() is 'y':
        return "%s %s %s".format(str(year),str(month),str(day))
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

if args['image'] is not None:
    image = args['image']
    imagePath = 'site/images/' + uniqueid + ':' + description
    print('copying the image file to' + imagePath)
    subprocess.call(['cp',image,imagepath])
 


with open("feed.ini",'a') as feedfile:
    feedfile.write('[' + title + ']')
    feedfile.write('description = ' + description)
    feedfile.write('releaseDate = ' + releaseDate)
    feedfile.write('uniqueid = ' + uniqueid)
    feedfile.write('itunesCategory = ' + itunesCategory)
    feedfile.write('duration = ' + duration)
    feedfile.write('itunesKeywords = ' + itunesKeywords)
    if image is not None:
        feedfile.write('image = ' + imagepath)



