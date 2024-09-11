import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

# Convert the date to the format expected by the website (YYYY-MM-DD)
date_input = input('Enter a date in the following format MM/DD/YYYY: ')
try:
    date = datetime.strptime(date_input, '%m/%d/%Y').strftime('%Y-%m-%d')
    print(f"Converted date: {date}")  # Debugging print
except ValueError:
    print("Invalid date format. Please use MM/DD/YYYY format.")
    exit()

# Send request to the website
url = requests.get(f"https://www.yallakora.com/match-center/?date={date}")
print(f"Request status code: {url.status_code}")  # Debugging print to check if request is successful

if url.status_code != 200:
    print("Failed to retrieve data. Please check the date and try again.")
    exit()

def main(url):
    src = url.content
    soup = BeautifulSoup(src, 'lxml')
    
    # Debugging print to check if HTML is being parsed
    print(f"Page content length: {len(src)}")  

    championships = soup.find_all('div', {'class': 'matchCard'})
    print(f"Number of championships found: {len(championships)}")  # Debugging print

    if not championships:
        print("No match data found for the specified date.")
        return

    details = []

    # Function to extract match information
    def match_info(championship):
        championship_title = championship.contents[1].find('h2').text.strip()
        print(f"Championship title: {championship_title}")  # Debugging print

        matches = championship.contents[3].find_all('li')
        num_matches = len(matches)
        print(f"Number of matches: {num_matches}")  # Debugging print
        
        for match in range(num_matches):
            team_a = matches[match].find('div', {'class': 'teamA'}).text.strip()
            team_b = matches[match].find('div', {'class': 'teamB'}).text.strip()

            # Extract match result
            match_res = matches[match].find('div', {'class': 'MResult'}).find_all('span', {'class': 'score'})
            score = f"{match_res[0].text.strip()} - {match_res[1].text.strip()}"

            # Extract match time
            match_time = matches[match].find('div', {'class': 'MResult'}).find('span', {'class': 'time'}).text.strip()

            details.append({
                'championship': championship_title,
                'team A': team_a,
                'team B': team_b,
                'Score': score,
                'Match time': match_time
            })

    # Loop through each championship and extract match details
    for champ in championships:
        match_info(champ)

    # Write the data to a CSV file if there are any details
    if details:
        keys = details[0].keys()
        with open('matches.csv', 'w', newline='', encoding='utf-8') as m:
            dict_writer = csv.DictWriter(m, keys)
            dict_writer.writeheader()
            dict_writer.writerows(details)
            print('File created: matches.csv')
    else:
        print("No match details found.")

# Run the main function
main(url)
