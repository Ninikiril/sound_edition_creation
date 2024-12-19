""" Script to reset the project to its initial state """

import os
import shutil
import json

# Define paths
out_path = "out/"
folders_to_clear = ["apps/", "include/", "src/", "tests/"]
files_to_reset = {
    "CMakeUserPresets.json": {
        "version": 8,
        "configurePresets": [
            {
                "name": "default-config",
                "inherits": "conf-windows",
                "generator": "Ninja Multi-Config",
                "cacheVariables": {
                    "CMAKE_TOOLCHAIN_FILE": "$env{VCPKG_ROOT}/scripts/buildsystems/vcpkg.cmake",
                    "VCPKG_TARGET_TRIPLET": "x64-windows",
                    "CMAKE_C_COMPILER": "cl.exe",
                    "CMAKE_CXX_COMPILER": "cl.exe",
                    "CMAKE_CUDA_COMPILER": "C:/Users/Name/NVIDIA_Toolkit/CUDA/bin/nvcc.exe"
                },
                "environment": {
                    "VCPKG_ROOT": "C:/Users/Name/repositories/vcpkg"
                }
            }
        ],
        "buildPresets": [
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
            }
        ],
        "testPresets": [
            {
                "name": "common-test",
                "configurePreset": "default-config",
                "hidden": True,
                "output": {
                    "outputLogFile": "test_output.log",
                    "outputJUnitFile": "test_output.xml"
                }
            },
            {
                "name": "release-test",
                "inherits": "common-test",
                "configuration": "Release"
            },
            {
                "name": "debug-test",
                "inherits": "common-test",
                "configuration": "Debug"
            },
            {
                "name": "debinfo-test",
                "inherits": "common-test",
                "configuration": "RelWithDebInfo"
            }
        ],
        "packagePresets": [
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
            }
        ]
    },
    ".vscode/launch.json": {
        "configurations": []
    },
    "json/project_data.json": {
        "lib_count": -1,
        "libs": [],
        "app_count": -1,
        "apps": []
    }
}

# Delete out/ folder and everything inside
if os.path.exists(out_path):
    shutil.rmtree(out_path)

# Delete everything inside specified folders
for folder in folders_to_clear:
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

# Reinitialize JSON files
for filename, content in files_to_reset.items():
    file_path = filename
    with open(file_path, 'w') as json_file:
        json.dump(content, json_file, indent=4)
