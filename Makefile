.PHONY: all clean upload_src submodule_update install uninstall

TARGET=modbus_converter
TARGET_DIR=/home/pi/.modbus_converter

# PREFIX = arm-linux-gnueabihf-
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
		-DMODBUS_USE_DEFAULT_CONFIG_IN_CASE_OF_JSON_ERROR=1 \
		-DMODBUS_SUPPORT_MORE_THAN_1_TCP_CONNECTION=0 \
		-DMODBUS_CONVERTER_SUPPORT_CAMERA_COMMAND=1

LDFLAGS='-Wl,-rpath=/usr/local/lib'

SOURCES_PATH=.
SOURCES_EXTENSION=c
SOURCES=$(shell find $(SOURCES_PATH) -name '*.$(SOURCES_EXTENSION)' -not -path '$(JSONLIB_DIR)*')

SCRIPTS_DIR=./scripts

all:
	$(CC) $(SOURCES) $(CFLAGS) $(LDFLAGS) -o $(TARGET)

clean:
	rm -rf $(TARGET) *.o

upload_src:
	@./$(SCRIPTS_DIR)/upload_converter_scr_to_rpi.sh

submodule_update:
	@git submodule update --init --recursive

install: all
	$(SCRIPTS_DIR)/stop_modbus_converter_service_if_running.sh $(TARGET)
	mkdir -p $(TARGET_DIR)
	cp $(SCRIPTS_DIR)/update_host_ip_for_video_streaming.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/update_host_ip_for_video_streaming.sh
	cp modbus_converter.conf $(TARGET_DIR)
	chmod 666 $(TARGET_DIR)/modbus_converter.conf
	touch $(TARGET_DIR)/host_ip.conf
	sudo cp modbus_converter.service /etc/systemd/system/
	cp $(TARGET) $(TARGET_DIR)
	sync
	sudo systemctl daemon-reload
	sudo systemctl enable $(TARGET)
	sudo systemctl start modbus_converter

uninstall:
	@$(SCRIPTS_DIR)/stop_modbus_converter_service_if_running.sh $(TARGET)
	rm -rf $(TARGET_DIR)
	sudo rm -rf /etc/systemd/system/modbus_converter.service
