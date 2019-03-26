#!/usr/bin/env python3
from string import Template
from email.utils import formatdate
import os, re, configparser, xml.dom.minidom, datetime

indextemplatefile = 'templates/html/index.html'
episodestemplatefile = 'templates/html/podcastsection.html'

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

def populateClasses(config):
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
            newepisode = Episode(\
                    link = ep['link'],\
                    length = str(os.path.getsize(globalconfig['serverSiteRoot'] + '/' + ep['link'])),\
                    title = ep['title'],\
                    description = ep['description'],\
                    releasedate = formatdate(float(datetime.datetime.strptime(ep['releaseDate'],  '%Y %b %d').strftime('%s']))),\
                    uniqueId = ep['uniqueid'],\
                    keywords = ep['itunesKeywords'],\
                    duration = str(ep['duration']))
            try:
                newepisode.altImage = ep['image']
            except KeyError:
                newepisode.altImage = globalconfig['imageUrlFromRoot']

## I could have done this whole thing with the xml tree builtin, but I didn't for two reasons 1. I hate using that module and 2. It's much more difficult to read and understand for no good reason other than "it's pythonic"
## Don't @ me.
def genRss(podcast):
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
                            <link>'''               + podcast.externalroot + '''</link>
                            <title>'''              + podcast.title + '''</title> 
                        </image>
                        <itunes:author>'''          + podcast.ownername + '''</itunes:author>
                        <itunes:explicit>'''        + podcast.explicit + '''</itunes:explicit>
                        <itunes:owner>
                            <itunes:email>'''       + podcast.owneremail + '''</itunes:email>
                            <itunes:name>'''        + podcast.ownername + '''</itunes:name>
                        </itunes:owner>
                        <itunes:category text="'''  + podcast.category + '''"/>'''

    tailxml = '''</channel></rss>'''
    episodes = ''
        for episode in podcast.episodes:
            if episode.releasedate < datetime.datetime.now():
                episodes += '''
                        <item>
                        <enclosure url="'''         + podcast.externalroot + '/' + episode.link + '\" length=\"' + episode.length + '/' + episode.length + '''" type="audio/mpeg"/>
                        <title>'''                  + episode.title + '''</title>
                        <description>'''            + episode.description + '''</description>
                        <pubDate>'''                + episode.releasedate + '''</pubDate>
                        <guid isPermaLink="false">''' + podcast.externalroot + '/#' + episode.uniqueId + '''</guid>
                        <link>'''                   + podcast.externalroot + '/'+ episode.link + '''</link>
                        <itunes:keywords>'''        + episode.keywords + '''</itunes:keywords>
                        <itunes:duration>'''        + episode.duration +'''</itunes:duration>
                        <itunes:image href="'''     + episode.altImage + '''/>
                        </item>
                        '''
    return  xml.dom.minidom.parseString(headerxml + episodes + tailxml).toprettyxml()

def genHtml(podcast,indexTemplate,episodeTemplate):
    episodestemplatestring = ''
    
    with open(episodehtmltemplatefile, 'r') as episodehtmltemplatehandler:
        episodetemplatestring = episodehtmltemplatehandler.read()
    
    compiledEpisodes = ''

    for episode in podcast.episodes:
        episodereplacements = dict(\
                image=episode.altImage,\
                episodeTitle=episode.title,\
                mp3file=episode.link,\
                description=episode.description
                )
    
        episodetemplate = Template(episodestemplatestring)
        compiledEpisodes.append(episodetemplate.substitute(episodereplacements))

    mainreplacements = dict(\
            Title=podcast.title,\
            globalDescription=podcast.description,\
            EpisodesHtml=compiledEpisodes,\
            image=podcast.imagelink\
            )
    
    templatestring = ''
    
    with open(indexhtmltemplatefile, 'r') as indexhtmltemplatehandler:
        templatestring = indexhtmltemplatehandler.read()
    
    maintemplate = Template(templatestring)
    indexhtmlshellstring = maintemplate.substitute(mainreplacements)

    return xml.dom.minidom.parseString(fullhtml).toprettyxml()

print('parsing configfile')
config = configparser.ConfigParser()
config.read('feed.ini')
podcast = populateClasses(config)

print('Writing rss feed')
with open("site/podcast.rss",'w+') as rssfeed:
    rssfeed.write(genRss(config))

print('Writing html site')
with open("site/index.html",'w+') as htmlsite:
    htmlsite.write(genHtml(config))

print('Done!')

