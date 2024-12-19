"""Create the structure of a new app in the project."""
import os
import json
from common import PROJECT_DATA_PATH

def lib_in_project(lib_name: str) -> bool:
    """Check if a library is in the project."""
    with open(PROJECT_DATA_PATH, 'r') as file:
        project_data = json.load(file)
    return lib_name in project_data["libs"]

def create_app_structure(app_name: str, libs: list[str]) -> None:
    """Create the structure of a new app in the project."""
    # Define the directory structure
    _dir = f"apps/{app_name}"
    os.makedirs(_dir, exist_ok=True)
    # Create base file
    base_files = f"apps/{app_name}/{app_name}.cpp"
    with open(base_files, 'w') as file:
        for lib in libs:
            file.write(f'#include "{lib}/{lib}.h"\n')
        file.write('\nint main()\n{\n')
        file.write('    // App code here\n')
        file.write('    return 0;\n')
        file.write('}\n')
    # CMakelists.txt
    with open(f"apps/{app_name}/CMakeLists.txt", 'w') as file:
        file.write('AUX_SOURCE_DIRECTORY(. DIR_LIB_SRCS)\n')
        file.write(f'add_executable({app_name} ${{DIR_LIB_SRCS}})\n')
        file.write(f'install(TARGETS {app_name} RUNTIME DESTINATION bin COMPONENT {app_name}_apps)\n\n')
        file.write(f'target_compile_features({app_name} PRIVATE cxx_std_17)\n\n')
        libs_string = ' '.join(libs)
        file.write(f'target_link_libraries({app_name} PRIVATE {libs_string})\n')
    # Add the app to json/project_data.json
    with open(PROJECT_DATA_PATH, 'r') as file:
        project_data = json.load(file)
        project_data["app_count"] += 1
        app_data = {
            "name": app_name,
            "lib_count": len(libs) - 1,
            "libs": libs
        }
        project_data["apps"].append(app_data)
    with open(PROJECT_DATA_PATH, 'w') as file:
        json.dump(project_data, file, indent=4)

if __name__ == "__main__":
    app_name = input("Enter the name of the app: ")
    number_of_libs = int(input("Enter the number of libraries to add to the app: "))
    libs = []
    for i in range(number_of_libs):
        lib_name = input(f"Enter the name of library {i+1}: ")
        libs.append(lib_name)
    for lib in libs:
        if not lib_in_project(lib):
            print(f"Library '{lib}' not found in the project. Please create the library first.")
            exit()
    create_app_structure(app_name, libs)
