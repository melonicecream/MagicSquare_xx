# MagicSquare_xx — {제목} Checklist

| 항목 | 내용 |
|------|------|
| 문서 ID | `{NN}.{Slug}-Checklist` |
| 작성일 | {YYYY-MM-DD} |
| Report | `Report/{NN}.{Slug}-Report.md` |
| Phase | {red / green / refactor / review / Release} |

---

## ARRR 파이프라인

| # | 단계 | 커맨드 | 완료 | 비고 |
|---|------|--------|------|------|
| 1 | Ask — 플랜 | `/red-test-plan` | ☐ | C2C 4블록 |
| 2 | Ask — 스켈레톤 | `/red-skeleton` | ☐ | pytest.fail only |
| 3 | Ask — RED | `/tdd-red` | ☐ | AAA assert |
| 4 | Respond | `/green-minimal` | ☐ | src/ only |
| 5 | Review | `/golden-master` | ☐ | GM fixture |
| 6 | Refine — smell | `/refactor-smell` | ☐ | 코드 변경 없음 |
| 7 | Refine — safe | `/refactor-safe` | ☐ | pytest GREEN |
| 8 | Release | `/export-session` | ☐ | Report+Transcript 쌍 |

---

## TDD 규칙 (`.cursorrules`)

| # | 항목 | 완료 | 비고 |
|---|------|------|------|
| T1 | Phase 선언 첫 줄 | ☐ | RED/GREEN/REFACTOR 혼합 없음 |
| T2 | RED = tests/ only | ☐ | |
| T3 | GREEN = src/ only (assert 교체 예외) | ☐ | |
| T4 | skip / xfail / assert 완화 없음 | ☐ | |
| T5 | 한 RED 묶음 = 한 목적 | ☐ | Test ID: {T-R…} |

---

## 도메인·ECB

| # | 항목 | 완료 | 비고 |
|---|------|------|------|
| D1 | 4×4, `0`=빈 칸, 1~16 | ☐ | Rule1 |
| D2 | 10선 R1~R4, C1~C4, D1, D2, 합 34 | ☐ | Rule2 |
| D3 | `validate_lines` → status + failed_lines | ☐ | Rule3 |
| D4 | Domain Mock 없음 | ☐ | |
| D5 | E001~E005 Logic Track emit 없음 | ☐ | |

---

## FR·성공 기준 (해당 Test ID)

| FR/S | 기대 | 완료 | Test / GM |
|------|------|------|-----------|
| FR-001 | incomplete, failed_lines [] | ☐ | |
| FR-002 | fail + 선 ID | ☐ | |
| FR-003 | pass | ☐ | |
| FR-004 / S1 | 대각선만 fail | ☐ | |
| FR-005 / S3 | 재호출 동일 결과 | ☐ | |

---

## pytest (실행한 경우)

| 명령 | 기대 | 실제 | ☐ |
|------|------|------|---|
| `{pytest … -k …}` | FAIL (RED) | | ☐ |
| `{pytest tests/ -v}` | 전체 PASS | | ☐ |

---

## Export·문서

| # | 항목 | 완료 |
|---|------|------|
| E1 | Report `{NN}.{Slug}-Report.md` | ☐ |
| E2 | Transcript `{NN}.{Slug}-Transcript.md` | ☐ |
| E3 | 순번·Slug `01.XXX` 형식 | ☐ |
| E4 | 합성 데이터 없음 또는 명시 | ☐ |

---

## 서명 (실습용)

| 역할 | 이름 | 날짜 |
|------|------|------|
| 작성 | | |
| 리뷰 | | |
