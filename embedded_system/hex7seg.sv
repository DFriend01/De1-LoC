// Hardware to encode a 4-bit numbers, to be displayed on a 
// seven-segment display as decimal numbers.

// Based on the HDL code found in Intel's "Making Platform Designer Components Tutorial", Appendix A
// (https://ftp.intel.com/Public/Pub/fpgaup/pub/Teaching_Materials/current/Tutorials/Making_Qsys_Components.pdf)  

module hex7seg(in, out);
    input [3:0] in;
    output [6:0] out;

    logic [6:0] out;

    always @( in )
        case ( in )
            0: out = 7'b100_000_0;
            1: out = 7'b111_100_1;
            2: out = 7'b010_010_0;
            3: out = 7'b011_000_0;
            4: out = 7'b001_100_1;
            5: out = 7'b001_001_0;
            6: out = 7'b000_001_0;
            7: out = 7'b111_100_0;
            8: out = 7'b000_000_0;
            9: out = 7'b001_000_0;
			10: out = 7'b000_100_0;
        	11: out = 7'b000_001_1;
        	12: out = 7'b100_011_0;
        	13: out = 7'b010_000_1;
            default:  out = 7'b011_111_1;
        endcase
endmodule