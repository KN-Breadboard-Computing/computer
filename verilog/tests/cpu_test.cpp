#include <cstdint>
#include <cstdio>
#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest/doctest.h"
#include "Vcpu.h"
#include "Vmem_unit.h"
#include "verilated.h"
#include <iostream>
#include <iomanip>

enum ReadFlags {
    READ_ZP = 1, // zero page
    READ_HP = 2, // high part
};

enum WriteFlags {
    WRITE_ZP = 1, // zero page
    WRITE_HP = 2, // high part
};

void reset(Vmem_unit& mem) {
    mem.zero_page = 1;
    mem.mem_part = 0;
    mem.mem_out = 1;
    mem.mem_in = 1;
    mem.reg_mbr_load = 0;
    mem.reg_mar_load = 0;
    mem.reg_mbr_word_dir = 1;
    mem.data_in_en = 0;
    //mem.reg_mbr_use_bus = 1;
}

void load_mar_mbr(Vmem_unit& mem, int addr, int data) {
    mem.reg_mar_load = 1;
    mem.reg_mbr_load = 1;
    mem.mem_out = 1;
    mem.mem_in = 1;
    mem.mem_part = 0;
    mem.zero_page = 1;
    mem.reg_mbr_word_dir = 1;
    mem.data_in = data;
    mem.data_in_en = 1;
    mem.address = addr;
    //mem.reg_mbr_use_bus = 0;
}

void load_mbr_to_mem(Vmem_unit& mem, int flags = 0) {
    mem.reg_mar_load = 0;
    mem.reg_mbr_load = 0;
    mem.mem_out = 1;
    mem.mem_in = 0;
    mem.mem_part = (flags & READ_HP) ? 1 : 0;
    mem.zero_page = (flags & READ_ZP) ? 0 : 1;
    mem.reg_mbr_word_dir = 1;
    mem.data_in_en = 0;
    //mem.reg_mbr_use_bus = 1;
}

void load_mem(Vmem_unit& mem, int flags = 0) {
    mem.reg_mar_load = 0;
    mem.reg_mbr_load = 0;
    mem.mem_out = 0;
    mem.mem_in = 1;
    mem.mem_part = (flags & READ_HP) ? 1 : 0;
    mem.zero_page = (flags & READ_ZP) ? 0 : 1;
    mem.reg_mbr_word_dir = 0;
    mem.data_in_en = 0;
    //mem.reg_mbr_use_bus = 0;
}

void load_mar(Vmem_unit& mem, int addr) {
    mem.reg_mar_load = 1;
    mem.reg_mbr_load = 0;
    mem.mem_out = 1;
    mem.mem_in = 1;
    mem.mem_part = 0;
    mem.zero_page = 1;
    mem.reg_mbr_word_dir = 1;
    mem.address = addr;
    mem.data_in_en = 0;
    //mem.reg_mbr_use_bus = 0;
}

TEST_CASE("Mov works") {
    VerilatedContext* ctx = new VerilatedContext;
    Vmem_unit mem;
    Vcpu cpu(ctx, "cpu");

    ctx->debug(0);
    ctx->traceEverOn(true);

    reset(mem);
    mem.eval();

    bool clk = false;
    cpu.clk = clk;
    cpu.bus_in_en = 0;
    cpu.bus_in = 0;
    cpu.rst = 0;
    cpu.eval();
    ctx->timeInc(1);
    clk = !clk;
    cpu.clk = clk;
    cpu.bus_in_en = 0;
    cpu.bus_in = 0;
    cpu.rst = 0;
    cpu.eval();
    ctx->timeInc(1);

    cpu.rst = 1;

    uint8_t prog[] = { 
        0x11, 0x05,       // mov a, 0x05     | 4
        0x05,             // mov b, a        | 3
        0x0A,             // mov th, b       | 3
        0x0D,             // mov tl, a       | 3
        0x02,             // mov a, th       | 3
        0x07,             // mov b, tl       | 3
        0x01,             // mov a, b        | 3
        0x19, 0xDE, 0xAD, // mov [0xDEAD], a | 8
        0x19, 0xBE, 0xEF,  // mov [0xBEEF], a | 8
        0x11, 0x33,
        0x19, 0xCA, 0xFE,  // mov [0xCAFE], a | 8
        0xD8
    };

    // Copy program to memory
    for (size_t i = 0; i < sizeof(prog); i++) {
        load_mar_mbr(mem, 0x0000 + i, prog[i]);
        mem.eval();

        load_mbr_to_mem(mem);
        mem.eval();
    }

    for (size_t i = 0; i < 256; i++) {
        clk = !clk;
        cpu.clk = clk;
        cpu.eval();
        printf("[cpu] eval 1 clk = %d\n", clk);
        ctx->timeInc(1);
        mem.zero_page = cpu.zero_page;
        mem.mem_part = cpu.mem_part;
        mem.mem_in = cpu.mem_in;
        if (!mem.mem_in) printf("MEM IN\n");
        printf("mem_in = %d, mem_out = %d, load_mar = %d, load_mbr = %d\n", cpu.mem_in, cpu.mem_out, cpu.reg_mar_load, cpu.reg_mbr_load);
        mem.mem_out = cpu.mem_out;
        mem.reg_mbr_load = cpu.reg_mbr_load & clk;
        mem.reg_mbr_word_dir = cpu.reg_mbr_word_dir;
        mem.reg_mar_load = cpu.reg_mar_load & clk;
        mem.data_in_en = cpu.reg_mbr_load; //((cpu.reg_mbr_word_dir & ~cpu.mem_in) | cpu.reg_mbr_load) & 1;
        printf("mem.data_in_en = %u\n", mem.data_in_en); 
        mem.data_in = cpu.bus_out;
        mem.address = cpu.addr_bus;
        printf("[cpu] bus_in_en = %d\n", cpu.bus_in_en);
        printf("[mem] data_in = %02x, addr = %04x\n", mem.data_in, mem.address);
        printf("[cpu] %02x %04x\n", cpu.bus_out, cpu.addr_bus);
        mem.eval();
        printf("[mem] eval 1\n");
        // reg_mbr_word_dir
        // 1 = CPU -> MEM
        // 0 = MEM -> CPU
        cpu.bus_in_en = (~mem.mem_out & 1);
        cpu.bus_in = mem.data_out;
        printf("[mem] %02x\n", mem.data_out);
        cpu.eval();
        printf("[cpu] eval 2\n");
        printf("[cpu] %02x\n", cpu.bus_out);
        ctx->timeInc(1);
    }

    //// 6 cycles for MOVATABSA
    //for (size_t i = 0; i < 12; i++) {
    //    clk = !clk;
    //    cpu.clk = clk;
    //    cpu.eval();
    //    mem.zero_page = cpu.zero_page;
    //    mem.mem_part = cpu.mem_part;
    //    mem.mem_in = cpu.mem_in;
    //    mem.mem_out = cpu.mem_out;
    //    mem.reg_mbr_load = cpu.reg_mbr_load;
    //    mem.reg_mbr_word_dir = cpu.reg_mbr_word_dir;
    //    mem.reg_mar_load = cpu.reg_mar_load;
    //    mem.data_in_en = cpu.reg_mbr_word_dir;
    //    mem.data_in = cpu.bus_out;
    //    mem.address = cpu.addr_bus;
    //    printf("[cpu] %02x %04x\n", cpu.bus_out, cpu.addr_bus);
    //    mem.eval();
    //    cpu.bus_in_en = ~cpu.reg_mbr_word_dir;
    //    cpu.bus_in = mem.data_out;
    //    printf("[mem] %02x\n", mem.data_out);
    //    cpu.eval();
    //    printf("[cpu] %02x\n", cpu.bus_out);
    //}

    load_mar_mbr(mem, 0xDEAD, 0x00);
    mem.eval();

    load_mem(mem);
    mem.eval();
    CHECK_MESSAGE(mem.data_out == 0x05, "read @ 0xDEAD");

    load_mar_mbr(mem, 0xBEEF, 0x00);
    mem.eval();

    load_mem(mem);
    mem.eval();
    CHECK_MESSAGE(mem.data_out, 0x05, "read @ 0xBEEF");

    load_mar_mbr(mem, 0xCAFE, 0x00);
    mem.eval();

    load_mem(mem);
    mem.eval();
    CHECK_MESSAGE(mem.data_out, 0x33, "read @ 0xCAFE");
}
