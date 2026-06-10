# /export-session — ARRR R단계 (Release)

현재 Cursor 세션을 **보고서**와 **대화 Transcript** 두 파일로 내보낸다.

슬래시 메뉴: **`/export-session`**

ARRR 파이프라인: **A**(Ask) → **R**(Review) → **R**(Refine) → **R**(Release). 본 커맨드는 **Release** — 세션 산출물 고정 전용. 상세 템플릿은 **`magic-square-docs` Skill**을 따른다.

---

## 실행 조건

| 허용 | 금지 |
|------|------|
| `Report/` 보고서 생성·갱신 | `src/`·`tests/` 수정 |
| `Prompting/` Transcript 생성·갱신 | git commit·push (사용자 요청 전) |
| `Report/`·`Prompting/` 폴더 없으면 생성 | 범위 밖 기능·문서 추가 |

**한 실행 = 한 세션 쌍** (Report 1개 + Transcript 1개).

---

## SSOT (단일 진실 공급원)

추가 입력 없이 `/export-session`만 실행해도 동작한다.

| 우선순위 | 소스 | 용도 |
|----------|------|------|
| 1 | 현재 채팅·@참조·첨부 | Phase, Test ID, pytest 결과, 결정 |
| 2 | `.cursor/skills/magic-square-docs/` 템플릿 | Report·Transcript·Checklist 형식 |
| 3 | `docs/PRD.md`·`.cursorrules` | 도메인·FR·Phase 용어 |
| 4 | `Report/`·`Prompting/` 기존 파일 | 순번 `{NN}` 결정 |

불명확해도 **질문으로 멈추지 않고** 채팅·SSOT에서 최선 추론 후 `근거:` 한 줄로 명시한다. 합성·미확정 데이터는 Report에 **명시**한다.

---

## 파일명 규칙 (`01.XXX` 형식)

| 산출물 | 경로 | 파일명 |
|--------|------|--------|
| 보고서 | `Report/` | `{NN}.{Slug}-Report.md` |
| Transcript | `Prompting/` | `{NN}.{Slug}-Transcript.md` |

- `{NN}`: **2자리 순번** (`01`, `02`, …) — `Report/`·`Prompting/` 전체에서 `^(\d{2})[.\-]` 최댓값 + 1 (없으면 `01`)
- `{Slug}`: **PascalCase·하이픈** (예: `TDD-RED`, `ARRR-Green`, `Session3-Workbook`)
- Report·Transcript는 **같은 `{NN}`·같은 `{Slug}`**

---

## 절차 (필수 순서)

### 1. 세션 분석

| 항목 | 수집 |
|------|------|
| 주제 | 세션 한 줄 (한국어) |
| Phase | `red` / `green` / `refactor` / ARRR 단계 |
| Track | Logic (`validate_lines`) 등 |
| 핵심 산출 | Test ID, 변경 파일, pytest, C2C·ECB 결정 |
| 미완·리스크 | 미응답, 다음 RED 묶음 |

`agent-transcripts/` JSONL은 보조 참고. **본문은 현재 대화 기준**.

### 2. Report 작성

`Report/{NN}.{Slug}-Report.md` — **`magic-square-docs` Skill**의 `templates/report-template.md` 구조를 따른다.

TDD·ARRR 세션 필수 포함: **Phase, Test ID, 변경 파일, pytest 결과(실행한 경우만)**.

### 3. Transcript 작성

`Prompting/{NN}.{Slug}-Transcript.md` — **`templates/transcript-template.md`** 구조.

User turn: 원문 유지. Assistant: tool 로그는 「도구: …」 한 줄 축약, **결론·경로·판정** 유지.

### 4. (선택) Checklist

세션 종료·인수인계용이면 `Report/{NN}.{Slug}-Checklist.md` — **`templates/checklist-template.md`**.

---

## 완료 보고 (필수)

```
## Export 완료

| 산출물 | 경로 |
|--------|------|
| 보고서 | Report/{NN}.{Slug}-Report.md |
| Transcript | Prompting/{NN}.{Slug}-Transcript.md |
| (해당 시) Checklist | Report/{NN}.{Slug}-Checklist.md |

### 순번·Slug
- NN: {01}
- Slug: {…}
- 근거: {한 줄}

### 보고서 요약
- …

### Transcript
- Turn 수: N
```

보고 **마지막**에 정확히 한 줄:

```
/export-session Release 완료
```

---

## 관련 폴더

| 폴더 | 용도 |
|------|------|
| `Report/` | 구조화된 보고서 |
| `Prompting/` | 세션 Transcript |
| `prompt/` | 재사용 프롬프트 (본 커맨드와 별도) |

---

## 금지 (재확인)

- `01-XXX` (하이픈 순번) 형식 저장 금지.
- Report·Transcript **쌍** 없이 한쪽만 생성 금지.
- 대화에 없는 pytest 결과·Mom Test 증거 **꾸며 넣기** 금지.
- `src/`·`tests/` 수정 금지.
- git commit·push — 사용자 요청 전까지 하지 않는다.
