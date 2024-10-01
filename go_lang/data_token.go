package main

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"time"
)

// Generate a random timestamp between start and end dates
func generateRandomTimestamp(start, end string) (string, error) {
	layout := "2006-01-02_1504_05"
	startTime, err := time.Parse(layout, start)
	if err != nil {
		return "", err
	}
	endTime, err := time.Parse(layout, end)
	if err != nil {
		return "", err
	}

	randomTime := startTime.Add(time.Duration(rand.Int63n(endTime.UnixNano()-startTime.UnixNano())))
	return randomTime.Format(layout), nil
}

// Convert a timestamp to Unix time
func timestampToUnix(timestamp string) (int64, error) {
	layout := "2006-01-02_1504_05"
	t, err := time.Parse(layout, timestamp)
	if err != nil {
		return 0, err
	}
	return t.Unix(), nil
}

// Convert Unix time back to a timestamp
func unixToTimestamp(unixTime int64) string {
	return time.Unix(unixTime, 0).Format("2006-01-02_1504_05")
}

// Check if the given timestamp is expired
func isExpired(timestamp string) (bool, error) {
	currentTime := time.Now()
	layout := "2006-01-02_1504_05"
	timestampTime, err := time.Parse(layout, timestamp)
	if err != nil {
		return false, err
	}
	return timestampTime.Before(currentTime), nil
}

// Create JSON with dictionary
func createJSONWithDictionary(data map[string]string) (string, error) {
	timeStart := data["time_start"]
	timeEnd := data["time_end"]

	randomTimestamp, err := generateRandomTimestamp(timeStart, timeEnd)
	if err != nil {
		return "", err
	}

	data["timestamp"] = randomTimestamp
	dataJSON, err := json.MarshalIndent(data, "", "    ")
	if err != nil {
		return "", err
	}
	return string(dataJSON), nil
}

// Check if a specific field exists in the JSON and return its value if it does
func checkFieldInJSON(filename, field string) (interface{}, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var data map[string]interface{}
	if err := json.NewDecoder(file).Decode(&data); err != nil {
		return nil, err
	}

	if value, exists := data[field]; exists {
		return value, nil
	}
	return nil, nil
}

// Store the JSON string to a file
func storeJSONAsFile(dataJSON, jsonFilename string) error {
	return os.WriteFile(jsonFilename, []byte(dataJSON), 0644)
}

// Read the JSON content from a file and return it
func readJSONFromFile(jsonFilename string) (map[string]interface{}, error) {
	file, err := os.Open(jsonFilename)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var data map[string]interface{}
	if err := json.NewDecoder(file).Decode(&data); err != nil {
		return nil, err
	}
	return data, nil
}

// Print the contents of a JSON in a pretty format
func printJSON(data map[string]interface{}) {
	prettyJSON, _ := json.MarshalIndent(data, "", "    ")
	fmt.Println(string(prettyJSON))
}

func main() {
	// Example usage
	timeStart := "2023-09-01_0000_00"
	timeEnd := "2024-09-01_0000_00"

	randomTimestamp, err := generateRandomTimestamp(timeStart, timeEnd)
	if err != nil {
		fmt.Println("Error generating random timestamp:", err)
		return
	}
	fmt.Println("Random Timestamp:", randomTimestamp)

	unixTime, err := timestampToUnix(randomTimestamp)
	if err != nil {
		fmt.Println("Error converting to Unix time:", err)
		return
	}
	fmt.Println("Unix Time:", unixTime)

	convertedTimestamp := unixToTimestamp(unixTime)
	fmt.Println("Converted Timestamp:", convertedTimestamp)

	expired, err := isExpired(randomTimestamp)
	if err != nil {
		fmt.Println("Error checking expiration:", err)
		return
	}
	fmt.Println("Is Expired:", expired)

	// JSON file operations
	jsonFilename := "data.json"

	dataDict := map[string]string{
		"event":     "example_event",
		"details":   "This is an example data dictionary.",
		"time_start": timeStart,
		"time_end":   timeEnd,
	}

	// Create JSON with dictionary
	dataJSON, err := createJSONWithDictionary(dataDict)
	if err != nil {
		fmt.Println("Error creating JSON:", err)
		return
	}
	fmt.Println("Updated JSON String:")
	fmt.Println(dataJSON)

	err = storeJSONAsFile(dataJSON, jsonFilename)
	if err != nil {
		fmt.Println("Error storing JSON to file:", err)
		return
	}
	fmt.Println("Data stored in", jsonFilename)

	jsonDataRecovered, err := readJSONFromFile(jsonFilename)
	if err != nil {
		fmt.Println("Error reading JSON from file:", err)
		return
	}

	// Check field in JSON
	fieldToLookFor := "time_start"
	fieldValue, err := checkFieldInJSON(jsonFilename, fieldToLookFor)
	if err != nil {
		fmt.Println("Error checking field in JSON:", err)
		return
	}
	if fieldValue != nil {
		fmt.Printf("Field '%s' exists in %s with value: %v\n", fieldToLookFor, jsonFilename, fieldValue)
	} else {
		fmt.Printf("Field '%s' does not exist in %s\n", fieldToLookFor, jsonFilename)
	}

	// Print JSON file
	fmt.Println("Pretty JSON Content:")
	printJSON(jsonDataRecovered)
}

/*
Random Timestamp: 2024-01-11_1633_11
Unix Time: 1704990791
Converted Timestamp: 2024-01-11_1633_11
Is Expired: true
Updated JSON String:
{
    "details": "This is an example data dictionary.",
    "event": "example_event",
    "time_end": "2024-09-01_0000_00",
    "time_start": "2023-09-01_0000_00",
    "timestamp": "2023-12-27_0513_43"
}
Data stored in data.json
Field 'time_start' exists in data.json with value: 2023-09-01_0000_00
Pretty JSON Content:
{
    "details": "This is an example data dictionary.",
    "event": "example_event",
    "time_end": "2024-09-01_0000_00",
    "time_start": "2023-09-01_0000_00",
    "timestamp": "2023-12-27_0513_43"
}
*/
