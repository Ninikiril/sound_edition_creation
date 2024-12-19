AUX_SOURCE_DIRECTORY(. DIR_LIB_TESTS)
add_executable(test_import_export ${DIR_LIB_TESTS})

find_package(Catch2 3 REQUIRED)

target_compile_features(test_import_export PRIVATE cxx_std_17)

target_link_libraries(test_import_export PRIVATE import_export Catch2::Catch2WithMain)

add_test(NAME test_import_exporttest COMMAND test_import_export)
