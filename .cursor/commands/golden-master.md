# /golden-master — ARRR R단계 (Review = Golden Master)

**GREEN 완료 후** S1~S3·FR 대표 격자에 대한 **기대 결과(Golden Master)** 를 fixture로 고정하고, 현재 구현이 Golden과 일치하는지 **Review**한다.

슬래시 메뉴: **`/golden-master`**

ARRR 파이프라인: **A**(Ask) → **R**(Review) → **R**(Refine) → **R**(Release). 본 커맨드는 **R단계(Review)** — Golden Master 검증·fixture 고정. 앞단 = `/green-minimal`, 뒷단 = `/refactor-smell` 또는 다음 RED 묶음.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (소문자 `review`):

```
Phase: review | Layer: boundary | Track: Logic
```

| 필드 | 값 | 설명 |
|------|-----|------|
| `Phase` | `review` | Golden Master Review. RED/GREEN/REFACTOR 혼합 금지 |
| `Layer` | `boundary` | golden fixture·pytest 경계 (Entity 로직 변경 아님) |
| `Track` | `Logic` | `validate_lines` |

---

## SSOT (단일 진실 공급원)

추가 입력 없이 `/golden-master`만 실행해도 동작한다.

| 우선순위 | 소스 | 용도 |
|----------|------|------|
| 1 | 현재 채팅·`/green-minimal` 보고 | PASS Test ID·pytest 결과 |
| 2 | `docs/PRD.md` FR-001~005, S1~S3 | Golden 케이스 선정 |
| 3 | `tests/test_validate_lines.py` | 기존 격자·중복 회피 |
| 4 | `.cursorrules` | API 계약·선 ID |

불명확해도 **질문으로 멈추지 않고** SSOT에서 최선 추론 후 `근거:` 한 줄로 명시한다.

---

## 범위

| 허용 | 금지 |
|------|------|
| `tests/fixtures/golden/` 에 grid + expected dict 추가 | `src/` **어떤 파일도** 수정 (불일치 시 **보고만**) |
| `tests/test_golden_master.py` 또는 기존 파일에 **parametrize Golden 테스트** 추가 | GREEN 선행 구현·REFACTOR |
| `pytest` 실행으로 Golden PASS 확인 | Domain Mock·`validate_lines` patch |
| golden 데이터: `{ "grid", "expected": {"status", "failed_lines"} }` | assert 완화·skip·xfail |

**한 Review = Golden 세트 1묶음** (S1~S3 대표 또는 이번 RED 묶음 FR 1개).

---

## Golden Master 규칙

### 1. Golden 케이스 선정 (PRD 기준)

| Golden ID | FR/S | Given (요약) | expected.status | expected.failed_lines |
|-----------|------|--------------|-----------------|------------------------|
| **GM-001** | FR-001 | `0` 포함 격자 | `incomplete` | `[]` |
| **GM-002** | FR-003 | 완전 마방진 4×4 | `pass` | `[]` |
| **GM-003** | FR-004 / S1 | 행·열 OK, **D1만** 깨짐 | `fail` | `D1` (및 다른 깨진 선 있으면 포함) |
| **GM-004** | FR-004 / S1 | 행·열 OK, **D2만** 깨짐 | `fail` | `D2` |
| **GM-005** | FR-005 / S3 | GM-002와 동일 grid 2회 호출 | 동일 결과 | (테스트에서 2회 Act) |

- 선 ID: `R1`~`R4`, `C1`~`C4`, `D1`, `D2` only.
- pass·incomplete → `failed_lines == []` 필수.

### 2. Fixture 형식

`tests/fixtures/golden/` — Python 모듈 또는 JSON. 예:

```python
# tests/fixtures/golden/complete_pass.py
GRID = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]
EXPECTED = {"status": "pass", "failed_lines": []}
```

### 3. 테스트 패턴

```python
import pytest

from validate_lines import validate_lines


@pytest.mark.parametrize(
    "grid,expected",
    [
        (GM_INCOMPLETE_GRID, {"status": "incomplete", "failed_lines": []}),
        (GM_PASS_GRID, {"status": "pass", "failed_lines": []}),
    ],
    ids=["GM-001", "GM-002"],
)
def test_golden_master_matches_contract(grid, expected):
    result = validate_lines(grid)
    assert result["status"] == expected["status"]
    assert result["failed_lines"] == expected["failed_lines"]
```

- Golden 테스트는 **항상 PASS**여야 한다 (구현이 Golden과 일치).
- 아직 GREEN 미완이면 FAIL → **보고만** 하고 `src/` 수정하지 않는다.

---

## 절차 (필수 순서)

1. **SSOT에서 Golden ID 선정** — 이번 Review 묶음 (기본: GM-001~005 중 미커버).
2. **fixture 작성** — grid·expected를 PRD Then과 일치시킨다.
3. **pytest 실행** — `pytest tests/ -v -k "golden"` (또는 해당 파일).
4. **결과 판정** — 전부 PASSED ✅ / FAIL → 불일치 Golden ID·diff 보고, **`src/` 수정 금지**.

---

## 보고 형식 (필수)

```
Phase: review | Layer: boundary | Track: Logic

## Golden Master 세트
| Golden ID | FR/S | status | failed_lines | fixture |
|-----------|------|--------|--------------|---------|
| GM-…      | FR-… | …      | …            | tests/fixtures/golden/… |

## 변경 파일 (tests/만)
- tests/fixtures/golden/… : …
- tests/test_…py          : parametrize N건

## pytest 결과
- 명령: pytest … -k golden
- 결과: N passed / (FAIL 시) GM-xxx 불일치 요약

## Review 판정
- Golden 일치 ✅ / 불일치 — GREEN 재확인 필요 (src/ 수정은 /green-minimal)
```

보고 **마지막**에 정확히 한 줄:

```
Golden Master Review 완료 — REFACTOR는 /refactor-smell
```

---

## 다음 단계 (참고만 — 실행 금지)

| 커맨드 | 역할 |
|--------|------|
| `/refactor-smell` | 구현 냄새 탐지 (코드 변경 없음) |
| `/refactor-safe` | pytest GREEN 유지 Refactor |
| `/export-session` | Release — Report + Transcript |

---

## 금지 (재확인)

- `src/` 하위 **어떤 파일도** 생성·수정하지 않는다 (Review만).
- Golden expected를 구현에 **맞춰** 완화하지 않는다 — PRD·`.cursorrules` 기준.
- `@pytest.mark.skip`, `xfail`, assert 약화 금지.
- Domain Mock·`validate_lines` patch 금지.
- Solver·UI·클래스·범위 밖 기능 금지.
- git commit·push — 사용자 요청 전까지 하지 않는다.
