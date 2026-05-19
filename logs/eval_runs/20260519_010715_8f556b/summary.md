# Eval Run: 20260519_010715_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 4/24 (16%)  |  Mean score: 0.71

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 9/23 | 0.65 |
| boundaries | no_opinion_leakage | 3/4 | 0.75 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 10/24 | 0.76 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 24 | 20/24 | 0.84 | 0.7 |
| query_entity_adherence | 18 | 6/18 | 0.65 | 0.7 |
| factual_accuracy | 22 | 13/22 | 0.56 | 0.7 |
| groundedness | 16 | 11/16 | 0.77 | 0.8 |
| no_opinion_leakage | 4 | 3/4 | 0.75 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.30) |
| Q003 | query_entity_adherence (0.00) |
| Q004 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.67) |
| Q008 | tool_use_appropriateness (0.50), query_entity_adherence (0.50), factual_accuracy (0.00) |
| Q009 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q010 | query_entity_adherence (0.67) |
| Q011 | tool_use_appropriateness (0.50), factual_accuracy (0.00) |
| Q012 | tool_use_appropriateness (0.50), query_entity_adherence (0.60), factual_accuracy (0.00) |
| Q013 | tool_use_appropriateness (0.67), factual_accuracy (0.00) |
| Q014 | query_entity_adherence (0.50) |
| Q015 | query_entity_adherence (0.67) |
| Q020 | no_opinion_leakage (0.00) |
| Q021 | groundedness (0.00) |
| Q022 | query_entity_adherence (0.33), groundedness (0.50) |
| Q023 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q024 | groundedness (0.00) |
