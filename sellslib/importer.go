package sellslib

import (
	"errors"
	"fmt"
	"io"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

const (
	minFileSize  = 5000
	pathTemplate = "/home/oliver/rapnet_data/Rapnet_%s_%s.csv"
	urlTemplate  = "https://technet.rapaport.com/HTTP/Prices/CSV2_%s.aspx"
)

func exists(path string) bool {
	_, err := os.Stat(path)
	if err == nil {
		return true
	}
	if os.IsNotExist(err) {
		return false
	}
	return false
}

func getPath(csvType, date string) (filePath string) {
	filePath = fmt.Sprintf(pathTemplate, date, csvType)
	return filePath
}

func importCSV(csvType, date string) (filePath string, err error) {
	filePath = getPath(csvType, date)
	if !exists(filePath) && !exists(filePath+".gz") {
		var resp *http.Response = nil
		if csvType != "Main" {
			resp, err = http.PostForm(fmt.Sprintf(urlTemplate, csvType), url.Values{"username": {"omellet"}, "password": {"omellet5355"}})
		} else {
			resp, err = http.PostForm("https://technet.rapaport.com/HTTP/Authenticate.aspx", url.Values{"username": {"omellet"}, "password": {"omellet5355"}})
			if err != nil {
				fmt.Printf("Error: %v\n", err)
			} else {
				var body []byte = nil
				body, err = ioutil.ReadAll(resp.Body)
				resp.Body.Close()
				if err != nil {
					fmt.Printf("Error: %v\n", err)
					return
				} else {
					csvUrl := "http://technet.rapaport.com/HTTP/RapLink/download.aspx?ShapeIDs=1&Programmatically=yes"
					tickBytes := []byte("ticket=")
					tickBytes = append(tickBytes, body...)
					var req *http.Request = nil
					ticketStr := string(body)
					fmt.Printf("Using ticket %s", ticketStr)
					vals := url.Values{"ticket": {ticketStr}}
					req, err = http.NewRequest("POST", csvUrl, strings.NewReader(vals.Encode()))
					req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
					req.Header.Set("Accept-Encoding", "gzip, deflate")
					if err != nil {
						return
					}
					client := new(http.Client)
					resp, err = client.Do(req)
					if err != nil {
						return
					}
				}
			}
		}
		if err != nil {
			fmt.Printf("Error: %v\n", err)
		} else {
			defer resp.Body.Close()
			// TODO: buffered read / write
			if resp.Header.Get("Content-Encoding") == "gzip" {
				filePath = filePath + ".gz"
			}
			var fOut *os.File = nil
			fOut, err = os.Create(filePath)
			defer fOut.Close()
			if err != nil {
				return
			}
			io.Copy(fOut, resp.Body)
		}
	} else {
		fmt.Printf("%s already exists!\n", filePath)
	}
	return
}

func checkFileSize(file string) (int64, bool) {
	info, err := os.Stat(file)
	if err == nil && info.Size() >= minFileSize {
		return info.Size(), true
	}
	if info != nil {
		return info.Size(), false
	}
	return 0, false
}

func ImportLatest() error {
	date := time.Now().Format("20060102")
	files := []string{"Main", "Round", "Pear"}
	for _, f := range files {
		fname, err := importCSV(f, date)
		if err != nil {
			return err
		}
		size, succeeded := checkFileSize(fname)
		if !succeeded {
			return errors.New(fmt.Sprintf("File %s less than min size (min = %d bytes, file = %d bytes)", fname, minFileSize, size))
		} else {
			fmt.Printf("Sucessfully fetched file %s (size = %d bytes)\n", fname, size)
		}
	}
	return nil
}

type Swearer interface {
	Fuck() string
	Shit() string
}

func runSwearer(s Swearer) {
	fmt.Println(s.Fuck())
	fmt.Println(s.Shit())
}

type SwearerImpl int

func (f SwearerImpl) Fuck() string {
	return "fuck"
}

func (f SwearerImpl) Shit() string {
	return "shit"
}

func Echo() {
	//today := time.Now()
	//fmt.Printf("%s\n", today.Format("20060102"))

	s := 1
	runSwearer(SwearerImpl(s))
}
