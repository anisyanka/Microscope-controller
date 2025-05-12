.PHONY: all clean upload_src upload_scripts submodule_update install uninstall upload_web install_converter install_scripts install_web_server upload_all

TARGET=modbus_converter
WEB_SERV_TARGET=microscope_server
TARGET_DIR=/home/pi/.microscope

# PREFIX = arm-linux-gnueabihf-
# The gcc compiler bin path can be either defined in make command via GCC_PATH variable (> make GCC_PATH=xxx)
# either it can be added to the PATH environment variable.
ifdef GCC_PATH
CC = $(GCC_PATH)/$(PREFIX)gcc
else
CC = $(PREFIX)gcc
endif

MODBUS_CONVERTER_DIR=./modbus_tcp_rtu_converter
SCRIPTS_DIR=./scripts
WEB_DIR=./web_server

# Headers are in /usr/local/include/modbus
# Shared lib is in /usr/local/lib
MODBUSLIB=$(shell pkg-config --cflags --libs libmodbus)
MODBUSLIB_SUBMODULE_DIR=$(MODBUS_CONVERTER_DIR)/libmodbus/

JSONLIB_SUBMODULE_DIR=$(MODBUS_CONVERTER_DIR)/jsmn/
JSONLIB=-I$(JSONLIB_SUBMODULE_DIR)

CFLAGS=-I$(MODBUS_CONVERTER_DIR) \
		$(MODBUSLIB) \
		$(JSONLIB) \
		-DMODBUS_CONVERTER_DEBUG=0 \
		-DMODBUS_USE_DEFAULT_CONFIG_IN_CASE_OF_JSON_ERROR=1 \
		-DMODBUS_SUPPORT_MORE_THAN_1_TCP_CONNECTION=0 \
		-DMODBUS_CONVERTER_SUPPORT_CAMERA_COMMAND=1 \
		-DMODBUS_CONVERTER_UPDATE_HOST_IP_CONFIG=1

LDFLAGS='-Wl,-rpath=/usr/local/lib'

SOURCES_PATH=$(MODBUS_CONVERTER_DIR)
SOURCES_EXTENSION=c
SOURCES=$(shell find $(SOURCES_PATH) -name '*.$(SOURCES_EXTENSION)' -not -path '$(JSONLIB_SUBMODULE_DIR)*' -not -path '$(MODBUSLIB_SUBMODULE_DIR)*')

all:
	$(CC) $(SOURCES) $(CFLAGS) $(LDFLAGS) -o $(TARGET)

clean:
	rm -rf $(TARGET) *.o

upload_src:
	@./$(SCRIPTS_DIR)/upload_converter_sources_to_rpi.sh

upload_scripts:
	@./$(SCRIPTS_DIR)/upload_converter_scripts_to_rpi.sh

upload_web:
	@./$(SCRIPTS_DIR)/upload_web_server_to_rpi.sh

submodule_update:
	@git submodule update --init --recursive

install_converter:
	@echo
	@echo "---> INSTALL MODBUS TCP/RTU CONVERTER <---"
	mkdir -p $(TARGET_DIR)
	$(SCRIPTS_DIR)/stop_service_if_running.sh $(WEB_SERV_TARGET)
	$(SCRIPTS_DIR)/stop_service_if_running.sh $(TARGET)
	$(SCRIPTS_DIR)/rpi_stop_video_stream.sh
	$(SCRIPTS_DIR)/check_config_exists.sh $(TARGET_DIR)/modbus_converter.conf $(MODBUS_CONVERTER_DIR)/modbus_converter.conf $(TARGET_DIR) "MODBUS-TCP/RTU-converter"
	chmod 666 $(TARGET_DIR)/modbus_converter.conf
	touch $(TARGET_DIR)/host_ip.conf
	sudo cp $(MODBUS_CONVERTER_DIR)/modbus_converter.service /etc/systemd/system/
	cp $(TARGET) $(TARGET_DIR)
	sync
	sudo systemctl daemon-reload
	sudo systemctl enable $(TARGET)
	sudo systemctl start $(TARGET)

install_scripts:
	@echo
	@echo "---> INSTALL WEB SCRIPTS <---"
	mkdir -p $(TARGET_DIR)
	cp -r $(SCRIPTS_DIR) $(TARGET_DIR)
	chmod +x $(TARGET_DIR)/scripts/update_host_ip_for_video_streaming.sh
	chmod +x $(TARGET_DIR)/scripts/stop_service_if_running.sh
	chmod +x $(TARGET_DIR)/scripts/rpi_stop_video_stream.sh
	chmod +x $(TARGET_DIR)/scripts/rpi_launch_udp_4k_soft_h264.sh
	chmod +x $(TARGET_DIR)/scripts/rpi_launch_udp_1080p_mjpg.sh

install_web_server:
	@echo
	@echo "---> INSTALL WEB SERVER <---"
	mkdir -p $(TARGET_DIR)
	mkdir -p $(TARGET_DIR)/videos
	sudo rm -rf $(WEB_DIR)/__pycache__ 2>/dev/null
	cp -r $(WEB_DIR) $(TARGET_DIR)
	$(SCRIPTS_DIR)/check_config_exists.sh $(TARGET_DIR)/microscope_server.conf $(WEB_DIR)/microscope_server.conf $(TARGET_DIR) "MICROSCOPE"
	chmod 666 $(TARGET_DIR)/microscope_server.conf
	chmod +x $(TARGET_DIR)/web_server/stream_scripts/camera_set_resolution_4k.sh
	chmod +x $(TARGET_DIR)/web_server/stream_scripts/camera_set_resolution_1920x1080.sh
	chmod +x $(TARGET_DIR)/web_server/stream_scripts/camera_capture_one_image_frame.sh
	chmod +x $(TARGET_DIR)/web_server/stream_scripts/camera_capture_frames_continuously.sh
	chmod +x $(TARGET_DIR)/web_server/ftp_scripts/check_conn.sh
	chmod +x $(TARGET_DIR)/web_server/ftp_scripts/create_dir_on_server.sh
	chmod +x $(TARGET_DIR)/web_server/ftp_scripts/does_file_exist_on_server_in_dir.sh
	chmod +x $(TARGET_DIR)/web_server/ftp_scripts/does_file_exist_on_server.sh
	chmod +x $(TARGET_DIR)/web_server/ftp_scripts/stop_ftp_transfer.sh
	chmod +x $(TARGET_DIR)/web_server/ftp_scripts/upload_to_server.sh
	chmod +x $(TARGET_DIR)/web_server/microscope_server.py
	$(SCRIPTS_DIR)/stop_service_if_running.sh $(WEB_SERV_TARGET)
	sudo cp $(WEB_DIR)/microscope_server.service /etc/systemd/system/
	sync
	sudo systemctl daemon-reload
	sudo systemctl enable $(WEB_SERV_TARGET)
	sudo systemctl start $(WEB_SERV_TARGET)

upload_all: upload_src upload_scripts upload_web
install: install_converter install_scripts install_web_server

uninstall:
	@echo
	@echo "---> UNINSTALL ALL (remove web server, scripts and tcp/rtu converter)<---"
	$(SCRIPTS_DIR)/stop_service_if_running.sh $(TARGET)
	$(SCRIPTS_DIR)/stop_service_if_running.sh $(WEB_SERV_TARGET)
	sudo systemctl disable $(TARGET)
	sudo systemctl disable $(WEB_SERV_TARGET)
	sudo rm -rf /etc/systemd/system/modbus_converter.service
	sudo rm -rf /etc/systemd/system/microscope_server.service
	sudo rm -rf $(TARGET_DIR)
	sudo systemctl daemon-reload
