#ifndef __LOGGER_H
#define __LOGGER_H

#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

void logger_dbg_print(const char *format, ...);
void logger_info_print(const char *format, ...);
void logger_err_print(const char *format, ...);

#ifdef __cplusplus
}
#endif

#endif /* __LOGGER_H */
