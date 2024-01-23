#include "camera_api.h"
#include "logger.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

void camera_api_setup_host_ip_config(const char *host_ip)
{
    int rv = 0;
    char command[128];

    strcpy(command, CAMERA_API_SETUP_HOST_IP_SCRIPT " ");
    strcat(command, host_ip);

    logger_dbg_print("Trying to exec camera command=%s\t\n", command);

    rv = system(command);
    if (rv < 0) {
        logger_err_print("Unable to execute command <%s>. errno=%d --> %s\r\n", command, errno, strerror(errno));
    }

    logger_info_print("Host ip config has been updated with ip=%s\r\n", host_ip);
}
