import re
import csv
import json
import requests

# Set the search query and pagination parameters
search_query = 'language:ruby stars:>=10 forks:>=10 pushed:>=10 archived:false is:public'
base_url = 'https://github.com'
num_pages = 11
pattern = r"(.+/.+/)star"

repository_links = []


def start_parsing():
    for page in range(1, num_pages + 1):
        search_url = f'https://github.com/search?q=language%3Aruby+stars%3A%3E%3D10+forks%3A%3E%3D10+pushed%3A%3E%3D10+archived%3Afalse+is%3Apublic&type=repositories&p={page}'

        # Send an HTTP GET request to the search URL
        response = requests.get(search_url)

        # Check if response good
        if not response.text:
            print('not JSON type')
            break

        # Parse the JSON content
        try:
            data = json.loads(response.text)
        except Exception:
            print(response.text)

        # Access the 'csrf_tokens' part of the data
        csrf_tokens = data['payload']['csrf_tokens']

        # Add the repository URLs to the list
        repo_urls = []
        for key in csrf_tokens:
            match = re.match(pattern, key)
            if match:
                repo_name = match.group(1)
                repo_urls.extend([f"{base_url}{repo_name}"])

        # Add the repository URLs to the list
        repository_links.extend(repo_urls)


def safe_results():
    # Save to a CSV file (comma-separated)
    with open('repository_links.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for link in repository_links:
            csv_writer.writerow([link])

    # Save to a TXT file
    with open('repository_links.txt', 'w') as txt_file:
        for link in repository_links:
            txt_file.write(link + '\n')


if __name__ == '__main__':
    start_parsing()
    safe_results()
