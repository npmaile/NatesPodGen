package rss

import (
	"html/template"
	"io"

	"github.com/npmaile/NatesPodGen/models"
)

var templ *template.Template

func init() {
	var err error
	templ, err = template.New("rss_feed").Parse(rsstemplate)
	if err != nil {
		panic("unable to parse template")
	}
}

func Render(data models.Podcast, writer io.Writer) error {
	return templ.Execute(writer, data)
}

const rsstemplate = `
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
	<channel>
		<atom:link href="{{.FeedLocation}}" rel="self" type="application/rss+xml"/>
		<title>{{.Title}}</title>
		<link>{{.Homepage}}</link>
		<description>.Description</description>
		<language>.Language</language>
		<lastBuildDate> Thu, 12 Nov 2020 22:39:23 -0000</lastBuildDate>
		<generator>Nate's sweet custom podcast generator</generator>
		<webMaster>{{.OwnerEmail}} ({{.OwnerName}})</webMaster>
		<image>
			<url>https://podcast.npmaile.com/images/logo.png</url>
			<link>{{.Homepage}}</link>
			<title>{{.Title}}</title>
		</image>
		<itunes:author>{{.OwnerName}}</itunes:author>
		<itunes:explicit>{{if .Explicit}}yes{{else}}no{{end}}</itunes:explicit>
		<itunes:owner>
			<itunes:email>{{.OwnerEmail}}</itunes:email>
			<itunes:name>{{.OwnerName}}</itunes:name>
		</itunes:owner>
		<itunes:category text="{{.Category}}"/>
		{{range .Episodes}}
		<item>
			<enclosure length="{{.BytesLength}}" type="audio/mpeg" url="{{.Link}}"/>
			<title>{{.Title}}</title>
			<description>{{.Description}}</description>
			<pubDate>Mon, 11 Mar 2019 00:00:00 -0000</pubDate>
			<guid isPermaLink="false">https://podcast.npmaile.com/#1</guid>
			<link>{{.Link}}</link>
			<itunes:keywords>{{.Keywords}}</itunes:keywords>
			<itunes:duration>{{.Duration}}</itunes:duration>
			<itunes:image href="{{.AltImage}}"/>
		</item>
		{{end}}
	</channel>
</rss>`
