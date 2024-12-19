""" Configure build targets for an application based on its libraries. """

import json
from common import PROJECT_DATA_PATH

def app_in_project(app_name: str) -> bool:
    """ Check if the application is in the project """
    with open(PROJECT_DATA_PATH, 'r') as file:
        project = json.load(file)
        for app in project['apps']:
            if app['name'] == app_name:
                return True
        return False

def get_libs(app_name: str) -> list[str]:
    """ Get the libraries used by the application """
    with open(PROJECT_DATA_PATH, 'r') as file:
        project = json.load(file)
    for app in project['apps']:
        if app['name'] == app_name:
            return app['libs']
    return []

def set_build_config_and_packaging(app_name: str, libs: list[str]) -> None:
    """ Set the build configuration for the CMakeUserPresets.json file """
    build_presets = create_build_presets(app_name, libs)
    package_presets = create_package_presets(app_name)

    # Write the CMakeUserPresets.json file
    with open("CMakeUserPresets.json", 'r') as file:
        cmake_presets = json.load(file)
    cmake_presets["buildPresets"] = build_presets
    cmake_presets["packagePresets"] = package_presets
    with open("CMakeUserPresets.json", 'w') as file:
        json.dump(cmake_presets, file, indent=4)

    print(f"Build configuration and packaging for '{app_name}' added successfully.")

def create_build_presets(app_name: str, libs: list[str]) -> list[dict[str, any]]:
    """ Create build presets for the new application """
    return [
        {
            "name": "common-build",
            "configurePreset": "default-config",
            "jobs": 6,
            "hidden": True
        },
        {
            "name": "release-build",
            "inherits": "common-build",
            "configuration": "Release",
            "hidden": True
        },
        {
            "name": "debug-build",
            "inherits": "common-build",
            "configuration": "Debug",
            "hidden": True
        },
        {
            "name": "debinfo-build",
            "inherits": "common-build",
            "configuration": "RelWithDebInfo",
            "hidden": True
        },
        {
            "name": "docs-build",
            "configurePreset": "default-config",
            "configuration": "Release",
            "targets": [
                "docs"
            ]
        },
        {
            "name": f"{app_name}-release-build",
            "inherits": "release-build",
            "targets": [
                app_name,
                *libs,
                *[f"test_{lib}" for lib in libs]
            ]
        },
        {
            "name": f"{app_name}-debug-build",
            "inherits": "debug-build",
            "targets": [
                app_name,
                *libs,
                *[f"test_{lib}" for lib in libs]
            ]
        },
        {
            "name": f"{app_name}-debinfo-build",
            "inherits": "debinfo-build",
            "targets": [
                app_name,
                *libs,
                *[f"test_{lib}" for lib in libs]
            ]
        }
    ]

def create_package_presets(app_name: str) -> list[dict[str, any]]:
    """ Create package presets for the new application """
    return [
        {
            "name": "default-package",
            "description": "default-package",
            "displayName": "default-package",
            "configurePreset": "default-config",
            "generators": [
                "TGZ"
            ],
            "output": {
                "debug": False,
                "verbose": False
            },
            "packageDirectory": "../install/",
            "hidden": True
        },
        {
            "name": f"{app_name}-package",
            "inherits": "default-package",
            "configurations": [
                f"{app_name}-release-build"
            ]
        }
    ]

def set_launch_config(app_name: str, libs: list[str]) -> None:
    """ Set the launch configuration for the launch.vs.json file """
    data = {
        "configurations": [],
    }
    # Set the new launch configurations
    data["configurations"].append(
        {
            "name": f"Release {app_name}",
            "type": "cppvsdbg",
            "request": "launch",
            "program": f"${{workspaceFolder}}/out/build/apps/{app_name}/Release/{app_name}.exe",
            "args": [],
            "stopAtEntry": False,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "console": "internalConsole"
        }
    )
    data["configurations"].append(
        {
            "name": f"Debug {app_name}",
            "type": "cppvsdbg",
            "request": "launch",
            "program": f"${{workspaceFolder}}/out/build/apps/{app_name}/Debug/{app_name}.exe",
            "args": [],
            "stopAtEntry": False,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "console": "internalConsole"
        }
    )
    for lib in libs:
        data["configurations"].append({
            "name": f"Release {lib}",
            "type": "cppvsdbg",
            "request": "launch",
            "program": f"${{workspaceFolder}}/out/build/tests/{lib}/Release/test_{lib}.exe",
            "args": [],
            "stopAtEntry": False,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "console": "internalConsole"
        })
        data["configurations"].append({
            "name": f"Debug {lib}",
            "type": "cppvsdbg",
            "request": "launch",
            "program": f"${{workspaceFolder}}/out/build/tests/{lib}/Debug/test_{lib}.exe",
            "args": [],
            "stopAtEntry": False,
            "cwd": "${workspaceFolder}",
            "environment": [],
            "console": "internalConsole"
        })

    # Write the updated launch.json file
    with open(".vscode/launch.json", 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Launch configuration for '{app_name}' added successfully.")

if __name__ == "__main__":
    app_name = input("Enter the name of the application: ")
    if app_in_project(app_name):
        libs = get_libs(app_name)
        set_build_config_and_packaging(app_name, libs)
        set_launch_config(app_name, libs)
    else:
        print(f"Application '{app_name}' is not in the project.")
