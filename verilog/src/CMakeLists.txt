find_package(verilator HINTS $ENV{VERILATOR_ROOT})
if (NOT verilator_FOUND)
    message(FATAL_ERROR "Verilator not found")
endif()

function (add_module MODULE_NAME)
    add_library(${MODULE_NAME} SHARED)

    set(MODULE_VERILOG_SOURCES ${ARGN})
    verilate(${MODULE_NAME} SOURCES ${MODULE_VERILOG_SOURCES} INCLUDE_DIRS "." VERILATOR_ARGS -Wall -cc)
endfunction()

add_module(ALU alu.v)