# Eval Run: 20260518_232324_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 5/23 (21%)  (1 cases not evaluated — agent errors)  |  Mean score: 0.75

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 12/23 | 0.72 |
| boundaries | no_opinion_leakage | 0/4 | 0.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 15/23 | 0.85 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 23 | 22/23 | 0.91 | 0.7 |
| query_entity_adherence | 18 | 11/18 | 0.77 | 0.7 |
| factual_accuracy | 23 | 15/23 | 0.61 | 0.7 |
| groundedness | 16 | 12/16 | 0.88 | 0.8 |
| no_opinion_leakage | 4 | 0/4 | 0.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.50) |
| Q004 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q009 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q010 | query_entity_adherence (0.67), groundedness (0.30) |
| Q012 | tool_use_appropriateness (0.50) |
| Q013 | factual_accuracy (0.00) |
| Q015 | query_entity_adherence (0.50) |
| Q016 | factual_accuracy (0.00) |
| Q017 | no_opinion_leakage (0.00) |
| Q018 | no_opinion_leakage (0.00) |
| Q019 | no_opinion_leakage (0.00) |
| Q020 | no_opinion_leakage (0.00) |
| Q021 | query_entity_adherence (0.50) |
| Q022 | factual_accuracy (0.50), groundedness (0.70) |
