# Eval Run: 20260518_230426_02d681
Prompt: v2 | Model: claude-sonnet-4-6 | Cases: 10

## Overall
Pass rate: 2/10 (20%)  |  Mean score: 0.85

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 3/8 | 0.77 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 7/8 | 0.94 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 8 | 8/8 | 0.94 | 0.7 |
| query_entity_adherence | 8 | 7/8 | 0.94 | 0.7 |
| factual_accuracy | 8 | 8/8 | 1.00 | 0.7 |
| groundedness | 7 | 2/7 | 0.50 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.30) |
| Q005 | groundedness (0.00) |
| Q007 | groundedness (0.70) |
| Q008 | groundedness (0.00) |
| Q009 | query_entity_adherence (0.50) |
