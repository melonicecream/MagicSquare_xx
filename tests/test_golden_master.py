import pytest

from validate_lines import validate_lines


def test_gm_001_incomplete(grid_incomplete):
    # Arrange (Given): grid_incomplete — 0 포함 격자 (GM-001)
    grid = grid_incomplete

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red 또는 /golden-master에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: GM-001 — 0 포함 격자 → status=incomplete, failed_lines=[]"
    )


def test_gm_002_pass(complete_magic_square):
    # Arrange (Given): complete_magic_square — 완전 마방진 (GM-002)
    grid = complete_magic_square

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red 또는 /golden-master에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: GM-002 — 완전 마방진 → status=pass, failed_lines=[]"
    )


def test_gm_003_d1_fail(grid_d1_fail):
    # Arrange (Given): grid_d1_fail — 행·열 OK, D1만 깨짐 (GM-003)
    grid = grid_d1_fail

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red 또는 /golden-master에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: GM-003 — D1만 깨짐 → status=fail, D1 ∈ failed_lines"
    )


def test_gm_004_d2_fail(grid_d2_fail):
    # Arrange (Given): grid_d2_fail — 행·열 OK, D2만 깨짐 (GM-004)
    grid = grid_d2_fail

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red 또는 /golden-master에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: GM-004 — D2만 깨짐 → status=fail, D2 ∈ failed_lines"
    )


def test_gm_005_idempotent(complete_magic_square):
    # Arrange (Given): complete_magic_square — GM-002와 동일 grid (GM-005)
    grid = complete_magic_square

    # Act (When): validate_lines 2회 호출 (결과 검증은 /tdd-red 또는 /golden-master에서)
    _ = validate_lines(grid)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail(
        "RED: GM-005 — 동일 grid 2회 호출 → 동일 status·failed_lines"
    )
