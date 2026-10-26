package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"

	"git.meridian.internal/release/artifact-fetcher/internal/fetcher"
)

func main() {
	configPath := flag.String("config", "configs/sources.json", "source catalog path")
	flag.Parse()

	settings, err := fetcher.LoadSettings(*configPath)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	summary, err := fetcher.Run(settings)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	encoded, err := json.Marshal(summary)
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(string(encoded))
}
