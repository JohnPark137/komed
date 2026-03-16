# Korean Medicine Retrieval Benchmark

- Date: 2026-03-13
- Mode: `Codex only`
- Benchmark arms:
  1. `Baseline`: no injected local excerpt, no web evidence intentionally used in the answer
  2. `Web-enabled`: answer built only from official online NIKOM/NCKM pages or PDFs found during this turn
  3. `Local-doc-augmented`: answer built from the local markdown corpus in `docs/modern-korean-medicine/markdown/`

## Important limitations

You asked not to use an external model key and to use Codex only. Because of that, this benchmark was run in the same session.

That creates two methodological limits:

1. The `baseline` arm is not a cold-start blind run, because Codex had already inspected the local corpus while constructing the benchmark.
2. The `web-enabled` arm depended on whatever the browser/search stack could reach from the official NIKOM/NCKM site in this session. Some full PDFs were directly reachable; some were only exposed through quick-reference or infographic material.

This means the results are useful for directional product decisions, not for a publication-grade retrieval study.

## Question set and source policy

All five questions were deliberately hard and tied to official Korean medicine clinical practice guidelines that are publicly available online. I limited the web arm to official NIKOM/NCKM sources.

Primary online sources used:

1. Type 2 Diabetes Mellitus guideline DB page: https://nikom.or.kr/engnckm/module/practiceGuide/view.do?guide_idx=295&menu_idx=4
2. Type 2 Diabetes Mellitus PDF: https://nikom.or.kr/engnckm/module/practiceGuide/download.do?file_type=pdf&guide_idx=295
3. Obesity PDF: https://nikom.or.kr/engnckm/module/practiceGuide/download.do?file_type=pdf&guide_idx=328
4. Depression guideline DB page: https://nikom.or.kr/engnckm/module/practiceGuide/view.do?guide_idx=337&menu_idx=4
5. Depression quick-reference PDF: https://nikom.or.kr/board/boardFile/download/138/565473/35178.do
6. Dizziness infographic PDF: https://nikom.or.kr/board/boardFile/download/138/567287/36676.do
7. Prostatic hypertrophy guideline DB page: https://nikom.or.kr/engnckm/module/practiceGuide/view.do?guide_idx=353&menu_idx=4
8. Prostatic hypertrophy PDF: https://nikom.or.kr/engnckm/module/practiceGuide/download.do?file_type=pdf&guide_idx=353

Search queries used during the web arm:

- `site:nikom.or.kr 2형 당뇨병 한의표준임상진료지침 PDF`
- `site:nikom.or.kr 비만 한의표준임상진료지침 PDF`
- `site:nikom.or.kr 우울증 한의표준임상진료지침 PDF`
- `site:nikom.or.kr 현훈 한의표준임상진료지침 PDF`
- `site:nikom.or.kr 전립선증식증 한의표준임상진료지침 PDF`

## Scoring rubric

Each answer was scored manually on a 20-point rubric:

- `core recommendation accuracy`
- `guideline specificity`
- `safety or referral nuance`
- `completeness`

## Headline result

| Run | Total | Average / 20 |
| --- | ---: | ---: |
| Baseline | 70 / 100 | 14.0 |
| Web-enabled | 96 / 100 | 19.2 |
| Local-doc-augmented | 100 / 100 | 20.0 |

## Direct answer to the question

Empirically: `almost, but not fully`.

In this benchmark, web-enabled retrieval closed most of the gap and matched the local-doc result on 4 of 5 questions. It still underperformed on 1 question where web retrieval exposed only an official quick-reference artifact rather than the full pattern-specific recommendation passage.

So the measured ranking here was:

1. `Local-doc-augmented`: 100
2. `Web-enabled`: 96
3. `Baseline`: 70

## Per-question summary

| ID | Topic | Baseline | Web-enabled | Local-doc | Web vs Local |
| --- | --- | ---: | ---: | ---: | ---: |
| `q1_t2dm_oral_agents` | Type 2 Diabetes Mellitus | 16 | 20 | 20 | 0 |
| `q2_obesity_herbal_safety` | Obesity | 11 | 20 | 20 | 0 |
| `q3_depression_menstrual_perimenopause` | Depression | 16 | 16 | 20 | -4 |
| `q4_dizziness_cervicogenic` | Dizziness | 13 | 20 | 20 | 0 |
| `q5_bph_tongguan_tang` | Prostatic Hypertrophy | 14 | 20 | 20 | 0 |

## Detailed findings

### Q1. Type 2 diabetes on oral hypoglycemic agents

- Official web sources:
  - https://nikom.or.kr/engnckm/module/practiceGuide/view.do?guide_idx=295&menu_idx=4
  - https://nikom.or.kr/engnckm/module/practiceGuide/download.do?file_type=pdf&guide_idx=295
- Local doc: `docs/modern-korean-medicine/markdown/km-cpg-type-2-diabetes-mellitus.md`

Question:

> An adult with type 2 diabetes is already taking oral hypoglycemic agents but remains above glycemic target and asks for Korean medicine adjuncts. According to the Korean medicine clinical practice guideline, which two herbal formulas have the strongest explicit recommendations in this setting, and what acupuncture modality is also recommended for glycemic improvement?

Measured outcome:

- Baseline: `16/20`
- Web-enabled: `20/20`
- Local-doc: `20/20`

What happened:

- The official web PDF was directly reachable and included the exact summary rows:
  - `육미지황환 (R7-1, A/Moderate)`
  - `금궤신기환 (R7-5, A/Moderate)`
  - `전침 (R11, B/Moderate)`
- Because the web arm could reach the same official PDF content, it matched the local-doc result.

### Q2. Obesity herbal selection and mahuang safety

- Official web source:
  - https://nikom.or.kr/engnckm/module/practiceGuide/download.do?file_type=pdf&guide_idx=328
- Local doc: `docs/modern-korean-medicine/markdown/km-cpg-obesity.md`

Question:

> An adult with obesity (BMI 31 kg/m2), hypertension, and dyslipidemia asks about herbal treatment. According to the Korean medicine obesity guideline, which prescription has the strongest standalone recommendation overall, which prescription is specifically highlighted for high BMI or cardiometabolic comorbidity, and what safety monitoring is required for mahuang-modified prescriptions?

Measured outcome:

- Baseline: `11/20`
- Web-enabled: `20/20`
- Local-doc: `20/20`

What happened:

- The official web PDF exposed the decisive lines:
  - `의이인탕 A/High`
  - `태음조위탕 B/Moderate`
  - high-BMI/comorbidity relevance
  - mahuang monitoring including `blood pressure` and `heart rate`
- This made the web arm just as good as the local-doc arm for this question.

### Q3. Perimenopausal depression with menstrual worsening

- Official web sources:
  - https://nikom.or.kr/engnckm/module/practiceGuide/view.do?guide_idx=337&menu_idx=4
  - https://nikom.or.kr/board/boardFile/download/138/565473/35178.do
- Local doc: `docs/modern-korean-medicine/markdown/km-cpg-depression.md`

Question:

> A perimenopausal woman with mild-to-moderate major depressive disorder reports worsening around menstruation, declines antidepressants, and has no suicidality, psychosis, or alcohol dependence. According to the Korean medicine depression guideline, which herbal formula is best supported, what pattern does it fit, and what findings would trigger referral rather than routine primary Korean medicine management?

Measured outcome:

- Baseline: `16/20`
- Web-enabled: `16/20`
- Local-doc: `20/20`

What happened:

- The official web material was enough to verify:
  - `소요산 B/Moderate`
  - referral for psychiatric emergency / severe depression / specialist care
- But the web-retrieved official artifact available in this session was the one-page quick reference, not a directly accessible full recommendation passage with the exact pattern paragraph.
- As a result, the web arm could not cleanly recover the explicit pattern wording `간울비허 / 혈허`, while the local corpus could.

This was the only question where local-doc augmentation materially outperformed web retrieval.

### Q4. Cervicogenic dizziness

- Official web source:
  - https://nikom.or.kr/board/boardFile/download/138/567287/36676.do
- Local doc: `docs/modern-korean-medicine/markdown/km-cpg-dizziness.md`

Question:

> For cervicogenic dizziness with persistent neck muscle tension, which Korean medicine intervention has the strongest recommendation in the dizziness guideline, and what is one B/Moderate combination therapy aimed at improving symptoms plus vertebrobasilar blood flow?

Measured outcome:

- Baseline: `13/20`
- Web-enabled: `20/20`
- Local-doc: `20/20`

What happened:

- The official infographic was enough for this specific question.
- It explicitly exposed:
  - `수기요법 권고 (IIIa-D-1 A/High)`
  - `한약과 수기요법 병행 고려 (IIIa-B-2 B/Moderate)`
- That let the web arm fully match the local-doc result.

### Q5. BPH pattern-matched formula and duration

- Official web sources:
  - https://nikom.or.kr/engnckm/module/practiceGuide/view.do?guide_idx=353&menu_idx=4
  - https://nikom.or.kr/engnckm/module/practiceGuide/download.do?file_type=pdf&guide_idx=353
- Local doc: `docs/modern-korean-medicine/markdown/km-cpg-prostatic-hypertrophy.md`

Question:

> A 68-year-old man with benign prostatic hyperplasia has no acute urinary retention, IPSS 18, Qmax 12 mL/s, prostate volume 32 mL, burning urethral pain, and weak urinary stream. According to the Korean medicine prostatic hypertrophy guideline, which herbal prescription best matches this profile, how long is treatment generally considered, and what formula modification is suggested for the burning-pain pattern?

Measured outcome:

- Baseline: `14/20`
- Web-enabled: `20/20`
- Local-doc: `20/20`

What happened:

- The official web PDF exposed all decisive details:
  - `통관탕`
  - age/IPSS/Qmax/PV fit
  - `6개월 이상`
  - `황련`, `적작약`
- So the web arm matched the local-doc result.

## Interpretation

This empirical test answers the question more precisely:

- If the relevant official guideline PDF is directly reachable online, web-enabled retrieval can produce almost the same result as local-doc augmentation.
- If web retrieval only surfaces a compressed official artifact such as an infographic or quick-reference sheet, local-doc augmentation retains an edge on fine-grained details.

In this benchmark:

- `4/5` questions: web-enabled matched local-doc
- `1/5` question: local-doc was better

The decisive difference was not “internet vs local” in the abstract. It was `retrieval fidelity`.

When the web arm reached the same official PDF content, it performed the same.
When the web arm only reached a thinner official representation, it lost specificity.

## Practical implication

For your product decision:

- If your deployment will always have reliable web access to the exact official guideline PDFs, local docs may offer only a small incremental gain on many public-reference questions.
- If your deployment needs stable performance without retrieval friction, or if you care about exact pattern language, recommendation grades, modification rules, and threshold details, local document grounding still adds measurable value.

## Files produced

- `performance/questions.json`
- `performance/results.json`
- `performance/REPORT.md`
