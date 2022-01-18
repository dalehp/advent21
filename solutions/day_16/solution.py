from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import prod
from typing import Callable, Protocol

FILE = "solutions/day_16/input.txt"


@dataclass
class LiteralPacket:
    version: int
    value: int
    subpackets: list[Packet] = field(init=False, default_factory=list)


@dataclass
class OperatorPacket:
    version: int
    subpackets: list[Packet]
    type: PacketType


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GT = 5
    LT = 6
    EQUALITY = 7


class OperatorCallable(Protocol):
    def __call__(*args: int) -> int:
        ...


TYPE_TO_FN: dict[PacketType, OperatorCallable] = {
    PacketType.SUM: lambda *x: sum(x),
    PacketType.PRODUCT: lambda *x: prod(x),
    PacketType.MIN: lambda *x: min(x),
    PacketType.MAX: lambda *x: max(x),
    PacketType.GT: lambda *x: int(x[0] > x[1]),
    PacketType.LT: lambda *x: int(x[0] < x[1]),
    PacketType.EQUALITY: lambda *x: int(x[0] == x[1]),
}


Packet = LiteralPacket | OperatorPacket


def chunks(s: str, l: int) -> list[str]:
    num_chunks = len(s) // l
    return [s[i * l : l + i * l] for i in range(num_chunks)]


def parse_literal_bits(bits: str) -> tuple[bool, str]:
    last_byte = bits[0] == "0"
    byte_value = bits[1:]
    return last_byte, byte_value


def parse_literal(body_str: str) -> tuple[int, str]:
    bytes = []
    for bits in chunks(body_str, 5):
        last, byte = parse_literal_bits(bits)
        bytes.append(byte)
        if last:
            break
    remaining = body_str[5 * len(bytes) :]
    return int("".join(bytes), 2), remaining


def padded_bin_string(packet_str: str) -> str:
    packet_int = int(packet_str, 16)
    bin_length = len(packet_str) * 4
    return f"{packet_int:0{bin_length}b}"


def parse_hex_packet(packet_str: str) -> Packet:
    bin_str = padded_bin_string(packet_str)
    packet, _ = parse_packet(bin_str)
    return packet


def length_type_0_exhausted(length: int, chars_used: int, packets_used: int) -> bool:
    _ = packets_used
    return chars_used >= length


def length_type_1_exhausted(length: int, chars_used: int, packets_used: int) -> bool:
    _ = chars_used
    return packets_used >= length


def get_operator_length_and_fn(
    bin_str: str,
) -> tuple[int, Callable[[int, int, int], bool], str]:
    type_str = bin_str[0]
    if type_str == "0":
        length = int(bin_str[1:16], 2)
        remainder = bin_str[16:]
        fn = length_type_0_exhausted
    elif type_str == "1":
        length = int(bin_str[1:12], 2)
        remainder = bin_str[12:]
        fn = length_type_1_exhausted
    else:
        raise RuntimeError(f"bin string should only contain 1 and 0: {bin_str}")
    return length, fn, remainder


def parse_packet(bin_str: str) -> tuple[Packet, str]:
    version = int(bin_str[:3], 2)
    type = PacketType(int(bin_str[3:6], 2))
    body_bin = bin_str[6:]
    if type == PacketType.LITERAL:
        value, remaining = parse_literal(body_bin)
        return LiteralPacket(version=version, value=value), remaining

    length, length_exceeded_fn, subpackets_str = get_operator_length_and_fn(body_bin)
    starting_length = len(subpackets_str)

    subpacket, subpackets_str = parse_packet(subpackets_str)
    subpackets = [subpacket]

    while not length_exceeded_fn(
        length, starting_length - len(subpackets_str), len(subpackets)
    ):
        subpacket, subpackets_str = parse_packet(subpackets_str)
        subpackets.append(subpacket)

    return (
        OperatorPacket(
            version=version,
            subpackets=subpackets,
            type=type,
        ),
        subpackets_str,
    )


def get_version_sum(packet: Packet) -> int:
    total = packet.version
    for subpacket in packet.subpackets:
        total += get_version_sum(subpacket)
    return total


def get_packet_value(packet: Packet) -> int:
    if isinstance(packet, LiteralPacket):
        return packet.value

    args = [get_packet_value(p) for p in packet.subpackets]
    return TYPE_TO_FN[packet.type](*args)


def solve_part_a() -> int:
    with open(FILE) as f:
        hex_str = f.readline().rstrip()
    packet = parse_hex_packet(hex_str)
    return get_version_sum(packet)


def solve_part_b() -> int:
    with open(FILE) as f:
        hex_str = f.readline().rstrip()
    packet = parse_hex_packet(hex_str)
    return get_packet_value(packet)


def run():
    print(solve_part_a())
    print(solve_part_b())
