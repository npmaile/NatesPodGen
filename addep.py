#!/usr/bin/env python
import os
import subprosess
import argparse
import configparser
import re
import datetime

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
    
def calculateduration(path):
    duration = input('what is the duration of your podcast h:mm:ss')
    #todo: actually calculate this... actually probably calculate this in the genrate script
    return duration

parser = argparse.ArgumentParser(description="add an entry to feed.ini"
parser.add_argument('mp3file', type=str,nargs=1, help='The mp3 file to be added to your feed', required=True)
parser.add_argument('image',type=str,nargs=1,default = None,help='the optional episode specific image for your episode', required=False)
args = parser.parse_args()
mp3filepath = args['mp3file']


image = None
if args['image']
    image = args['image']

title = input("Title: ")
description = input("Description")
itunesCategory = input("itunes Category")
itunesKeywords = input("itunes Keywords(separated by commas)") 
releaseDate = askforreleasedate()
uniqueid = getuuid() + 1
duration = calculateduration(mp3filepath)

link = 'site/episodes/' + uniqueid +':'+ description
print('copying the mp3 file to' + link
subprocess.call(['cp',mp3filepath,'site/episodes/' + 

with open("feed.ini",'a') as feedfile:

