// Top level module for smart lock embedded system
module smart_lock (CLOCK_50, KEY, SW, GPIO_0, GPIO_1, LEDR, HEX5, HEX4, HEX3, HEX2, HEX1, HEX0);
    // inputs from the DE1-SoC board
    input CLOCK_50;
    input [9:0] SW;
    input [3:0] KEY;

    // GPIO_0[24, 22, 20, 18] are outputs to the pin pad (for enabling columns),
    // GPIO_0[16, 14, 12, 10] are inputs from the pin pad (for reading rows)
    inout [35:0] GPIO_0;
    inout [35:0] GPIO_1;
    
    logic [3:0] column;
    assign GPIO_0[18] = column[3];
    assign GPIO_0[20] = column[2]; 
    assign GPIO_0[22] = column[1]; 
    assign GPIO_0[24] = column[0];
    
    logic [3:0] row;
    assign row = {~GPIO_0[16], ~GPIO_0[14], ~GPIO_0[12], ~GPIO_0[10]};
     
    // outputs to components of the DE1-SoC board
    output [6:0] HEX5, HEX4, HEX3, HEX2, HEX1, HEX0;
    output [9:0] LEDR;

    wire pio_wifi_reset;

    wire LSENSOR_INT 	 = GPIO_1[0];
    wire MPU_INT 		 = GPIO_1[2];
    wire RH_TEMP_I2C_SCL = GPIO_1[3];
    wire RH_TEMP_DRDY_n  = GPIO_1[4];
    wire RH_TEMP_I2C_SDA = GPIO_1[5];
    wire LSENSOR_SCL     = GPIO_1[7];
    wire BT_KEY          = GPIO_1[8];
    wire LSENSOR_SDA     = GPIO_1[9];
    wire MPU_SCL_SCLK 	 = GPIO_1[11];
    wire WIFI_UART1_RX 	 = GPIO_1[12];
    wire MPU_SDA_SDI 	 = GPIO_1[13];
    wire WIFI_UART0_RX 	 = GPIO_1[14];
    // UART_TX 			 = wire GPIO_1[16];
    // UART_RX 			 = wire GPIO_1[17];
    // wire BT_UART_RX 	 = GPIO_1[18]; 
    wire WIFI_UART0_CTS  = GPIO_1[20]; 
    wire UART_RTS 		 = GPIO_1[22];
    wire UART_CTS 		 = GPIO_1[23]; 
    wire BT_UART_CTS 	 = GPIO_1[24]; 
    wire BT_UART_RTS 	 = GPIO_1[25];
    wire MPU_AD0_SD0 	 = GPIO_1[27];

    wire WIFI_RST_n, MPU_CS_n, MPU_FSYNC, WIFI_EN, WIFI_UART0_TX, WIFI_UART0,RTS;

    assign GPIO_1[1]  	 = WIFI_RST_n;
    // assign GPIO_1[19] 	 = BT_UART_TX;
    assign GPIO_1[26]  	 = MPU_CS_n;
    assign GPIO_1[6]       = MPU_FSYNC;
    assign GPIO_1[10]		 = WIFI_EN;
    assign GPIO_1[15]      = WIFI_UART0_TX;
    assign GPIO_1[21] 	 = WIFI_UART0_RTS;

    //wire HEX0_DP, HEX1_DP, HEX2_DP, HEX3_DP, HEX4_DP, HEX5_DP;

    //=======================================================
    //  Structural coding
    //=======================================================

    assign WIFI_RST_n = KEY[0] & pio_wifi_reset;
    assign WIFI_EN = 1'b1;

    assign LEDR[6] = ~GPIO_1[15];
    assign LEDR[7] = ~GPIO_1[14];

nios2_system u0 (
        .clk_clk                                     (CLOCK_50),        //                                 clk.clk
        .pinpad_col_conduit                          (column),          //
        .pinpad_row_conduit                          (row),             //                          pinpad_row.conduit
        .reset_reset_n                               (KEY[0]),          //                               reset.reset_n
        .servo_pwm_conduit                           (GPIO_0[9]),       //                           servo_pwm.conduit
        .wifi_uart0_external_connection_rxd          (WIFI_UART0_RX),   //          wifi_uart0_external_connection.rxd
        .wifi_uart0_external_connection_txd          (WIFI_UART0_TX),   //                                        .txd
        .wifi_uart0_external_connection_cts_n        (WIFI_UART0_CTS),  //                                      .cts_n
        .wifi_uart0_external_connection_rts_n        (WIFI_UART0_RTS),  //                                      .rts_n
        .pio_wifi_reset_external_connection_export   (pio_wifi_reset),  //   pio_wifi_reset_external_connection.export
        .pio_key_external_connection_export          (KEY[1]),          //          pio_key_external_connection.export
        .pio_led_external_connection_export          (LEDR[3:0]),       //         pio_led_external_connection.export
        .get_req_keys_export                         (KEY[3:2])   
    );


endmodule