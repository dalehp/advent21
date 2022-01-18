import pytest

from solutions.day_16.solution import (
    LiteralPacket,
    OperatorPacket,
    PacketType,
    chunks,
    get_packet_value,
    get_version_sum,
    parse_hex_packet,
)


@pytest.mark.parametrize(
    "string,length,chunked",
    [
        ("abcdefghi", 3, ["abc", "def", "ghi"]),
        ("010010001110000100100", 5, ["01001", "00011", "10000", "10010"]),
    ],
)
def test_chunks(string: str, length: int, chunked: list[str]):
    assert chunked == chunks(string, length)


def test_literal():
    expected = LiteralPacket(version=6, value=2021)
    actual = parse_hex_packet("D2FE28")
    assert actual == expected
    assert get_version_sum(actual) == 6


def test_single_layer_operator_type_0():
    expected = OperatorPacket(
        version=1,
        type=PacketType.LT,
        subpackets=[
            LiteralPacket(version=6, value=10),
            LiteralPacket(version=2, value=20),
        ],
    )
    actual = parse_hex_packet("38006F45291200")
    assert actual == expected
    assert get_version_sum(actual) == 9


def test_single_layer_operator_type_1():
    expected = OperatorPacket(
        version=7,
        type=PacketType.MAX,
        subpackets=[
            LiteralPacket(version=2, value=1),
            LiteralPacket(version=4, value=2),
            LiteralPacket(version=1, value=3),
        ],
    )
    actual = parse_hex_packet("EE00D40C823060")
    assert actual == expected
    assert get_version_sum(actual) == 14


def test_nested_operator():
    expected = OperatorPacket(
        version=4,
        type=PacketType.MIN,
        subpackets=[
            OperatorPacket(
                version=1,
                type=PacketType.MIN,
                subpackets=[
                    OperatorPacket(
                        version=5,
                        type=PacketType.MIN,
                        subpackets=[
                            LiteralPacket(
                                version=6,
                                value=15,
                            )
                        ],
                    )
                ],
            )
        ],
    )
    actual = parse_hex_packet("8A004A801A8002F478")
    assert actual == expected
    assert get_version_sum(actual) == 16


def test_multiple_operators_in_operator_type_1():
    actual = parse_hex_packet("620080001611562C8802118E34")
    expected = OperatorPacket(
        version=3,
        type=PacketType.SUM,
        subpackets=[
            OperatorPacket(
                version=0,
                type=PacketType.SUM,
                subpackets=[
                    LiteralPacket(
                        version=0,
                        value=10,
                    ),
                    LiteralPacket(
                        version=5,
                        value=11,
                    ),
                ],
            ),
            OperatorPacket(
                version=1,
                type=PacketType.SUM,
                subpackets=[
                    LiteralPacket(
                        version=0,
                        value=12,
                    ),
                    LiteralPacket(
                        version=3,
                        value=13,
                    ),
                ],
            ),
        ],
    )
    assert actual == expected
    assert get_version_sum(actual) == 12


def test_multiple_operators_in_operator_type_0():
    actual = parse_hex_packet("C0015000016115A2E0802F182340")
    expected = OperatorPacket(
        version=6,
        type=PacketType.SUM,
        subpackets=[
            OperatorPacket(
                version=0,
                type=PacketType.SUM,
                subpackets=[
                    LiteralPacket(
                        version=0,
                        value=10,
                    ),
                    LiteralPacket(
                        version=6,
                        value=11,
                    ),
                ],
            ),
            OperatorPacket(
                version=4,
                type=PacketType.SUM,
                subpackets=[
                    LiteralPacket(
                        version=7,
                        value=12,
                    ),
                    LiteralPacket(
                        version=0,
                        value=13,
                    ),
                ],
            ),
        ],
    )
    assert actual == expected
    assert get_version_sum(actual) == 23


def test_deeply_nested():
    actual = parse_hex_packet("A0016C880162017C3686B18A3D4780")
    assert get_version_sum(actual) == 31


def test_sum_op():
    actual = parse_hex_packet("C200B40A82")
    assert get_packet_value(actual) == 3


def test_product_op():
    actual = parse_hex_packet("04005AC33890")
    assert get_packet_value(actual) == 54


def test_min_op():
    actual = parse_hex_packet("880086C3E88112")
    assert get_packet_value(actual) == 7


def test_max_op():
    actual = parse_hex_packet("880086C3E88112")
    assert get_packet_value(actual) == 7


def test_lt_op():
    actual = parse_hex_packet("D8005AC2A8F0")
    assert get_packet_value(actual) == 1


def test_nested_eq_op():
    actual = parse_hex_packet("9C0141080250320F1802104A08")
    assert get_packet_value(actual) == 1
