

#####################################
# PROJECT SETTINGS
#####################################

cmake_minimum_required(VERSION 3.8)
PROJECT(encoder_test C CXX ASM)
SET(CMAKE_VERBOSE_MAKEFILE ON)


#####################################
# SOURCE CODE SETTINGS
#####################################

SET(C_SOURCES ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_i2c_ex.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_flash_ex.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_uart.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_dma.c ${PROJECT_SOURCE_DIR}/Src/main.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_adc.c ${PROJECT_SOURCE_DIR}/Src/stm32l4xx_it.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_tim_ex.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_cortex.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_uart_ex.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_i2c.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_pwr.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_adc_ex.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_tim.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_flash_ramfunc.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_gpio.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_rcc.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_pwr_ex.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_rcc_ex.c ${PROJECT_SOURCE_DIR}/Src/system_stm32l4xx.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal.c ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Src/stm32l4xx_hal_flash.c ${PROJECT_SOURCE_DIR}/Src/stm32l4xx_hal_msp.c ${PROJECT_SOURCE_DIR}/Lib/test.c )

SET(ASM_SOURCES ${PROJECT_SOURCE_DIR}/startup_stm32l476xx.s )


#####################################
# INCLUDES SETTINGS
#####################################

SET(C_INCLUDES ${PROJECT_SOURCE_DIR}/Inc ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Inc ${PROJECT_SOURCE_DIR}/Drivers/STM32L4xx_HAL_Driver/Inc/Legacy ${PROJECT_SOURCE_DIR}/Drivers/CMSIS/Device/ST/STM32L4xx/Include ${PROJECT_SOURCE_DIR}/Drivers/CMSIS/Include ${PROJECT_SOURCE_DIR}/Lib )

SET(AS_INCLUDES )

INCLUDE_DIRECTORIES(${AS_INCLUDES})
INCLUDE_DIRECTORIES(${C_INCLUDES})


#####################################
# DEFINITIONS
#####################################

add_definitions(-DUSE_HAL_DRIVER)
add_definitions(-DSTM32L476xx)



#####################################
# COMPILER FALGS
#####################################

SET(MCU "-mcpu=cortex-m4 -mthumb -mfpu=fpv4-sp-d16 -mfloat-abi=hard ")

SET(OPT "-Og ")

SET(ASFLAGS "-x assembler-with-cpp ${MCU} ${OPT} -Wall -fdata-sections -ffunction-sections")
SET(CMAKE_ASM_FLAGS ${ASFLAGS})

SET(CFLAGS "${MCU} ${OPT} -Wall -fdata-sections -ffunction-sections -g -gdwarf-2")
SET(CMAKE_C_FLAGS ${CFLAGS})

#####################################
# LINKER FALGS
#####################################

SET(LDSCRIPT ${PROJECT_SOURCE_DIR}/STM32L476RGTx_FLASH.ld )

SET(LIBS "-lc -lm -lnosys ")

SET(LDFLAGS "${MCU} -specs=nano.specs -T${LDSCRIPT} ${LIBS} -Wl,-Map=${PROJECT_BINARY_DIR}/${PROJECT_NAME}.map,--cref -Wl,--gc-sections")
SET(CMAKE_EXE_LINKER_FLAGS ${LDFLAGS})

#####################################
# CROSS COMPILER SETTINGS
#####################################

SET(CMAKE_C_COMPILER /opt/env/gcc-arm-none-eabi-6-2017-q2-update/bin/arm-none-eabi-gcc)

SET(CMAKE_CXX_COMPILER /opt/env/gcc-arm-none-eabi-6-2017-q2-update/bin/arm-none-eabi-g++)

SET(CMAKE_ASM_COMPILER /opt/env/gcc-arm-none-eabi-6-2017-q2-update/bin/arm-none-eabi-gcc)

SET(OBJCP /opt/env/gcc-arm-none-eabi-6-2017-q2-update/bin/arm-none-eabi-objcopy)




#####################################
# EXECUTE
#####################################
add_executable(${PROJECT_NAME}.elf ${C_SOURCES} ${ASM_SOURCES})

set(HEX_FILE ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.hex)
set(BIN_FILE ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.bin)
add_custom_command(TARGET ${PROJECT_NAME}.elf POST_BUILD
        COMMAND ${OBJCP} -O ihex $<TARGET_FILE:${PROJECT_NAME}.elf> ${HEX_FILE}
        COMMAND ${OBJCP} -O binary -S $<TARGET_FILE:${PROJECT_NAME}.elf> ${BIN_FILE}
        COMMAND make -C ${PROJECT_SOURCE_DIR} -f ${PROJECT_SOURCE_DIR}/Makefile
        COMMENT "Building ${HEX_FILE} \nBuilding ${BIN_FILE}")



