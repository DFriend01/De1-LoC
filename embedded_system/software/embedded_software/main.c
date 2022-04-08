#include <stdio.h>
#include "sys/alt_stdio.h"
#include "sys/alt_irq.h"
#include "altera_avalon_pio_regs.h"
#include "alt_types.h"
#include "system.h"
#include "HAL/inc/io.h"
#include "unistd.h"
#include "esp8266.h"
#include <string.h>
#include "requests.h"

/************************************************************************
					External Sources and Documentation
-------------------------------------------------------------------------
send_http_request: 
	Terasic RFS Wifi Network Time demo
ESP8266 AT commands: 
	https://docs.espressif.com/projects/esp-at/en/latest/esp32/AT_Command_Set/TCP-IP_AT_Commands.html
ESP8266 AT command examples: 
	https://www.espressif.com/sites/default/files/documentation/4b-esp8266_at_command_examples_en.pdf
	
 ************************************************************************/


/*************************************************************************
                        Defines and Variables
 *************************************************************************/
/* pinpad constants and data structures */
#define PIN_LENGTH 4
int pincode[PIN_LENGTH];
/*
 * variables and function prototfor interrupt from get request trigger-key
 * (for unlock initiated from Andoid app)
 */
volatile int edge_capture; 		// for capturing get_req_key presses
volatile int verification_source_app;
volatile int verification_source_pinpad;

/**************************************************************************
                        Function Prototypes
 **************************************************************************/
int send_http_request(char* req);
void read_passcode(void);
int parse_http_response_status(char* http_response);
static void init_get_req_key_pio(void);
static void get_req_key_isr(void *context);


/***************************************************************************
                            Main Routine
 ***************************************************************************/
int main()
{
  	int servo_input_unlocked = 0xff000000; // careful, the last 24 bits will be chopped off by IOWR!
  	int servo_input_locked = 0x00000000;

  	int verification_result = 0;
   	char pinpad_req[300];
	char app_req[300];
   	char* app_request_result;
	char* pinpad_request_result;
   	bool success = true;

   	verification_source_app = 0;
	verification_source_pinpad = 0;
   	alt_putstr("Hello world!\n");

   	init_get_req_key_pio();

   	// initialize esp8266
   	while (esp8266_init1(true) == false) {
	   	usleep(3 * 1000 * 1000);
   	}

	while (1) {
		if (verification_source_pinpad == 1) {
			verification_source_pinpad = 0;		/* reset flag that indicates necessity to send a GET
										   	       request for unlock initiated from pinpad */
			read_passcode();
			sprintf(pinpad_req, req_pinpad_verify, host, REQ_PINPAD_VERIFY_BODY_LENGTH,
				pincode[0], pincode[1], pincode[2], pincode[3]);	
			verification_result = send_http_request(pinpad_req);
			if (verification_result == 200){
				IOWR(SERVO_COMPONENT_0_BASE, 0, servo_input_unlocked);
				usleep(3 * 1000 * 1000);
				IOWR(SERVO_COMPONENT_0_BASE, 0, servo_input_locked);
			}
		} if (verification_source_app == 1) {
			verification_source_app = 0;	/* reset flag that indicates necessity to send a GET
										   	   request for unlock initiated in Android app */
			sprintf(app_req, req_app_verify, host);
			verification_result = send_http_request(app_req);
			if (verification_result == 200){
				IOWR(SERVO_COMPONENT_0_BASE, 0, servo_input_unlocked);
				usleep(3 * 1000 * 1000);
				IOWR(SERVO_COMPONENT_0_BASE, 0, servo_input_locked);
			}
		}
	}

   return 0;
}

/********************************************************************************
                                	ISRs
 ********************************************************************************/

/**
 * @brief ISR for KEY[1] and KEY[2]. Sets verification_source_app and verification_source_pinpad;
 */
#ifdef ALT_ENHANCED_INTERRUPT_API_PRESENT
static void get_req_key_isr (void * context)
#else
static void get_req_key_isr (void * context, alt_u32 id)
#endif
{
	/* cast the context pointer to an integer pointer. */
	volatile int* edge_capture_ptr = (volatile int*) context;
	/*
	 * Read the edge capture register on the button PIO.
	 * Store value.
	 */

	*edge_capture_ptr = IORD_ALTERA_AVALON_PIO_EDGE_CAP(GET_REQ_KEYS_BASE);
	
	if (*edge_capture_ptr == 2) {
		verification_source_app = 1;
	} else if (*edge_capture_ptr == 1) {
		verification_source_pinpad = 1;
	}
	
	/* Write to the edge capture register to reset it. */
	IOWR_ALTERA_AVALON_PIO_EDGE_CAP(GET_REQ_KEYS_BASE, 0);
	/* reset interrupt capability for the Button PIO. */
	IOWR_ALTERA_AVALON_PIO_IRQ_MASK(GET_REQ_KEYS_BASE, 0xf);
 }

/*********************************************************************************
                              	Helper functions
 *********************************************************************************/

/**
 * @brief Registers the interrupts accosiated with KEY[3] and KEY[2].
 * KEY[3] marks HTTP request to be sent as GET for unlocks initiated from Android app.
 * KEY[2] marks HTTP request to be sent as POST for unlocks initiated from physical pinpad. 
 */
static void init_get_req_key_pio(void) {
	/* Recast the edge_capture pointer to match the
	   alt_irq_register() function prototype. */
	void* edge_capture_ptr = (void*) &edge_capture;
	/* Enable all 4 button interrupts. */
	IOWR_ALTERA_AVALON_PIO_IRQ_MASK(GET_REQ_KEYS_BASE, 0xf);
	/* Reset the edge capture register. */
	IOWR_ALTERA_AVALON_PIO_EDGE_CAP(GET_REQ_KEYS_BASE, 0);
	/* Register the ISR. */
#ifdef ALT_ENHANCED_INTERRUPT_API_PRESENT
	alt_ic_isr_register(
			GET_REQ_KEYS_IRQ_INTERRUPT_CONTROLLER_ID,
			GET_REQ_KEYS_IRQ,
			get_req_key_isr,
			edge_capture_ptr,
			0x0);
#else
	alt_irq_register(GET_REQ_KEYS_IRQ, edge_capture_ptr, get_req_key_isr);
#endif
}

 /**
  * @brief Polls at PINPAD_READER_COMPONENT_0_BASE to read four pressed digits of
  * the pinpad, and stores the digits pressed in pincode[PIN_LENGTH]. 
  */
void read_passcode(void){
	unsigned int pinpad_input, pinpad_input_prev;
	int i;
	// initialize pincode
  	for (i = 0; i < PIN_LENGTH; i++) {
		pincode[i] = 15;
  	}
  	pinpad_input_prev = 15;
  	pinpad_input = 15;

 	// read pincode
	printf("Enter passcode\n");
  	i = 0;
  	while (i < PIN_LENGTH) {
		pinpad_input = IORD(PINPAD_READER_COMPONENT_0_BASE, 0);
		if (pinpad_input_prev == 15) {
			if (pinpad_input != 15) {
			   	pincode[i] = pinpad_input;
			   	printf("pinpad[%d]: %d\n", i, pincode[i]);
			   	i++;
		   	}
	   	}
	   	pinpad_input_prev = pinpad_input;
	   	usleep(250000);
  	}
	printf("Passcode registered\n");
}

/**
 * @brief Send an HTTP GET/POST request to the backend. Adapted from Terasic RFS Wifi Network Time demo.
 * 
 * @param req - the type of HTTP method
 * @return int - parsed response status code
 */
int send_http_request(char* req){
	char cmd_buffer[100];
	char buffer[1000] = {0};
	bool success = true;

	sprintf(cmd_buffer, "AT+CIPSTART=\"TCP\",\"%s\",80", host);
   	success = esp8266_send_command(cmd_buffer);

	int length = 0;

	if (success){
		// modify the success message below with correct url each time you expose the backend
		sprintf(cmd_buffer, "AT+CIPSEND=%d", strlen(req));
		success = esp8266_send_command(cmd_buffer);
	}
	if (success) {
		// printf("Before sending HTTP request...\n");
		success = esp8266_send_data(req, strlen(req));
		printf("After sending HTTP request...\n");
	}
	if (success) {
		while (1) {	
			esp8266_gets(buffer, sizeof(buffer));
			if (strstr(buffer, "+IPD") != NULL) {
				length = strlen(buffer);
				while (1) {
					esp8266_gets(buffer + length, sizeof(buffer) - length);
					if (strcmp(buffer + length, "\r\n") == 0)
						break;
					length += strlen(buffer + length);
				}
				break;
			}
		}

		printf("passcode verification result: ");
		for (int i = 0; i < sizeof(buffer); i++) {
			if (buffer[i] >> 7 == 0) {
				printf("%c", buffer[i]);
			}
		}
		printf("\n");
	}
	

	sprintf(cmd_buffer, "AT+CIPCLOSE");
	success = esp8266_send_command(cmd_buffer);


	return parse_http_response_status(buffer);
}

/**
 * @brief Parses received HTTP responses for their status code.
 *
 * @param http_response the HTTP response to parse.
 * @return the status code extracted from http_response 
 */
int parse_http_response_status(char* http_response) {
	http_response = strstr(http_response, "HTTP/1.1 ");
	printf("status code: %c%c%c\n", http_response[9], http_response[10], http_response[11]); // buffer[9,10,11] should be the status code returned for GET request
	return (http_response[9]- '0')*100 + (http_response[10] - '0')*10 + (http_response[11] - '0')*1;
}
