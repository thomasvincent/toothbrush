import os
import re


def parse_requirements_file(file_path):
    """Parse a requirements file and return a list of dependencies."""
    with open(file_path) as file:
        dependencies = [line.strip() for line in file if line.strip() and not line.startswith("#")]
    return dependencies


def parse_dockerfile(file_path):
    """Parse a Dockerfile and return a list of dependencies."""
    dependencies = []
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            if line.startswith("RUN pip install"):
                match = re.search(r"pip install (.*)", line)
                if match:
                    dependencies.extend(match.group(1).split())
    return dependencies


def generate_dependency_report(file_paths):
    """Compare the dependencies in the given files and return a report."""
    reports = {}
    for file_path in file_paths:
        file_type = os.path.splitext(file_path)[1].replace(".", "")
        if file_type == "txt":
            dependencies = parse_requirements_file(file_path)
        elif file_type == "Dockerfile":
            dependencies = parse_dockerfile(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        reports[file_path] = dependencies

    report = "Dependency Report\n"
    report += "-----------------\n"
    for file_path, dependencies in reports.items():
        report += f"\n{file_path}:\n"
        for dependency in dependencies:
            report += f"  - {dependency}\n"
    return report


def main(file_paths):
    """Print the dependency report to the console."""
    try:
        report = generate_dependency_report(file_paths)
        print(report)
    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    file_paths = ["requirements.txt", "Dockerfile"]
    main(file_paths)
