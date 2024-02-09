package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"log"
	"os"

	"github.com/npmaile/NatesPodGen/models"
	"github.com/npmaile/NatesPodGen/rss"
	"github.com/pelletier/go-toml/v2"
)

func main() {
	fmt.Println(`
	|==========================================|
	|                                          |
	|                                          |
	|       Welcome to  Nate's Pod Gen         |
	|             /_ _\                        |
	|            |  -  |                       |
	|             \___/                        |
	|                                          |
	|                                          |
	|                                          |
	|==========================================|
	`)
	podcast, err := readConfig("conf.toml")
	if err != nil {
		log.Fatalf("unable to read configuration %s", errors.Join(err).Error())
	}

	existingEpisodes, err := getExistingEpisodes("episodes.json")
	if err != nil {
		log.Fatalf("unable to read existing episodes %s", errors.Join(err).Error())
	}

	podcast.Episodes = existingEpisodes

	//todo: call the following code to get the last build date time.Now().Format(time.RFC822)
	//todo: set up image link
	//todo: call the same code used to generate a build date to generate an episode release date
	//todo: come up with the location to write the rendered podcast rss
	rss.Render(podcast, w)
	//todo: Podcast.RenderHtml()
}

func getExistingEpisodes(fileName string) ([]models.Episode, error) {
	f, err := os.Open(fileName)
	if err != nil {
		return nil, fmt.Errorf("[readEpisodes] unable to open Episodes file: %w", err)
	}
	confBytes, err := io.ReadAll(f)
	if err != nil {
		return nil, fmt.Errorf("[readEpisodes] unable to read Episodes file: %w", err)
	}
	var episodes []models.Episode
	err = json.Unmarshal(confBytes, &episodes)
	if err != nil {
		return nil, fmt.Errorf("[readEpisodes] unable to decipher Episodes file: %w", err)
	}
	return episodes, nil
}

func readConfig(configName string) (models.Podcast, error) {
	f, err := os.Open(configName)
	if err != nil {
		return models.Podcast{}, fmt.Errorf("[readConfig] unable to open config file: %w", err)
	}
	confBytes, err := io.ReadAll(f)
	if err != nil {
		return models.Podcast{}, fmt.Errorf("[readConfig] unable to read config file: %w", err)
	}
	var pcast models.Podcast
	err = toml.Unmarshal(confBytes, &pcast)
	if err != nil {
		return models.Podcast{}, fmt.Errorf("[readConfig] unable to decipher config file: %w", err)
	}
	return pcast, nil
}
