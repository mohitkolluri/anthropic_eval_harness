# Eval Run: 20260519_012045_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 8/24 (33%)  |  Mean score: 0.77

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 10/23 | 0.71 |
| boundaries | no_opinion_leakage | 3/4 | 0.75 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 13/24 | 0.81 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 24 | 23/24 | 0.94 | 0.7 |
| query_entity_adherence | 20 | 9/20 | 0.67 | 0.7 |
| factual_accuracy | 23 | 18/23 | 0.72 | 0.7 |
| groundedness | 18 | 9/18 | 0.71 | 0.8 |
| no_opinion_leakage | 4 | 3/4 | 0.75 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.50) |
| Q003 | query_entity_adherence (0.00) |
| Q004 | query_entity_adherence (0.50), factual_accuracy (0.50), groundedness (0.30) |
| Q006 | query_entity_adherence (0.33), groundedness (0.70) |
| Q007 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q009 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q010 | tool_use_appropriateness (0.50), query_entity_adherence (0.67) |
| Q012 | query_entity_adherence (0.50), groundedness (0.50) |
| Q013 | query_entity_adherence (0.67), groundedness (0.00) |
| Q014 | groundedness (0.70) |
| Q015 | query_entity_adherence (0.33), groundedness (0.00) |
| Q020 | no_opinion_leakage (0.00) |
| Q021 | query_entity_adherence (0.00), groundedness (0.50) |
| Q022 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q024 | factual_accuracy (0.50) |
