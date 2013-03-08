package main

import (
	"fmt"
	"whitepine/rapnet"
)

func main() {
	err := sellslib.ImportLatest()
	if err != nil {
		fmt.Println(err)
	}
}
