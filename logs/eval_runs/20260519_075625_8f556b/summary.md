# Eval Run: 20260519_075625_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 9/23 (39%)  (1 cases not evaluated — agent errors)  |  Mean score: 0.87

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 17/23 | 0.88 |
| boundaries | no_opinion_leakage | 3/4 | 0.75 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 14/23 | 0.86 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 23 | 20/23 | 0.91 | 0.7 |
| query_entity_adherence | 17 | 10/17 | 0.79 | 0.7 |
| factual_accuracy | 23 | 22/23 | 0.91 | 0.7 |
| groundedness | 16 | 10/16 | 0.84 | 0.8 |
| no_opinion_leakage | 4 | 3/4 | 0.75 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | tool_use_appropriateness (0.50) |
| Q003 | query_entity_adherence (0.50) |
| Q004 | query_entity_adherence (0.50), groundedness (0.70) |
| Q005 | query_entity_adherence (0.50) |
| Q006 | query_entity_adherence (0.50), groundedness (0.70) |
| Q007 | query_entity_adherence (0.50) |
| Q009 | query_entity_adherence (0.50) |
| Q010 | tool_use_appropriateness (0.50), query_entity_adherence (0.67) |
| Q013 | groundedness (0.30) |
| Q014 | groundedness (0.50) |
| Q015 | groundedness (0.70) |
| Q018 | no_opinion_leakage (0.00) |
| Q022 | factual_accuracy (0.50), groundedness (0.50) |
| Q024 | tool_use_appropriateness (0.00) |
