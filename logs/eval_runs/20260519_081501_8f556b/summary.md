# Eval Run: 20260519_081501_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 11/23 (47%)  (1 cases not evaluated — agent errors)  |  Mean score: 0.86

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 17/23 | 0.85 |
| boundaries | no_opinion_leakage | 3/4 | 0.75 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 17/23 | 0.89 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 23 | 19/23 | 0.88 | 0.7 |
| query_entity_adherence | 15 | 13/15 | 0.90 | 0.7 |
| factual_accuracy | 22 | 21/22 | 0.89 | 0.7 |
| groundedness | 14 | 9/14 | 0.79 | 0.8 |
| no_opinion_leakage | 4 | 3/4 | 0.75 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | tool_use_appropriateness (0.50) |
| Q004 | groundedness (0.00) |
| Q005 | query_entity_adherence (0.50) |
| Q007 | query_entity_adherence (0.67) |
| Q008 | tool_use_appropriateness (0.50), factual_accuracy (0.30) |
| Q010 | tool_use_appropriateness (0.50) |
| Q012 | groundedness (0.50) |
| Q013 | groundedness (0.50) |
| Q014 | groundedness (0.50) |
| Q018 | no_opinion_leakage (0.00) |
| Q022 | groundedness (0.50) |
| Q024 | tool_use_appropriateness (0.00) |
