import re
import csv
import json
import requests

# Set the search query and pagination parameters
search_query = 'language:ruby size:>240000 stars:>=10 forks:>=10 pushed:>=10 archived:false is:public'
base_url = 'https://github.com'
num_pages = 11
pattern = r"(.+/.+/)star"


def bad_response(response):
    data = None
    # Check if response good
    if not response.text:
        print('not JSON type')

    # Parse the JSON content
    try:
        data = json.loads(response.text)
    except Exception as err:
        print(f'wrong data format (not json) {err}')

    return data


def start_parsing(option):
    search_url1 = 'https://github.com/search?q=language%3Aruby+size%3A%3E240000+stars%3A%3E%3D10+forks%3A%3E%3D10+pushed%3A%3E%3D10+archived%3Afalse+is%3Apublic&type=repositories&p={}'
    search_url2 = 'https://api.github.com/search/repositories?q=stars:%3E10+forks:%3E10+language:ruby+is:public+archived:false+size:%3E240000&per_page=100'

    search_url = search_url1 if option != 'from_api' else search_url2
    repository_links = []

    if option != 'from_api':
        for page in range(1, num_pages + 1):
            # Send an HTTP GET request to the search URL
            response = requests.get(search_url.format(page))

            data = bad_response(response)
            if not data:
                break

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
    else:
        response = requests.get(search_url)
        data = bad_response(response)
        temp_dict_with_reps = {}
        for item in data['items']:
            temp_dict_with_reps[item['html_url']] = item['size']

        sorted_dict = dict(sorted(temp_dict_with_reps.items(), key=lambda item: item[1], reverse=True))
        repository_links = list(sorted_dict.keys())
    return repository_links


def safe_results(repository_links, option):
    # Save to a CSV file (comma-separated)
    with open(f'repository_links_{option}.csv', 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for link in repository_links:
            csv_writer.writerow([link])

    # Save to a TXT file
    with open(f'repository_links_{option}.txt', 'w') as txt_file:
        for link in repository_links:
            txt_file.write(link + '\n')


if __name__ == '__main__':
    option = 'from_api' # from search box
    repos = start_parsing(option)
    safe_results(repos, option)
