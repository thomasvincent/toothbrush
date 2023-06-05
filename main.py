from typing import List
from pathlib import Path

class DependencyChecker:
    def __init__(self, requirements_file: str, dockerfile: str):
        self.requirements_file = Path(requirements_file)
        self.dockerfile = Path(dockerfile)

    def get_dependencies(self, file_path: Path) -> List[str]:
        if file_path.is_file():
            return file_path.read_text().splitlines()
        else:
            print(f"Error: File not found: {file_path}")
            exit(1)

    def check_missing_dependencies(self):
        requirements_dependencies = self.get_dependencies(self.requirements_file)
        dockerfile_dependencies = self.get_dependencies(self.dockerfile)
        missing_dependencies = [dep for dep in requirements_dependencies if dep not in dockerfile_dependencies]
        return missing_dependencies

    def __str__(self):
        missing_dependencies = self.check_missing_dependencies()
        if not missing_dependencies:
            return "No missing dependencies"
        else:
            return "Missing dependencies:\n" + "\n".join(missing_dependencies)


if __name__ == "__main__":
    checker = DependencyChecker("requirements.txt", "Dockerfile")
    print(checker)
