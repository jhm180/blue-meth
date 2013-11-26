package main

import (
	"flag"
	"fmt"
	"io"
	"os"
	"strings"
	"text/template"
	"whitepine/rapnet"
)

// Taken from the code for the revel command, which borrows from the "go" command.
type Command struct {
	Run                    func(args []string) error
	UsageLine, Short, Long string
}

func (cmd *Command) Name() string {
	name := cmd.UsageLine
	i := strings.Index(name, " ")
	if i >= 0 {
		name = name[:i]
	}
	return name
}

var cmdImport = &Command{
	UsageLine: "import",
	Short:     "Import the latest rapnet data",
	Long: `
Connect to rapnet and download compressed CSV of the latest copy of the database, 
and load it into the whitepine db.
`,
}

var cmdDownload = &Command{
	UsageLine: "download",
	Short:     "Download the latest rapnet data file",
	Long: `
Connect to rapnet and download compressed CSV of the latest copy of the database, 
and load it into the whitepine db.
`,
}

func init() {
	cmdImport.Run = rapnet.ImportLatest
	cmdDownload.Run = rapnet.DownloadLatest
}

var commands = []*Command{
	cmdImport,
	cmdDownload,
}

func main() {
	flag.Usage = usage
	flag.Parse()
	args := flag.Args()

	if len(args) < 1 || args[0] == "help" {
		if len(args) > 1 {
			for _, cmd := range commands {
				if cmd.Name() == args[1] {
					tmpl(os.Stdout, helpTemplate, cmd)
					return
				}
			}
		}
		usage()
	}

	defer func() {
		if err := recover(); err != nil {
			if v, ok := err.(error); ok {
				fmt.Println(v.Error())
			}
			os.Exit(1)
		}
	}()

	for _, cmd := range commands {
		if cmd.Name() == args[0] {
			if err := cmd.Run(args[1:]); err != nil {
				fmt.Println(err.Error())
				os.Exit(1)
			}
			return
		}
	}

	fmt.Printf("Unknown command '%s'\nRun 'wpcmd help' for usage.\n", args[0])
}

const usageTemplate = `usage: wpcmd [arguments]

The commands are:
{{range .}}
    {{.Name | printf "%-11s"}} {{.Short}}{{end}}

Use "wpcmd help [command]" for more information.
`

var helpTemplate = `usage: wpcmd {{.UsageLine}}
{{.Long}}
`

func usage() {
	tmpl(os.Stderr, usageTemplate, commands)
	os.Exit(2)
}

func tmpl(w io.Writer, text string, data interface{}) {
	t := template.New("top")
	template.Must(t.Parse(text))
	if err := t.Execute(w, data); err != nil {
		panic(err)
	}
}
