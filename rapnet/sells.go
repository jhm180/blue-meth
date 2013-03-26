package rapnet

import (
	"database/sql"
	"github.com/coopernurse/gorp"
	"github.com/go-sql-driver/mysql"
	"os"
	"time"
)

type Sell struct {
	LotNum    int64
	Owner     string
	Shape     string
	Carat     string
	Color     string
	Clarity   string
	CutGrade  string
	Price     string
	PctRap    string
	Cert      string
	Depth     string
	Table     string
	Girdle    string
	Culet     string
	Polish    string
	Sym       string
	Fluor     string
	Meas      string
	Comment   string
	NumStones string
	CertNum   string
	StockNum  string
	Make      string
	Date      *time.Time
	City      string
	State     string
	Country   string
	Image     string
}

type SellEventCode int

const (
	Added SellEventCode = iota + 1
	Removed
	PriceChanged
	BulkLoadQuery = "
load data local infile 'LOAD DATA LOCAL INFILE Reader::sells_reader' into table {table_name}
fields terminated by ',' enclosed by '\"' escaped by '\\'
ignore 1 lines
(               LotNum,
               `Owner`,
               Shape,
               Carat,
               Color,
               Clarity,
               CutGrade,
               Price,
               PctRap,
               Cert,
               Depth,
               `Table`,
               Girdle,
               Culet,
               Polish,
               Sym,
               Fluor,
               Meas,
               `Comment`,
               NumStones,
               CertNum,
               StockNum,
               Make,
               @dateVal,
               City,
               State,
               Country,
               Image)
set Date = str_to_date(@dateVal, '%%m/%%d/%%Y %%h:%%i:%%s %%p');"
)

type SellEvent struct {
	EventId   int64
	LotNum    int64
	Price     string
	Date      *time.Time
	EventDate *time.Time
	EventCode SellEventCode
}

func readerCreator(name string) io.ReadCloser {
	return os.Open()
}

blu

func LoadCSV(csvPath string, loadDate *time.Time) {
	var conn sql.DB = nil
	defer conn.Close()


	mysql.RegisterReaderHandler("sells_loader", func () {
		return os.Open(csvPath)
		})

	conn = sql.Open('mymysql', "localhost*sells/root/3lihu_r007")

   cmd.CommandText = "select count(*) from active_sells;";
   object res = cmd.ExecuteScalar();
   bool firstLoad = (int.Parse(res.ToString())) == 0;

   string tableName = "active_sells";
   if (!firstLoad)
   {
      cmd.CommandText = "create table sells_tmp like sells;";
      cmd.ExecuteNonQuery();
      tableName = "sells_tmp";
   }
   // bulkLoader.TableName = tableName;
   // bulkLoader.FieldTerminator = ",";
   // bulkLoader.EscapeCharacter = '\\';
   // bulkLoader.FieldQuotationCharacter = '"';
   // bulkLoader.NumberOfLinesToSkip = 1;
   // bulkLoader.FileName = fileName;
   // bulkLoader.Columns.AddRange(new[] {
   //    "LotNum",
   //    "Owner",
   //    "Shape",
   //    "Carat",
   //    "Color",
   //    "Clarity",
   //    "CutGrade",
   //    "Price",
   //    "PctRap",
   //    "Cert",
   //    "Depth",
   //    "`Table`",
   //    "Girdle",
   //    "Culet",
   //    "Polish",
   //    "Sym",
   //    "Fluor",
   //    "Meas",
   //    "`Comment`",
   //    "NumStones",
   //    "CertNum",
   //    "StockNum",
   //    "Make",
   //    "@dateVal",
   //    "City",
   //    "State",
   //    "Country",
   //    "Image"
   // });
   // bulkLoader.Expressions.Add("date = str_to_date(@dateVal, '%m/%d/%Y %h:%i:%s %p')");
   // mysql.RegisterLocalFile(fileName)
   // int loaded = bulkLoader.Load();
   Log.Information("Bulk-loaded {0} rows from {1}", loaded, fileName);

   if (!firstLoad)
   {
      cmd.CommandTimeout = 60 * 30; // up to a half hour
      cmd.CommandText = "call track_changes(@loadDate);";
      cmd.Parameters.Add(new MySqlParameter("@loadDate", MySqlDbType.DateTime));
      cmd.Parameters["@loadDate"].Value = loadDate;
      cmd.ExecuteNonQuery();
   }
   else
   {
      cmd.CommandText = "insert into sells select * from active_sells;";
      cmd.ExecuteNonQuery();
   }
}
