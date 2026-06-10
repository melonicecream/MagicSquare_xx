# MagicSquare_xx — PRD (Product Requirements Document)

| 항목 | 내용 |
|------|------|
| 프로젝트 | MagicSquare_xx |
| 세션 | 3 — 10선 판정 (`validate_lines`) |
| 작성일 | 2026-06-10 |
| SSOT | 본 문서는 ARRR·TDD·커맨드의 요구사항 기준. **충돌 시 `.cursorrules` 우선** |

---

## 1. 배경 (Mom Test)

### 1.1 페르소나

| 항목 | 내용 |
|------|------|
| **역할** | 4×4 부분 마방진을 손으로/코드로 다루는 **학습자** |
| **맥락** | 수업·프로젝트 자료(4×4 마방진, ECB 분류)를 바탕으로 빈칸 채우기·검증 수행 |
| **행동** | 격자에 숫자를 채우고, 행·열·대각선 합을 수동으로 검증 |

### 1.2 진짜 문제 (한 문장)

> **4×4 부분 마방진을 손으로 채울 때, 행·열이 맞으면 거의 끝난 것으로 보고 대각선 검증을 늦게 하다가 합이 어긋난 뒤에야 알아차려 약 20분을 다시 맞추는 데 쓴다.**

### 1.3 Mom Test 증거 3줄

1. “빈칸 2개 넣고 행·열·대각선 합 맞췄는데 **대각선 하나를 빼먹어서 20분 날렸다**”
2. “**남은 빈칸이 거의 없고, 대각선을 제외하곤 다 맞았다고 생각했어**”
3. “**숫자 합을 내서 검증을 하다보니** 알았어” → “**대각선이었어**”

### 1.4 문제 구성 요소

| Mom Test 축 | 관찰 |
|-------------|------|
| **불편** | 대각선 누락을 늦게 발견 |
| **비용** | 약 20분 재작업 |
| **판정** | “대각선 제외하고는 다 맞다”는 잘못된 완료 기준 |
| **재현** | 합을 수동으로 내는 검증 과정에서야 이상 징후 포착 |

### 1.5 주제 한 줄 (솔루션 최소화)

> **10선(4행·4열·2대각선) 합 34 판정으로 대각선 늦은 발견·재작업을 줄인다.**

*(앱·Solver·ECB “프로그램 만들기”는 주제에 넣지 않음.)*

### 1.6 R-G-I-O

| | 내용 |
|---|------|
| **Role** | 4×4 부분 마방진을 **손으로** (또는 과제용 **코드로**) 빈칸을 채우고 행·열·대각선 합을 확인하는 **학습자** |
| **Goal** | 빈칸을 채운 상태에서 **10선 합 34**를 끝까지 확인하고, “대각선 제외하고는 다 맞다”는 **잘못된 완료 판정** 없이 pass/fail을 확신한다 |
| **Input** | 4×4 정수 격자 (`0` = 빈 칸, 값 1~16 일부 기입), 목표 합 **34** |
| **Output** | **통과/실패** + 실패 시 **깨진 선 ID** (`R1`~`R4`, `C1`~`C4`, `D1`, `D2`) |

---

## 2. 범위

### 2.1 In Scope

| 항목 | 설명 |
|------|------|
| **Command** | 4×4 격자 10선 판정: `validate_lines(grid) -> dict` |
| **Test Loop** | pytest 기반 RED → GREEN → REFACTOR |
| **ECB** | Entity(격자·선·합) / Control(`validate_lines`) / Boundary(pytest·fixture) |
| **ARRR 파이프라인** | Ask(RED) → Respond(GREEN) → Review(Golden) → Refine(Refactor) → Release(Export) |
| **Golden Master** | S1~S3·FR 대표 격자 fixture 고정·Review |

### 2.2 Out of Scope

| 항목 | 이유 (Mom Test) |
|------|-----------------|
| **Solver** (빈칸 자동 완성) | 문제는 “채우기”가 아니라 **검증·판정·완료 기준** |
| **UI·마방진 앱** | “대신 풀기/보기 좋게” ≠ “대각선 늦게 알아차림” |
| **클래스 기반 Validator/Solver** | 클래스 이름·아키텍처는 표면; 이번엔 **판정 행동**만 |
| **ECB 전체 프로그램** | 솔루션·과제 형식이지 학습자 **완료 착각·20분 재작업** 증거와 직접 연결되지 않음 |
| **E001~E005 입력 검증·예외 emit** | Boundary 후속 세션 (Logic Track에서 금지) |

### 2.3 8계층 — 이번 세션

| 계층 | 이번 세션 | 내용 |
|------|-----------|------|
| **Rule** | ✅ | 4×4, `0` = 빈 칸, 1~16(중복 없음), **10선** 합 = 34 |
| **Command** | ✅ | `validate_lines(grid)` → `{status, failed_lines}` |
| **(Skill)** | △ 선택 | 실패 선만 요약 헬퍼 (Solver 아님) |
| **Test Loop** | ✅ | S1~S3 fixture + Red→Green→Refactor |
| *(Boundary, Entity 저장, Solver, Policy 등)* | ❌ | 후속 세션 |

---

## 3. 도메인 Rule

| Rule | ECB | 내용 |
|------|-----|------|
| **Rule1** | Entity | 격자 4×4, `0` = 빈 칸, 값 1~16(중복 없음) |
| **Rule2** | Entity | 10선 `R1`~`R4`, `C1`~`C4`, `D1`, `D2`. 마법상수 **34**. **전 선 검사** |
| **Rule3** | Control | `validate_lines` → `{status, failed_lines}` 계약 |

### 3.1 10선 정의

| 선 ID | 의미 | 셀 (0-indexed row, col) |
|-------|------|-------------------------|
| `R1`~`R4` | 행 1~4 | 각 행 전체 |
| `C1`~`C4` | 열 1~4 | 각 열 전체 |
| `D1` | 주대각선 | (0,0), (1,1), (2,2), (3,3) |
| `D2` | 반대각선 | (0,3), (1,2), (2,1), (3,0) |

### 3.2 판정 우선순위

1. 격자에 `0`이 **하나라도** 남아 있으면 → `incomplete` (`failed_lines == []`)
2. `0`이 없고, 채워진 선 중 합 ≠ 34인 선이 있으면 → `fail` (깨진 선 ID 목록)
3. `0`이 없고, 10선 모두 합 34이면 → `pass` (`failed_lines == []`)

---

## 4. Functional Requirements (FR)

| ID | 요약 | Given | When | Then (기대) |
|----|------|-------|------|-------------|
| **FR-001** | 빈 칸(`0`)이 하나라도 남으면 incomplete | `0` 포함 4×4 격자 | `validate_lines(grid)` | `status == "incomplete"`, `failed_lines == []` |
| **FR-002** | 채워진 선 중 합 ≠ 34이면 fail | `0` 없음, 일부 선 합 ≠ 34 | `validate_lines(grid)` | `status == "fail"`, 해당 선 ID ∈ `failed_lines` |
| **FR-003** | 10선 모두 합 34·빈 칸 없으면 pass | 완전 채워진 4×4, 10선 합 34 | `validate_lines(grid)` | `status == "pass"`, `failed_lines == []` |
| **FR-004** | 행·열만 맞고 대각선만 틀려도 fail | 행·열 OK, D1 또는 D2만 깨짐 | `validate_lines(grid)` | `status == "fail"`, `D1` 또는 `D2` ∈ `failed_lines` |
| **FR-005** | 동일 격자 재판정 시 동일 결과 | 동일 grid | `validate_lines` 2회 호출 | 동일 `status`·`failed_lines` |

---

## 5. API 계약 (Rule3 — Control)

```python
validate_lines(grid: list) -> dict
```

### 5.1 반환 형식

```python
{
    "status": "pass" | "fail" | "incomplete",
    "failed_lines": list[str]  # 깨진 선 ID. pass·incomplete 시 []
}
```

### 5.2 `failed_lines` 규칙

| status | `failed_lines` |
|--------|----------------|
| `pass` | `[]` (필수) |
| `incomplete` | `[]` (필수) |
| `fail` | 깨진 선 ID만 포함 (`R1`~`R4`, `C1`~`C4`, `D1`, `D2`) |

### 5.3 공개 상수 (Control)

| 상수 | 값 | 설명 |
|------|-----|------|
| `MAGIC_CONSTANT` | `34` | 마법상수 |
| `LINE_IDS` | `("R1",…,"D2")` | 10선 ID 튜플 |

---

## 6. 성공 기준 (워크북 S1~S3)

| ID | 기준 | 연결 증거 | FR |
|----|------|-----------|-----|
| **S1** | 행·열은 통과인데 **대각선만** 깨진 격자를 넣으면 `D1`/`D2` 실패를 **한 번의 판정**으로 반환 | ② “대각선 제외하고 다 맞다” → ③ “대각선이었어” | FR-004 |
| **S2** | 판정은 **행·열·대각선 10선 전부**를 검사한다. 대각선을 빼면 통과로 오판하지 않는다 | ① “대각선 하나를 빼먹어서 20분 날렸다” | FR-002, FR-004 |
| **S3** | 동일 격자에 대해 **재실행·재검증**해도 같은 pass/fail·같은 실패 선 목록 | ③ “숫자 합을 내서 검증” — 수동 검증 비용·재현 | FR-005 |

### 6.1 Test Loop 개념 (S1~S3 재현)

| Phase | 의도 | 기대 |
|-------|------|------|
| **RED** | 행·열만 검사하는 stub → 대각선만 틀린 격자에서 **통과 오판** | S1/S2 실패 (증거 ②·③ 재현) |
| **GREEN** | 10선 전부 검사 | `D1` 또는 `D2` 반환 (S1) |
| **REFACTOR** | 동일 입력 2회 → 동일 결과 | S3 |

---

## 7. 아키텍처 (ECB)

| 계층 | 역할 | 파일 | import 규칙 |
|------|------|------|-------------|
| **Entity** | 격자·선·합 규칙, 상수 SSOT | `src/entity/constants.py`, entity 헬퍼 | Boundary/Control **금지** |
| **Control** | `validate_lines` — Entity만 호출·조합 | `src/validate_lines.py` | Entity ✅, Boundary ❌ |
| **Boundary** | pytest, fixture, golden, 입력 격자 | `tests/`, `tests/fixtures/` | Control 호출 ✅ |

### 7.1 상수 SSOT — `entity/constants.py`

| 상수 | 값 | 용도 |
|------|-----|------|
| `MAGIC_CONSTANT` | `34` | 선 합 기준 |
| `GRID_SIZE` | `4` | 격자 크기 |
| `VALUE_MAX` | `16` | 셀 값 상한 |
| `LINE_IDS` | 10선 ID 튜플 | 선 ID 집합 |

**금지:** 매직 넘버 `34`/`16`/`4`를 로직·테스트 본문에 직접 산재.

### 7.2 E001~E005 (Logic Track — Out of Scope)

Logic Track 테스트·구현에서 **raise·emit·assert 금지**. Boundary 후속 세션에서 다룬다.

| 코드 | 의미 | Logic Track |
|------|------|-------------|
| E001 | 격자 크기 ≠ 4×4 | 금지 |
| E002 | 셀 값 범위 위반 (0·1~16 외) | 금지 |
| E003 | 1~16 중복 | 금지 |
| E004 | 반환 dict 추가 키·비계약 필드 | 금지 — `status`, `failed_lines`만 |
| E005 | 예외 throw·로그·부수 emit | 금지 — 항상 `dict` 반환 |

---

## 8. 코드 구조

```
src/
  validate_lines.py          # Control — validate_lines(grid)
  entity/
    constants.py             # Entity — 상수 SSOT (GREEN에서 생성)
tests/
  test_validate_lines.py     # Boundary — 단위 테스트
  test_golden_master.py      # Boundary — Golden Master (선택)
  conftest.py                # 공유 fixture
  fixtures/
    golden/                  # Golden Master grid + expected
pyproject.toml               # pytest pythonpath=["src"]
```

### 8.1 제약

- 함수 중심, **클래스·Solver·UI 추가 금지** (요청 전)
- Domain Mock / `validate_lines` patch **금지**
- git commit·push — **사용자 요청 전까지 금지**

---

## 9. TDD · ARRR 워크플로

### 9.1 Classic TDD Phase

| Phase | 선언 | 수정 허용 | 목적 |
|-------|------|-----------|------|
| **RED** | `Phase: RED` | `tests/` only | 실패하는 테스트 추가 |
| **GREEN** | `Phase: GREEN` | `src/` only | RED 통과 최소 구현 |
| **REFACTOR** | `Phase: REFACTOR` | 동작 불변 정리 | 코드 품질 개선 |

**금지:** assert 완화, `@pytest.mark.skip`, `xfail`, 기대값 변경으로 RED 회피.

### 9.2 ARRR 파이프라인

```
A (Ask)     → /red-test-plan → /red-skeleton → /tdd-red
R (Respond) → /green-minimal
R (Review)  → /golden-master
R (Refine)  → /refactor-smell → /refactor-safe
R (Release) → /export-session
```

| 커맨드 | ARRR | Phase 선언 | 수정 범위 |
|--------|------|------------|-----------|
| `/red-test-plan` | A | `red \| Layer: entity \| Track: Logic` | 문서만 (C2C·플랜) |
| `/red-skeleton` | A | `red \| Layer: entity \| Track: Logic` | `tests/` 스켈레톤 |
| `/tdd-red` | A | `Phase: RED` | `tests/` assert 완성 |
| `/green-minimal` | R | `green \| Layer: entity \| Track: Logic` | `src/` 최소 구현 |
| `/golden-master` | R | `review \| Layer: boundary \| Track: Logic` | `tests/fixtures/golden/` |
| `/refactor-smell` | R | `refactor \| Mode: smell` | 읽기만 |
| `/refactor-safe` | R | `refactor \| Mode: safe` | `src/` 동작 불변 정리 |
| `/export-session` | R | Release | `Report/`, `Prompting/` |

**원칙:** 한 Phase = 한 목적. 한 RED/GREEN = 한 묶음 Test ID.

### 9.3 Test ID 규칙

| 접두 | Rule | 예 |
|------|------|-----|
| `T-R1xx` | Rule1 (격자) | `T-R101` |
| `T-R2xx` | Rule2 (10선·34) | `T-R201` |
| `T-R3xx` | Rule3 (Control 계약) | `T-R301` |
| `GM-xxx` | Golden Master | `GM-001`~`GM-005` |

### 9.4 AAA 테스트 패턴

```python
# Arrange — 4×4 grid (0 = 빈 칸)
# Act
result = validate_lines(grid)
# Assert
assert result["status"] == "…"
assert result["failed_lines"] == …
```

### 9.5 pytest 명령

```bash
pytest tests/test_validate_lines.py -v
pytest tests/ -v -k "golden"
```

---

## 10. Golden Master (Review)

GREEN 완료 후 S1~S3·FR 대표 격자를 fixture로 고정하고 Review한다. **`src/` 수정 금지** — 불일치 시 보고만.

| Golden ID | FR/S | Given (요약) | expected.status | expected.failed_lines |
|-----------|------|--------------|-----------------|------------------------|
| **GM-001** | FR-001 | `0` 포함 격자 | `incomplete` | `[]` |
| **GM-002** | FR-003 | 완전 마방진 4×4 | `pass` | `[]` |
| **GM-003** | FR-004 / S1 | 행·열 OK, **D1만** 깨짐 | `fail` | `D1` (및 다른 깨진 선) |
| **GM-004** | FR-004 / S1 | 행·열 OK, **D2만** 깨짐 | `fail` | `D2` |
| **GM-005** | FR-005 / S3 | GM-002와 동일 grid 2회 호출 | 동일 결과 | (테스트에서 2회 Act) |

### 10.1 Fixture 형식

`tests/fixtures/golden/` — `{grid, expected: {status, failed_lines}}`

---

## 11. 비기능 요구사항 (NFR)

| ID | 요약 |
|----|------|
| **NFR-001** | Python ≥ 3.10, pytest ≥ 8.0 |
| **NFR-002** | ECB import 방향 준수 (Entity → Control → Boundary) |
| **NFR-003** | 상수 SSOT — `entity/constants.py` 단일 출처 |
| **NFR-004** | 최소 diff — 범위 밖 파일·기능 추가 금지 |
| **NFR-005** | AI 응답 한국어, 코드·식별자·선 ID 영문 |

---

## 12. 관련 문서

| 경로 | 설명 |
|------|------|
| `.cursorrules` | TDD·ECB·Phase 규칙 (충돌 시 우선) |
| `.cursor/skills/magic-square-tdd/SKILL.md` | TDD·ARRR·Test ID·Golden 규칙 |
| `.cursor/skills/magic-square-docs/SKILL.md` | 세션 Export·Report·Transcript 템플릿 |
| `.cursor/commands/*.md` | 슬래시 커맨드 상세 (`red-test-plan`, `tdd-red`, `green-minimal` 등) |
| `Report/01-MomTest-Report.md` | STEP 1 Mom Test 인터뷰 |
| `Report/02-MomTest-RoleSimulation-Report.md` | 역할 분리 시뮬레이션 |
| `Report/03-SESSION3-Workbook.md` | R-G-I-O·S1~S3·Test Loop |
| `prompt/` | 재사용 프롬프트 (Mom Test 인터뷰 등) |
| `Report/` | 세션 보고서·Checklist |
| `Prompting/` | 세션 Transcript |

---

## 13. 붙여넣기용 요약

```markdown
### MagicSquare_xx — 세션 3 PRD 요약

**주제:** 행·열만으로 “거의 끝” 오판 → 대각선 늦은 발견 → 20분 재작업을, 10선 판정으로 줄인다.

**API:** `validate_lines(grid) -> {status, failed_lines}`

**FR:** FR-001 incomplete | FR-002 fail+선ID | FR-003 pass | FR-004 대각선 fail | FR-005 멱등

**성공 기준:** S1 대각선만 실패 식별 | S2 10선 전부 검사 | S3 재검증 동일 결과

**범위 밖:** Solver, UI, 클래스, E001~E005, 자동 채우기

**ECB:** Entity(constants) → Control(validate_lines) → Boundary(pytest)
```
