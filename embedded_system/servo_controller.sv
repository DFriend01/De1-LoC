module servo_controller(input logic locked,
						input logic clk,		
						output logic servo);


	logic [19:0] counter = 0; // 20 bits width to count up to 1,000,000 clock cycles

	// counter to control the PWM's duty cycle
	always_ff @(posedge clk) begin
		// reset counter (start a new pulse) every 20ms (= 1,000,000 clock cycles at 50Mhz)
		if (counter == 20'd1000000) counter <= 0; 
		else counter <= counter + 1; 
	end

	parameter count_1ms = 16'd50000;
	parameter count_2ms = 17'd100000;

	logic [16:0] count_to;
	assign count_to = locked ? count_1ms : count_2ms;

	assign servo = (counter > count_to) ? 0: 1;

endmodule