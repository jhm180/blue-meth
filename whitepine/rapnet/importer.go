package rapnet

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
	minFileSize  = 50000
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

func importCSV(date string) (filePath string, err error) {
	filePath = getPath("Main", date)
	if exists(filePath) {
		fmt.Printf("%s already exists!\n", filePath)
		err = nil
		return
	}
	if exists(filePath + ".gz") {
		err = nil
		filePath = filePath + ".gz"
		fmt.Printf("%s already exists!\n", filePath)
		return
	}

	var resp *http.Response = nil
	resp, err = http.PostForm("https://technet.rapaport.com/HTTP/Authenticate.aspx", url.Values{"username": {"73906"}, "password": {"Certs5355"}})
	if err != nil {
		fmt.Printf("Error: %v\n", err)
	} else {
		fmt.Printf("Authenticated...\n")
		var body []byte = nil
		body, err = ioutil.ReadAll(resp.Body)
		resp.Body.Close()
		if err != nil {
			fmt.Printf("Error: %v\n", err)
			return
		} else {
			csvUrl := "http://technet.rapaport.com/HTTP/DLS/GetFile.aspx"
			tickBytes := []byte("ticket=")
			tickBytes = append(tickBytes, body...)
			var req *http.Request = nil
			ticketStr := string(body)
			vals := url.Values{"ticket": {ticketStr}}
			req, err = http.NewRequest("POST", csvUrl, strings.NewReader(vals.Encode()))
			if err != nil {
				fmt.Printf("Error creating NewRequest: %v\n", err)
				return
			}
			req.Header.Set("Content-Type", "application/x-www-form-urlencoded")
			req.Header.Set("Accept-Encoding", "gzip, deflate")
			client := new(http.Client)
			resp, err = client.Do(req)
			if err != nil {
				fmt.Printf("Error in client.Do: %v\n", err)
				return
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
	return
}

func checkFileSize(file string) (int64, error) {
	info, err := os.Stat(file)
	if err == nil && info.Size() >= minFileSize {
		return info.Size(), nil
	}
	if info != nil {
		return info.Size(), errors.New("Bad file size")
	}
	return 0, err
}

func ImportLatest(args []string) (err error) {
	var now time.Time
	if len(args) > 0 {
		now, err = time.Parse("20060102", args[0])
		if err != nil {
			return err
		}
	} else {
		now = time.Now()
	}
	date := now.Format("20060102")
	for i := 0; i < 3; i++ {
		fmt.Printf("Attempt %d\n", i+1)
		fname, err := importCSV(date)
		if err != nil {
			return err
		}
		size, err := checkFileSize(fname)
		if err != nil {
			err = os.Remove(fname)
			if err != nil {
				break
			}
			err = errors.New(fmt.Sprintf("File %s less than min size (min = %d bytes, file = %d bytes) (error = %s)", fname, minFileSize, size, err.Error()))
		} else {
			err = nil
			fmt.Printf("Successfully fetched file %s (size = %d bytes)\n", fname, size)
			break
		}
	}
	return err
}
