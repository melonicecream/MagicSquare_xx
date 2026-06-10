# TDD RED — validate_lines

`validate_lines` 기능에 **실패하는 테스트만** 추가한다. 구현(GREEN)은 하지 않는다.

## Phase 선언 (필수)

응답 **첫 줄**에 반드시:

```
Phase: RED
```

RED/GREEN/REFACTOR 혼합 금지. 이번 작업은 RED만.

---

## 범위

| 허용 | 금지 |
|------|------|
| `tests/test_validate_lines.py` 수정 | `src/` 및 그 외 모든 파일 수정 |
| `tests/fixtures/` fixture 추가(필요 시) | `validate_lines` 구현·스텁 변경 |
| `pytest` 실행으로 RED 확인 | assert 완화, `@pytest.mark.skip`, `xfail`, 기대값 변경으로 RED 회피 |

**한 RED = 한 목적.** 한 번에 검증할 동작·규칙은 하나만.

---

## AAA 절차

각 테스트는 **Arrange → Act → Assert** 순서를 지킨다.

1. **Arrange** — 4×4 격자 준비. `0` = 빈 칸, 값은 1~16(중복 없음). fixture·인라인 리스트 모두 가능.
2. **Act** — `result = validate_lines(grid)` 호출.
3. **Assert** — 반환 dict 검증:
   - `result["status"]` ∈ `"pass"` | `"fail"` | `"incomplete"`
   - `result["failed_lines"]`: 깨진 선 ID 문자열 목록 (`R1`~`R4`, `C1`~`C4`, `D1`, `D2`)
   - `pass`·`incomplete` → `failed_lines == []`
   - `fail` → 깨진 선 ID만 포함(마법상수 **34** 기준)

테스트 함수명·docstring으로 **무엇을 검증하는지** 드러낸다.

---

## pytest 예시

```python
import pytest

from validate_lines import MAGIC_CONSTANT, validate_lines


def test_incomplete_when_grid_has_zero():
    # Arrange — 0이 하나라도 있으면 incomplete
    grid = [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 0],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "incomplete"
    assert result["failed_lines"] == []


def test_fail_reports_broken_row_line_id():
    # Arrange — R1만 합이 34가 아님(나머지 선은 의도적으로 pass 후보)
    grid = [
        [1, 1, 1, 1],   # R1 sum != 34
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]

    # Act
    result = validate_lines(grid)

    # Assert
    assert result["status"] == "fail"
    assert "R1" in result["failed_lines"]
```

fixture 사용 시:

```python
@pytest.fixture
def complete_magic_square():
    return [
        [16, 3, 2, 13],
        [5, 10, 11, 8],
        [9, 6, 7, 12],
        [4, 15, 14, 1],
    ]


def test_pass_when_all_ten_lines_sum_to_magic_constant(complete_magic_square):
    result = validate_lines(complete_magic_square)

    assert result["status"] == "pass"
    assert result["failed_lines"] == []
```

RED 확인:

```bash
pytest tests/test_validate_lines.py -v
```

**기대:** 새 테스트는 **실패**(구현 미완·`...`·stub). 기존 통과 테스트는 깨지지 않아야 한다.

---

## 보고 형식

작업 후 아래 순서로 **한국어** 보고(코드·식별자·선 ID는 영문):

```
Phase: RED

## 목적
<이번 RED가 검증하려는 규칙·동작 한 줄>

## 변경 파일
- tests/... (추가·수정 내용 요약)

## 테스트
- `<함수명>`: Arrange / Act / Assert 요약

## pytest 결과
- 명령: pytest ...
- 결과: FAILED (expected) — `<실패 테스트명>` / `<실패 메시지 요약>`
- (선택) 기존 테스트: N passed

## 다음 단계
GREEN에서 `src/validate_lines.py`만 수정해 위 테스트를 통과시킨다.
```

---

## 금지 (재확인)

- `src/validate_lines.py` 및 `src/` 하위 **어떤 파일도** 수정·생성하지 않는다.
- assert를 약하게 바꾸거나, skip/xfail·기대값 변경으로 RED를 **피하지** 않는다.
- Solver·UI·클래스 추가 등 `.cursorrules` 범위 밖 기능을 넣지 않는다.
- git commit·push는 사용자 요청 전까지 하지 않는다.
