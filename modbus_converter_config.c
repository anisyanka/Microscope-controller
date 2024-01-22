#include "modbus_converter_config.h"

#include "jsmn/jsmn.h"
#include "logger.h"

#include <errno.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static modbus_converter_config_t configuration = { 0 };

/* Prototypes */
static char *_convert_config_file_content_to_string(char *conf_file_name);
static int _jsoneq(const char *json, jsmntok_t *tok, const char *s);

modbus_converter_config_t *modbus_converter_read_config(void)
{
    int i = 0;
    int r = 0;
    const char *json_string = NULL;
    jsmn_parser p = { 0 };
    jsmntok_t tokens[MODBUS_CONV_CONFIG_JSON_MAX_TOKEN_CNT]; /* We expect no more than 128 tokens */

    json_string = _convert_config_file_content_to_string(MODBUS_CONV_CONFIG_JSON_FILE_PATH);
    if (json_string == NULL) {
        logger_err_print("[json] Failed to convert json file to string\r\n");
        return NULL;
    }

    jsmn_init(&p);
    r = jsmn_parse(&p, json_string, strlen(json_string), tokens, sizeof(tokens)/sizeof(tokens[0]));
    if (r < 0) {
        logger_err_print("[json] Failed to parse JSON: %d\r\n", r);
        free((void *)json_string);
        return NULL;
    }

    /* Assume the top-level element is an object */
    if (r < 1 || tokens[0].type != JSMN_OBJECT) {
        logger_err_print("[json] Object expected\r\n");
        free((void *)json_string);
        return NULL;
    }

    logger_dbg_print("[json] string = \"%s\"\r\n", json_string);

    /* Loop over all keys of the root object */
    for (i = 1; i < r; i++) {
        if (_jsoneq(json_string, &tokens[i], "uart_device") == 0) {
            logger_dbg_print("[json] - Uart device: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(configuration.uart_device_name,
                   json_string + tokens[i + 1].start,
                   ((tokens[i + 1].end - tokens[i + 1].start) > MODBUS_CONV_MAX_UART_DEV_NAME_LEN) ? MODBUS_CONV_MAX_UART_DEV_NAME_LEN : tokens[i + 1].end - tokens[i + 1].start);
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "uart_baud") == 0) {
            char temp[32] = { 0 };
            logger_dbg_print("[json] - Uart baud: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(temp, json_string + tokens[i + 1].start, tokens[i + 1].end - tokens[i + 1].start);
            configuration.baud = atoi((const char *)temp);
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "uart_parity") == 0) {
            logger_dbg_print("[json] - Uart parity: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            configuration.parity = (char)(*(json_string + tokens[i + 1].start));
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "uart_data_bit") == 0) {
            char temp[32] = { 0 };
            logger_dbg_print("[json] - Uart data bit: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(temp, json_string + tokens[i + 1].start, tokens[i + 1].end - tokens[i + 1].start);
            configuration.data_bit = atoi((const char *)temp);
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "uart_stop_bit") == 0) {
            char temp[32] = { 0 };
            logger_dbg_print("[json] - Uart stop bit: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(temp, json_string + tokens[i + 1].start, tokens[i + 1].end - tokens[i + 1].start);
            configuration.stop_bit = atoi((const char *)temp);
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "modbus_port") == 0) {
            char temp[32] = { 0 };
            logger_dbg_print("[json] - Port where open socket: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(temp, json_string + tokens[i + 1].start, tokens[i + 1].end - tokens[i + 1].start);
            configuration.modbus_port = atoi((const char *)temp);
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "modbus_number_of_tcp_connections") == 0) {
            char temp[32] = { 0 };
            logger_dbg_print("[json] - number of allowed connections: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(temp, json_string + tokens[i + 1].start, tokens[i + 1].end - tokens[i + 1].start);
            configuration.modbus_number_of_tcp_connections = atoi((const char *)temp);
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "modbus_connected_microcontroller_slave_addr") == 0) {
            char temp[32] = { 0 };
            logger_dbg_print("[json] - connectd mcu slave addr: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(temp, json_string + tokens[i + 1].start, tokens[i + 1].end - tokens[i + 1].start);
            configuration.modbus_micro_slave_addr = atoi((const char *)temp);
            i++;
        } else if (_jsoneq(json_string, &tokens[i], "modbus_camera_slave_addr") == 0) {
            char temp[32] = { 0 };
            logger_dbg_print("[json] - camera slave addr: %.*s\n", tokens[i + 1].end - tokens[i + 1].start, json_string + tokens[i + 1].start);
            memcpy(temp, json_string + tokens[i + 1].start, tokens[i + 1].end - tokens[i + 1].start);
            configuration.modbus_camera_slave_addr = atoi((const char *)temp);
            i++;
        } else {
            logger_dbg_print("[json] Unexpected key: %.*s\n", tokens[i].end - tokens[i].start, json_string + tokens[i].start);
        }
    }

    free((void *)json_string);
    return &configuration;
}

static char *_convert_config_file_content_to_string(char *conf_file_name)
{
    size_t cur_read_len = 0;
    long length = 0;
    char *buffer = 0;
    FILE *f = NULL;

    f = fopen(conf_file_name, "rb");
    if (f == NULL) {
        logger_err_print("[json] Failed to open file %s; errno=%d --> %s\r\n", conf_file_name, errno, strerror(errno));
        return NULL;
    }

    fseek(f, 0, SEEK_END);
    length = ftell(f);
    fseek(f, 0, SEEK_SET);

    if (length < 0) {
        logger_err_print("[json] Failed to calculate file size for %s; errno=%d --> %s\r\n", conf_file_name, errno, strerror(errno));
        fclose (f);
        return NULL;
    }

    logger_dbg_print("[json] file size is %ld bytes\r\n", length);

    if (length > MODBUS_CONV_CONFIG_JSON_MAX_FILE_SIZE_BYTES) {
        logger_err_print("[json] too big file (%ld bytes)\r\n", length);
        fclose (f);
        return NULL;
    }

    buffer = malloc(length);
    if (buffer == NULL) {
        logger_err_print("[json] can't allocate buffer (%ld bytes) for json string\r\n", length);
        fclose (f);
        return NULL;
    }

    while (cur_read_len < length) {
        cur_read_len += fread(buffer + cur_read_len, sizeof(char), length - cur_read_len, f);
    }

    fclose (f);
    return buffer;
}

static int _jsoneq(const char *json, jsmntok_t *tok, const char *s)
{
    if (tok->type == JSMN_STRING && (int)strlen(s) == tok->end - tok->start && \
        strncmp(json + tok->start, s, tok->end - tok->start) == 0) {
        return 0;
    }

    return -1;
}

modbus_converter_config_t *modbus_converter_apply_default_configuration(void)
{
    configuration.baud = MODBUS_CONV_UART_BAUD_DEFAULT;
    configuration.parity = MODBUS_CONV_UART_PARITY_DEFAULT;
    configuration.data_bit = MODBUS_CONV_UART_DATA_BIT_DEFAULT;
    configuration.stop_bit = MODBUS_CONV_UART_STOP_BIT_DEFAULT;
    configuration.modbus_micro_slave_addr = MODBUS_CONV_CONNECTED_MICROCONTROLLER_SLAVE_ADDR_DEFAULT;
    configuration.modbus_camera_slave_addr = MODBUS_CONV_CAMERA_SLAVE_ADDR_DEFAULT;
    configuration.modbus_port = MODBUS_CONV_PORT_DEFAULT;
    configuration.modbus_number_of_tcp_connections = MODBUS_CONV_NC_DEFAULT;

    size_t uart_name_size = strlen(MODBUS_CONV_UART_DEV_DEFAULT) + 1;
    memcpy(configuration.uart_device_name, MODBUS_CONV_UART_DEV_DEFAULT, (uart_name_size > sizeof(configuration.uart_device_name)) ? sizeof(configuration.uart_device_name) : uart_name_size);

    return &configuration;
}
