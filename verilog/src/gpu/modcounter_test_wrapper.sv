module modcounter_test_wrapper(
    input wire clk,
    output wire overflow,
    output wire [9 : 0] data_out
);

modcounter #(.rst_value(799), .width(10)) counter(.clk(clk), .rst(1'b1), .overflow(overflow), .data_out(data_out));

endmodule
