module pinpad_reader_avalon_interface(
    input logic clk_50, 
    input logic reset, 
    input logic read, 
	input logic [3:0] row,
    output logic [31:0] readdata, 
    output logic waitrequest,
	output logic [3:0] column
	// output logic [6:0] debug_num,
	// output logic [6:0] debug_state_info,
	// output logic [6:0] debug_readdata_upper_display,
	// output logic [6:0] debug_readdata_lower_display,
	// output logic [6:0] debug_column,
	// output logic [6:0] debug_row
);
	
	// STATE ENCODINGS
	parameter IDLE = 5'b000_01;
	parameter GET_DIGIT = 5'b001_01;
	parameter READ_DIGIT = 5'b010_10;

	logic [3:0] state = IDLE;
    logic get_digit_done;
    
	assign waitrequest = state[0];
	
	logic readdata_en;
	assign readdata_en = state[1];

	logic clk;
	clk_divider cd (.inClk(clk_50), .reset(), .clock_count(15'd25000), .outClk(clk));

	always_ff @(posedge clk) begin
		if (reset) state <= IDLE;
		else 
		    case(state) 
		        IDLE: 	
                    if (read) state <= GET_DIGIT;
					else state <= IDLE;
	        	GET_DIGIT: 
					if (get_digit_done) state <= READ_DIGIT;
					else state <= GET_DIGIT;
				READ_DIGIT: state <= IDLE;
                default: state <= IDLE;
            endcase
	end

	logic [3:0] num;
	always_ff @(posedge clk) begin 
		if (reset) readdata <= 4'd15;
		else readdata <= num; 
	end
    pinpad_get_digit pgd (
        .clk_50     (clk_50), 
        .reset_n    (reset), 
        .row        (row), 
        .column     (column), 
		.num        (num), 
		.done		(get_digit_done)
    );

	// hex7seg ss5 (.in(num), .out(debug_num));
	// hex7seg ss4 (.in(state), .out(debug_state_info));
	// hex7seg ss3 (.in(readdata[7:4]), .out(debug_readdata_upper_display));
	// hex7seg ss2 (.in(readdata[3:0]), .out(debug_readdata_lower_display));
	// hex7seg ss1 (.in(column), .out(debug_column));
	// hex7seg ss0 (.in(row), .out(debug_row));

endmodule