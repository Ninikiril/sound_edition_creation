AUX_SOURCE_DIRECTORY(. DIR_LIB_SRCS)
AUX_SOURCE_DIRECTORY(${PROJECT_SOURCE_DIR}/include/import_export DIR_LIB_HEADERS)
add_library(import_export ${DIR_LIB_SRCS} ${DIR_LIB_HEADERS})
install(TARGETS import_export ARCHIVE DESTINATION lib COMPONENT import_export_libs)
install(FILES ${DIR_LIB_HEADERS} DESTINATION include COMPONENT import_export_headers)

target_include_directories(import_export PUBLIC ${PROJECT_SOURCE_DIR}/include)

target_compile_features(import_export PUBLIC cxx_std_11)

source_group(
  TREE "${PROJECT_SOURCE_DIR}/include"
  PREFIX "Header Files"
  FILES ${DIR_LIB_HEADERS})
