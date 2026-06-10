---
name: magic-square-docs
description: >-
  Export MagicSquare_xx session artifacts to Report/ and Prompting/ using
  standardized templates. Use with /export-session, when writing session
  reports, transcripts, or ARRR checklists for MagicSquare_xx.
---

# MagicSquare_xx — Docs Skill

세션 산출물(Report, Transcript, Checklist) 형식 SSOT. `/export-session` 실행 시 본 Skill 템플릿을 따른다.

**SSOT:** `.cursor/commands/export-session.md`, `docs/PRD.md`, `.cursorrules`

---

## 파일명 규칙

| 산출물 | 경로 | 패턴 |
|--------|------|------|
| Report | `Report/` | `{NN}.{Slug}-Report.md` |
| Transcript | `Prompting/` | `{NN}.{Slug}-Transcript.md` |
| Checklist | `Report/` | `{NN}.{Slug}-Checklist.md` |

- `{NN}`: 2자리 순번 (`01`, `02`, …) — 기존 파일 최댓값 + 1
- `{Slug}`: PascalCase·하이픈 (예: `ARRR-Red-Plan`, `TDD-Green`)
- ❌ `01-Slug` (하이픈 순번)

Report·Transcript는 **같은 NN·Slug**. Checklist는 선택(인수인계·실습용).

---

## Slug 추론 (질문 금지)

| 세션 내용 | Slug 예 |
|-----------|---------|
| RED 플랜 | `ARRR-Red-Plan` |
| RED 스켈레톤·assert | `ARRR-Red-Skeleton` |
| GREEN | `ARRR-Green` |
| Golden Master | `ARRR-Golden-Review` |
| Refactor | `ARRR-Refactor` |
| Mom Test | `MomTest-Interview` |
| 워크북 | `Session3-Workbook` |

불명확하면 채팅 Phase·커맨드명에서 추론 후 `근거:` 한 줄.

---

## Export 절차

1. 세션 분석 (주제, Phase, Test ID, pytest, 변경 파일)
2. `templates/report-template.md` → `Report/{NN}.{Slug}-Report.md`
3. `templates/transcript-template.md` → `Prompting/{NN}.{Slug}-Transcript.md`
4. (선택) `templates/checklist-template.md` → `Report/{NN}.{Slug}-Checklist.md`
5. 완료 보고 + `/export-session Release 완료`

**금지:** 대화에 없는 pytest·증거 꾸미기, `src/`·`tests/` 수정.

---

## TDD·ARRR Report 필수 필드

| 필드 | 내용 |
|------|------|
| Phase | `red` / `green` / `refactor` / `review` |
| Layer | `entity` / `boundary` |
| Track | `Logic` |
| Test ID | `T-R…` / `GM-…` |
| 변경 파일 | 경로 목록 |
| pytest | **실행한 경우만** 명령·결과 |

---

## Transcript 규칙

- User: `<user_query>` 태그 제거, 격자·코드 원문 유지
- Assistant: tool 호출 → 「도구: Glob, Write …」한 줄
- 결론·파일 경로·Phase 선언·pytest 판정은 **유지**

---

## Checklist 사용 시

- ARRR 실습 **자가 점검**·강사 인수인계
- 항목별 ✅/❌/N/A — 미확정은 `미확정 (근거: …)` 명시

---

## 템플릿 위치

| 파일 | 용도 |
|------|------|
| `templates/report-template.md` | 구조화 보고서 |
| `templates/transcript-template.md` | 대화 export |
| `templates/checklist-template.md` | ARRR·TDD 체크리스트 |

템플릿 `{placeholder}`를 세션 fact로 치환. placeholder 그대로 두지 않는다.

---

## 관련 폴더

| 폴더 | 용도 |
|------|------|
| `Report/` | 보고서·Checklist |
| `Prompting/` | Transcript |
| `prompt/` | 재사용 프롬프트 (export와 별도) |
