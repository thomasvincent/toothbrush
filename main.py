import os
from typing import List

class DependencyChecker:
    def __init__(self, requirements_file: str, dockerfile: str):
        self.requirements_file = requirements_file
        self.dockerfile = dockerfile

    def get_dependencies(self, file_path: str) -> List[str]:
        try:
            with open(file_path, "r") as f:
                return f.read().splitlines()
        except FileNotFoundError as e:
            print(f"Error: File not found: {e.filename}")
            exit(1)

    def check_missing_dependencies(self):
        requirements_dependencies = self.get_dependencies(self.requirements_file)
        dockerfile_dependencies = self.get_dependencies(self.dockerfile)
        missing_dependencies = [dep for dep in requirements_dependencies if dep not in dockerfile_dependencies]
        return missing_dependencies

    def print_missing_dependencies(self):
        missing_dependencies = self.check_missing_dependencies()
        if not missing_dependencies:
            print("No missing dependencies")
        else:
            print("Missing dependencies:")
            for dependency in missing_dependencies:
                print(dependency)


if __name__ == "__main__":
    checker = DependencyChecker("requirements.txt", "Dockerfile")
    checker.print_missing_dependencies()
