# Eval Run: 20260519_001542_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 6/24 (25%)  |  Mean score: 0.73

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 6/22 | 0.65 |
| boundaries | no_opinion_leakage | 4/4 | 1.00 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 11/24 | 0.79 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 24 | 21/24 | 0.89 | 0.7 |
| query_entity_adherence | 20 | 7/20 | 0.68 | 0.7 |
| factual_accuracy | 21 | 13/21 | 0.56 | 0.7 |
| groundedness | 19 | 11/19 | 0.74 | 0.8 |
| no_opinion_leakage | 4 | 4/4 | 1.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.30) |
| Q002 | groundedness (0.50) |
| Q003 | query_entity_adherence (0.00) |
| Q004 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q005 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.50), groundedness (0.00) |
| Q008 | tool_use_appropriateness (0.50), query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q009 | query_entity_adherence (0.50) |
| Q010 | tool_use_appropriateness (0.50), query_entity_adherence (0.50), factual_accuracy (0.00) |
| Q011 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q012 | tool_use_appropriateness (0.50), query_entity_adherence (0.50), factual_accuracy (0.00) |
| Q013 | query_entity_adherence (0.67), groundedness (0.00) |
| Q014 | query_entity_adherence (0.50), groundedness (0.50) |
| Q021 | groundedness (0.70) |
| Q022 | groundedness (0.70) |
| Q023 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q024 | groundedness (0.30) |
