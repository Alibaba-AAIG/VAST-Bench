package fetcher

import (
	"encoding/json"
	"os"
)

type Source struct {
	Name string `json:"name"`
	URL  string `json:"url"`
}

type Settings struct {
	StagingDir string   `json:"staging_dir"`
	Sources    []Source `json:"sources"`
}

func LoadSettings(path string) (Settings, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return Settings{}, err
	}
	var settings Settings
	if err := json.Unmarshal(data, &settings); err != nil {
		return Settings{}, err
	}
	return settings, nil
}
