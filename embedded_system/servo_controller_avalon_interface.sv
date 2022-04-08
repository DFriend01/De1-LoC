// Avalon interface for servo controller module
module servo_controller_avalon_interface (
    input logic clk,
    input logic reset, 
    input logic write, 
    input logic [7:0] writedata,
    // output logic [6:0] servo_state,         // input for a seven segment LED display
    // output logic [6:0] input_received_1,    // input for a seven segment LED display
    // output logic [6:0] input_received_0,    // input for a seven segment LED display
    // output logic [6:0] write_status,        // input for a seven segment LED display
    // output logic [6:0] reset_status,        // input for a seven segment LED display
    output logic servo_pwm
);
    logic locked;

    always_ff @(posedge clk) begin 
        if (reset) 
            locked <= 0;
        else if (write) 
            locked <= |writedata;
    end


    // hex7seg ss0 (.in({3'b0, locked}), .out(servo_state));           // DEBUG TOOL: display current state
    // hex7seg ss1 (.in({3'b0, write}), .out(write_status));           // DEBUG TOOL: display current write value
    // hex7seg ss2 (.in(writedata[7:4]), .out(input_received_1));      // DEBUG TOOL: display current writedata
    // hex7seg ss3 (.in(writedata[3:0]), .out(input_received_0));      // DEBUG TOOL: display current writedata
    // hex7seg ss4 (.in(reset), .out(reset_status));                   // DEBUG TOOL: display current reset status

	servo_controller sc (
        .locked(locked),
		.clk(clk),		
		.servo(servo_pwm)
    );

endmodule

