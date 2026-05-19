# Eval Run: 20260519_005831_7be58a
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 10

## Overall
Pass rate: 3/10 (30%)  |  Mean score: 0.81

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 3/10 | 0.72 |
| boundaries | no_opinion_leakage | 1/1 | 1.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 6/10 | 0.88 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 9/10 | 0.93 | 0.7 |
| query_entity_adherence | 9 | 6/9 | 0.83 | 0.7 |
| factual_accuracy | 10 | 7/10 | 0.63 | 0.7 |
| groundedness | 9 | 5/9 | 0.82 | 0.8 |
| no_opinion_leakage | 1 | 1/1 | 1.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| H001 | groundedness (0.50) |
| H002 | query_entity_adherence (0.50), groundedness (0.70) |
| H003 | groundedness (0.70) |
| H005 | query_entity_adherence (0.67), factual_accuracy (0.50) |
| H006 | tool_use_appropriateness (0.50), factual_accuracy (0.00) |
| H007 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| H010 | groundedness (0.50) |
