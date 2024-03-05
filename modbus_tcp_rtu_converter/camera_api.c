#include "camera_api.h"
#include "logger.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <modbus.h>

/* Prototypes */
static int _run_script(const char *command);
static int _exec_cmd(uint16_t cmd);

void camera_api_setup_host_ip_config(const char *host_ip)
{
    int rv = 0;
    static char command[256];

    strcpy(command, CAMERA_API_SETUP_HOST_IP_SCRIPT " ");
    strcat(command, host_ip);

    logger_dbg_print("Trying to exec camera command=%s\r\n", command);

    rv = system(command);
    if (rv < 0) {
        logger_err_print("Unable to execute command <%s>. rc=%d, errno=%d --> %s\r\n", command, rv, errno, strerror(errno));
    } else {
        logger_info_print("Host ip config has been updated with ip=%s\r\n", host_ip);
    }
}

int camera_api_parse_and_execute_cmd(uint8_t *rtu_query)
{
    uint8_t fc = rtu_query[1];
    uint16_t reg = (uint16_t)(rtu_query[2]) << 8 | rtu_query[3];
    uint16_t value = (uint16_t)(rtu_query[4]) << 8 | rtu_query[5];

    if (fc != CAMERA_API_REACT_TO_FC) {
        return CAMERA_API_ERROR_ILLEGAL_FUNCTION;
    }

    switch (reg) {
    case CAMERA_API_LAUNCH_VIDEO_REG_ADDR:
        return _exec_cmd(value);

    default:
        return CAMERA_API_ERROR_ILLEGAL_DATA_ADDRESS;
    }

    return CAMERA_API_ERROR_ILLEGAL_FUNCTION;
}

static int _run_script(const char *command)
{
    int rv = 0;

    logger_dbg_print("Trying to exec camera command=%s\t\n", command);

    rv = system(command);
    if (rv < 0) {
        logger_err_print("Unable to execute command <%s>. errno=%d --> %s\r\n", command, errno, strerror(errno));
        return CAMERA_API_ERROR_INTERNAL;
    } else {
        logger_info_print("Command has been executed with code=%d\r\n", rv);
    }

    return 1;
}

static int _exec_cmd(uint16_t cmd)
{
    char command[128] = { 0 };

    switch (cmd) {
    case CAMERA_API_LAUNCH_VIDEO_4K_VALUE:
        strcpy(command, CAMERA_API_LAUNCH_4K_VIDEO_SCRIPT);
        break;
    case CAMERA_API_LAUNCH_VIDEO_1080P_VALUE:
        strcpy(command, CAMERA_API_LAUNCH_1080P_VIDEO_SCRIPT);
        break;
    case CAMERA_API_LAUNCH_VIDEO_STOP_VALUE:
        strcpy(command, CAMERA_API_LAUNCH_STOP_VIDEO_SCRIPT);
        break;
    default:
        return CAMERA_API_ERROR_ILLEGAL_DATA_VALUE;
    }

    return _run_script(command);
}
