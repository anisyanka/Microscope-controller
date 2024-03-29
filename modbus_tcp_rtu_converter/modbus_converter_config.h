#ifndef __MODBUS_CONVERTER_CONFIG_H
#define __MODBUS_CONVERTER_CONFIG_H

#include <stddef.h>
#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define MODBUS_CONV_MAX_UART_DEV_NAME_LEN  (64U)
#define MODBUS_CONV_MAX_HOST_IPV4_ADDR_LEN (16U)

#define MODBUS_CONV_CONFIG_JSON_FILE_PATH "/home/pi/.microscope/modbus_converter.conf"
#define MODBUS_CONV_CONFIG_JSON_MAX_TOKEN_CNT (128U)
#define MODBUS_CONV_CONFIG_JSON_MAX_FILE_SIZE_BYTES (2048U)

#define MODBUS_CONV_UART_DEV_DEFAULT "/dev/ttyAMA5"
#define MODBUS_CONV_UART_BAUD_DEFAULT 9600
#define MODBUS_CONV_UART_PARITY_DEFAULT 'N'
#define MODBUS_CONV_UART_DATA_BIT_DEFAULT 8
#define MODBUS_CONV_UART_STOP_BIT_DEFAULT 1
#define MODBUS_CONV_PORT_DEFAULT 1502
#define MODBUS_CONV_NC_DEFAULT 1
#define MODBUS_CONV_LOSS_OF_CONNECTION_MS_DEFAULT 1000
#define MODBUS_CONV_CONNECTED_MICROCONTROLLER_SLAVE_ADDR_DEFAULT 0x01
#define MODBUS_CONV_CAMERA_SLAVE_ADDR_DEFAULT 0x02

typedef struct {
    /* Name of the serial port */
    char uart_device_name[MODBUS_CONV_MAX_UART_DEV_NAME_LEN];

    /* Baud rate of the communication, eg. 9600, 19200, 57600, 115200, etc */
    int baud;

    /* The number of bits of data, the allowed values are 5, 6, 7 and 8. */
    int data_bit;

    /* Specifies the bits of stop, the allowed values are 1 and 2 */
    int stop_bit;

    /* Argument can have one of the following values: 'N' for none, 'E' for even, 'O' for odd */
    char parity;

    /* Slave address of conneted microcontroller to UART */
    uint8_t modbus_micro_slave_addr;

    /* Slave address camera */
    uint8_t modbus_camera_slave_addr;

    /* Port where TCP socket will be opened */
    int modbus_port;

    /* How many clients connects to the tcp server */
    int modbus_number_of_tcp_connections;

    /* If serial don'r answer during this time -> loss of connection */
    int modbus_loss_connection_timeout_ms;
} modbus_converter_config_t;

modbus_converter_config_t *modbus_converter_read_config(void);
modbus_converter_config_t *modbus_converter_apply_default_configuration(void);

#ifdef __cplusplus
}
#endif

#endif /* __MODBUS_CONVERTER_CONFIG_H */
