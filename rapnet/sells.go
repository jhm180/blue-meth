package rapnet

import (
	"database/sql"
	// "github.com/coopernurse/gorp"
	"compress/gzip"
	"fmt"
	"github.com/go-sql-driver/mysql"
	"io"
	"os"
	"path"
	"time"
)

type Sell struct {
	LotNum        int64
	Owner         string
	Shape         string
	Carat         string
	Color         string
	Clarity       string
	CutGrade      string
	Price         string
	PctRap        string
	Cert          string
	Depth         string
	TableWidth    string
	Girdle        string
	Culet         string
	Polish        string
	Sym           string
	Fluor         string
	Meas          string
	RapnetComment string
	NumStones     string
	CertNum       string
	StockNum      string
	Make          string
	Date          *time.Time
	City          string
	State         string
	Country       string
	Image         string
}

type SellEventCode int

const (
	Added SellEventCode = iota + 1
	Removed
	PriceChanged
	BulkLoadQuery = `LOAD DATA LOCAL INFILE 'Reader::listing_reader' INTO TABLE %s
fields terminated by ',' enclosed by '"' escaped by '\\'
ignore 1 lines
(              LotNum,
               Owner,
               Shape,
               Carat,
               Color,
               Clarity,
               CutGrade,
               Price,
               PctRap,
               Cert,
               Depth,
               TableWidth,
               Girdle,
               Culet,
               Polish,
               Sym,
               Fluor,
               Meas,
               RapnetComment,
               NumStones,
               CertNum,
               StockNum,
               Make,
               @dateVal,
               City,
               State,
               Country,
               Image)
set Date = str_to_date(@dateVal, '%%m/%%d/%%Y %%h:%%i:%%s %%p');`
)

type SellEvent struct {
	EventId   int64
	LotNum    int64
	Price     string
	Date      *time.Time
	EventDate *time.Time
	EventCode SellEventCode
}

func dumpTableCount(conn *sql.DB, tableName string) {
	var count sql.NullInt64
	r := conn.QueryRow(fmt.Sprintf("select count(*) from %s", tableName))
	if r != nil && r.Scan(&count) == nil {
		fmt.Printf("Table %s has %d rows\n", tableName, count.Int64)
	}
}

func runCMD(conn *sql.DB, cmdText string) (bool, error) {
	res, err := conn.Exec(cmdText)
	if err != nil {
		fmt.Printf("Error during command '%s': %s\n", cmdText, err)
		return false, err
	} else if rows, err := res.RowsAffected(); err == nil {
		fmt.Printf("%d row(s) affected\n", rows)
	} else {
		fmt.Printf("RowsAffected error for cmd '%s': %s", cmdText, err.Error())
	}
	return true, nil
}

func LoadCSV(csvPath string, loadDate *time.Time) {
	var conn *sql.DB = nil
	defer func() {
		if conn != nil {
			conn.Close()
		}
	}()

	mysql.RegisterReaderHandler("listing_reader", func() io.Reader {
		r, _ := os.Open(csvPath)
		if path.Ext(csvPath) == ".gz" {
			fmt.Printf("Opening gzip file %s\n", csvPath)
			zipr, err := gzip.NewReader(r)
			if err != nil {
				panic(err.Error())
			}
			return zipr
		}
		return r
	})
	//mysql.RegisterLocalFile(csvPath)

	conn, err := sql.Open("mysql", "root:3lihu_r007@tcp(localhost:3306)/rapnet_listings?timeout=30m")
	if conn == nil || err != nil {
		fmt.Printf("Error opening db: %s", err.Error())
	}
	r := conn.QueryRow("select count(*) from active_listing;")
	var c sql.NullInt64
	if r != nil && r.Scan(&c) == nil && c.Int64 > 0 {
		queries := []string{"drop table if exists listing_tmp;",
			"create table listing_tmp like listing;",
			fmt.Sprintf(BulkLoadQuery, "listing_tmp"),
			"start transaction;",
			fmt.Sprintf("call track_changes(date('%s'))", loadDate.Format("2006-01-02")),
			"commit;"}
		for _, q := range queries {
			if ok, _ := runCMD(conn, q); !ok {
				return
			}
		}
	} else {
		fmt.Printf("Initial load\n")
		queries := []string{"truncate table active_listing;",
			fmt.Sprintf(BulkLoadQuery, "active_listing"),
			"insert into listing select * from active_listing;"}
		for _, q := range queries {
			if ok, _ := runCMD(conn, q); !ok {
				return
			}
		}
	}
	dumpTableCount(conn, "active_listing")
	dumpTableCount(conn, "listing")
	dumpTableCount(conn, "listing_event")

}
