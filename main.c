#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <modbus.h>
#include <time.h>

#include "modbus_converter_config.h"
#include "logger.h"

/* Prototypes */
static void _hello_print(const char *software_name);

/* Global device struct describing all states */
typedef struct {
    modbus_converter_config_t *config;
    modbus_t *uart_ctx;
    modbus_t *tcp_ctx;
    int server_socket;
} modbus_converter_dev_t;

static modbus_converter_dev_t modbus_converter_dev = { 0 };

int main(int argc, char *argv[])
{
    int rc = 0;

    /* Log starting time */
    _hello_print(argv[0]);

    /* Obtain converter configuration */
    modbus_converter_dev.config = modbus_converter_read_config();
    if (modbus_converter_dev.config == NULL) {
        logger_err_print("Unable to read modbus converter configuration. Check existance and content of file <%s>\r\n", MODBUS_CONV_CONFIG_JSON_FILE_PATH);

        #if (MODBUS_USE_DEFAULT_CONFIG_IN_CASE_OF_JSON_ERROR == 1)
            logger_info_print("Apply default configuration\r\n");
            modbus_converter_dev.config = modbus_converter_apply_default_configuration();
        #else
            exit(EXIT_FAILURE);
        #endif
    }

    logger_info_print("uart device              - %s\r\n", modbus_converter_dev.config->uart_device_name);
    logger_info_print("uart baud                - %d\r\n", modbus_converter_dev.config->baud);
    logger_info_print("uart parity              - %c\r\n", modbus_converter_dev.config->parity);
    logger_info_print("uart data bit            - %d\r\n", modbus_converter_dev.config->data_bit);
    logger_info_print("uart stop bit            - %d\r\n", modbus_converter_dev.config->stop_bit);
    logger_info_print("modbus port              - %d\r\n", modbus_converter_dev.config->modbus_port);
    logger_info_print("modbus TCP nc            - %d\r\n", modbus_converter_dev.config->modbus_number_of_tcp_connections);
    logger_info_print("modbus mcu slave addr    - %d\r\n", modbus_converter_dev.config->modbus_micro_slave_addr);
    logger_info_print("modbus camera slave addr - %d\r\n", modbus_converter_dev.config->modbus_camera_slave_addr);

    #if (MODBUS_SUPPORT_MORE_THAN_1_TCP_CONNECTION == 0)
        if (modbus_converter_dev.config->modbus_number_of_tcp_connections > 1) {
            logger_info_print("For now only 1 tcp connection supported\r\n");
            modbus_converter_dev.config->modbus_number_of_tcp_connections = 1;
        }
    #endif

    /*
     * CREATE and SETUP context for SERIAL device.
     *
     * Slave address must be set:
     * Client is called master in Modbus terminology, the program will send requests to servers to read or write data
     * from them. Before issuing the requests, we should define the slave ID of the remote device with modbus_set_slave.
     * 
     * So the remotly connected mcu (serial microcontroller) is a server(slave). We are a client(master).
     */
    modbus_converter_dev.uart_ctx = modbus_new_rtu(modbus_converter_dev.config->uart_device_name,
                                                   modbus_converter_dev.config->baud,
                                                   modbus_converter_dev.config->parity,
                                                   modbus_converter_dev.config->data_bit,
                                                   modbus_converter_dev.config->stop_bit);
    if (modbus_converter_dev.uart_ctx == NULL) {
        logger_err_print("Unable to create the libmodbus context for uard device %d\r\n", modbus_converter_dev.config->uart_device_name);
        exit(EXIT_FAILURE);
    }
    rc = modbus_set_slave(modbus_converter_dev.uart_ctx,
                          modbus_converter_dev.config->modbus_micro_slave_addr);
    if (rc == -1) {
        logger_err_print("Invalid slave ID (%d)\r\n", modbus_converter_dev.config->modbus_micro_slave_addr);
        modbus_free(modbus_converter_dev.uart_ctx);
        exit(EXIT_FAILURE);
    }
    rc = modbus_connect(modbus_converter_dev.uart_ctx);
    if (rc == -1) {
        logger_err_print("Connection to serial device %s failed: %s\r\n", modbus_converter_dev.config->uart_device_name, modbus_strerror(errno));
        modbus_free(modbus_converter_dev.uart_ctx);
        exit(EXIT_FAILURE);
    }

    /*
     * CREATE and SETUP context for TCP server device(slave).
     * In case of TCP we are a slave device.
     * Modbus poll will connect to us and send queries.
     */
    modbus_converter_dev.tcp_ctx = modbus_new_tcp(NULL, modbus_converter_dev.config->modbus_port);
    if (modbus_converter_dev.tcp_ctx == NULL) {
        logger_err_print("Unable to create the libmodbus context for TCP connection :%d\r\n", modbus_converter_dev.config->modbus_port);
        modbus_free(modbus_converter_dev.uart_ctx);
        exit(EXIT_FAILURE);
    }
    rc = modbus_tcp_listen(modbus_converter_dev.tcp_ctx,
                           modbus_converter_dev.config->modbus_number_of_tcp_connections);
    if (rc < 0) {
        logger_err_print("Unable to create TCP socket on :%d\r\n", modbus_converter_dev.config->modbus_port);
        modbus_free(modbus_converter_dev.uart_ctx);
        modbus_free(modbus_converter_dev.tcp_ctx);
        exit(EXIT_FAILURE);
    }
    logger_dbg_print("TCP socket=%d\r\n", rc);
    modbus_converter_dev.server_socket = rc;
    rc = modbus_tcp_accept(modbus_converter_dev.tcp_ctx, &modbus_converter_dev.server_socket);
    if (rc < 0) {
        logger_err_print("Unable to accept TCP connection: %s\r\n",  modbus_strerror(errno));
        modbus_free(modbus_converter_dev.uart_ctx);
        modbus_free(modbus_converter_dev.tcp_ctx);
        close(modbus_converter_dev.server_socket);
        exit(EXIT_FAILURE);
    }

    for (;;) {
        sleep(1);
        logger_info_print("Alive\r\n");
    }
}

static void _hello_print(const char *software_name)
{
    time_t ltime = 0;

    time(&ltime);
    logger_info_print("%s service started: %s", software_name, ctime(&ltime));
}
