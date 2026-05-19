# Eval Run: 20260518_230939_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 1/24 (4%)  |  Mean score: 0.69

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 4/15 | 0.64 |
| boundaries | no_opinion_leakage | 0/3 | 0.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 10/16 | 0.82 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 16 | 15/16 | 0.89 | 0.7 |
| query_entity_adherence | 12 | 6/12 | 0.72 | 0.7 |
| factual_accuracy | 15 | 8/15 | 0.51 | 0.7 |
| groundedness | 12 | 8/12 | 0.79 | 0.8 |
| no_opinion_leakage | 3 | 0/3 | 0.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.50) |
| Q003 | query_entity_adherence (0.00) |
| Q004 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q008 | tool_use_appropriateness (0.50), query_entity_adherence (0.33), factual_accuracy (0.30) |
| Q009 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q010 | groundedness (0.50) |
| Q015 | factual_accuracy (0.00) |
| Q017 | no_opinion_leakage (0.00) |
| Q018 | no_opinion_leakage (0.00) |
| Q020 | no_opinion_leakage (0.00) |
| Q024 | groundedness (0.00) |
