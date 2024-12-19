""" Delete the directory structure for a library """

import json
import shutil
from common import PROJECT_DATA_PATH

def lib_in_project(lib_name: str) -> bool:
    """ Check if the library is in the project """
    with open(PROJECT_DATA_PATH, 'r') as file:
        project = json.load(file)
    return lib_name in project['libs']

def delete_lib_from_project(lib_name: str) -> None:
    """ Delete the directory structure for a library """
    # Define the directory structure
    dirs = [
        f"src/{lib_name}",
        f"include/{lib_name}",
        f"tests/{lib_name}"
    ]
    # Delete directories
    for dir in dirs:
        shutil.rmtree(dir)

    # Remove the library from the project
    with open(PROJECT_DATA_PATH, 'r') as file:
        project = json.load(file)
    project['lib_count'] -= 1
    project['libs'].remove(lib_name)
    with open(PROJECT_DATA_PATH, 'w') as file:
        json.dump(project, file, indent=4)

if __name__ == "__main__":
    lib_name = input("Enter the name of the library: ")
    if lib_in_project(lib_name):
        delete_lib_from_project(lib_name)
        print(f"Library structure for '{lib_name}' deleted successfully.")
    else:
        print(f"Library '{lib_name}' is not in the project.")
