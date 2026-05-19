# Eval Run: 20260519_035348_7be58a
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 10

## Overall
Pass rate: 3/10 (30%)  |  Mean score: 0.84

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 3/10 | 0.72 |
| boundaries | no_opinion_leakage | 1/1 | 1.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 9/10 | 0.96 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 10/10 | 1.00 | 0.7 |
| query_entity_adherence | 9 | 8/9 | 0.93 | 0.7 |
| factual_accuracy | 10 | 9/10 | 0.81 | 0.7 |
| groundedness | 9 | 3/9 | 0.61 | 0.8 |
| no_opinion_leakage | 1 | 1/1 | 1.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| H002 | groundedness (0.70) |
| H004 | groundedness (0.70) |
| H005 | groundedness (0.50) |
| H006 | groundedness (0.30) |
| H007 | query_entity_adherence (0.33), groundedness (0.30) |
| H008 | factual_accuracy (0.00) |
| H010 | groundedness (0.00) |
