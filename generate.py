#!/usr/bin/env python3
import xml.dom.minidom
import configparser
import datetime
from email.utils import formatdate
import os
import re


config = configparser.ConfigParser()
config.read('feed.ini')

headerxml = '''<rss version= "2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"><channel>
                    <atom:link href="'''        + config['global']['externalSiteRoot'] + '/' + config['global']['feedLocation'] + '''" rel="self" type="application/rss+xml" />
                    <title>'''                  + config['global']['title'] + '''</title>
                    <link>'''                   + config['global']['externalSiteRoot']+ '''</link>
                    <description>'''            + config['global']['description'] + '''</description>
                    <language>'''               + config['global']['language'] + '''</language>
                    <lastBuildDate> '''         + formatdate() +'''</lastBuildDate>
                    <generator>Nate's sweet custom podcast generator</generator>
                    <webMaster>'''              + config['global']['ownerEmail'] +' (' + config['global']['ownerName'] + ')' '''</webMaster>
                    <image>
                        <url>'''                + config['global']['externalSiteRoot']+'/'+config['global']['imageUrlFromRoot'] + '''</url>
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
