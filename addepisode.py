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
workingPath = os.path.realpath("/".join(__file__.split('/')[:-1])
print(mp3filepath)

def calclength(mp3file):
    answer = input('what is the length of your mp3 audio file?(HH:MM:SS)')
    while not re.match('[0-9][0-9]:[0-9][0-9]:[0-9][0-9]',answer):
        answer = input('Please put it in the correct format')##todo generate this instead of asking for it because I'm a good programmer, Damnit!
    return answer

def getuniqueid():
    config = configparser.ConfigParser()
    config.read('feed.ini')
    maxnumber = 0
    for x in config.sections():
        try:
            if config[x]['uniqueid'] is not None:
                if int(config[x]['uniqueid']) > maxnumber:
                    print(config[x]['uniqueid'])
                    maxnumber = int(config[x]['uniqueid'])
        except KeyError: #this is probably not a great way to do this
            pass

    return maxnumber
    

def askforreleasedate():
    validMonths = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec')
    answer = input('Would you like to release immediately?[y,N]')
    if answer[0].lower() == 'y':
        today = datetime.date.fromtimestamp(time.time())
        return today.strftime('%Y %b %d')

    else:
        date = input("When would you like to release(yyyy mon dd):")
        while not re.match('[0-9][0-9][0-9][0-9]\s(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s[0-9][0-9]', date):
            date = input("date did not match the format. please input it in format of yyyy mon(month abbreviated to three characters) dd")
        return date

image = None
uniqueid = getuniqueid() + 1
title = input("Title: ")
description = input("Description")
title = str(uniqueid) + ':' + title
itunesCategory = input("itunes Category")
itunesKeywords = input("itunes Keywords(separated by commas)") 
releaseDate = askforreleasedate()
duration = calclength(mp3filepath)

link = 'episodes/' + title + '.mp3'
print('copying the mp3 file to' + workingPath + '/site/' + link)
shutil.copy(mp3filepath, workingPath + '/site/' + link)

if vars(args)['image'] is not None:
    image = args['image'][0]
    imagePath = 'site/images/' + uniqueid + ':' + description
    print('copying the image file to' + workingPath+ '/' + imagePath)
    shutil.copy(image, workingPath + '/' + imagepath)
 


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



