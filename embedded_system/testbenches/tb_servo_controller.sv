// testbench for servo controller

module tb_servo_controller();

    // inputs to DUT
    logic locked, clk;
    // outputs from DUT
    logic servo;
    // instantiat DUT
    servo_controller DUT (.locked(locked), .clk(clk), .servo(servo));

    logic [19:0] clock_cycle_count = 0;
    event twenty_ms;
    // clock signal
    always begin 
        forever begin
            clk = 0; #5;
            clk = 1; #5;

            // trigger the twenty_ms event every 1,000,000 clock cycles
            if (clock_cycle_count < 1000000) 
                clock_cycle_count = clock_cycle_count + 1;
            else begin 
                clock_cycle_count = 0; -> twenty_ms;
            end
        end
    end

    // test
    initial begin 
        locked = 0; 
        
        @(twenty_ms);
        @(twenty_ms);
        locked = 1;

        @(twenty_ms);
        @(twenty_ms);
        $stop;
    end

endmodule