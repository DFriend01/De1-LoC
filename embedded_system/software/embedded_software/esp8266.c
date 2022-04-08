/*
 * esp8266.c 
 *
 *  Created on: 2016/10/7
 *      Author: (from Terasic RFS WiFi Server demo)
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "system.h"
#include <fcntl.h>
#include <unistd.h>
#include "esp8266.h"
#include <string.h>
#include <altera_avalon_pio_regs.h>

#define esp8266_uart WIFI_UART0_NAME
#define ESP8266_DEBUG

FILE *esp8266_file;
char buffer[1024];

struct http_request {
    enum http_methods_enum {
        GET, POST, OTHER
    } http_methods;
    char *path;
    bool connected;
    int id;
};

void set_esp8266_file_blocking(bool blocking)
{
    if (blocking == false) {
        fcntl(fileno(esp8266_file), F_SETFL, O_NONBLOCK);
    } else {
        int file_fl = fcntl(fileno(esp8266_file), F_GETFL);
        file_fl = file_fl & ~O_NONBLOCK;
        fcntl(fileno(esp8266_file), F_SETFL, file_fl);
    }
}

bool esp8266_init(bool reset)
{
    bool bSuccess = true;
    esp8266_file = fopen(esp8266_uart, "rw+");
    if (esp8266_file == NULL) {
        printf("Open UART_0 failed\n");
        return false;
    }

    if (reset) {
        IOWR_ALTERA_AVALON_PIO_DATA(PIO_WIFI_RESET_BASE, 0);
        usleep(50);
        IOWR_ALTERA_AVALON_PIO_DATA(PIO_WIFI_RESET_BASE, 1);
        usleep(3 * 1000 * 1000);
        esp8266_dump_rx();
    }

    esp8266_send_command("AT+CWSAP_CUR=\"Terasic_RFS\",\"1234567890\",5,3");
    esp8266_send_command("AT+CWMODE_CUR=2");
    esp8266_send_command("AT+CWLIF");

    char cmd1[100];
    sprintf(cmd1, "AT+CIPSTART=\"TCP\",\"127.0.0.1\",5000");
    bSuccess = esp8266_send_command(cmd1);

    if (bSuccess) {
        printf("Successfully created a TCP connection to 127.0.0.1:5000.\n");
    }

    return bSuccess;
}

bool esp8266_init1(bool reset)
{
	char ssid[20]  = "";
	char passwd[20] = "";

    bool bSuccess = true;
    esp8266_file = fopen(esp8266_uart, "rw+");
    if (esp8266_file == NULL) {
        printf("Open UART_0 failed\n");
        return false;
    }

    if (reset) {
        IOWR_ALTERA_AVALON_PIO_DATA(PIO_WIFI_RESET_BASE, 0);
        usleep(50);
        IOWR_ALTERA_AVALON_PIO_DATA(PIO_WIFI_RESET_BASE, 1);
        usleep(3 * 1000 * 1000);
        esp8266_dump_rx();
    }

    esp8266_send_command("AT+CWMODE_CUR=1");

    printf("Connecting to WiFi AP (SSID: %s)\n", ssid);
    char cmd[100];
    sprintf(cmd, "AT+CWJAP=\"%s\",\"%s\"", ssid, passwd);
    bSuccess = esp8266_send_command(cmd);
    if (bSuccess) {
        printf("Connect to WiFi AP successfully\n");
    } else {
        printf("Connect to WiFi AP failed\n");
    }

    return bSuccess;
}

char *esp8266_gets(char *str, int str_size)
{
    return fgets(str, str_size, esp8266_file);
}

char *get_line_noblock()
{
    set_esp8266_file_blocking(false);
    buffer[0] = fgetc(esp8266_file);
    set_esp8266_file_blocking(true);
    if (buffer[0] != EOF) {
        if (fgets(buffer + 1, sizeof(buffer) - 1, esp8266_file) != NULL)
            return buffer;
    }
    return NULL;
}

bool esp8266_send_command(const char *cmd)
{
    fprintf(esp8266_file, "%s\r\n", cmd);
    int length = 0;
    while (1) {
        if (fgets(buffer + length, sizeof(buffer) - length,
                esp8266_file) != NULL) {
#ifdef ESP8266_DEBUG
            printf("%s", buffer + length);
#endif
            if (strstr(buffer + length, "OK") != NULL) {
#ifndef ESP8266_DEBUG
                if (strcmp("AT+CWLAP", cmd) == 0) {
                    printf("%s", buffer);
                }
#endif
                return true;
            } else if (strstr(buffer + length, "ERROR") != NULL) {
                return false;
            } else if (strstr(buffer + length, "FAIL") != NULL) {
                return false;
            }
            length += strlen(buffer + length);
        }
    }
    return false;
}

bool esp8266_send_data(const char *data, int length)
{
    write(fileno(esp8266_file), data, length);

    length = 0;
    while (1) {
        if (fgets(buffer + length, sizeof(buffer) - length,
                esp8266_file) != NULL) {
#ifdef ESP8266_DEBUG
            printf("%s", buffer + length);
#endif
            if (strstr(buffer + length, "SEND OK") != NULL) {
                return true;
            } else if (strstr(buffer + length, "SEND FAIL") != NULL) {
#ifndef ESP8266_DEBUG
                printf("%s", buffer);
#endif
                return false;
            }
            length += strlen(buffer + length);
        }
    }
    return false;
}

void esp8266_dump_rx()
{
    set_esp8266_file_blocking(false);
    while (fgets(buffer, sizeof(buffer), esp8266_file) != NULL) {
#ifdef ESP8266_DEBUG
        printf("%s", buffer);
#endif
    }
    set_esp8266_file_blocking(true);
    fflush(stdout);
}