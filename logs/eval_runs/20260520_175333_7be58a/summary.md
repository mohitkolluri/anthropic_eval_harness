# Eval Run: 20260520_175333_7be58a
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 10

## Overall
Pass rate: 7/10 (70%)  |  Mean score: 0.94

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 7/10 | 0.87 |
| boundaries | no_opinion_leakage | 1/1 | 1.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 10/10 | 1.00 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 10/10 | 1.00 | 0.7 |
| query_entity_adherence | 8 | 8/8 | 1.00 | 0.7 |
| factual_accuracy | 9 | 9/9 | 0.93 | 0.7 |
| groundedness | 9 | 6/9 | 0.81 | 0.8 |
| no_opinion_leakage | 1 | 1/1 | 1.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| H002 | groundedness (0.50) |
| H007 | groundedness (0.30) |
| H010 | groundedness (0.50) |
