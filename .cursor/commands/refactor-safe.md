# /refactor-safe — ARRR R단계 (Refine ② = Safe Refactor)

`/refactor-smell` handoff 범위만 **동작 유지** Refactor한다. **전체 pytest GREEN** 확정 후 보고한다.

슬래시 메뉴: **`/refactor-safe`**

ARRR 파이프라인: **A**(Ask) → **R**(Review) → **R**(Refine) → **R**(Release). 본 커맨드는 **Refine ②** — Safe Refactor 실행. 앞단 = `/refactor-smell`, 뒷단 = `/export-session` 또는 다음 RED 묶음.

---

## Phase 선언 (필수)

응답 **첫 줄**에 반드시 (소문자 `refactor`):

```
Phase: refactor | Mode: safe | Layer: entity | Track: Logic
```

| 필드 | 값 | 설명 |
|------|-----|------|
| `Phase` | `refactor` | Safe Refactor만. RED/GREEN 혼합 금지 |
| `Mode` | `safe` | smell handoff 범위 내 |
| `Layer` | `entity` \| `control` | `validate_lines`·entity 헬퍼 |
| `Track` | `Logic` | MagicSquare_xx 세션 3 |

---

## SSOT (단일 진실 공급원)

추가 입력 없이 `/refactor-safe`만 실행해도 동작한다.

| 우선순위 | 소스 | 용도 |
|----------|------|------|
| 1 | 현재 채팅 `/refactor-smell` 블록 3 | 이번 safe 묶음 Smell ID |
| 2 | `src/validate_lines.py`·`src/entity/` | Refactor 대상 |
| 3 | `.cursorrules`·`docs/PRD.md` | ECB·API 계약·상수 SSOT |
| 4 | `tests/test_validate_lines.py` | 회귀 범위 |

불명확해도 **질문으로 멈추지 않고** smell 표·코드에서 최선 추론 후 `근거:` 한 줄로 명시한다. smell 표 없으면 **S1~S3(매직 넘버·중복·ECB)** 만 최소 safe 적용.

---

## 범위

| 허용 | 금지 |
|------|------|
| `src/` 구조 정리 (extract·rename·상수 이동) — **동작 동일** | FR·API 계약·테스트 기대값 변경 |
| `entity/constants.py` SSOT 정리 | 새 기능·선행 Rule 구현 |
| tests: **import 경로·fixture 이름** 정리 (assert 불변) | assert 완화·skip·xfail |
| `pytest` 전체 PASS 확인 | Solver·UI·클래스 추가 |
| git commit — **사용자 요청 시만** | smell 표 **밖** 대규모 재설계 |

**한 safe = smell handoff 1묶음 (Smell 1~3개).**

---

## Safe Refactor 규칙

### 1. 동작 불변 (필수)

| 항목 | 불변 |
|------|------|
| `validate_lines(grid)` 시그니처 | 유지 |
| 반환 키 | `status`, `failed_lines` only |
| `status` 값 | `pass` \| `fail` \| `incomplete` |
| `failed_lines` 선 ID | `R1`~`R4`, `C1`~`C4`, `D1`, `D2` |
| FR-001~005·S1~S3 | 테스트로 고정 |

### 2. 허용 Refactor 유형

| 유형 | 예 |
|------|-----|
| Extract function | `_line_sum(cells) -> int` |
| Move constant | `MAGIC_CONSTANT` → `entity/constants.py` |
| Remove duplication | 10선 순회 공통 루프 |
| Rename (내부) | `_check_rows` → `_collect_row_failures` |
| Import 정리 | ECB 방향 준수 |

### 3. 금지 Refactor

- public API·테스트 assert 변경
- E001~E005 추가
- Entity → Boundary/Control 역방향 import
- “깔끔해 보여서” 범위 밖 파일 대량 이동

---

## 절차 (필수 순서)

1. **Baseline pytest** — Refactor 전 전체 PASS 확인. FAIL이면 **멈추고** 보고 (GREEN 선행).
2. **smell handoff 적용** — 블록 3 우선순위대로 **최소 diff**.
3. **회귀 pytest** — `pytest tests/ -v` 전부 PASS.
4. **FR-005 (S3) spot-check** — 동일 grid 2회 호출 동일 결과 (해당 테스트 있으면 자동, 없으면 보고에 수동 확인 한 줄).

---

## pytest 명령

```bash
pytest tests/ -v
```

**기대:** Refactor 전·후 **동일 passed 수**, 실패 0.

---

## 보고 형식 (필수)

```
Phase: refactor | Mode: safe | Layer: entity | Track: Logic

## 적용 Smell
| Smell ID | 조치 | 파일 |
|----------|------|------|
| SM-…     | …    | src/… |

## 변경 파일
- src/entity/constants.py : …
- src/validate_lines.py   : …
- tests/…                 : import만 (해당 시)

## pytest 결과
- Refactor 전: N passed
- Refactor 후: N passed (회귀 없음)

## ECB·계약
- API·FR 불변 ✅
```

보고 **마지막**에 정확히 한 줄:

```
Safe Refactor 완료 — Release는 /export-session
```

---

## 다음 단계 (참고만 — 실행 금지)

| 커맨드 | 역할 |
|--------|------|
| `/export-session` | Report + Transcript Release |
| 다음 RED | `/red-test-plan` → … |

---

## 금지 (재확인)

- 동작·계약·assert 변경으로 “Refactor” 명목 **기능 수정** 금지.
- smell handoff **외** 대규모 재작성.
- `@pytest.mark.skip`, `xfail`, assert 완화.
- Solver·UI·클래스·범위 밖 기능.
- **git commit·push** — 사용자 요청 전까지 하지 않는다.
