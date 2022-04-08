/*
 * requests.h
 *
 *  Created on: Apr 5, 2022
 *      Author: User
 */

#ifndef REQUESTS_H_
#define REQUESTS_H_

#define METHOD_GET 1
#define METHOD_POST 0

#define REQ_PINPAD_VERIFY_BODY_LENGTH 53

const char *host = "5a94-206-87-134-234.ngrok.io";

// GET request string, for unlocks initiated from Android app
const char *req_app_verify = "GET /auth/verify/app HTTP/1.1\r\n\
Cache-Control: no-store\r\n\
Host: %s\r\n\
\r\n\
";

// POST request string, for unlocks initiated from physical pinpad
const char *req_pinpad_verify = "POST /auth/verify/pinpad HTTP/1.1\r\n\
Host: %s\r\n\
Content-Type: application/json\r\n\
Content-Length: %d\r\n\
\r\n\
{\"msg\": {\"num1\": %d, \"num2\": %d, \"num3\": %d, \"num4\": %d}}\r\n\
\r\n\
";

#endif /* REQUESTS_H_ */