#include <errno.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <modbus.h>
#include <time.h>

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <net/if.h>
#include <arpa/inet.h>

#include "modbus_converter_config.h"
#include "logger.h"

#include "camera_api.h"

/* Prototypes */
static void _hello_print(const char *software_name);
static void _obtain_and_copy_my_ip_to_dev_struct(void);
static void _free_all_ctx(void);
static void _free_tcp_ctx(void);
static void _free_serial_ctx(void);
static void _setup_serial_connection(void);
static void _setup_tcp_connection(void);
static void _reply_tcp_exeptions(uint8_t *q);

/* Global device struct describing all states */
typedef struct {
    modbus_converter_config_t *config;
    modbus_t *uart_ctx;
    modbus_t *tcp_ctx;
    modbus_mapping_t *mb_mapping;
    int modbus_socket;
    int listen_socket;
    char my_ip[INET_ADDRSTRLEN];
    char host_ip[INET_ADDRSTRLEN];
    int is_my_ip_obtained;
} modbus_converter_dev_t;

static modbus_converter_dev_t modbus_converter_dev = { 0 };

int main(int argc, char *argv[])
{
    int rc = 0;

    /* Log starting time */
    _hello_print(argv[0]);

    modbus_converter_dev.listen_socket = -1;
    modbus_converter_dev.modbus_socket = -1;

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

    _obtain_and_copy_my_ip_to_dev_struct();

    logger_info_print("uart device               - %s\r\n", modbus_converter_dev.config->uart_device_name);
    logger_info_print("uart baud                 - %d\r\n", modbus_converter_dev.config->baud);
    logger_info_print("uart parity               - %c\r\n", modbus_converter_dev.config->parity);
    logger_info_print("uart data bit             - %d\r\n", modbus_converter_dev.config->data_bit);
    logger_info_print("uart stop bit             - %d\r\n", modbus_converter_dev.config->stop_bit);
    logger_info_print("modbus port               - %d\r\n", modbus_converter_dev.config->modbus_port);
    logger_info_print("modbus TCP nc             - %d\r\n", modbus_converter_dev.config->modbus_number_of_tcp_connections);
    logger_info_print("modbus mcu slave addr     - %d\r\n", modbus_converter_dev.config->modbus_micro_slave_addr);
    logger_info_print("modbus camera slave addr  - %d\r\n", modbus_converter_dev.config->modbus_camera_slave_addr);
    logger_info_print("modbus loss connection ms - %d\r\n", modbus_converter_dev.config->modbus_loss_connection_timeout_ms);
    logger_info_print("RPI IPv4 addr             - %s\r\n", modbus_converter_dev.my_ip);

    #if (MODBUS_SUPPORT_MORE_THAN_1_TCP_CONNECTION == 0)
        if (modbus_converter_dev.config->modbus_number_of_tcp_connections > 1) {
            logger_info_print("For now only 1 tcp connection supported\r\n");
            modbus_converter_dev.config->modbus_number_of_tcp_connections = 1;
        }
    #endif

    _setup_serial_connection();
    _setup_tcp_connection();

#if (MODBUS_CONVERTER_DEBUG == 1)
    modbus_set_debug(modbus_converter_dev.uart_ctx, 1);
    modbus_set_debug(modbus_converter_dev.tcp_ctx, 1);
#endif

    modbus_converter_dev.mb_mapping = modbus_mapping_new(MODBUS_MAX_READ_BITS, 0, MODBUS_MAX_READ_REGISTERS, 0);
    if (modbus_converter_dev.mb_mapping == NULL) {
        logger_err_print("Failed to allocate the mapping: %s\n", modbus_strerror(errno));
        _free_serial_ctx();
        exit(EXIT_FAILURE);
    }

    /* Main loop */
    for (;;) {
        uint8_t query[MODBUS_TCP_MAX_ADU_LENGTH];
        uint8_t rsp[MODBUS_TCP_MAX_ADU_LENGTH];

        rc = modbus_receive(modbus_converter_dev.tcp_ctx, query);
        if (rc > 0) {
            logger_dbg_print("Rx addr=%d\r\n", query[0]);
            logger_dbg_print("Rx func=%d\r\n", query[1]);
            logger_dbg_print("Rx header len=%d\r\n", modbus_get_header_length(modbus_converter_dev.tcp_ctx));

            if (query[0] == modbus_converter_dev.config->modbus_camera_slave_addr) {
                /* Parse and execute camera comands */
            } else {
                /* Send data to serial device */
                //modbus_send_raw_request();
                //modbus_receive_confirmation(modbus_converter_dev.uart_ctx, rsp);

                /* Send the responce to TCP client */
                //modbus_send_raw_request();
            }

            modbus_reply(modbus_converter_dev.tcp_ctx, query, rc, modbus_converter_dev.mb_mapping);
        } else if ((rc == -1) && (errno != EMBBADCRC)) {
            logger_err_print("TCP connection closed by the client or error: %s. Try again..\r\n", modbus_strerror(errno));
            _free_tcp_ctx();
            _setup_tcp_connection();
        } else {
            /* The connection is not closed on errors which require on reply such as bad CRC in RTU. */
            _reply_tcp_exeptions(query);
        }
    }
}

static void _hello_print(const char *software_name)
{
    time_t ltime = 0;

    time(&ltime);
    logger_info_print("%s service started: %s", software_name, ctime(&ltime));
}

static void _obtain_and_copy_my_ip_to_dev_struct(void)
{
    int fd = 0;
    int ret = 0;
    struct ifreq ifr = { 0 };
    char *ip = NULL;

    memcmp(modbus_converter_dev.my_ip, "00.00.00.00", 12);
    modbus_converter_dev.is_my_ip_obtained = 0;

    fd = socket(AF_INET, SOCK_DGRAM, 0);
    if (fd < 0) {
        logger_err_print("Unable to open socket to get my IP\r\n");
        return;
    }

    ifr.ifr_addr.sa_family = AF_INET;
    (void)strncpy(ifr.ifr_name, "wlan0", IFNAMSIZ-1);
    ret = ioctl(fd, SIOCGIFADDR, &ifr);
    if (ret < 0) {
        logger_err_print("Failed to fill ifreq struct with ioctl; errno=%d --> %s\r\n", errno, strerror(errno));
        close(fd);
        return;
    }

    close(fd);

    ip = inet_ntoa(((struct sockaddr_in *)&ifr.ifr_addr)->sin_addr);
    if (ip == NULL) {
        logger_err_print("Failed to convert rpi ip to sctring\r\n");
        return;
    }

    (void)strncpy(modbus_converter_dev.my_ip, ip, sizeof(modbus_converter_dev.my_ip));
    logger_dbg_print("RPI IPv4 addr=%s\r\n", modbus_converter_dev.my_ip);
    modbus_converter_dev.is_my_ip_obtained = 1;
}

static void _free_all_ctx(void)
{
    _free_tcp_ctx();
    _free_serial_ctx();
}

static void _free_tcp_ctx(void)
{
    if (modbus_converter_dev.listen_socket != -1) {
        close(modbus_converter_dev.listen_socket);
    }

    if (modbus_converter_dev.modbus_socket != -1) {
        close(modbus_converter_dev.modbus_socket);
    }

    modbus_close(modbus_converter_dev.tcp_ctx);
    modbus_free(modbus_converter_dev.tcp_ctx);
}

static void _free_serial_ctx(void)
{
    modbus_mapping_free(modbus_converter_dev.mb_mapping);
    modbus_close(modbus_converter_dev.uart_ctx);
    modbus_free(modbus_converter_dev.uart_ctx);
}

static void _setup_serial_connection(void)
{
    int rc = 0;

    logger_dbg_print("Start setup serial connection...\r\n");

    /*
     * CREATE and SETUP context for SERIAL device.
     *
     * Slave address must be set:
     * Client is called master in Modbus terminology, the program will send requests to servers to read or write data
     * from them. Before issuing the requests, we should define the slave ID of the remote device with modbus_set_slave.
     * 
     * So the remotely connected mcu (serial microcontroller) is a server(slave). We are a client(master).
     */
    modbus_converter_dev.uart_ctx = modbus_new_rtu(modbus_converter_dev.config->uart_device_name,
                                                   modbus_converter_dev.config->baud,
                                                   modbus_converter_dev.config->parity,
                                                   modbus_converter_dev.config->data_bit,
                                                   modbus_converter_dev.config->stop_bit);
    if (modbus_converter_dev.uart_ctx == NULL) {
        logger_err_print("Unable to create the libmodbus context for uard device %d. %s\r\n", modbus_converter_dev.config->uart_device_name, modbus_strerror(errno));
        exit(EXIT_FAILURE);
    }

    uint32_t timeout_s = 0;
    uint32_t timeout_us = modbus_converter_dev.config->modbus_loss_connection_timeout_ms * 1000;
    rc = modbus_get_response_timeout(modbus_converter_dev.uart_ctx, &timeout_s, &timeout_us);
    if (rc < 0) {
        logger_err_print("Unable to setup response timeout: %s\r\n", modbus_strerror(errno));
        _free_serial_ctx();
        exit(EXIT_FAILURE);
    }

    rc = modbus_set_slave(modbus_converter_dev.uart_ctx,
                          modbus_converter_dev.config->modbus_micro_slave_addr);
    if (rc < 0) {
        logger_err_print("Invalid slave ID (%d). %s\r\n", modbus_converter_dev.config->modbus_micro_slave_addr, modbus_strerror(errno));
        _free_serial_ctx();
        exit(EXIT_FAILURE);
    }

    rc = modbus_connect(modbus_converter_dev.uart_ctx);
    if (rc < 0) {
        logger_err_print("Connection to serial device %s failed: %s\r\n", modbus_converter_dev.config->uart_device_name, modbus_strerror(errno));
        _free_serial_ctx();
        exit(EXIT_FAILURE);
    }

    logger_info_print("Serial connection has been established successfully\r\n");
}

static void _setup_tcp_connection(void)
{
    int rc = 0;
    char *ip = NULL;

    logger_dbg_print("Wait for host TCP connection request...\r\n");

    /*
     * CREATE and SETUP context for TCP server device(slave).
     * In case of TCP we are a slave device.
     * Modbus poll will connect to us and send queries.
     */
    modbus_converter_dev.tcp_ctx = modbus_new_tcp((modbus_converter_dev.is_my_ip_obtained) ? modbus_converter_dev.my_ip : NULL,
                                                  modbus_converter_dev.config->modbus_port);
    if (modbus_converter_dev.tcp_ctx == NULL) {
        logger_err_print("Unable to create the libmodbus context for TCP connection %s:%d. %s\r\n", modbus_converter_dev.my_ip, modbus_converter_dev.config->modbus_port, modbus_strerror(errno));
        _free_serial_ctx();
        exit(EXIT_FAILURE);
    }

    modbus_set_indication_timeout(modbus_converter_dev.tcp_ctx, 0, 0); /* wait for connection or indication forever */

    rc = modbus_set_slave(modbus_converter_dev.tcp_ctx, MODBUS_TCP_SLAVE);
    if (rc < 0) {
        logger_err_print("Unable to set TCP slave. %s\r\n", modbus_strerror(errno));
        _free_all_ctx();
        exit(EXIT_FAILURE);
    }

    rc = modbus_tcp_listen(modbus_converter_dev.tcp_ctx,
                           modbus_converter_dev.config->modbus_number_of_tcp_connections);
    if (rc < 0) {
        logger_err_print("Unable to create TCP socket on %s:%d. %s\r\n", modbus_converter_dev.my_ip, modbus_converter_dev.config->modbus_port, modbus_strerror(errno));
        _free_all_ctx();
        exit(EXIT_FAILURE);
    }

    modbus_converter_dev.listen_socket = rc;
    logger_dbg_print("TCP listen socket=%d\r\n", modbus_converter_dev.listen_socket);

    rc = modbus_tcp_accept(modbus_converter_dev.tcp_ctx, &modbus_converter_dev.listen_socket);
    if (rc < 0) {
        logger_err_print("Unable to accept TCP connection: %s\r\n",  modbus_strerror(errno));
        _free_all_ctx();
        exit(EXIT_FAILURE);
    }

    struct sockaddr_in addr = { 0 };
    socklen_t addr_size = sizeof(struct sockaddr_in);

    modbus_converter_dev.modbus_socket = rc;
    logger_dbg_print("TCP modbus socket=%d\r\n", modbus_converter_dev.modbus_socket);

    rc = getpeername(modbus_converter_dev.modbus_socket, (struct sockaddr *)&addr, &addr_size);
    if (rc < 0) {
        logger_err_print("Failed to get connected peer name; errno=%d --> %s\r\n", errno, strerror(errno));
    } else {
        ip = inet_ntoa(addr.sin_addr);
        if (ip == NULL) {
            logger_err_print("Failed to convert host ip to sctring\r\n");
        } else {
            (void)strncpy(modbus_converter_dev.host_ip, ip, sizeof(modbus_converter_dev.host_ip));

            #if (MODBUS_CONVERTER_SUPPORT_CAMERA_COMMAND == 1)
                camera_api_setup_host_ip_config(modbus_converter_dev.host_ip);
            #endif
        }
    }

    logger_info_print("TCP connection has been established successfully; Host IPv4 addr=%s\r\n", modbus_converter_dev.host_ip);
}

static void _reply_tcp_exeptions(uint8_t *q)
{
    int rc = 0;
    unsigned int exception_code = 0;

    if (errno == EMBXILFUN) {
        exception_code = MODBUS_EXCEPTION_ILLEGAL_FUNCTION;
    } else if (errno == EMBXILADD) {
        exception_code = MODBUS_EXCEPTION_ILLEGAL_DATA_ADDRESS;
    } else if (errno == EMBXILVAL) {
        exception_code = MODBUS_EXCEPTION_ILLEGAL_DATA_VALUE;
    } else if (errno == EMBXSFAIL) {
        exception_code = MODBUS_EXCEPTION_SLAVE_OR_SERVER_FAILURE;
    } else if (errno == EMBXACK) {
        exception_code = MODBUS_EXCEPTION_ACKNOWLEDGE;
    } else if (errno == EMBXSBUSY) {
        exception_code = MODBUS_EXCEPTION_SLAVE_OR_SERVER_BUSY;
    } else if (errno == EMBXNACK) {
        exception_code = MODBUS_EXCEPTION_NEGATIVE_ACKNOWLEDGE;
    } else if (errno == EMBXMEMPAR) {
        exception_code = MODBUS_EXCEPTION_MEMORY_PARITY;
    } else if (errno == EMBXGPATH) {
        exception_code = MODBUS_EXCEPTION_GATEWAY_PATH;
    } else if (errno == EMBXGTAR) {
        exception_code = MODBUS_EXCEPTION_GATEWAY_TARGET;
    } else {
        exception_code = MODBUS_EXCEPTION_NOT_DEFINED;
    }
    
    logger_dbg_print("Exeption #%d has been raised\r\n", exception_code);
    rc = modbus_reply_exception(modbus_converter_dev.tcp_ctx, q, exception_code);
    if (rc < 0) {
        logger_err_print("Failed to reply exeption: %s.\r\n", modbus_strerror(errno));
    }
}
