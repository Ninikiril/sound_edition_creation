""" Create the directory structure for a library """
import json
from common import PROJECT_DATA_PATH

def lib_in_project(lib_name: str) -> bool:
    """ Check if the library is in the project """
    with open(PROJECT_DATA_PATH, 'r') as file:
        project = json.load(file)
    return lib_name in project['libs']

def set_build_config_and_packaging(lib_name: str) -> None:
    """ set the build configuration for the CMakeUserPresets.json file """
    build_presets = create_build_presets(lib_name)
    package_presets = create_package_presets(lib_name)

    # Write the CMakeUserPresets.json file
    with open("CMakeUserPresets.json", 'r') as file:
        cmake_presets = json.load(file)
    cmake_presets["buildPresets"] = build_presets
    cmake_presets["packagePresets"] = package_presets
    with open("CMakeUserPresets.json", 'w') as file:
        json.dump(cmake_presets, file, indent=4)

    print(f"Build configuration and packaging for '{lib_name}' added successfully.")

def create_build_presets(lib_name: str) -> list[dict[str, any]]:
    """ Create build presets for the new library """
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
            "name": f"{lib_name}-release-build",
            "inherits": "release-build",
            "targets": [
                lib_name,
                f"test_{lib_name}"
            ]
        },
        {
            "name": f"{lib_name}-debug-build",
            "inherits": "debug-build",
            "targets": [
                lib_name,
                f"test_{lib_name}"
            ]
        },
        {
            "name": f"{lib_name}-debinfo-build",
            "inherits": "debinfo-build",
            "targets": [
                lib_name,
                f"test_{lib_name}"
            ]
        }
    ]

def create_package_presets(lib_name: str) -> list[dict[str, any]]:
    """ Create package presets for the new library """
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
            "name": f"{lib_name}-package",
            "inherits": "default-package",
            "configurations": [
                f"{lib_name}-release-build"
            ]
        }
    ]

def set_launch_config(lib_name: str) -> None:
    """ Set the launch configuration in the .vscode/launch.json file """
    data = {
        "configurations": [],
    }
    # Set the new launch configurations
    data["configurations"].append({
        "name": f"Release {lib_name}",
        "type": "cppvsdbg",
        "request": "launch",
        "program": f"${{workspaceFolder}}/out/build/tests/{lib_name}/Release/test_{lib_name}.exe",
        "args": [],
        "stopAtEntry": False,
        "cwd": "${workspaceFolder}",
        "environment": [],
        "console": "internalConsole"
    })
    data["configurations"].append({
        "name": f"Debug {lib_name}",
        "type": "cppvsdbg",
        "request": "launch",
        "program": f"${{workspaceFolder}}/out/build/tests/{lib_name}/Debug/test_{lib_name}.exe",
        "args": [],
        "stopAtEntry": False,
        "cwd": "${workspaceFolder}",
        "environment": [],
        "console": "internalConsole"
    })

    # Write the updated launch.json file
    with open(".vscode/launch.json", 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Launch configuration for '{lib_name}' added successfully.")

if __name__ == "__main__":
    lib_name = input("Enter the name of the library: ")
    if lib_in_project(lib_name):
        set_build_config_and_packaging(lib_name)
        set_launch_config(lib_name)
    else:
        print(f"Library '{lib_name}' is not in the project.")
