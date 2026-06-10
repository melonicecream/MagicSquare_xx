# /refactor-smell — ARRR R단계 (Refine ① = Smell 탐지)

`src/` 구현을 **읽기만** 하고 코드 냄새(Smell)를 표로 정리한다. **코드 변경·pytest 실행으로 동작 변경 금지.**

슬래시 메뉴: **`/refactor-smell`**

ARRR 파이프라인: **A**(Ask) → **R**(Review) → **R**(Refine) → **R**(Release). 본 커맨드는 **Refine ①** — Smell **탐지·우선순위**만. 앞단 = `/golden-master` 또는 GREEN 완료, 뒷단 = `/refactor-safe`.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (소문자 `refactor`):

```
Phase: refactor | Mode: smell | Layer: entity | Track: Logic
```

| 필드 | 값 | 설명 |
|------|-----|------|
| `Phase` | `refactor` | Smell 탐지만. GREEN/RED 혼합 금지 |
| `Mode` | `smell` | 코드 수정·REFACTOR 실행 금지 |
| `Layer` | `entity` \| `control` | `validate_lines`·entity 헬퍼 중심 |
| `Track` | `Logic` | MagicSquare_xx 세션 3 |

---

## SSOT (단일 진실 공급원)

추가 입력 없이 `/refactor-smell`만 실행해도 동작한다.

| 우선순위 | 소스 | 용도 |
|----------|------|------|
| 1 | `src/validate_lines.py`·`src/entity/` | Smell 대상 |
| 2 | `tests/test_validate_lines.py` | 커버리지·중복 fixture 힌트 |
| 3 | `.cursorrules`·`docs/PRD.md` | ECB·상수 SSOT·범위 |
| 4 | 현재 채팅 GREEN·Golden 보고 | 최근 변경 파일 |

불명확해도 **질문으로 멈추지 않고** 코드·SSOT에서 최선 추론 후 `근거:` 한 줄로 명시한다.

---

## 범위

| 허용 | 금지 |
|------|------|
| `src/`·`tests/` **읽기**·분석 | **어떤 파일도** 생성·수정 |
| Smell 표·우선순위·`/refactor-safe` handoff | REFACTOR 실행·이름 변경·추출 |
| ECB·E001~E005·Domain Mock 위반 여부 점검 | pytest 실행 (선택적 — **동작 변경 검증 목적 아님**) |
| git 없음 (조회만) | Solver·UI·클래스 추가 제안 |

---

## Smell 체크리스트 (MagicSquare_xx)

아래 항목을 **코드 기준**으로 Yes/No·근거 한 줄씩 점검한다.

| # | Smell | 탐지 기준 | ECB/프로젝트 |
|---|-------|-----------|--------------|
| S1 | **매직 넘버** | `34`, `16`, `4` 리터럴이 `entity/constants.py` 밖에 산재 | 상수 SSOT 위반 |
| S2 | **중복 합계** | 행·열·대각선 합 계산이 copy-paste | DRY |
| S3 | **긴 함수** | `validate_lines` 한 함수에 10선+분기 전부 | Control 단순화 후보 |
| S4 | **경계 침범** | Entity가 pytest·Control import / Control이 Boundary import | ECB |
| S5 | **계약 확장** | 반환 dict에 `status`·`failed_lines` 외 키 | E004 |
| S6 | **선 ID 하드코딩** | `LINE_IDS` 없이 `"R1"` 문자열 산재 | Rule2 |
| S7 | **Dead code** | unreachable 분기·미사용 변수 | — |
| S8 | **테스트 결합** | Control이 tests 전용 분기 | ECB |

---

## 출력 3블록 (표 형식, 필수)

### 블록 1 — Smell 목록

| ID | Smell | 위치 (파일:개념) | 심각도 (H/M/L) | 근거 한 줄 | refactor-safe 조치 (1동사) |
|----|-------|------------------|----------------|------------|---------------------------|
| SM-01 | … | `src/…` | H | … | Extract … / Move constant … |

- 심각도: **H** = ECB·FR 위험 / **M** = 유지보수 / **L** = 스타일.
- 조치는 **한 동사구** — `/refactor-safe` handoff용.

### 블록 2 — ECB·E001~E005

| 점검 | 결과 | 근거 |
|------|------|------|
| Entity ↔ Control 분리 | ✅/❌ | … |
| E001~E005 emit | 없음 ✅ / 위반 ❌ | … |
| Domain Mock (tests) | 없음 ✅ | … |

### 블록 3 — refactor-safe 범위 제안

| 우선순위 | Smell ID | 이번 safe 묶음 포함 | 제외 사유 |
|----------|----------|---------------------|-----------|
| 1 | SM-… | ✅ | — |
| 2 | SM-… | ❌ | 범위 밖·동작 변경 위험 |

**한 safe 묶음 = Smell 1~3개, 동작 불변.**

---

## 완료 한 줄 (필수)

3블록 출력 **마지막**에 정확히 한 줄:

```
/refactor-safe 로 넘길 준비됐다
```

---

## 다음 단계 (참고만 — 실행 금지)

| 커맨드 | 역할 |
|--------|------|
| `/refactor-safe` | 블록 3 범위만 **동작 유지** Refactor + pytest GREEN |
| `/export-session` | Release |

---

## 금지 (재확인)

- `src/`·`tests/` **수정 금지** (탐지만).
- REFACTOR를 실제로 수행하지 않는다.
- Solver·UI·클래스·`.cursorrules` 범위 밖 제안 금지.
- git commit·push — 사용자 요청 전까지 하지 않는다.
