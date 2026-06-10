# /green-minimal — ARRR R단계 (Respond = GREEN)

**RED 1묶음**에 대해 `src/` **최소 구현**만 수행한다. 이번 묶음 Test ID를 PASS시키고, 회귀 없이 전체 pytest를 통과시킨다.

슬래시 메뉴: **`/green-minimal`**

ARRR 파이프라인: **A**(Ask) → **R**(Review) → **R**(Refine) → **R**(Release). 본 커맨드는 **R단계(Respond)** — GREEN(최소 구현) 전용. 앞단 = `/tdd-red`(assert 완성·RED 확인), 뒷단 = REFACTOR(본 커맨드 범위 밖).

**1커밋 = 1 RED 묶음.** git commit은 사용자 요청 시에만 수행한다.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (소문자 `green`):

```
Phase: green | Layer: entity | Track: Logic
```

| 필드 | 값 | 설명 |
|------|-----|------|
| `Phase` | `green` | 최소 구현만. RED/REFACTOR 혼합 금지 |
| `Layer` | `entity` \| `boundary` | Logic Track 기본 = `entity`. Track A(boundary)는 `boundary`로만 바꿔 재사용 |
| `Track` | `Logic` \| `UI` | MagicSquare_xx 세션 3 기본 = `Logic` (`validate_lines`) |

**Track A(boundary):** 본문은 그대로 두고 선언의 `Layer`만 `boundary`로 바꾼다.

---

## 입력 (SSOT)

추가 입력 없이 `/green-minimal`만 실행해도 동작한다. 아래를 **자동 조회**한다.

| 우선순위 | 소스 | 용도 |
|----------|------|------|
| 1 | 현재 채팅의 RED 묶음·Test ID·`/red-test-plan` 블록 3 | 이번 GREEN 범위 |
| 2 | `pytest` 실패 로그 | 어떤 Test ID·assert가 RED인지 |
| 3 | `tests/test_validate_lines.py` | 대상 함수·`pytest.fail` 잔존 여부 |
| 4 | `src/validate_lines.py`·`src/entity/` | 현재 stub·구현 상태 |
| 5 | `.cursorrules` | 도메인 Rule·ECB·API 계약 |

불명확해도 **질문으로 멈추지 않고** SSOT에서 최선 추론 후 `근거:` 한 줄로 명시한다.

---

## 범위

| 허용 | 금지 |
|------|------|
| `src/` 최소 구현 (`validate_lines.py`, `entity/constants.py`, entity 헬퍼) | 이번 RED 묶음 **외** Test ID를 동시에 해결하는 선행 구현 |
| (선행) 동일 묶음 `pytest.fail` → `assert` 교체 — **완화 없이** | `assert` 완화, `@pytest.mark.skip`, `xfail`, 기대값 변경 |
| `entity/constants.py`에 상수 추가·사용 (SSOT) | 하드코딩·매직 넘버 `34`/`16`/`4` 직접 산재 |
| `pytest` 실행으로 PASS·회귀 확인 | REFACTOR(구조 정리·이름 변경·범위 밖 정리) |
| git commit — **사용자 요청 시만** | Solver·UI·클래스·`.cursorrules` 범위 밖 기능 |

**한 GREEN = 한 RED 묶음.** 이번에 PASS시킬 Test ID만 구현한다.

---

## 절차 (필수 순서)

### 1. RED 재확인

이번 RED 묶음 Test ID만 대상으로 pytest를 실행해 **의도된 FAIL**인지 확인한다.

- 아직 PASS면: 구현이 이미 있거나 assert가 약함 → **멈추고** 보고.
- `pytest.fail("RED: …")`만 있고 assert가 없으면: 아래 3단계( assert 교체 )를 **먼저** 수행한 뒤 다시 FAIL 확인.

### 2. `src/` 최소 구현

- **이번 RED 묶음**을 PASS시키는 **최소** 코드만 추가·수정한다.
- 후속 Test ID·Rule을 미리 해결하지 않는다 (YAGNI).
- Control(`validate_lines`)은 Entity 규칙을 **호출·조합**만; 판정 계약 `{status, failed_lines}` 유지.

### 3. `pytest.fail` 제거 · `assert` 교체 (해당 시)

| 상황 | 조치 |
|------|------|
| `/tdd-red` 완료 — assert 있음 | tests/ **수정 금지** (`.cursorrules` GREEN = `src/`만) |
| 스켈레톤만 있고 assert 없음 | **동일 Test ID**에 대해 AAA + assert로 교체. `pytest.fail` 삭제. 완화·skip 금지 |

### 4. PASS 확인

- 이번 묶음 Test ID: **PASSED**
- `tests/test_validate_lines.py` **전체**: 회귀 없음 (전부 PASSED)
- 회귀 실패 시: **즉시** 원인 수정 후 4단계 재실행. 보고는 PASS 확정 후.

---

## 상수 SSOT — `entity/constants.py`

매직 넘버·하드코딩 **금지**. 도메인 상수는 **`src/entity/constants.py`** 단일 출처.

```python
# src/entity/constants.py (예시)
MAGIC_CONSTANT = 34
GRID_SIZE = 4
VALUE_MAX = 16
LINE_IDS = ("R1", "R2", "R3", "R4", "C1", "C2", "C3", "C4", "D1", "D2")
```

| 규칙 | 내용 |
|------|------|
| **import** | entity·Control 모듈은 `from entity.constants import …` |
| **금지** | `34`, `16`, `4` 리터럴을 로직·테스트 본문에 직접 산재 |
| **없을 때** | GREEN에서 `entity/constants.py` **생성** 후 기존 `validate_lines.py` 상수를 이전 |

---

## ECB · E001~E005 (Logic Track)

| 계층 | GREEN에서 |
|------|-----------|
| **Entity** | 격자·선·합 규칙. **boundary/control import 금지** |
| **Control** | `validate_lines(grid) -> dict` only. Entity import **허용** |
| **Boundary** | tests/fixture — GREEN에서 **기본 수정 금지** (assert 교체 예외만) |

**E001~E005 — Logic Track에서 raise/return/emit 금지:**

| 코드 | 의미 | GREEN |
|------|------|-------|
| E001 | 격자 크기 ≠ 4×4 | 구현·반환에 **넣지 않음** (Boundary 후속) |
| E002 | 셀 값 범위 위반 | **넣지 않음** |
| E003 | 1~16 중복 | **넣지 않음** |
| E004 | 반환 dict 비계약 키 | **넣지 않음** — `status`, `failed_lines`만 |
| E005 | 예외 throw·로그·부수 emit | **금지** — 항상 `dict` 반환 |

Entity 모듈은 pytest·`validate_lines`·tests를 import하지 않는다.

---

## pytest 명령 예시

**단일 테스트 (이번 RED 묶음 1개):**

```bash
pytest tests/test_validate_lines.py -v -k "test_incomplete_when_grid_has_zero"
```

**파일 전체 (회귀 확인):**

```bash
pytest tests/test_validate_lines.py -v
```

**이번 묶음 패턴 + 전체 순서 권장:**

```bash
pytest tests/test_validate_lines.py -v -k "<이번 RED 묶음 패턴>"
pytest tests/test_validate_lines.py -v
```

**기대:** 이번 묶음 Test ID **PASSED**, 기존 테스트 **회귀 없음**.

---

## 보고 형식 (필수)

작업 후 아래 순서로 **한국어** 보고 (코드·Test ID·선 ID는 영문):

```
Phase: green | Layer: entity | Track: Logic

## PASS Test ID
| Test ID | 테스트 함수 | 결과 |
|---------|-------------|------|
| T-R…    | test_…      | PASSED |

## 변경 파일 (src/ 중심)
- src/entity/constants.py : <상수 추가·SSOT 이전, 해당 시>
- src/validate_lines.py   : <최소 구현 요약>
- tests/…                 : <pytest.fail→assert만, 해당 시>

## pytest 결과
- 명령: pytest tests/test_validate_lines.py -v -k "…"
- 결과: N passed (이번 묶음)
- 명령: pytest tests/test_validate_lines.py -v
- 결과: N passed (전체, 회귀 없음)

## 회귀
- 없음 ✅ / (있었으면) <원인·즉시 수정 내용>

## git
- 커밋: 사용자 미요청 — 수행 안 함 / (요청 시) `<메시지 한 줄>`
```

보고는 **PASS Test ID · 변경 파일 · pytest 전체 PASS** 세 가지를 반드시 포함한다. 회귀 실패 시 PASS 보고 전에 **즉시 수정**한다.

---

## 완료 한 줄 (필수)

보고 **마지막**에 정확히 한 줄:

```
이번 RED 묶음 GREEN 완료 — REFACTOR는 별도 Phase
```

---

## Skill 참조 (선택)

**`magic-square-tdd` Skill**이 있으면 GREEN·상수 SSOT·ECB 규칙을 따른다.

---

## 다음 단계 (참고만 — 실행 금지)

| 커맨드 | ARRR | 역할 |
|--------|------|------|
| `/golden-master` | R (Review) | S1~S3 Golden fixture 검증 — **본 커맨드 범위 밖** |
| `/refactor-smell` | R (Refine) | Smell 탐지 — **본 커맨드 범위 밖** |
| **다음 RED 묶음** | A | `/red-test-plan` → `/red-skeleton` → `/tdd-red` → `/green-minimal` |

---

## 금지 (재확인)

- 이번 RED 묶음 **외** Test ID를 한 번에 해결하는 선행·과잉 구현.
- **REFACTOR**를 GREEN과 혼합 (이름 변경·대규모 추출·범위 밖 정리).
- `assert` 완화, `@pytest.mark.skip`, `xfail`, 기대값 변경으로 PASS **피하기**.
- 하드코딩·매직 넘버 — `entity/constants.py` SSOT 위반.
- E001~E005에 해당하는 raise·비계약 return·추가 dict 키.
- Entity가 boundary/control(pytest, `validate_lines` 역방향 등)을 import.
- Solver·UI·클래스·`.cursorrules` 범위 밖 기능.
- **git commit·push** — 사용자 요청 전까지 하지 않는다.
