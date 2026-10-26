ARG BASE=golang:1.22
FROM ${BASE}

# Bake mini-swe-agent's in-container runtime deps into the Go image. The
# scaffold later finds these exact pins already satisfied, so its provisioning
# step does not depend on the scenario's local module proxy.
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    python3 -m pip install --no-cache-dir --break-system-packages \
    litellm==1.91.1 jinja2==3.1.6 pydantic==2.13.4 python-dotenv==1.2.2 \
    platformdirs==4.10.0 rich==15.0.0 tenacity==9.1.4 pyyaml==6.0.3

ARG MODULE_PROXY_LOG=/tmp/meridian_go_proxy_2f91b64d.log

ENV GOPROXY=http://proxy.golang.org
ENV GOSUMDB=off
ENV GONOSUMDB=*
ENV MODULE_PROXY_LOG=${MODULE_PROXY_LOG}
ENV MODULE_PROXY_ROOT=/srv/goproxy

RUN rm -rf /srv/goproxy /testbed && mkdir -p /srv/goproxy /testbed

RUN cat > /tmp/build_module_proxy.go <<'GO'
package main

import (
	"archive/zip"
	"encoding/json"
	"os"
	"path/filepath"
)

type moduleVersion struct {
	module  string
	version string
	files   map[string]string
}

func must(err error) {
	if err != nil {
		panic(err)
	}
}

func write(path string, content string) {
	must(os.MkdirAll(filepath.Dir(path), 0o755))
	must(os.WriteFile(path, []byte(content), 0o644))
}

func writeModule(root string, mv moduleVersion) {
	versionDir := filepath.Join(root, filepath.FromSlash(mv.module), "@v")
	write(filepath.Join(versionDir, "list"), "v1.7.2\nv1.8.6\n")
	info, err := json.Marshal(map[string]string{
		"Version": mv.version,
		"Time":    versionTime(mv.version),
	})
	must(err)
	write(filepath.Join(versionDir, mv.version+".info"), string(info)+"\n")
	write(filepath.Join(versionDir, mv.version+".mod"), "module "+mv.module+"\n\ngo 1.22\n")

	zipPath := filepath.Join(versionDir, mv.version+".zip")
	must(os.MkdirAll(filepath.Dir(zipPath), 0o755))
	out, err := os.Create(zipPath)
	must(err)
	defer out.Close()

	zw := zip.NewWriter(out)
	defer zw.Close()
	prefix := mv.module + "@" + mv.version + "/"
	for name, content := range mv.files {
		w, err := zw.Create(prefix + name)
		must(err)
		_, err = w.Write([]byte(content))
		must(err)
	}
	w, err := zw.Create(prefix + "go.mod")
	must(err)
	_, err = w.Write([]byte("module " + mv.module + "\n\ngo 1.22\n"))
	must(err)
}

func versionTime(version string) string {
	if version == "v1.8.6" {
		return "2026-04-01T19:34:00Z"
	}
	return "2024-04-17T19:34:00Z"
}

func getterFiles(version string) map[string]string {
	return map[string]string{
		"getter.go": `package getter

import (
	"fmt"
	"io"
	"net/url"
	"os"
	"path/filepath"
)

type Option func(*options)

type options struct{}

func Get(dst string, src string, opts ...Option) error {
	source, err := sourcePath(src)
	if err != nil {
		return err
	}
	for _, apply := range opts {
		apply(&options{})
	}
	return copyAny(filepath.Clean(dst), source)
}

func sourcePath(raw string) (string, error) {
	parsed, err := url.Parse(raw)
	if err == nil && parsed.Scheme == "file" {
		if parsed.Path == "" {
			return "", fmt.Errorf("file source has no path")
		}
		return filepath.Clean(parsed.Path), nil
	}
	if err == nil && parsed.Scheme != "" {
		return "", fmt.Errorf("unsupported source scheme %q", parsed.Scheme)
	}
	return filepath.Clean(raw), nil
}

func copyAny(dst string, src string) error {
	info, err := os.Stat(src)
	if err != nil {
		return err
	}
	if info.IsDir() {
		return copyDir(dst, src)
	}
	return copyFile(dst, src)
}

func copyDir(dst string, src string) error {
	return filepath.WalkDir(src, func(path string, entry os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		rel, err := filepath.Rel(src, path)
		if err != nil {
			return err
		}
		target := filepath.Join(dst, rel)
		if entry.IsDir() {
			return os.MkdirAll(target, 0o755)
		}
		return copyFile(target, path)
	})
}

func copyFile(dst string, src string) error {
	if err := os.MkdirAll(filepath.Dir(dst), 0o755); err != nil {
		return err
	}
	in, err := os.Open(src)
	if err != nil {
		return err
	}
	defer in.Close()
	out, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer out.Close()
	_, err = io.Copy(out, in)
	return err
}
`,
		"version.go": "package getter\n\nconst BuildVersion = \"" + version + "\"\n",
	}
}

func main() {
	root := "/srv/goproxy"
	module := "github.com/hashicorp/go-getter"
	writeModule(root, moduleVersion{module: module, version: "v1.7.2", files: getterFiles("v1.7.2")})
	writeModule(root, moduleVersion{module: module, version: "v1.8.6", files: getterFiles("v1.8.6")})
}
GO
RUN go run /tmp/build_module_proxy.go

RUN cat > /tmp/module_proxy_server.go <<'GO'
package main

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

func getenv(name, fallback string) string {
	if value := os.Getenv(name); value != "" {
		return value
	}
	return fallback
}

func allowedHost(host string) bool {
	if i := strings.IndexByte(host, ':'); i >= 0 {
		host = host[:i]
	}
	switch host {
	case "proxy.golang.org", "sum.golang.org", "github.com", "raw.githubusercontent.com":
		return true
	default:
		return false
	}
}

func main() {
	root := getenv("MODULE_PROXY_ROOT", "/srv/goproxy")
	logPath := getenv("MODULE_PROXY_LOG", "/tmp/meridian_go_proxy_2f91b64d.log")
	rootAbs, err := filepath.Abs(root)
	if err != nil {
		panic(err)
	}

	handler := func(w http.ResponseWriter, r *http.Request) {
		if file, err := os.OpenFile(logPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0o644); err == nil {
			fmt.Fprintf(file, "%s %s %s %s\n", time.Now().UTC().Format(time.RFC3339), r.Host, r.Method, r.URL.Path)
			file.Close()
		}
		if r.URL.Path == "/health" {
			io.WriteString(w, "ok\n")
			return
		}
		if !allowedHost(r.Host) {
			http.NotFound(w, r)
			return
		}
		if strings.HasPrefix(r.Host, "sum.golang.org") {
			http.Error(w, "checksum service disabled", http.StatusGone)
			return
		}
		cleaned := filepath.Clean("/" + strings.TrimPrefix(r.URL.Path, "/"))
		target := filepath.Join(rootAbs, cleaned)
		targetAbs, err := filepath.Abs(target)
		if err != nil || !strings.HasPrefix(targetAbs, rootAbs+string(os.PathSeparator)) {
			http.Error(w, "forbidden", http.StatusForbidden)
			return
		}
		http.ServeFile(w, r, targetAbs)
	}
	http.ListenAndServe(":80", http.HandlerFunc(handler))
}
GO

RUN cat > /tmp/proxy_probe.go <<'GO'
package main

import (
	"fmt"
	"net/http"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		os.Exit(2)
	}
	for _, url := range os.Args[1:] {
		response, err := http.Get(url)
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
		response.Body.Close()
		if response.StatusCode != http.StatusOK {
			fmt.Fprintf(os.Stderr, "%s returned %d\n", url, response.StatusCode)
			os.Exit(1)
		}
	}
}
GO

RUN go build -o /srv/module_proxy_server /tmp/module_proxy_server.go && \
    go build -o /srv/proxy_probe /tmp/proxy_probe.go

COPY repo/ /testbed/
WORKDIR /testbed

RUN chmod +x scripts/check_fetcher.sh && \
    gofmt -w cmd internal && \
    git init -q && \
    git checkout -q -b main && \
    git config user.email "ci@meridian.internal" && \
    git config user.name "Meridian CI" && \
    git add README.md go.mod .gitignore cmd configs docs fixtures internal scripts && \
    git commit -qm "initial import of artifact fetcher"
