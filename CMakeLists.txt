cmake_minimum_required(VERSION 3.21)

project(
  cpp_project_name
  VERSION 0.4.3
  DESCRIPTION "project_description"
  LANGUAGES CUDA CXX)

# testing
include(CTest)

# for SONAR LINT
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# generating docs with doxygen
find_package(Doxygen)
if(Doxygen_FOUND)
  message(STATUS "Doxygen found, building docs")
  add_subdirectory(docs)
else()
  message(STATUS "Doxygen not found, not building docs")
endif()

# packaging
include(CPack)

function(config_libs json_file)
  file(READ ${json_file} json_content)
  string(JSON lib_count GET ${json_content} lib_count)
  if(lib_count STREQUAL "-1")
    message(WARNING "No libraries found in json file")
  else()
    foreach(lib_index RANGE ${lib_count})
      string(JSON lib_name GET ${json_content} libs ${lib_index})
      message(STATUS "Adding subdirectories for ${lib_name}")
      add_subdirectory(src/${lib_name})
      add_subdirectory(tests/${lib_name})
      cpack_add_component(${lib_name}_libs)
      cpack_add_component(${lib_name}_headers)
    endforeach()
  endif()
endfunction()

config_libs(${CMAKE_SOURCE_DIR}/json/project_data.json)

function(configs_apps json_file)
  file(READ ${json_file} json_content)
  string(JSON app_count GET ${json_content} app_count)
  if(app_count STREQUAL "-1")
    message(WARNING "No apps found in json file")
  else()
    foreach(app_index RANGE ${app_count})
      string(JSON app_name GET ${json_content} apps ${app_index} name)
      message(STATUS "Adding subdirectories for ${app_name}")
      add_subdirectory(apps/${app_name})
      cpack_add_component(${app_name}_apps)
    endforeach()
  endif()
endfunction()

configs_apps(${CMAKE_SOURCE_DIR}/json/project_data.json)
