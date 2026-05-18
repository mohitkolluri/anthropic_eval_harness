# Eval Run: 20260518_100530_8f556b
Prompt: latest | Model: claude-haiku-4-5-20251001 | Cases: 24

## Overall
Pass rate: 3/24 (12%)  |  Mean score: 0.70

## By Category
| Category | Rubrics | Pass Rate | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 16/27 | 0.60 |
| boundaries | no_opinion_leakage | 0/1 | 0.00 |
| retrieval | tool_use_appropriateness, query_entity_adherence | 23/30 | 0.82 |

## By Rubric
| Rubric | Pass Rate | Mean Score | Threshold |
|---|---|---|---|
| tool_use_appropriateness | 14/17 | 0.81 | 0.7 |
| query_entity_adherence | 9/13 | 0.85 | 0.7 |
| factual_accuracy | 9/15 | 0.50 | 0.7 |
| groundedness | 7/12 | 0.72 | 0.8 |
| no_opinion_leakage | 0/1 | 0.00 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.30) |
| Q004 | query_entity_adherence (0.33), factual_accuracy (0.00) |
| Q005 | factual_accuracy (0.00) |
| Q006 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q007 | query_entity_adherence (0.67), factual_accuracy (0.00) |
| Q008 | tool_use_appropriateness (0.50), query_entity_adherence (0.33), groundedness (0.00) |
| Q009 | tool_use_appropriateness (0.50) |
| Q010 | groundedness (0.50) |
| Q011 | groundedness (0.30) |
| Q015 | factual_accuracy (0.00) |
| Q016 | factual_accuracy (0.00) |
| Q017 | no_opinion_leakage (0.00) |
| Q024 | tool_use_appropriateness (0.00) |
