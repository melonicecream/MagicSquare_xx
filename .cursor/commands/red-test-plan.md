# /red-test-plan — ARRR A단계 (Ask = RED ③)

**C2C 설계표**와 **테스트 플랜**만 작성한다. `tests/`·`src/` 파일은 생성·수정하지 않는다.

슬래시 메뉴: **`/red-test-plan`**

ARRR 파이프라인: **A**(Ask) → R(Review) → R(Refine) → R(Release). 본 커맨드는 **A단계** — RED ③(설계·플랜) 전용.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (소문자 `red`):

```
Phase: red | Layer: entity | Track: Logic
```

| 필드 | 값 | 설명 |
|------|-----|------|
| `Phase` | `red` | 설계·플랜만. GREEN/REFACTOR 혼합 금지 |
| `Layer` | `entity` \| `boundary` | Logic Track 기본 = `entity`. Track A(boundary)는 `boundary`로만 바꿔 재사용 |
| `Track` | `Logic` \| `UI` | MagicSquare_xx 세션 3 기본 = `Logic` (`validate_lines`) |

**Track A(boundary):** 본 커맨드 본문은 그대로 두고, 선언의 `Layer`만 `boundary`로 바꾸면 Track A에도 재사용 가능하다. (`Track: UI`는 UI 세션에서만.)

---

## SSOT (단일 진실 공급원)

추가 입력 없이 `/red-test-plan`만 실행해도 동작한다. 아래를 **자동 조회·추론**한다.

| 우선순위 | 소스 | 용도 |
|----------|------|------|
| 1 | 현재 채팅·@참조·첨부 | 세션 주제, 이미 합의된 Test ID·FR |
| 2 | `docs/PRD.md` | FR 인용, 범위 밖 기능 확인 |
| 3 | `.cursorrules` | 도메인 Rule, ECB, API 계약 |
| 4 | `Report/03-SESSION3-Workbook.md` | S1~S3·Mom Test 맥락 (PRD 부재 시 보조) |
| 5 | `.cursor/commands/export-session.md` | Release·문서 형식 (참고) |

### 자동 추출 규칙

| 항목 | 추출 방법 |
|------|-----------|
| **세션 주제** | 대화·PRD 한 줄 요약. 없으면 워크북 주제: "10선 합 34 판정으로 대각선 늦은 발견·재작업 방지" |
| **Test ID** | `T-{Rule}{seq}` — Rule1→`T-R1xx`, Rule2→`T-R2xx`, Rule3→`T-R3xx` (예: `T-R101`). 채팅에 기존 ID가 있으면 **이어서 번호** |
| **대상 함수** | Logic·entity → `validate_lines`. boundary → fixture·입력 격자·pytest 경계 |
| **RED 묶음** | 한 묶음 = Rule 1개 또는 동일 FR 1개. 한 목적만 |

불명확해도 **질문으로 멈추지 않고** SSOT에서 최선 추론 후 표에 `근거:` 한 줄로 명시한다.

---

## 범위

| 허용 | 금지 |
|------|------|
| C2C 표·Track B 표·테스트 플랜·ECB 점검 **문서 출력** | `src/`·`tests/` **어떤 파일도** 생성·수정 |
| SSOT 읽기·채팅 맥락 분석 | GREEN / REFACTOR 단계 수행·언급을 실행으로 진행 |
| `/red-skeleton` handoff용 플랜 | `@pytest.mark.skip`, `xfail`, assert 완화·기대값 변경으로 RED 회피 설계 |
| git 없음 (조회만) | Solver·UI·클래스·Domain Mock 설계 (Logic Track) |

**한 RED = 한 목적.** 플랜에 여러 Test ID가 있어도 **이번 RED 묶음**은 검증 규칙 하나에 묶는다.

---

## 출력 4블록 (표 형식, 필수)

응답 본문은 아래 **4개 블록을 순서대로** 표로 작성한다. 설명은 한국어, 코드·식별자·선 ID·Test ID는 영문.

---

### 블록 1 — C2C (Rule1~3)

PRD **FR** 인용 → **To-Do 1개** → **Test ID** + Given/When/Then.

**C2C Rule 매핑 (MagicSquare_xx Logic·entity 기본):**

| Rule | ECB | 내용 |
|------|-----|------|
| **Rule1** | Entity | 격자: 4×4, `0`=빈 칸, 값 1~16(중복 없음) |
| **Rule2** | Entity | 10선(R1~R4, C1~C4, D1, D2), 마법상수 **34**, **전 선 검사** |
| **Rule3** | Control | `validate_lines(grid)` → `status` + `failed_lines` 계약 (`incomplete`/`fail`/`pass`) |

**표 템플릿:**

| Rule | PRD FR (인용) | To-Do (1개) | Test ID | Given | When | Then |
|------|---------------|-------------|---------|-------|------|------|
| Rule1 | `FR-…` "…" | … | T-R1xx | … | `validate_lines(grid)` 호출 | … |
| Rule2 | `FR-…` "…" | … | T-R2xx | … | … | … |
| Rule3 | `FR-…` "…" | … | T-R3xx | … | … | … |

- PRD에 `FR-xxx`가 없으면 `.cursorrules`·워크북 S1~S3에서 **동등 FR 문장**을 인용하고 `근거: …` 표기.
- **To-Do**는 Rule당 정확히 **1개** 동사구 (예: "대각선만 깨진 격자에서 D1을 failed_lines에 보고한다").
- Given: 4×4 격자 상태(인라인 또는 fixture명). When: 항상 Act 1회. Then: `status`·`failed_lines` 기대.

**PRD FR 참고 (docs/PRD.md 또는 .cursorrules 대응):**

| FR | 요약 |
|----|------|
| FR-001 | `0`이 남으면 `status == "incomplete"`, `failed_lines == []` |
| FR-002 | 채워진 선 중 합 ≠ 34이면 `status == "fail"`, 해당 선 ID ∈ `failed_lines` |
| FR-003 | 10선 모두 합 34·빈 칸 없으면 `status == "pass"`, `failed_lines == []` |
| FR-004 | 행·열만 맞고 대각선만 틀린 경우에도 fail (10선 전부 검사, S1/S2) |

---

### 블록 2 — Track B 표 (Logic·entity)

| Test ID | 대상 함수 | Given → Then | Invariant | Expected RED Failure |
|---------|-----------|--------------|-----------|----------------------|
| T-R1xx | `validate_lines` | … | … | … |
| T-R2xx | `validate_lines` | … | … | … |
| T-R3xx | `validate_lines` | … | … | … |

**열 정의:**

| 열 | 내용 |
|----|------|
| **Test ID** | 블록 1과 동일 ID |
| **대상 함수** | Logic Track → `validate_lines` (import: `from validate_lines import validate_lines`) |
| **Given → Then** | 격자 조건 → `status`·`failed_lines` (선 ID: R1~R4, C1~C4, D1, D2) |
| **Invariant** | 묶음 전체에서 깨지면 안 되는 것 (예: `failed_lines`는 `LINE_IDS` 부분집합, pass/incomplete 시 `[]`) |
| **Expected RED Failure** | 현재 stub(`...`)·미구현 시 pytest **예상 실패 형태** (예: `AssertionError: …`, `NotImplemented`/`Ellipsis` 관련) |

**Track A(boundary):** `Layer: boundary`일 때 대상 함수 열을 **fixture 함수명·conftest 헬퍼·입력 격자 팩토리**로 바꾼다. Given→Then은 Boundary 형식(격자 리스트 구조) 준수 여부 중심.

---

### 블록 3 — 테스트 플랜

| 항목 | 값 |
|------|-----|
| **테스트 파일** | `tests/test_validate_lines.py` |
| **테스트 함수명** | `test_<동작>_<조건>` (블록 2 Test ID와 1:1 매핑 권장) |
| **fixture 파일** | `tests/fixtures/` (필요 시; 없으면 인라인 격자) |
| **conftest** | `tests/conftest.py` — 공유 fixture만 (예: `complete_magic_square`, `diag_only_fail_grid`) |
| **import** | `from validate_lines import MAGIC_CONSTANT, LINE_IDS, validate_lines` |
| **pytest 명령** | `pytest tests/test_validate_lines.py -v -k "<이번 RED 묶음 패턴>"` |
| **RED 묶음 범위** | 이번에 추가할 Test ID 목록 + **제외**할 기존/후속 ID |
| **AAA** | Arrange(격자) → Act(`validate_lines`) → Assert(`status`, `failed_lines`) |

**예시 (이번 RED 묶음 = Rule2·대각선만 실패):**

```text
pytest tests/test_validate_lines.py -v -k "diag_only_fail"
RED 묶음: T-R201 (포함), T-R101·T-R301 (후속 /red-test-plan)
```

---

### 블록 4 — ECB·Mock 점검

| 점검 항목 | Logic Track (entity) | boundary Layer |
|-----------|----------------------|----------------|
| **ECB 준수** | Boundary=pytest·fixture·격자 입력 / Control=`validate_lines` / Entity=선·합 규칙만 | Boundary 계약(격자 형식·fixture)만 검증, Entity 로직 단정 금지 |
| **Domain Mock** | **금지** — `validate_lines`·격자 합·선 ID를 mock/patch하지 않음 | UI·외부 IO mock만 해당 시 허용 (본 프로젝트 세션 3: 해당 없음) |
| **E001~E005 emit** | 테스트 Then·Assert에 **포함 금지** | boundary 전용 FR일 때만 별도 플랜 |

**E001~E005 (Logic Track에서 emit·assert 금지):**

| 코드 | 의미 | Logic Track |
|------|------|-------------|
| E001 | 격자 크기 ≠ 4×4 | 금지 (Boundary 후속) |
| E002 | 셀 값 범위 위반 (0·1~16 외) | 금지 |
| E003 | 1~16 중복 | 금지 |
| E004 | 반환 dict 추가 키·비계약 필드 | 금지 |
| E005 | 예외 throw·로그·부수 emit | 금지 — `dict` 반환만 |

**점검 결과 표:**

| Test ID | Domain Mock | E001~E005 | ECB 위반 여부 | 조치 |
|---------|-------------|-----------|---------------|------|
| T-R… | 없음 ✅ | emit 없음 ✅ | 없음 ✅ | — |

---

## 완료 한 줄 (필수)

4블록 출력 **마지막**에 정확히 한 줄:

```
/red-skeleton 으로 넘길 준비됐다
```

---

## Skill 참조 (선택)

**`magic-square-tdd` Skill**이 있으면 Test ID·ECB·Phase 규칙을 따른다.

---

## 다음 단계 (참고만 — 실행 금지)

| 커맨드 | ARRR | 역할 |
|--------|------|------|
| `/red-skeleton` | A | 블록 3 플랜대로 `tests/` 스켈레톤·fixture **생성** |
| `/tdd-red` | A | 스켈레톤에 Assert 채워 **실패하는 테스트** 완성 |
| `/green-minimal` | R | `src/` 최소 구현 — **본 커맨드 범위 밖** |

---

## 금지 (재확인)

- `src/`·`tests/` 하위 **어떤 파일도** 생성·수정하지 않는다.
- GREEN / REFACTOR를 수행하거나 구현 코드를 제안하지 않는다 (플랜 수준 Then만).
- `@pytest.mark.skip`, `xfail`, assert 완화·기대값 변경으로 RED를 **피하는** 플랜을 세우지 않는다.
- Logic Track에서 Domain Mock·`validate_lines` patch·내부 합계 stub을 넣지 않는다.
- E001~E005를 Logic Track Test ID의 Then에 넣지 않는다.
- Solver·UI·클래스·`.cursorrules` 범위 밖 기능을 플랜에 넣지 않는다.
- git commit·push는 사용자 요청 전까지 하지 않는다.
