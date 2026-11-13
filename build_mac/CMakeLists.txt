#####################################################################################################################
#
# Parent project for building the CoPylot / PySolTrace API libraries on macOS
#   solarpilot.dylib     (from SSC, solarpilot-develop branch)
#   coretrace_api.dylib  (from SolTrace)
#
# Requires SSCDIR and CORETRACEDIR environment variables. See build-mac.md.
#
#####################################################################################################################

cmake_minimum_required(VERSION 3.19)
project(copilot_api_mac)

set(BUILD_COPILOT_API ON CACHE BOOL "Build SSC solarpilot as a shared API library" FORCE)

if(NOT DEFINED ENV{SSCDIR} OR NOT DEFINED ENV{CORETRACEDIR})
	message(FATAL_ERROR "Set the SSCDIR and CORETRACEDIR environment variables before configuring.")
endif()

add_subdirectory($ENV{CORETRACEDIR} ${CMAKE_BINARY_DIR}/coretrace)
add_subdirectory($ENV{SSCDIR} ${CMAKE_BINARY_DIR}/ssc)
