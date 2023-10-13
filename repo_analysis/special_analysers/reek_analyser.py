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


def run_reek_analysis(source_directory):
    reek_output = ""
    try:
        # Run Reek analysis and capture the output
        reek_command = "C:/Ruby31-x64/bin/reek"  # Replace with the actual path to the Reek executable
        reek_output = subprocess.check_output(
            [reek_command, source_directory], shell=True, text=True
        )

        print(reek_output)
    except subprocess.CalledProcessError as e:
        reek_output = e.output
        print(e.output)
    except FileNotFoundError:
        print("Reek command not found. Make sure it's installed and in your PATH.")
    finally:
        # Restore the original working directory
        # os.chdir(current_directory)
        pass
    # Count the number of detections for specific metrics
    # TODO: Add smells names that count each of the metrics
    metrics = {
        "Code Smell Detection": reek_output.count("<Insert smell name here>"),
        "Duplicate Code Detection": reek_output.count("DuplicateMethodCall"),
        "Method Complexity": reek_output.count("<Insert smell name here>"),
        "Method Length": reek_output.count("TooManyStatements"),
        "Class Complexity": reek_output.count("<Insert smell name here>"),
        "Control Parameter Count": reek_output.count("<Insert smell name here>"),
        "Class Count": reek_output.count("<Insert smell name here>"),
        "Constant Count": reek_output.count("<Insert smell name here>"),
        "Longest Method Length": reek_output.count("<Insert smell name here>"),
        "String Interpolation Count": reek_output.count("<Insert smell name here>"),
    }

    return metrics


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
                metrics = run_reek_analysis(clone_dir)
                if metrics is not None:
                    for metric, count in metrics.items():
                        print(f"{metric}: {count}")
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
