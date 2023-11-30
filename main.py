import csv
import requests
import time
from bs4 import BeautifulSoup

# Define a function to get the title of a webpage.
def get_title(url):
    try:
        # Send a request to the URL.
        response = requests.get(url, timeout=10)
        # Check if the request was successful (status code 200).
        if response.status_code == 200:
            # Parse the HTML content of the page.
            soup = BeautifulSoup(response.text, 'html.parser')
            # Return the content of the title tag, stripped of leading/trailing whitespace.
            # If the title tag is missing, return 'No Title Found'.
            return soup.title.string.strip() if soup.title else 'No Title Found'
        else:
            # If the request was not successful, return the error code.
            return 'Error: ' + str(response.status_code)
    except Exception as e:
        # If an exception occurred during the request, return the error message.
        return 'Error: ' + str(e)

# Define a function to process a list of URLs from an input file and write the titles to an output file.
def process_urls(input_file, output_file):
    # Open the input file for reading and the output file for writing.
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        # Create a CSV reader to read the input file.
        csv_reader = csv.reader(infile)
        # Create a CSV writer to write to the output file.
        csv_writer = csv.writer(outfile)
        # Write a header row to the output file.
        csv_writer.writerow(['URL', 'Title'])

        # Loop through each row in the input file.
        for row in csv_reader:
            # Extract the URL from the first column.
            url = row[0]
            # Get the title of the webpage using the get_title function.
            title = get_title(url)
            # Write the URL and the title to the output file.
            csv_writer.writerow([url, title])
            # Wait for 60 seconds before processing the next URL to avoid overloading the server.
            time.sleep(60)

# Specify the paths to your input and output files here.
# Replace 'input.csv' with the path to your input file containing URLs.
# Replace 'output.csv' with the path where you want to save the output.
process_urls('input.csv', 'output.csv')
