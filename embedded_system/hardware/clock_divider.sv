// References: concepts covered in pg 197-198 in the CHU textbook
// The clk_divider module works by staying at output 1 for a certain number of cycles (clock_count) before it inverts to output 0..
// This gives it the effect of dividing the frequency.
// However, the following implementation divides the input inClk by double the value of clock_count. 
// So, the pre requisite for the use of this module is that the input from clock_cyle_calc module must be half the intended value.
// In this way, the output is correct given this implementation
// This has been extended to divide up to a frequency of n (up till 32 bits as in generate_arbitrary_divided_clk32).

module clk_divider (inClk, reset, clock_count, outClk);
    input logic inClk;
    input logic reset;
    input logic [31:0] clock_count;
    output logic outClk = 1'b0;

    logic [31:0] count = 1'b0;

    always @(posedge inClk) begin
        if (reset) begin // If reset, set count back to 0, and set outClk to 0 (use first in tb)
            count <= 0;
            outClk <= 0;
        end

        else begin
            if (count < clock_count - 1) // Need to add -1 otherwise extra cycle showing up on tb (check with TA)
                count <= count + 1; // Count till required number of cycles given a required frequency.
            else begin
                outClk <= ~outClk; // After the required number of periods have elapsed, set outClk to 0.
                count <= 0;
            end

        end
    end

endmodule