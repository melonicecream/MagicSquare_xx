import pytest


@pytest.fixture
def grid_g1():
    """G1: 빈 칸(0) 2개, row-major 4×4."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 0],
        [4, 0, 14, 1],
    ]


@pytest.fixture
def grid_incomplete():
    """0이 하나 포함된 4×4 격자 (FR-001 / GM-001)."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]


@pytest.fixture
def grid_r1_fail():
    """R1 합 ≠ 34, 나머지 선 pass 후보 (FR-002 / T-R201)."""
    return [
        [1, 1, 1, 1],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]


@pytest.fixture
def grid_d1_fail():
    """행·열 OK, D1만 깨짐 (FR-004 / S1 / GM-003)."""
    return [
        [17, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 6, 12],
        [4, 15, 14, 1],
    ]


@pytest.fixture
def grid_d2_fail():
    """행·열 OK, D2만 깨짐 (FR-004 / S1 / GM-004)."""
    return [
        [16, 3, 2, 14],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]


@pytest.fixture
def complete_magic_square():
    """완전 마방진 4×4, 10선 합 34 (FR-003 / GM-002)."""
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]
