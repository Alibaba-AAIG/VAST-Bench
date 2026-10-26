package fetcher

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"

	getter "github.com/hashicorp/go-getter"
)

type BundleManifest struct {
	Bundle  string `json:"bundle"`
	Version string `json:"version"`
	SHA256  string `json:"sha256"`
}

type Summary struct {
	Fetched int              `json:"fetched"`
	Bundles []BundleManifest `json:"bundles"`
}

func Run(settings Settings) (Summary, error) {
	if settings.StagingDir == "" {
		return Summary{}, fmt.Errorf("staging_dir is required")
	}
	summary := Summary{Bundles: []BundleManifest{}}
	for _, source := range settings.Sources {
		if source.Name == "" || source.URL == "" {
			return Summary{}, fmt.Errorf("source name and url are required")
		}
		target := filepath.Join(settings.StagingDir, source.Name)
		if err := getter.Get(target, source.URL); err != nil {
			return Summary{}, fmt.Errorf("fetch %s: %w", source.Name, err)
		}
		manifest, err := readManifest(filepath.Join(target, "manifest.json"))
		if err != nil {
			return Summary{}, fmt.Errorf("read manifest for %s: %w", source.Name, err)
		}
		summary.Fetched++
		summary.Bundles = append(summary.Bundles, manifest)
	}
	return summary, nil
}

func readManifest(path string) (BundleManifest, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return BundleManifest{}, err
	}
	var manifest BundleManifest
	if err := json.Unmarshal(data, &manifest); err != nil {
		return BundleManifest{}, err
	}
	return manifest, nil
}
