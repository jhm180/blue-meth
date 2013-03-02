package sellslib

import (
	"fmt"
	"testing"
)

func TestEcho(t *testing.T) {
	Echo()
}

func TestGetPath(t *testing.T) {
	filePath := getPath("Pear", "20130225")
	fmt.Println(filePath)
	if filePath != "~/rapnet_data/Rapnet_20130225_Pear.csv" {
		t.Fail()
	}
}

func TestImportLatest(t *testing.T) {
	ImportLatest()
}
