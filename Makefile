.PHONY: all clean upload_src submodule_update

TARGET=modbus_converter

# PREFIX = arm-none-eabi-
# The gcc compiler bin path can be either defined in make command via GCC_PATH variable (> make GCC_PATH=xxx)
# either it can be added to the PATH environment variable.
ifdef GCC_PATH
CC = $(GCC_PATH)/$(PREFIX)gcc
else
CC = $(PREFIX)gcc
endif

# Headers are in /usr/local/include/modbus
# Shared lib is in /usr/local/lib
MODBUSLIB=$(shell pkg-config --cflags --libs libmodbus)

JSONLIB_DIR=./jsmn/
JSONLIB=-I$(JSONLIB_DIR)

CFLAGS=-I./ \
		$(MODBUSLIB) \
		$(JSONLIB) \
		-DMODBUS_CONVERTER_DEBUG=1 \

LDFLAGS='-Wl,-rpath=/usr/local/lib'

SOURCES_PATH=.
SOURCES_EXTENSION=c
SOURCES=$(shell find $(SOURCES_PATH) -name '*.$(SOURCES_EXTENSION)' -not -path '$(JSONLIB_DIR)*')

all:
	$(CC) $(SOURCES) $(CFLAGS) $(LDFLAGS) -o $(TARGET)

clean:
	rm -rf $(TARGET) *.o

upload_src:
	@cd ..; ./upload_converter_scr_to_rpi

submodule_update:
	@git submodule update --init --recursive
