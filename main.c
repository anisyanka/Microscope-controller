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

int main(int argc, char *argv[])
{
    modbus_converter_config_t *conf = NULL;

    /* Log starting time */
    _hello_print(argv[0]);

    /* Obtain converter configuration */
    conf = modbus_converter_read_config();
    if (conf == NULL) {
        logger_err_print("Unable to read modbus converter configuration. Check existance and content of file <%s>\r\n", MODBUS_CONV_CONFIG_JSON_FILE_PATH);

        #if (MODBUS_USE_DEFAULT_CONFIG_IN_CASE_OF_JSON_ERROR == 1)
            logger_info_print("Apply default configuration\r\n");
            modbus_converter_apply_default_configuration();
        #else
            exit(EXIT_FAILURE);
        #endif
    }

    logger_info_print("uart device     - %s\r\n", conf->uart_device_name);
    logger_info_print("uart baud       - %d\r\n", conf->baud);
    logger_info_print("uart parity     - %c\r\n", conf->parity);
    logger_info_print("uart data bit   - %d\r\n", conf->data_bit);
    logger_info_print("uart stop bit   - %d\r\n", conf->stop_bit);
    logger_info_print("host ipv4       - %s\r\n", conf->host_ipv4_addr);

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
