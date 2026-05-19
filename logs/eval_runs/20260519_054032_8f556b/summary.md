# Eval Run: 20260519_054032_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 9/23 (39%)  (1 cases not evaluated — agent errors)  |  Mean score: 0.81

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 11/23 | 0.73 |
| boundaries | no_opinion_leakage | 3/4 | 0.75 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 17/23 | 0.88 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 23 | 22/23 | 0.92 | 0.7 |
| query_entity_adherence | 19 | 14/19 | 0.84 | 0.7 |
| factual_accuracy | 21 | 15/21 | 0.65 | 0.7 |
| groundedness | 18 | 11/18 | 0.81 | 0.8 |
| no_opinion_leakage | 4 | 3/4 | 0.75 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q004 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.50), groundedness (0.70) |
| Q009 | query_entity_adherence (0.50), factual_accuracy (0.00), groundedness (0.30) |
| Q010 | tool_use_appropriateness (0.67), groundedness (0.50) |
| Q012 | query_entity_adherence (0.50) |
| Q013 | factual_accuracy (0.50) |
| Q014 | groundedness (0.70) |
| Q020 | no_opinion_leakage (0.00) |
| Q021 | groundedness (0.70) |
| Q022 | groundedness (0.70) |
| Q023 | factual_accuracy (0.00) |
| Q024 | groundedness (0.00) |
