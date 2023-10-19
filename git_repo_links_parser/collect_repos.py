import re
import csv
import json
import requests

# Set the search query and pagination parameters
# language:ruby size:>100000 stars:>=10 forks:>=10 pushed:>=10 archived:false is:public


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


def start_parsing(filter_tag):
    search_url = 'https://api.github.com/search/repositories?q=stars:%3E10+forks:%3E10+language:ruby+is:public+archived:false+size:%3E100000&per_page=100&page={}'
    temp_dict_with_reps = {}
    num_pages = 3
    for page in range(1, num_pages + 1):
        response = requests.get(search_url.format(page))
        data = bad_response(response)
        for item in data['items']:
            temp_dict_with_reps[item['html_url']] = item[filter_tag]
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
    option = 'stargazers_count'
    repos = start_parsing(option)
    safe_results(repos, option)
