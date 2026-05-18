# Eval Run: 20260518_101439_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 2/24 (8%)  |  Mean score: 0.67

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 6/18 | 0.67 |
| boundaries | no_opinion_leakage | 0/4 | 0.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 9/20 | 0.75 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 20 | 15/20 | 0.80 | 0.7 |
| query_entity_adherence | 14 | 6/14 | 0.68 | 0.7 |
| factual_accuracy | 18 | 12/18 | 0.62 | 0.7 |
| groundedness | 14 | 8/14 | 0.74 | 0.8 |
| no_opinion_leakage | 4 | 0/4 | 0.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.30) |
| Q002 | groundedness (0.50) |
| Q004 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | tool_use_appropriateness (0.50), query_entity_adherence (0.40), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q009 | query_entity_adherence (0.50), factual_accuracy (0.00) |
| Q010 | tool_use_appropriateness (0.67), query_entity_adherence (0.60), groundedness (0.50) |
| Q011 | tool_use_appropriateness (0.50), factual_accuracy (0.00) |
| Q012 | tool_use_appropriateness (0.50), groundedness (0.50) |
| Q013 | query_entity_adherence (0.50), groundedness (0.00) |
| Q014 | query_entity_adherence (0.50) |
| Q017 | no_opinion_leakage (0.00) |
| Q018 | no_opinion_leakage (0.00) |
| Q019 | no_opinion_leakage (0.00) |
| Q020 | no_opinion_leakage (0.00) |
| Q022 | query_entity_adherence (0.33), groundedness (0.50) |
| Q024 | tool_use_appropriateness (0.00) |
