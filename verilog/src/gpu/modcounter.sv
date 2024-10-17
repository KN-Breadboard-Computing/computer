module modcounter #(parameter rst_value = 0, parameter width = 9) (
    input wire clk,
    input wire rst,
    output wire overflow,
    output wire [width - 1 : 0] data_out
);

reg [width - 1 : 0] data;
wire ov;

always_ff @(posedge clk or negedge rst) begin
    if (ov | ~rst) data <= 0;
    else data <= data + 1;
end

assign ov = (data == rst_value);
assign overflow = ov;
assign data_out = data;

endmodule
