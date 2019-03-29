#!/usr/bin/env python3
import os
import shutil
import argparse
import configparser
import re
import datetime
import time    
parser = argparse.ArgumentParser(description="add an entry to feed.ini")
parser.add_argument('mp3file', type=str , nargs=1 , help='The mp3 file to be added to your feed')
parser.add_argument('-i','--image',type=str,nargs=1,default = None ,help='the optional episode specific image for your episode')
args = parser.parse_args()
mp3filepath = vars(args)['mp3file'][0]

print(mp3filepath)

def calclength(mp3file):
    answer = input('what is the length of your mp3 audio file?(HH:MM:SS)')
    while not re.match('[0-9][0-9]:[0-9][0-9]:[0-9][0-9]',answer):
        answer = input('Please put it in the correct format')##todo generate this instead of asking for it because I'm a good programmer, Damnit!
    return answer

def getuuid():
    config = configparser.ConfigParser()
    config.read('feed.ini')
    maxnumber = 0
    for x in config.sections():
        try:
            if config[x]['uuid'] is not None:
                if int(config[x]['uuid']) > maxnumber:
                    maxnumber = int(config[x]['uuid'])
        except KeyError:
            pass

    return maxnumber
    

def askforreleasedate():
    validMonths = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
    answer = input('Would you like to release immediately?[y,N]')
    if answer[0].lower() == 'y':
        today = datetime.date.fromtimestamp(time.time())
        return today.strftime('%Y %b %d')

    else:
        print('tough tiddies')
        return input("When would you like to release(dd mon yyyy):")

image = None
   
uniqueid = getuuid() + 1
title = input("Title: ")
description = input("Description")
title = str(uniqueid) + ':' + title
itunesCategory = input("itunes Category")
itunesKeywords = input("itunes Keywords(separated by commas)") 
releaseDate = askforreleasedate()
duration = calclength(mp3filepath)

link = 'episodes/' + title + '.mp3'
print('copying the mp3 file to' + 'site/' + link)
shutil.copy(mp3filepath,'site/' + link)

if vars(args)['image'] is not None:
    image = args['image'][0]
    imagePath = 'site/images/' + uniqueid + ':' + description
    print('copying the image file to' + imagePath)
    shutil.copy(image,imagepath)
 


with open("feed.ini",'a') as feedfile:
    feedfile.write('[' + title + ']\n')
    feedfile.write('description = ' + description + '\n')
    feedfile.write('releaseDate = ' + releaseDate + '\n')
    feedfile.write('uniqueid = ' + str(uniqueid) + '\n')
    feedfile.write('itunesCategory = ' + itunesCategory + '\n')
    feedfile.write('duration = ' + duration + '\n')
    feedfile.write('itunesKeywords = ' + itunesKeywords + '\n')
    feedfile.write('link = ' + link + '\n')
    if image is not None:
        feedfile.write('image = ' + imagepath + '\n')



