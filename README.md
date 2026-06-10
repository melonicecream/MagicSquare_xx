# MagicSquare_xx

4×4 부분 마방진 **10선 판정** 학습 프로젝트. 행·열·대각선(총 10선)의 합이 마법상수 **34**인지 검사하고, 실패 시 **깨진 선 ID**를 반환한다.

> 상세 요구사항: [`docs/PRD.md`](docs/PRD.md)

---

## 왜 이 프로젝트인가

4×4 부분 마방진을 채울 때, 행·열만 맞으면 거의 끝난 것으로 보고 **대각선 검증을 늦게** 하다가 합이 어긋난 뒤에야 알아차리는 경우가 있다. 그때마다 약 **20분**을 다시 맞추는 데 쓴다.

이 프로젝트는 **10선(4행·4열·2대각선) 합 34 판정**으로 대각선 늦은 발견·재작업을 줄이는 것을 목표로 한다.

---

## 빠른 시작

### 요구 사항

- Python ≥ 3.10
- pytest ≥ 8.0

### 설치

```bash
pip install -e ".[dev]"
```

### 테스트 실행

```bash
pytest tests/test_validate_lines.py -v
pytest tests/ -v -k "golden"
```

---

## API

```python
from validate_lines import validate_lines

grid = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

result = validate_lines(grid)
# {"status": "pass", "failed_lines": []}
```

### 반환 형식

| 필드 | 타입 | 설명 |
|------|------|------|
| `status` | `str` | `"pass"` \| `"fail"` \| `"incomplete"` |
| `failed_lines` | `list[str]` | 깨진 선 ID. `pass`·`incomplete` 시 `[]` |

### 판정 규칙

1. 격자에 `0`(빈 칸)이 **하나라도** 있으면 → `incomplete`
2. 빈 칸 없이 채워진 선 중 합 ≠ 34인 선이 있으면 → `fail` + 해당 선 ID
3. 빈 칸 없이 10선 모두 합 34이면 → `pass`

### 10선 ID

| ID | 의미 |
|----|------|
| `R1`~`R4` | 행 1~4 |
| `C1`~`C4` | 열 1~4 |
| `D1` | 주대각선 |
| `D2` | 반대각선 |

---

## 프로젝트 구조

```
src/
  validate_lines.py          # Control — validate_lines(grid)
  entity/
    constants.py             # Entity — 상수 SSOT
tests/
  test_validate_lines.py     # 단위 테스트
  test_golden_master.py      # Golden Master (선택)
  conftest.py
  fixtures/golden/
docs/
  PRD.md                     # 요구사항 문서 (SSOT)
```

### ECB 아키텍처

| 계층 | 역할 |
|------|------|
| **Entity** | 격자·선·합 규칙, `entity/constants.py` |
| **Control** | `validate_lines` — Entity만 호출 |
| **Boundary** | pytest, fixture, golden |

---

## TDD 워크플로

```
RED → GREEN → REFACTOR
```

| Phase | 수정 범위 | 목적 |
|-------|-----------|------|
| RED | `tests/` only | 실패하는 테스트 추가 |
| GREEN | `src/` only | 최소 구현으로 테스트 통과 |
| REFACTOR | 동작 불변 | 코드 정리 |

Cursor ARRR 파이프라인:

```
/red-test-plan → /red-skeleton → /tdd-red
/green-minimal → /golden-master
/refactor-smell → /refactor-safe → /export-session
```

---

## 범위

### 포함

- `validate_lines(grid)` 10선 판정 Command
- pytest Test Loop (RED → GREEN → REFACTOR)
- Golden Master fixture (S1~S3 검증)

### 제외

- Solver (빈칸 자동 완성)
- UI·마방진 앱
- 클래스 기반 Validator/Solver
- 입력 검증 예외 (E001~E005) — 후속 세션

---

## 성공 기준 (S1~S3)

| ID | 기준 |
|----|------|
| **S1** | 행·열만 맞고 대각선만 깨진 격자 → `D1`/`D2`를 한 번의 판정으로 식별 |
| **S2** | 10선 전부 검사 — 대각선 누락으로 pass 오판 금지 |
| **S3** | 동일 격자 재판정 시 동일 `status`·`failed_lines` |

---

## 관련 문서

| 경로 | 설명 |
|------|------|
| [`docs/PRD.md`](docs/PRD.md) | 전체 요구사항 (FR, API, ECB, Golden Master) |
| [`.cursorrules`](.cursorrules) | TDD·ECB·Phase 규칙 (충돌 시 우선) |
| [`Report/03-SESSION3-Workbook.md`](Report/03-SESSION3-Workbook.md) | Mom Test·R-G-I-O·Test Loop |
| [`.cursor/commands/`](.cursor/commands/) | ARRR 슬래시 커맨드 상세 |
