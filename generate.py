#!/usr/bin/env python3
import xml.dom.minidom
import configparser
import datetime
from email.utils import formatdate
import os
import re

class Episode:
    def __init__(self, link, length, title, description, releasedate, uniqueId, keywords, duration, altImage = None)
        self.link = link
        self.length = length
        self.title = title
        self.description = description 
        self.releasedate = releasedate
        self.uniqueId = uniqueId
        self.keywords = keywords
        self.duration = duration
        self.altImage = altImage

class Podcast:
    def __init__(self,externalroot,feedlocation,title,description,language,imagelocation,explicit,ownername,owneremail,category))
        self.episodes = []
        self.externalroot = externalroot
        self.feedlocation = feedlocation
        self.title = title
        self.description = description
        self.language = language
        self.builddate = builddate
        self.imagelocation = imagelocation
        self.explicit = explicit
        self.ownername = ownername
        self.owneremail = owneremail
        self.category = category
        self.builddate = formatdate()
def PopulateClasses(config):
    globalconfig = config['global']
    Cast = Podcast(\
            externalroot = globalconfig['externalSiteRoot'],\
            feedlocation = globalconfig['feedlocation'],\
            title = globalconfig['title'],\
            description = globalconfig['description'],\
            language = globalconfig['language'],\    
            imagelocation = globalconfig['imageUrlFromRoot'],\
            explicit = globalconfig['explicit'],\ 
            ownername = globalconfig['ownerName'],\
            owneremail = globalconfig['ownerEmail'],\
            category = globalconfig['category'])

    for episode in config.sections():
        if episode == 'global':
            pass
        else:
            ep = config[episode]
            Cast.append(Episode(\
                    link = ep['link'],\
                    length = str(os.path.getsize(config['global']['serverSiteRoot'] + '/' + config[section]['link'])),\
                    title = ep['title'],\
                    description = ep['description'],\
                    releasedate = formatdate(float(datetime.datetime.strptime(ep['releaseDate'],  '%Y %b %d').strftime('%s']))),\
                    uniqueId = ep['uniqueid'],\
                    keywords = ep['itunesKeywords'],\
                    duration = ep['duration']))

def genRss(config):
    podcast = PopulateClasses(config)

    headerxml = '''<rss version= "2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"><channel>
                        <atom:link href="'''        + podcast.externalroot + '/' + podcast.feedlocation + '''" rel="self" type="application/rss+xml" />
                        <title>'''                  + podcast.title + '''</title>
                        <link>'''                   + podcast.link + '''</link>
                        <description>'''            + podcast.description + '''</description>
                        <language>'''               + podcast.language + '''</language>
                        <lastBuildDate> '''         + formatdate() +'''</lastBuildDate>
                        <generator>Nate's sweet custom podcast generator</generator>
                        <webMaster>'''              + podcast.owneremail +' (' + podcast.ownername + ')' '''</webMaster>
                        <image>
                            <url>'''                + podcast.externalroot +'/'+ podcast.imagelink + '''</url>
                            <link>'''               + config['global']['externalSiteRoot'] + '''</link>
                            <title>'''              + config['global']['title'] + '''</title> 
                        </image>
                        <itunes:author>'''          + config['global']['ownerName'] + '''</itunes:author>
                        <itunes:explicit>'''        + config['global']['explicit'] + '''</itunes:explicit>
                        <itunes:owner>
                            <itunes:email>'''       + config['global']['ownerEmail'] + '''</itunes:email>
                            <itunes:name>'''        + config['global']['ownerName'] + '''</itunes:name>
                        </itunes:owner>
                        <itunes:category text="'''  + config['global']['category']+ '''"/>'''

    tailxml = '''</channel></rss>'''

    episodes = ''
    for section in config.sections():
        
        if section == 'global':
            pass
        else:
            releasedate = datetime.datetime.strptime(config[section]['releaseDate'], '%Y %b %d')
            if releasedate < datetime.datetime.now():
                podcasttime = ''
                #generate the length of the podcast some kind of way
                episodes += '''
                        <item>
                        <enclosure url="'''         + config['global']['externalSiteRoot'] + '/' + config[section]['link'] + '\" length=\"' + str(os.path.getsize(config['global']['serverSiteRoot'] + '/' + config[section]['link'])) + '''" type="audio/mpeg"/>
                        <title>'''                  + section + '''</title>
                        <description>'''            + config[section]['description'] + '''</description>
                        <pubDate>'''                + formatdate(float(releasedate.strftime('%s'))) + '''</pubDate>
                        <guid isPermaLink="false">''' + config['global']['externalSiteRoot'] + '/#' + config[section]['uniqueid'] + '''</guid>
                        <link>'''                   + config['global']['externalSiteRoot'] + '/'+ config[section]['link'] + '''</link>
                        <itunes:keywords>'''        +config[section]['itunesKeywords'] + '''</itunes:keywords>
                        <itunes:duration>'''        + str(config[section]['duration']) +'''</itunes:duration>
                        </item>
                        '''
    rssxml = xml.dom.minidom.parseString(headerxml + episodes + tailxml)
    with open("site/podcast.rss",'w+') as rssfeed:
        rssfeed.write(rssxml.toprettyxml())

configfile = configparser.ConfigParser()
config.read('feed.ini')
with open("site/podcast.rss",'w+') as rssfeed:
    rssfeed.write(genRss(config))

