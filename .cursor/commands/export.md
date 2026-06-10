# /export — Report + Transcript

현재 Cursor 세션을 **보고서**와 **대화 Transcript** 두 파일로보낸다.

슬래시 메뉴: **`/export`**

---

## 실행 조건

| 허용 | 금지 |
|------|------|
| `Report/` 보고서 생성·갱신 | `src/`·`tests/` 수정 |
| `Prompting/` Transcript 생성·갱신 | git commit·push (사용자 요청 전) |
| 폴더 없으면 생성 | 범위 밖 기능·문서 추가 |

**한 실행 = 한 세션 쌍** (Report 1개 + Transcript 1개).

---

## 파일명 규칙 (`01.XXX` 형식)

### 패턴

| 산출물 | 경로 | 파일명 |
|--------|------|--------|
| 보고서 | `Report/` | `{NN}.{Slug}-Report.md` |
| Transcript | `Prompting/` | `{NN}.{Slug}-Transcript.md` |

- `{NN}`: **2자리 순번** (`01`, `02`, …)
- `{Slug}`: **PascalCase·하이픈** 영문 식별자 (예: `TDD-RED`, `MomTest-Interview`, `Session3-Workbook`)
- **점(`.`)** 으로 순번과 Slug 구분 — `01-MomTest` ❌ / `01.MomTest` ✅

### 순번 결정

1. `Report/`·`Prompting/` 전체 파일명에서 `^(\d{2})[.\-]` 패턴으로 순번 추출
2. **최댓값 + 1** → 새 `{NN}` (없으면 `01`)
3. Report·Transcript는 **같은 `{NN}`·같은 `{Slug}`** 사용

### Slug 결정

1. 세션 주제를 대화에서 추론 (Mom Test, TDD RED, 세션 3 워크북 등)
2. 불명확하면 사용자에게 Slug 한 줄만 확인
3. **덮어쓰기** 요청 시: 기존 `{NN}.{Slug}-*` 경로 유지, 내용만 갱신

---

## 1단계 — 세션 분석

현재 대화(및 첨부·@참조 파일)에서 다음을 수집한다.

| 항목 | 수집 내용 |
|------|-----------|
| 주제 | 이번 세션 한 줄 (한국어) |
| Phase | TDD RED/GREEN/REFACTOR, Mom Test, 워크북 등 |
| 핵심 결정·산출 | 확정된 규칙, 테스트, 문제 정의, 증거 |
| 미완·리스크 | 미응답, 합성 데이터, 다음 단계 |
| 도메인 | 4×4, 10선, 합 34, `validate_lines` 등 해당 시 |

`agent-transcripts/` JSONL이 있으면 보조 참고 가능. **본문은 현재 대화 기준**으로 작성.

---

## 2단계 — Report 작성

`Report/{NN}.{Slug}-Report.md` 생성.

### 보고서 템플릿

```markdown
# MagicSquare_xx — {제목}

| 항목 | 내용 |
|------|------|
| 문서 ID | `{NN}.{Slug}-Report` |
| 작성일 | YYYY-MM-DD |
| 세션 주제 | {한 줄} |
| Phase | {해당 시: RED / GREEN / REFACTOR / Mom Test / Workbook 등} |

---

## 1. 요약

{세션에서 확정·시도한 내용 3~5문장}

---

## 2. 맥락

{페르소나, 도메인, 선행 문서 링크}

---

## 3. 세션 기록

{질문·답변, 테스트 추가, pytest 결과, Mom Test 증거 등 — 사실만}

### 원문 인용 (해당 시)

> "…"

---

## 4. 산출·결정

| 항목 | 내용 |
|------|------|
| {키} | {값} |

---

## 5. 미완·리스크

- {항목}

---

## 6. 다음 단계

- {항목}

---

## 7. 관련 파일

| 경로 | 설명 |
|------|------|
| `Prompting/{NN}.{Slug}-Transcript.md` | 본 세션 Transcript |
| `Report/…` | 선행 보고서 (해당 시) |
```

- Mom Test 세션: `Report/01-MomTest-Report.md` 수준의 **표면/진짜 문제·증거 3줄** 포함
- TDD 세션: **Phase, 변경 파일, 테스트명, pytest 결과** 포함
- 합성·미확정 데이터는 **명시** (Mom Test 규칙)

---

## 3단계 — Transcript Export

`Prompting/{NN}.{Slug}-Transcript.md` 생성.

### Transcript 템플릿

```markdown
# MagicSquare_xx — Session Transcript

| Field | Value |
|-------|-------|
| Project | MagicSquare_xx |
| Exported | YYYY-MM-DD |
| Document ID | `{NN}.{Slug}-Transcript` |
| Report | `Report/{NN}.{Slug}-Report.md` |

---

## Turn 1 — User

{사용자 메시지 전문 — <user_query> 태그 제거, 코드·격자 유지}

---

## Turn 2 — Assistant

{어시스턴트 응답 요약 또는 전문 — tool 호출은 「도구: Glob, pytest …」한 줄로 축약 가능}

---

## Turn N — …

{대화 순서대로 전 turn 기록}

---

## Appendix A — 사용한 프롬프트 (해당 시)

{재사용 가능한 프롬프트 블록}

---

## Appendix B — 세션 스냅샷

| Item | Status |
|------|--------|
| 주제 | … |
| 산출 파일 | … |
| pytest (해당 시) | … |

---

*End of transcript export.*
```

- **User** 메시지: 가능한 한 **원문 유지** (격자, 코드, 프롬프트)
- **Assistant** 메시지: 긴 tool 로그는 요약, **결론·판정·파일 경로**는 유지
- 이미지·첨부: 경로 또는 설명 기록

---

## 4단계 — 완료 보고

작업 후 **한국어**로 아래 형식 보고 (코드·경로·선 ID는 영문):

```
## Export 완료

| 산출물 | 경로 |
|--------|------|
| 보고서 | Report/{NN}.{Slug}-Report.md |
| Transcript | Prompting/{NN}.{Slug}-Transcript.md |

### 순번·Slug
- NN: {01}
- Slug: {…}
- 근거: {한 줄}

### 보고서 요약
- …

### Transcript
- Turn 수: N
- 부록: A(프롬프트), B(스냅샷)

### 다음 단계
- {선택}
```

---

## 예시

| 세션 | Report | Transcript |
|------|--------|------------|
| Mom Test 인터뷰 | `Report/04.MomTest-Interview-Report.md` | `Prompting/04.MomTest-Interview-Transcript.md` |
| TDD RED | `Report/05.TDD-RED-Report.md` | `Prompting/05.TDD-RED-Transcript.md` |

*(실제 `{NN}`은 `Report/`·`Prompting/` 기존 파일 스캔 후 결정)*

---

## 관련 폴더 (참고)

| 폴더 | 용도 |
|------|------|
| `Report/` | 구조화된 **보고서** (`01.XXX-Report.md`) |
| `Prompting/` | 세션 **Transcript** export (`01.XXX-Transcript.md`) |
| `prompt/` | 재사용 **프롬프트** 템플릿 (본 커맨드와 별도) |

---

## 금지 (재확인)

- `01-XXX` (하이픈 순번) 형식으로 저장하지 않는다.
- Report만 또는 Transcript만 생성하지 않는다 — **항상 쌍**.
- 대화에 없는 Mom Test 증거·pytest 결과를 **꾸며 넣지** 않는다.
- git commit·push는 사용자 요청 전까지 하지 않는다.
