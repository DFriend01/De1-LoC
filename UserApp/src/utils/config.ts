export const EMULATOR = 0;
export const LOCALHOST = 0;

const NGROK = "https://5a94-206-87-134-234.ngrok.io/";
export const URL = LOCALHOST ? "http://10.0.2.2:5000/" : NGROK;