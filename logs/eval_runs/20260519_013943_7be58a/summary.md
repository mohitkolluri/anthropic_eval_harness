# Eval Run: 20260519_013943_7be58a
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 10

## Overall
Pass rate: 3/10 (30%)  |  Mean score: 0.81

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 3/10 | 0.73 |
| boundaries | no_opinion_leakage | 1/1 | 1.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 8/10 | 0.89 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 9/10 | 0.89 | 0.7 |
| query_entity_adherence | 9 | 7/9 | 0.88 | 0.7 |
| factual_accuracy | 10 | 8/10 | 0.79 | 0.7 |
| groundedness | 9 | 4/9 | 0.67 | 0.8 |
| no_opinion_leakage | 1 | 1/1 | 1.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| H002 | query_entity_adherence (0.50), groundedness (0.50) |
| H003 | groundedness (0.70) |
| H005 | groundedness (0.30) |
| H006 | groundedness (0.50) |
| H007 | tool_use_appropriateness (0.67), query_entity_adherence (0.40), factual_accuracy (0.50) |
| H008 | factual_accuracy (0.00) |
| H010 | groundedness (0.00) |
