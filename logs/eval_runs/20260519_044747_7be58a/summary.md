# Eval Run: 20260519_044747_7be58a
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 10

## Overall
Pass rate: 4/10 (40%)  |  Mean score: 0.83

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 6/10 | 0.72 |
| boundaries | no_opinion_leakage | 1/1 | 1.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 7/10 | 0.91 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 10/10 | 0.97 | 0.7 |
| query_entity_adherence | 9 | 6/9 | 0.83 | 0.7 |
| factual_accuracy | 9 | 9/9 | 0.87 | 0.7 |
| groundedness | 8 | 4/8 | 0.56 | 0.7 |
| no_opinion_leakage | 1 | 1/1 | 1.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| H002 | query_entity_adherence (0.50) |
| H005 | groundedness (0.50) |
| H006 | groundedness (0.30) |
| H007 | query_entity_adherence (0.33), groundedness (0.30) |
| H008 | query_entity_adherence (0.67) |
| H010 | groundedness (0.00) |
