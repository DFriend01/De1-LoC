// Pin pad reader for smart lock embedded system
// Note: for future implementation / transition to NIOS, add a done state signalled by "#" and output a 16 bit value (4 digits, 4 bits/digit) to the NIOS processor)

module pinpad_reader (clk_50, reset_n, row, column, seven_seg_out);
    // inputs
    input clk_50, reset_n;
    input [3:0] row;

    // outputs
    output logic [3:0] column;
    output logic [6:0] seven_seg_out;

    logic clk;

    // slow down the 50MHz clock to 50KHz, so that we can catch each button press reliably
    clk_divider cd (.inClk(clk_50), .reset(~reset_n), .clock_count(15'd25000), .outClk(clk));

    /***********************************************************************
                                    fsm
    ***********************************************************************/

    // state encoding
    parameter IDLE = 7'b000_0111; // Enable leftmost column (column 1), so that we can detect when our PIN's starting button "*" is pressed.
    parameter C1 = 7'b001_0111; // Enable Column 1 
    parameter C2 = 7'b010_1011; // Enable Column 2 
    parameter C3 = 7'b011_1101; // Enable Column 3
    parameter C4 = 7'b100_1110; // Enable Column 4

    logic [6:0] state, next_state;
    logic button_pressed;
    assign button_pressed = (row == 4'b1000 || row == 4'b0100 || row == 4'b0010 || row == 4'b0001) ? 1 : 0; // Button is considered pressed if any of the rows is enabled
    
    // Reset Logic
    always_ff @(posedge clk) begin 
        if (~reset_n) state = IDLE;
        else state = next_state;
    end

    // State Transition Logic
    always_comb begin 
        case(state) 
            IDLE: 
                if (row == 4'b1000) next_state <= C1;
                else next_state <= IDLE;
            C1: 
                if (button_pressed) next_state <= C1;
                else next_state <= C2;
            C2:
                if (button_pressed) next_state <= C2;
                else next_state <= C3;
            C3:
                if (button_pressed) next_state <= C3;
                else next_state <= C4;
            C4:
                if (button_pressed) next_state <= C4;
                else next_state <= C1;
            default: next_state <= IDLE;
        endcase
    end

    // state outputs
    assign column = state[3:0];

    /***********************************************************************
                                datapath
    ***********************************************************************/

    // decode and register the row detected (digit pressed) according to column 1 of the pin pad (leftmost column: 1, 4, 7)
    logic [3:0] num;
    logic [3:0] r1_digit;
    logic [3:0] r2_digit;
    logic [3:0] r3_digit;
    logic [3:0] r4_digit;
    
    always_ff @(posedge clk) begin
        if (~reset_n) r1_digit <= 4'd15;
        else
            case (row)
                4'b0001: r1_digit <= 4'd1;
                4'b0010: r1_digit <= 4'd4;
                4'b0100: r1_digit <= 4'd7;
                default: r1_digit <= 4'd15;
            endcase
    end

    always_ff @(posedge clk) begin
        if (~reset_n) r2_digit <= 4'd15;
        else 
            case (row)
                4'b0001: r2_digit = 4'd2;
                4'b0010: r2_digit = 4'd5;
                4'b0100: r2_digit = 4'd8;
                4'b1000: r2_digit = 4'd0;
                default: r2_digit = 4'd15;
            endcase
    end

    always_ff @(posedge clk) begin
        if (~reset_n) r3_digit <= 4'd15;
        else
            case (row)
                4'b0001: r3_digit = 4'd3;
                4'b0010: r3_digit = 4'd6;
                4'b0100: r3_digit = 4'd9;
                default: r3_digit = 4'd15;
            endcase
    end

    always_ff @(posedge clk) begin
        if (~reset_n) r4_digit <= 4'd15;
        else
            case (row)
                4'b0001: r4_digit = 4'd10;
                4'b0010: r4_digit = 4'd11;
                4'b0100: r4_digit = 4'd12;
                4'b1000: r4_digit = 4'd13;
            default: r4_digit = 4'd15;
            endcase
    end

    // multiplexer to decide which row's decoding we should output
    always_comb begin
        case (column)
            4'b0111: num = r1_digit;
            4'b1011: num = r2_digit;
            4'b1101: num = r3_digit;
            4'b1110: num = r4_digit;
            default: num = 4'd15;
        endcase
    end


    // Transform the digit pressed into a seven-segment display input, and connect to seven_seg_out
    hex7seg ss_decoder (.in(num), .out(seven_seg_out)); 

endmodule