import csv
import os
import subprocess
import hashlib
from tqdm import tqdm
import shutil
import stat


def clone_repository(repo_url, clone_dir):
    command = f"git clone --depth=1 {repo_url} {clone_dir}"
    subprocess.run(command, shell=True, check=True)


def run_sonarqube_analysis(project_key, source_directory):
    # Mock SonarQube analysis
    print(
        f"Running SonarQube analysis for project key: {project_key} in directory {source_directory}"
    )


def remove_readonly(func, path, _):
    """Clear the readonly attribute and try the removal again."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception as e:
        print(f"Error deleting directory {path}: {str(e)}")


def delete_directory(directory):
    try:
        shutil.rmtree(directory, onerror=remove_readonly)
    except Exception as e:
        print(f"Error deleting directory {directory}: {str(e)}")


def generate_project_key(repo_url):
    return hashlib.md5(repo_url.encode()).hexdigest()


if __name__ == "__main__":
    csv_file = "repository_links_from_api.csv"
    clone_directory = "temp_clones"
    results_csv_file = "repo_analysis_results.csv"
    os.makedirs(clone_directory, exist_ok=True)
    analysis_results = []

    with open(csv_file, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in tqdm(csv_reader, desc="Processing Repositories", unit="repo"):
            if len(row) == 1:
                repo_url = row[0]
                repo_name = repo_url.split("/")[-1].split(".")[0]
                clone_dir = os.path.join(clone_directory, repo_name)
                project_key = generate_project_key(repo_url)
                clone_repository(repo_url, clone_dir)
                run_sonarqube_analysis(project_key, clone_dir)
                delete_directory(clone_dir)
                analysis_results.append(
                    {"Repository": repo_url, "ProjectKey": project_key}
                )

    with open(results_csv_file, "w", newline="") as result_file:
        fieldnames = ["Repository", "ProjectKey"]
        writer = csv.DictWriter(result_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in analysis_results:
            writer.writerow(result)

    delete_directory(clone_directory)
    print(
        "All repositories processed. Analysis results saved to repo_analysis_results.csv."
    )
