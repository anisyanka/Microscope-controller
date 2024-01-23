#ifndef __CAMERA_API_H
#define __CAMERA_API_H

#ifdef __cplusplus
extern "C" {
#endif

#define CAMERA_API_SETUP_HOST_IP_SCRIPT "./update_host_ip_for_video_streaming.sh"

void camera_api_setup_host_ip_config(const char *host_ip);

#ifdef __cplusplus
}
#endif

#endif /* __CAMERA_API_H */
