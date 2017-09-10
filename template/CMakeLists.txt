

#####################################
# PROJECT SETTINGS
#####################################

cmake_minimum_required(VERSION 3.8)
###%PROJECT%###
SET(CMAKE_VERBOSE_MAKEFILE ON)


#####################################
# SOURCE CODE SETTINGS
#####################################

###%C_SOURCES%###

###%ASM_SOURCES%###


#####################################
# INCLUDES SETTINGS
#####################################

###%C_INCLUDES%###

###%ASM_INCLDUES%###

INCLUDE_DIRECTORIES(${AS_INCLUDES})
INCLUDE_DIRECTORIES(${C_INCLUDES})


#####################################
# DEFINITIONS
#####################################

###%DEFINITIONS%###


#####################################
# COMPILER FALGS
#####################################

###%MCU%###

###%OPT%###

###%ASM_FLAGS%###
SET(CMAKE_ASM_FLAGS ${ASFLAGS})

###%C_FLAGS%###
SET(CMAKE_C_FLAGS ${CFLAGS})

#####################################
# LINKER FALGS
#####################################

###%LDSCRIPTS%###

###%LIBS%###

###%LDFLAGS%###
SET(CMAKE_EXE_LINKER_FLAGS ${LDFLAGS})

#####################################
# CROSS COMPILER SETTINGS
#####################################

###%C_COMPILER%###

###%CXX_COMPILER%###

###%ASM_COMPILER%###

###%CP%###




#####################################
# EXECUTE
#####################################
add_executable(${PROJECT_NAME}.elf ${C_SOURCES} ${ASM_SOURCES})

set(HEX_FILE ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.hex)
set(BIN_FILE ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.bin)
add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
        COMMAND ${OBJCP} -O ihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}
        COMMAND ${OBJCP} -O binary -S $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}
        COMMENT "Building ${HEX_FILE} \nBuilding ${BIN_FILE}")



