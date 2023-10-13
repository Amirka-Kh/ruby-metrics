import os
import re

file_extension = ".rb"

# Directory path to search for .mrot files
directory_path = r"D:\test\Sniper-Game"

# Regular expression pattern to match 'if' statements
if_pattern = r".*\s(if|elsif|else)\s.*"
for_ternary_operator = r".*(\?\s.*\s+:\s+.*).*"

# Initialize a counter to keep track of the number of 'if' statements
if_statement_count = 0

# Iterate through files in the directory
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.endswith(file_extension):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                file_contents = f.read()
                # Use regex to find 'if' statements and count them
                if_statement_count += len(re.findall(if_pattern, file_contents))

print(f"Total 'if' statements found: {if_statement_count}")
