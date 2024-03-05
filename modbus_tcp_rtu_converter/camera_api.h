#ifndef __CAMERA_API_H
#define __CAMERA_API_H

#include <stdint.h>
#include <modbus.h>

#ifdef __cplusplus
extern "C" {
#endif

#define CAMERA_API_SETUP_HOST_IP_SCRIPT "./scripts/update_host_ip_for_video_streaming.sh"
#define CAMERA_API_LAUNCH_4K_VIDEO_SCRIPT "./scripts/rpi_launch_udp_4k_soft_h264.sh"
#define CAMERA_API_LAUNCH_1080P_VIDEO_SCRIPT "./scripts/rpi_launch_udp_1080p_mjpg.sh"
#define CAMERA_API_LAUNCH_STOP_VIDEO_SCRIPT "./scripts/rpi_stop_video_stream.sh"

#define CAMERA_API_REACT_TO_FC (MODBUS_FC_WRITE_SINGLE_REGISTER)

typedef enum {
    CAMERA_API_ERROR_ILLEGAL_FUNCTION = -1,
    CAMERA_API_ERROR_ILLEGAL_DATA_ADDRESS = -2,
    CAMERA_API_ERROR_ILLEGAL_DATA_VALUE = -3,
    CAMERA_API_ERROR_INTERNAL = -4,
} camera_api_err_codes_t;

typedef enum {
    CAMERA_API_LAUNCH_VIDEO_REG_ADDR = 0x01, /* Modbus reg address to manipulate streaming */
} camera_api_regs_t;

typedef enum {
    CAMERA_API_LAUNCH_VIDEO_4K_VALUE = 0x00,
    CAMERA_API_LAUNCH_VIDEO_1080P_VALUE = 0x01,
    CAMERA_API_LAUNCH_VIDEO_STOP_VALUE = 0x02,
} camera_api_supported_cmd_values_t;

void camera_api_setup_host_ip_config(const char *host_ip);
int camera_api_parse_and_execute_cmd(uint8_t *rtu_query); /* ret < 0 if error occured */

#ifdef __cplusplus
}
#endif

#endif /* __CAMERA_API_H */
