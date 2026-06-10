# MagicSquare_xx — 세션 3 워크북

> Mom Test 결과 → 문제 정의 · R-G-I-O · 8계층 범위  
> 재사용 프롬프트 — Cursor 등에 그대로 붙여넣어 실행

---

## 프롬프트 (복사용)

```
Mom Test 결과:
- 페르소나: [4×4 부분 마방진을 손으로/코드로 다루는 학습자]
- 진짜 문제 (한 문장): [Report/01-MomTest-Report.md §4 참고 또는 인터뷰에서 확정한 한 문장]
- Mom Test 증거 3줄: [인터뷰 답변에서 직접 인용 3줄]

MagicSquare_xx 세션 3 워크북을 채워줘:
1) 주제 한 문장 (Mom Test 기반, 솔루션 최소화)
2) R-G-I-O (Role/Goal/Input/Output)
3) 성공 기준 3개 (Mom Test 증거와 연결)
4) 표면 문제 — 이번 프로젝트에서 하지 않을 것
8계층 중 이번 세션에서 만드는 것만: Rule, Command, (Skill), Test Loop
```

> ⚠️ `[...]` 칸에 **질문 문장**이 아니라 **인터뷰 답변·인용**을 넣을 것. 비어 있으면 `Report/01-MomTest-Report.md`를 근거로 채움.

---

## 입력 체크리스트

| 칸 | 올바른 예 | 잘못된 예 |
|----|-----------|-----------|
| 페르소나 | "4×4, 빈칸 2, 합 34 학습자" | "누구나 쓸 앱 사용자" |
| 진짜 문제 | "대각선 검증을 늦게 해 20분 재작업" | "합 34 확인할 때 뭘 썼어?" (질문) |
| 증거 3줄 | "대각선 하나 빼먹어서 20분 날렸다" | "두 번째 풀 때 바꿨나요?" (질문) |

---

## Agent 출력 형식 (기대)

1. **주제 한 문장** — 솔루션(앱/Solver/ECB) 최소화, Mom Test 불편 중심  
2. **R-G-I-O** — Role / Goal / Input / Output 표  
3. **성공 기준 S1~S3** — 각각 증거 1줄과 연결  
4. **표면 문제** — 이번에 **하지 않을 것** 표  
5. **8계층** — Rule · Command · (Skill) · Test Loop 만 ✅  

---

## 8계층 (이번 세션 범위)

| 계층 | 이번 | MagicSquare_xx |
|------|------|----------------|
| **Rule** | ✅ | 4×4, `0`×2, 1~16, **10선** 합 34 |
| **Command** | ✅ | `validate(grid)` → pass/fail + 실패 선 ID |
| **(Skill)** | △ | `listViolations(grid)` — 선택 |
| **Test Loop** | ✅ | S1~S3 fixture, Red→Green |
| Boundary / Solver / UI / … | ❌ | 후속 |

**10선:** `row:0..3`, `col:0..3`, `diag:main`, `diag:anti`

---

## 후속 작업

```
Report 폴더에 기록해줘
```
→ `Report/03-SESSION3-Workbook.md`

```
prompt 폴더에 프롬프트를 저장해줘
```
→ `prompt/05-session-3-workbook.md` (본 파일)

---

## Mom Test 결과 예시 (MagicSquare_xx)

`Report/01-MomTest-Report.md` 기준 — 프롬프트 `[...]`에 그대로 넣을 수 있음:

| 항목 | 내용 |
|------|------|
| 페르소나 | 4×4 부분 마방진을 손으로/코드로 다루는 학습자 |
| 진짜 문제 | 행·열이 맞으면 거의 끝으로 보고 대각선 검증을 늦게 하다 ~20분 재작업 |
| 증거 ① | "대각선 하나를 빼먹어서 20분 날렸다" |
| 증거 ② | "대각선을 제외하곤 다 맞았다고 생각했어" |
| 증거 ③ | "숫자 합을 내서 검증을 하다보니 알았어" → "대각선이었어" |

---

## 관련 파일

| 경로 | 설명 |
|------|------|
| [`Report/03-SESSION3-Workbook.md`](../Report/03-SESSION3-Workbook.md) | 세션 3 워크북 산출물 |
| [`Report/01-MomTest-Report.md`](../Report/01-MomTest-Report.md) | STEP 1 Mom Test |
| [`prompt/02-mom-test-interview.md`](./02-mom-test-interview.md) | 인터뷰 시작 |
| [`prompt/03-mom-test-interview-end.md`](./03-mom-test-interview-end.md) | 인터뷰 종료·추출 |
