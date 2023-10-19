import os
import re
import csv
import copy
import regexes

file_extensions = [".rb", ".rake", "Rakefile", ".gemspec", "Gemfile", "rails"]

# Directory path to search for .rb files
directory_path = r"/mnt/d/test/"
github_repository_dirs = [os.path.join(directory_path, d) for d in os.listdir(directory_path) if
                          os.path.isdir(os.path.join(directory_path, d))]
results = {}

# Iterate through files in the directory
for repo_dir in github_repository_dirs:
    for root, dirs, files in os.walk(repo_dir):
        temp_results = {}
        for file in files:
            for extension in file_extensions:
                if file.endswith(extension):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_contents = f.read()
                            for key, item in regexes.metrics_regexes.items():
                                if key in temp_results:
                                    temp_results[key] += len(re.findall(item, file_contents))
                                else:
                                    temp_results[key] = len(re.findall(item, file_contents))
                        break
                    except Exception as err:
                        print(err)
                        continue
        try:
            temp_results['total_number_of_logical_statements'] = sum([
                    temp_results['number_of_not_statements'],
                    temp_results['number_of_or_statements'],
                    temp_results['number_of_and_statements']
            ])
            temp_results['total_number_of_loops'] = sum([
                temp_results['number_of_for_loops'],
                temp_results['number_of_while_loops'],
                temp_results['number_of_until_loops']
            ])
        except Exception:
            continue
        results[os.path.basename(repo_dir)] = copy.deepcopy(temp_results)

csv_file = 'ruby_metrics.csv'

# Extract the unique metric keys to create the CSV header
metric_keys = set([key for key in regexes.metrics_regexes.keys()])
metric_keys.add('total_number_of_logical_statements')
metric_keys.add('total_number_of_loops')

# Write the data to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['Repository'] + list(metric_keys))
    writer.writeheader()

    for repo_name, metrics in results.items():
        row = {'Repository': repo_name}
        row.update(metrics)
        writer.writerow(row)

print(f'Data saved to {csv_file}')
