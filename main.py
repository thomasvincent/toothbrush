import os
import subprocess

def get_dependencies(file_path):
  with open(file_path, "r") as f:
    return f.read().splitlines()

def main():
  requirements_file_path = "requirements.txt"
  dockerfile_path = "Dockerfile"

  requirements_dependencies = []  # Assign a default empty list value
  try:
    requirements_dependencies = get_dependencies(requirements_file_path)
    dockerfile_dependencies = get_dependencies(dockerfile_path)
  except FileNotFoundError as e:
    print("Error: File not found:", e.filename)
    exit(1)

  missing_dependencies = []
  for dependency in requirements_dependencies:
    if dependency not in dockerfile_dependencies:
      missing_dependencies.append(dependency)

  if len(missing_dependencies) == 0:
    print("No missing dependencies")
  else:
    print("Missing dependencies:")
    for dependency in missing_dependencies:
      print(dependency)


if __name__ == "__main__":
  main()
