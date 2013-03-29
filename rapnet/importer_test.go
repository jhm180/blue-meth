package rapnet

import (
	"database/sql"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
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

func TestMultiStatement(t *testing.T) {
	var conn *sql.DB = nil
	defer func() {
		if conn != nil {
			conn.Close()
		}
	}()
	conn, err := sql.Open("mysql", "root:3lihu_r007@tcp(localhost:3306)/rapnet_listings?timeout=30m")
	if conn == nil || err != nil {
		t.Errorf("Error opening db: %s", err.Error())
	}

	if ok, _ := runCMD(conn, "create table listings2 like listing; create table listing3 like listing;"); !ok {
		t.Errorf("Error calling track_changes: %s", err.Error())
	}

}
