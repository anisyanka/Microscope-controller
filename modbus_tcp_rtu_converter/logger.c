#include "logger.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>

void logger_dbg_print(const char *format, ...)
{
#if (MODBUS_CONVERTER_DEBUG == 1)
    va_list arg;

    printf("[debug] ");

    va_start(arg, format);
    vprintf(format, arg);
    va_end(arg);

    fflush(stdout);
#endif
}

void logger_info_print(const char *format, ...)
{
    va_list arg;

    printf("[info] ");

    va_start(arg, format);
    vprintf(format, arg);
    va_end(arg);

    fflush(stdout);
}

void logger_err_print(const char *format, ...)
{
    va_list arg;

    fprintf(stderr, "[error] ");

    va_start(arg, format);
    vfprintf(stderr, format, arg);
    va_end(arg);
}
