""" Delete an existing application. """
import json
import shutil
from common import PROJECT_DATA_PATH

def app_in_project(app_name: str) -> bool:
    """ Check if an application is in the project """
    with open(PROJECT_DATA_PATH, 'r') as file:
        project = json.load(file)
    return any(app['name'] == app_name for app in project['apps'])

def delete_app_from_project(app_name: str) -> None:
    """ Delete the directory structure for a library """
    # Define the directory structure
    dirs = [
        f"apps/{app_name}",
    ]
    # Delete directories
    for dir in dirs:
        shutil.rmtree(dir)

    # Remove the library from the project
    with open(PROJECT_DATA_PATH, 'r') as file:
        project = json.load(file)
    project['app_count'] -= 1
    project['apps'] = [app for app in project['apps'] if app['name'] != app_name]
    with open(PROJECT_DATA_PATH, 'w') as file:
        json.dump(project, file, indent=4)

if __name__ == "__main__":
    app_name = input("Enter the name of the app: ")
    if app_in_project(app_name):
        delete_app_from_project(app_name)
        print(f"Application structure for '{app_name}' deleted successfully.")
    else:
        print(f"Application '{app_name}' is not in the project.")
