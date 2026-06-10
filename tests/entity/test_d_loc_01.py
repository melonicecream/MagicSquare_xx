import pytest

from entity.grid import find_blank_coords


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Arrange (Given): grid_g1 — G1 격자, 빈 칸 0이 2개
    grid = grid_g1

    # Act (When): find_blank_coords 호출 (결과 검증은 /tdd-red에서)
    _ = find_blank_coords(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: T-D-LOC-01 — find_blank_coords가 1-index row-major로 [(2,3),(4,4)]를 반환해야 한다"
    )
