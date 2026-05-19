# Eval Run: 20260519_034520_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 9/24 (37%)  |  Mean score: 0.80

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 11/24 | 0.72 |
| boundaries | no_opinion_leakage | 3/4 | 0.75 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 18/24 | 0.90 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 24 | 22/24 | 0.91 | 0.7 |
| query_entity_adherence | 17 | 13/17 | 0.87 | 0.7 |
| factual_accuracy | 24 | 19/24 | 0.74 | 0.7 |
| groundedness | 19 | 11/19 | 0.70 | 0.8 |
| no_opinion_leakage | 4 | 3/4 | 0.75 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.50) |
| Q004 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.67) |
| Q010 | groundedness (0.50) |
| Q011 | groundedness (0.30) |
| Q012 | tool_use_appropriateness (0.50), groundedness (0.00) |
| Q013 | query_entity_adherence (0.67), factual_accuracy (0.50) |
| Q014 | groundedness (0.50) |
| Q015 | tool_use_appropriateness (0.67), factual_accuracy (0.00) |
| Q020 | no_opinion_leakage (0.00) |
| Q021 | groundedness (0.00) |
| Q024 | groundedness (0.00) |
