import pytest

from validate_lines import validate_lines


def test_r101_incomplete_when_grid_has_zero(grid_incomplete):
    # Arrange (Given): grid_incomplete — 0이 하나 포함된 4×4 격자
    grid = grid_incomplete

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: T-R101 — 0이 남으면 status=incomplete, failed_lines=[]를 반환해야 한다"
    )


def test_r201_fail_reports_broken_row_line_id(grid_r1_fail):
    # Arrange (Given): grid_r1_fail — R1 합 ≠ 34
    grid = grid_r1_fail

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: T-R201 — 채워진 선 합 ≠ 34이면 status=fail, R1 ∈ failed_lines"
    )


def test_r202_fail_when_only_d1_broken(grid_d1_fail):
    # Arrange (Given): grid_d1_fail — 행·열 OK, D1만 깨짐
    grid = grid_d1_fail

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: T-R202 — 행·열만 맞고 D1만 틀리면 status=fail, D1 ∈ failed_lines"
    )


def test_r203_fail_when_only_d2_broken(grid_d2_fail):
    # Arrange (Given): grid_d2_fail — 행·열 OK, D2만 깨짐
    grid = grid_d2_fail

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: T-R203 — 행·열만 맞고 D2만 틀리면 status=fail, D2 ∈ failed_lines"
    )


def test_r301_pass_when_all_ten_lines_sum_to_magic_constant(complete_magic_square):
    # Arrange (Given): complete_magic_square — 10선 모두 합 34
    grid = complete_magic_square

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: T-R301 — 10선 모두 합 34이면 status=pass, failed_lines=[]"
    )


def test_r302_idempotent_on_same_grid(complete_magic_square):
    # Arrange (Given): complete_magic_square — 동일 격자
    grid = complete_magic_square

    # Act (When): validate_lines 2회 호출 (결과 검증은 /tdd-red에서)
    _ = validate_lines(grid)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: T-R302 — 동일 격자 2회 호출 시 status·failed_lines가 동일해야 한다"
    )
