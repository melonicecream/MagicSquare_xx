# /red-skeleton — ARRR A단계 (Ask = RED ④)

`/red-test-plan` 설계표(블록 1~4)를 입력으로 받아, **`pytest.fail` 스켈레톤만** 작성한다. assert 본문·구현은 작성하지 않는다.

슬래시 메뉴: **`/red-skeleton`**

ARRR 파이프라인: **A**(Ask) → R(Review) → R(Refine) → R(Release). 본 커맨드는 **A단계** — RED ④(스켈레톤 생성) 전용. 앞단 = `/red-test-plan`(RED ③), 뒷단 = `/tdd-red`(assert 채우기).

---

## Skill 참조 (필수)

**`magic-square-tdd` Skill이 있으면 자동 따른다.** Skill의 RED 규칙(AAA 주석·`pytest.fail` 한 줄·skip/xfail 금지·`src/` 동결)이 본 커맨드와 충돌하면 Skill을 우선한다. Skill이 없으면 본 커맨드 본문만으로 동작한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (소문자 `red`):

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 설명 |
|------|-----|------|
| `Phase` | `red` | 스켈레톤만. GREEN/REFACTOR 혼합 금지 |
| `Layer` | `entity` | Logic Track 기본. Track A는 `boundary` |
| `Track` | `Logic` | MagicSquare_xx 세션 3 기본 (`validate_lines`) |

---

## 입력 (SSOT)

추가 입력 없이 `/red-skeleton`만 실행해도 동작한다. 아래를 **자동 조회**한다.

| 우선순위 | 소스 | 용도 |
|----------|------|------|
| 1 | 현재 채팅의 `/red-test-plan` 출력 (블록 1~4) | Test ID·Given/When/Then·함수명 |
| 2 | `tests/test_validate_lines.py` | 기존 테스트·중복 함수명 회피 |
| 3 | `.cursorrules` | 도메인 Rule·ECB·API 계약 |
| 4 | `tests/conftest.py` | 기존 fixture (재사용·중복 회피) |

설계표가 없으면 `/red-test-plan` 선행을 권하되, 채팅 맥락에서 Test ID·동작이 명확하면 멈추지 말고 최선 추론 후 `근거:` 한 줄로 명시한다.

---

## 범위

| 허용 | 금지 |
|------|------|
| `tests/test_validate_lines.py`에 **테스트 함수 스켈레톤** 추가 | `src/` **어떤 파일도** 생성·수정 |
| `tests/conftest.py`에 fixture(예: `grid_g1`) 추가 | `validate_lines` 구현·stub 변경 |
| AAA 주석 + `pytest.fail("RED: …")` 한 줄 본문 | `assert` 본문 작성 (그건 `/tdd-red` 단계) |
| `entity/constants.py`에서 상수 import (픽스처 데이터용) | `@pytest.mark.skip`, `xfail`, 통과하는 더미 본문 |
| 완료 후 `pytest` 실행해 FAIL 확인 | GREEN/REFACTOR 수행·구현 제안 |

**한 RED = 한 목적.** 이번 묶음의 Test ID만 스켈레톤화한다.

---

## 스켈레톤 규칙

각 테스트 함수는 아래 **3가지만** 담는다. 그 외 코드 금지.

1. **AAA 주석** — `# Arrange (Given)`, `# Act (When)`, `# Assert (Then)` 세 줄 주석으로 의도를 드러낸다.
2. **Arrange** — fixture 인자 또는 인라인 격자. 상수 `34`/`16`/`4`가 픽스처 데이터에 필요하면 **`entity/constants.py`에서 import**(매직 넘버 직접 작성 금지).
3. **Then 본문** — 정확히 `pytest.fail("RED: {Test ID} — <검증할 동작 한 줄>")` **한 줄만**.

`assert` 문, 실제 호출 결과 검증, 통과 더미(`pass`·`assert True`)는 넣지 않는다. Act 호출(`validate_lines(...)`)은 주석 또는 미사용 변수로 의도만 남기고, 검증은 `pytest.fail`로 대체한다.

### 상수 import

```python
from entity.constants import MAGIC_CONSTANT, GRID_SIZE, VALUE_MAX  # 34, 4, 16
```

- 픽스처 데이터(격자 크기·값 범위 표현)에만 사용. 매직 넘버 `34`/`16`/`4`를 테스트 본문에 직접 쓰지 않는다.
- `entity/constants.py`가 아직 없으면 그 사실을 보고에 적고, import 라인은 그대로 두어 `/red-skeleton` 단계에서 **ImportError로 RED**가 나도록 한다.

### conftest fixture

`tests/conftest.py`에 공유 fixture를 둔다. 예: `grid_g1` — **빈 칸 `0` 두 개**를 가진 4×4 격자, **row-major**(행 우선) 순서.

```python
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
```

---

## 템플릿 예시

설계표 Test ID 1개당 함수 1개. 함수명 = `test_<동작>_<조건>`(설계표 Test ID와 1:1).

```python
import pytest

from validate_lines import validate_lines


def test_d_loc_01_blank_coords_row_major(grid_g1):
    # Arrange (Given): grid_g1 — 빈 칸 0이 2개, row-major 격자
    grid = grid_g1

    # Act (When): validate_lines 호출 (결과 검증은 /tdd-red에서)
    _ = validate_lines(grid)

    # Assert (Then): 아직 미작성 — RED 고정
    pytest.fail("RED: T-D-LOC-01 — 빈 칸 좌표를 row-major 순서로 보고해야 한다")
```

- 함수당 `pytest.fail` 한 줄. 메시지에 **Test ID**와 **검증할 동작**을 영문/한국어로 명시.
- fixture가 필요 없으면 인자 없이 인라인 격자 사용.

---

## 완료 후 pytest 실행 + 보고 (필수)

스켈레톤 작성 후 아래를 실행하고 결과를 보고한다.

```bash
pytest tests/test_validate_lines.py -v -k "<이번 묶음 패턴>"
```

**보고 형식** (한국어 설명, 코드·Test ID·선 ID는 영문):

```
Phase: red | Layer: entity | Track: Logic

## 추가한 스켈레톤
| Test ID | 테스트 함수 | FAIL 메시지 (한 줄) |
|---------|-------------|---------------------|
| T-…     | test_…      | RED: T-… — …        |

## 변경 파일 (tests/만)
- tests/test_validate_lines.py : <함수 N개 추가>
- tests/conftest.py            : <fixture 추가, 해당 시>

## pytest 결과
- 명령: pytest tests/test_validate_lines.py -v -k "…"
- 결과: FAILED (expected) — 각 스켈레톤이 Failed: RED: … 로 실패
- (해당 시) entity/constants.py 부재 → ImportError 로 RED
```

보고는 **Test ID · FAIL 한 줄 · 변경 파일(tests/만)** 세 가지를 반드시 포함한다.

---

## SSOT (추가)

| 소스 | 용도 |
|------|------|
| `docs/PRD.md` | FR·S1~S3 Then |
| `.cursor/commands/export-session.md` | Release 형식 (참고) |

---

## 다음 단계 (참고만 — 실행 금지)

| 커맨드 | ARRR | 역할 |
|--------|------|------|
| `/tdd-red` | A | `pytest.fail` → `assert`로 **의미 있는 RED** 완성 |
| `/green-minimal` | R | `src/` 최소 구현 — **본 커맨드 범위 밖** |

---

## 금지 (재확인)

- `src/` 하위 **어떤 파일도** 생성·수정하지 않는다.
- `assert` 본문·통과 더미·실제 결과 검증을 넣지 않는다 (그건 `/tdd-red`).
- `@pytest.mark.skip`, `xfail`로 RED를 피하지 않는다.
- 상수 `34`/`16`/`4`를 본문에 직접 쓰지 않고 `entity/constants.py`에서 import한다.
- Solver·UI·클래스·`.cursorrules` 범위 밖 기능을 넣지 않는다.
- git commit·push는 사용자 요청 전까지 하지 않는다.
