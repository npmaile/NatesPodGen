package models

import "time"

type Episode struct {
	Link        string
	Title       string
	Description string
	Releasedate time.Time
	UniqueId    string
	Keywords    string
	Duration    string
	AltImage    string
	BytesLength int
}

type Podcast struct {
	Builddate     time.Time
	Homepage      string
	Feedlocation  string
	Title         string
	Description   string
	Language      string
	Imagelocation string
	OwnerName     string
	Owneremail    string
	Category      string
	Episodes      []Episode
	Explicit      bool
}
