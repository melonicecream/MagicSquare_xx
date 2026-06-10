# MagicSquare_xx — {제목}

| 항목 | 내용 |
|------|------|
| 문서 ID | `{NN}.{Slug}-Report` |
| 작성일 | {YYYY-MM-DD} |
| 세션 주제 | {한 줄 — 한국어} |
| Phase | {red / green / refactor / review / Mom Test / Workbook} |
| Layer | {entity / boundary — 해당 시} |
| Track | {Logic — 해당 시} |

---

## 1. 요약

{세션에서 확정·시도한 내용 3~5문장. Mom Test·TDD·ARRR 맥락 포함.}

---

## 2. 맥락

| 항목 | 내용 |
|------|------|
| 페르소나 | 4×4 부분 마방진 학습자 |
| 도메인 | 10선, 합 34, `validate_lines` |
| 선행 문서 | `docs/PRD.md`, `Report/03-SESSION3-Workbook.md` (해당 시) |

---

## 3. 세션 기록

{질문·답변, 커맨드 실행, 테스트·pytest, C2C·ECB 결정 — **사실만**}

### ARRR·TDD (해당 시)

| 단계 | 커맨드 | 산출 |
|------|--------|------|
| Ask | {/red-test-plan 등} | {Test ID, 플랜} |
| Respond | {/green-minimal} | {PASS Test ID} |
| Review | {/golden-master} | {GM ID} |
| Refine | {/refactor-smell → safe} | {Smell ID} |
| Release | {/export-session} | 본 Report |

### pytest (실행한 경우만)

| 명령 | 결과 |
|------|------|
| `{pytest …}` | {N passed / FAILED — 테스트명} |

### 원문 인용 (해당 시)

> "{인터뷰·증거·사용자 발화}"

---

## 4. 산출·결정

| 항목 | 내용 |
|------|------|
| Test ID | {T-R… / GM-…} |
| FR | {FR-001 등} |
| 변경 파일 | {tests/… / src/… — 해당 시} |
| ECB | {Entity/Control/Boundary 준수 여부} |

---

## 5. 미완·리스크

- {미완 항목 — 합성·미확정이면 **명시**}

---

## 6. 다음 단계

- {다음 커맨드 또는 RED 묶음}

---

## 7. 관련 파일

| 경로 | 설명 |
|------|------|
| `Prompting/{NN}.{Slug}-Transcript.md` | 본 세션 Transcript |
| `Report/{NN}.{Slug}-Checklist.md` | 체크리스트 (해당 시) |
| `.cursor/commands/{커맨드}.md` | 사용한 슬래시 커맨드 |
