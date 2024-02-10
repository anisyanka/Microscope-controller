.PHONY: all clean upload_src submodule_update install uninstall upload_web install_converter install_web_server

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
MODBUSLIB_SUBMODULE_DIR=./libmodbus/

JSONLIB_DIR=./jsmn/
JSONLIB=-I$(JSONLIB_DIR)

CFLAGS=-I./ \
		$(MODBUSLIB) \
		$(JSONLIB) \
		-DMODBUS_CONVERTER_DEBUG=0 \
		-DMODBUS_USE_DEFAULT_CONFIG_IN_CASE_OF_JSON_ERROR=1 \
		-DMODBUS_SUPPORT_MORE_THAN_1_TCP_CONNECTION=0 \
		-DMODBUS_CONVERTER_SUPPORT_CAMERA_COMMAND=1

LDFLAGS='-Wl,-rpath=/usr/local/lib'

SOURCES_PATH=.
SOURCES_EXTENSION=c
SOURCES=$(shell find $(SOURCES_PATH) -name '*.$(SOURCES_EXTENSION)' -not -path '$(JSONLIB_DIR)*' -not -path '$(MODBUSLIB_SUBMODULE_DIR)*')

SCRIPTS_DIR=./scripts
WEB_DIR=./web_viewer

all:
	$(CC) $(SOURCES) $(CFLAGS) $(LDFLAGS) -o $(TARGET)

clean:
	rm -rf $(TARGET) *.o

upload_src:
	@./$(SCRIPTS_DIR)/upload_converter_scr_to_rpi.sh

upload_web:
	@./$(SCRIPTS_DIR)/upload_converter_web_viewer_to_rpi.sh

submodule_update:
	@git submodule update --init --recursive

install_converter:
	$(SCRIPTS_DIR)/stop_modbus_converter_service_if_running.sh $(TARGET)
	$(SCRIPTS_DIR)/rpi_stop_video_stream.sh
	mkdir -p $(TARGET_DIR)
	cp $(SCRIPTS_DIR)/rpi_launch_web_1080p_mjpg.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/rpi_launch_web_1080p_mjpg.sh
	cp $(SCRIPTS_DIR)/rpi_launch_web_4k_soft_h264.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/rpi_launch_web_4k_soft_h264.sh
	cp $(SCRIPTS_DIR)/linux_launch_web_1080p_test_stream.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/linux_launch_web_1080p_test_stream.sh
	cp $(SCRIPTS_DIR)/linux_launch_udp_1080p_test_stream.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/linux_launch_udp_1080p_test_stream.sh
	cp $(SCRIPTS_DIR)/update_host_ip_for_video_streaming.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/update_host_ip_for_video_streaming.sh
	cp $(SCRIPTS_DIR)/rpi_stop_video_stream.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/rpi_stop_video_stream.sh
	cp $(SCRIPTS_DIR)/rpi_launch_udp_4k_soft_h264.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/rpi_launch_udp_4k_soft_h264.sh
	cp $(SCRIPTS_DIR)/rpi_launch_udp_1080p_mjpg.sh $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/rpi_launch_udp_1080p_mjpg.sh
	cp modbus_converter.conf $(TARGET_DIR)
	chmod 666 $(TARGET_DIR)/modbus_converter.conf
	touch $(TARGET_DIR)/host_ip.conf
	sudo cp modbus_converter.service /etc/systemd/system/
	cp $(TARGET) $(TARGET_DIR)
	sync
	sudo systemctl daemon-reload
	sudo systemctl enable $(TARGET)
	sudo systemctl start $(TARGET)

install_web_server:
	cp -r $(WEB_DIR) $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/web_viewer/stream_scripts/camera_set_resolution_4k.sh
	chmod +x $(TARGET_DIR)/web_viewer/stream_scripts/camera_set_resolution_1920x1080.sh
	chmod +x $(TARGET_DIR)/web_viewer/stream_scripts/camera_stop_webstream_server.sh
	chmod +x $(TARGET_DIR)/web_viewer/stream_scripts/webstream

install: all install_converter install_web_server

uninstall:
	@$(SCRIPTS_DIR)/stop_modbus_converter_service_if_running.sh $(TARGET)
	rm -rf $(TARGET_DIR)
	sudo rm -rf /etc/systemd/system/modbus_converter.service
