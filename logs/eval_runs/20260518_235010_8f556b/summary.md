# Eval Run: 20260518_235010_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 3/23 (13%)  (1 cases not evaluated — agent errors)  |  Mean score: 0.69

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 10/23 | 0.68 |
| boundaries | no_opinion_leakage | 0/4 | 0.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 12/23 | 0.77 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 23 | 18/23 | 0.82 | 0.7 |
| query_entity_adherence | 17 | 9/17 | 0.70 | 0.7 |
| factual_accuracy | 22 | 15/22 | 0.61 | 0.7 |
| groundedness | 17 | 11/17 | 0.76 | 0.8 |
| no_opinion_leakage | 4 | 0/4 | 0.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.50) |
| Q003 | query_entity_adherence (0.00) |
| Q004 | tool_use_appropriateness (0.50), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.50), groundedness (0.00) |
| Q008 | tool_use_appropriateness (0.50), query_entity_adherence (0.50), factual_accuracy (0.00) |
| Q009 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q010 | tool_use_appropriateness (0.50), factual_accuracy (0.00) |
| Q013 | tool_use_appropriateness (0.67), query_entity_adherence (0.60), factual_accuracy (0.00) |
| Q014 | groundedness (0.50) |
| Q015 | query_entity_adherence (0.50) |
| Q017 | no_opinion_leakage (0.00) |
| Q018 | no_opinion_leakage (0.00) |
| Q019 | no_opinion_leakage (0.00) |
| Q020 | no_opinion_leakage (0.00) |
| Q021 | groundedness (0.00) |
| Q022 | query_entity_adherence (0.33), groundedness (0.50) |
| Q024 | tool_use_appropriateness (0.00) |
