---
name: magic-square-tdd
description: >-
  MagicSquare_xx 4×4 10-line validate_lines TDD loop (RED/GREEN/REFACTOR) and
  ARRR commands. Use when running /red-test-plan, /red-skeleton, /tdd-red,
  /green-minimal, /golden-master, /refactor-smell, /refactor-safe, or when
  writing tests or src for validate_lines in this project.
---

# MagicSquare_xx — TDD Skill

4×4 부분 마방진 **10선 판정** (`validate_lines`) TDD·ARRR 공통 규칙. SSOT: `.cursorrules`, `docs/PRD.md`, `.cursor/commands/*.md`.

---

## 도메인 (요약)

| 항목 | 값 |
|------|-----|
| 격자 | 4×4, `0` = 빈 칸, 1~16 중복 없음 |
| 마법상수 | **34** |
| 10선 ID | `R1`~`R4`, `C1`~`C4`, `D1`, `D2` |
| API | `validate_lines(grid) -> {"status", "failed_lines"}` |
| status | `pass` \| `fail` \| `incomplete` |
| incomplete | `0` 남음 → `failed_lines == []` |
| fail | 채워진 선 합 ≠ 34 → 해당 선 ID in `failed_lines` |

---

## ECB

| 계층 | 역할 | import |
|------|------|--------|
| **Entity** | 격자·선·합 규칙, `entity/constants.py` | Boundary/Control **금지** |
| **Control** | `validate_lines` — Entity만 호출 | Entity ✅, Boundary ❌ |
| **Boundary** | pytest, fixture, golden | Control 호출 ✅ |

---

## Phase 규칙

응답 **첫 줄** Phase 선언. **한 Phase = 한 목적.**

| Phase | 선언 예 | 수정 허용 |
|-------|---------|-----------|
| RED (classic) | `Phase: RED` | `tests/` only |
| RED (ARRR) | `Phase: red \| Layer: entity \| Track: Logic` | 커맨드별 (플랜=없음, skeleton=tests/) |
| GREEN | `Phase: GREEN` 또는 `Phase: green \| …` | `src/` (classic GREEN = src only) |
| REFACTOR | `Phase: REFACTOR` 또는 `Phase: refactor \| Mode: …` | 동작 불변 정리 |
| Review | `Phase: review \| Layer: boundary \| Track: Logic` | golden tests/fixtures only |

**금지:** assert 완화, `@pytest.mark.skip`, `xfail`, 기대값 변경으로 RED 회피.

---

## ARRR 파이프라인

```
A (Ask)     → /red-test-plan → /red-skeleton → /tdd-red
R (Respond) → /green-minimal
R (Review)  → /golden-master
R (Refine)  → /refactor-smell → /refactor-safe
R (Release) → /export-session
```

각 슬래시 커맨드는 **추가 입력 없이** SSOT·채팅만으로 동작. 질문으로 멈추지 않는다.

---

## RED — AAA

```python
# Arrange — 4×4 grid
# Act
result = validate_lines(grid)
# Assert
assert result["status"] == "…"
assert result["failed_lines"] == …  # or "R1" in …
```

### 스켈레톤 (`/red-skeleton`)

- AAA 주석 3줄 + `pytest.fail("RED: {Test ID} — …")` **한 줄만**
- assert 본문은 `/tdd-red`에서 작성
- 상수: `from entity.constants import MAGIC_CONSTANT, GRID_SIZE, VALUE_MAX` (매직 넘버 `34`/`16`/`4` 직접 금지)

### Test ID

- `T-R1xx` Rule1 (격자)
- `T-R2xx` Rule2 (10선·34)
- `T-R3xx` Rule3 (Control 계약)

---

## GREEN — 최소 구현

- **한 GREEN = 한 RED 묶음**
- YAGNI: 후속 Test ID 선행 구현 금지
- 상수 SSOT: `src/entity/constants.py`
- E001~E005 Logic Track: raise·비계약 dict 키 **금지**

---

## Golden Master (`/golden-master`)

- `tests/fixtures/golden/`: `{grid, expected}`
- GM-001 incomplete, GM-002 pass, GM-003/004 diag fail, GM-005 idempotent (S3)
- Review: **`src/` 수정 금지** — 불일치 시 보고만

---

## Refactor

| Mode | 동작 |
|------|------|
| `smell` | 읽기만, Smell 표 출력 |
| `safe` | handoff 범위, pytest 전체 GREEN |

---

## pytest

```bash
pytest tests/test_validate_lines.py -v
pytest tests/ -v -k "golden"
```

- RED: 새 테스트 **FAIL** 기대
- GREEN/REFACTOR: **전체 PASS**

---

## 금지 (항상)

- Solver·UI·클래스 (요청 전)
- Domain Mock / `validate_lines` patch
- git commit·push (사용자 요청 전)
- 범위 밖 파일·기능

---

## 커맨드 매핑

| 슬래시 | Skill 섹션 |
|--------|------------|
| `/red-test-plan` | Test ID, C2C, ECB 점검 |
| `/red-skeleton` | 스켈레톤 규칙 |
| `/tdd-red` | AAA, RED |
| `/green-minimal` | GREEN, 상수 SSOT |
| `/golden-master` | Golden Master |
| `/refactor-smell` | smell 체크리스트 |
| `/refactor-safe` | safe 규칙 |
