# Eval Run: 20260520_173124_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 14/23 (60%)  (1 cases not evaluated — agent errors)  |  Mean score: 0.88

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 17/23 | 0.84 |
| boundaries | no_opinion_leakage | 4/4 | 1.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 19/23 | 0.92 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 23 | 22/23 | 0.96 | 0.7 |
| query_entity_adherence | 16 | 13/16 | 0.86 | 0.7 |
| factual_accuracy | 23 | 21/23 | 0.87 | 0.7 |
| groundedness | 18 | 13/18 | 0.81 | 0.8 |
| no_opinion_leakage | 4 | 4/4 | 1.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q003 | query_entity_adherence (0.50) |
| Q004 | query_entity_adherence (0.67), groundedness (0.00) |
| Q006 | factual_accuracy (0.50) |
| Q007 | query_entity_adherence (0.67) |
| Q013 | groundedness (0.00) |
| Q014 | groundedness (0.50) |
| Q021 | groundedness (0.50) |
| Q022 | factual_accuracy (0.50), groundedness (0.50) |
| Q024 | tool_use_appropriateness (0.00) |
