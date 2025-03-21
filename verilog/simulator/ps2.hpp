#pragma once
#include <array>
#include <cstdint>
#include <vector>
#include <queue>
#include <optional>
#include "raylib.h"

namespace ps2{
    struct Packet{
        std::array<bool,11> data{};
        explicit Packet(uint8_t value);
    };
    struct Keyboard {
        std::queue<Packet> packets_to_send;
        auto encode_key(KeyboardKey key,bool isRelease) -> std::optional<std::vector<Packet>>;
    };
}
