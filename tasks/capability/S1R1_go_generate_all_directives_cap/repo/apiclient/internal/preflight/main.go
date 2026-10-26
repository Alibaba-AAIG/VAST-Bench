package main
import ("encoding/json"; "fmt"; "os")
func main() {
 b,e:=os.ReadFile("types.json"); if e!=nil {panic(e)}
 var s struct {Version string `json:"schema_version"`; Types []string `json:"types"`}
 if e=json.Unmarshal(b,&s);e!=nil {panic(e)}
 if s.Version=="" || len(s.Types)==0 {panic("incomplete generation configuration")}
 seen:=map[string]bool{}; for _,t:=range s.Types {if t=="" || seen[t] {panic("invalid type configuration")}; seen[t]=true}
 fmt.Printf("Schema %s: %d configured types validated\n",s.Version,len(s.Types))
}
