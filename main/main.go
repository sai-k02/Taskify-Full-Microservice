package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"time"

	"github.com/go-rod/rod"
)

/*
https://go-rod.github.io/#/get-started/README?id=first-program
go run . -rod=show
*/

func main() {
	// PRINT MICROSERVICE INFORMATION
	fmt.Println("[Starting the data retrieval microservice...]")

	// SET ENVIRONMENT VARIABLES
	os.Setenv("UTD_USERNAME", "sxk180163")

	// SET ENVIRONMENT VARIABLES
	os.Setenv("UTD_PASSWORD", "E5SBSNk7ZxmabX")

	// DEFINE UTD_USERNAME
	var UTD_USERNAME string = os.Getenv("UTD_USERNAME")

	// DEFINE UTD_PASSWORD
	var UTD_PASSWORD string = os.Getenv("UTD_PASSWORD")

	// CALLING GETTING RAW TASKS
	getRawJSONTasks(UTD_USERNAME, UTD_PASSWORD, "", "")

	// OUTPUT
	fmt.Println("[Finished the data retrieval microservice...]")
}

// FUNCTION WILL TAKE IN USERNAME AND PASSWORD AND STARTDAT AND ENDDATE
func getRawJSONTasks(UTD_USERNAME string, UTD_PASSWORD string, startDate string, endDate string) {
	// CHECK TO SEE IF STARTDATE AND ENDDATE IS EMPTY
	if startDate == "" && endDate == "" {
		// DEFINE TODAY DATE
		var fromDate string = getFromDate()

		// DEFINE To DATE
		var toDate string = getToDate()
		// OUTPUT INITIAL INFORMATION
		fmt.Println("[Data Retrieval Microservice] Start and end date not given")
		fmt.Println("[Data Retrieval Microservice] Retrieving tasks for : " + UTD_USERNAME)
		fmt.Println("[Data Retrieval Microservice] From: " + fromDate)
		fmt.Println("[Data Retrieval Microservice] To: ")

		// DEFINE BROWSER
		browser := rod.New().MustConnect().NoDefaultDevice()

		// NAVIGATE TO LOGIN PAGE
		fmt.Println("[Data Retrieval Microservice] Navigating to https://elearning.utdallas.edu")

		// NAVIGATE TO PAGE
		page := browser.MustPage("https://elearning.utdallas.edu")

		// INPUT UTD_USERNAME AND UTD_PASSWORD
		page.MustWaitLoad().MustElement("#netid").MustInput(UTD_USERNAME)
		page.MustWaitLoad().MustElement("#password").MustInput(UTD_PASSWORD)

		// CLICK LOGIN BUTTON
		page.MustWaitLoad().MustElement("#submit").MustClick()

		page.MustElement("#main-heading")

		// WAIT FOR PAGE TO FULLY LOAD
		page.MustWaitLoad().MustNavigate("https://elearning.utdallas.edu/learn/api/public/v1/calendars/items?since=" + fromDate + "&until=" + toDate)

		// CREATE TEXT STRING OF DATA
		text := page.MustWaitLoad().MustElement("body > pre").MustText()

		// OUTPUT DATA
		e := outputToJSON("output.json", text)

		if e == true {
			fmt.Println("[Data Retrieval Microservice] JSON data file created")
		}
		if e == false {
			fmt.Println("[Data Retrieval Microservice] JSON data file could not be created")
		}

	}
}

func outputToJSON(outputFileName string, dataString string) bool {

	// CHECK TO SEE IF FILE EXISTS
	_, err := os.Stat(outputFileName)

	if err != nil {
		os.Remove(outputFileName)
	}

	_ = ioutil.WriteFile(outputFileName, []byte(dataString), 0644)

	return true
}

func getFromDate() string {
	// DEFINE CURRENT TIME
	currentTime := time.Now()

	// RETURN
	return currentTime.Format("2006-01-02")
}

func getToDate() string {
	// DEFINE CURRENT TIME
	fromDate := time.Now().AddDate(0, 2, 0)

	//RETURN DATE
	return fromDate.Format("2006-01-02")

}
