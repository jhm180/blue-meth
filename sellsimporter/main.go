package main

import (
	"fmt"
	"omellet/sellslib"
)

func main() {
	err := sellslib.ImportLatest()
	if err != nil {
		fmt.Println(err)
	}
}
