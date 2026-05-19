# Eval Run: 20260519_033636_35d029
Prompt: v6 | Model: claude-sonnet-4-6 | Cases: 10

## Overall
Pass rate: 3/10 (30%)  |  Mean score: 0.87

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 3/10 | 0.81 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 8/10 | 0.93 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 10/10 | 1.00 | 0.7 |
| query_entity_adherence | 10 | 8/10 | 0.85 | 0.7 |
| factual_accuracy | 10 | 10/10 | 0.99 | 0.7 |
| groundedness | 10 | 3/10 | 0.63 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.30) |
| Q004 | query_entity_adherence (0.00), groundedness (0.50) |
| Q005 | groundedness (0.70) |
| Q006 | query_entity_adherence (0.50), groundedness (0.50) |
| Q008 | groundedness (0.70) |
| Q010 | groundedness (0.10) |
