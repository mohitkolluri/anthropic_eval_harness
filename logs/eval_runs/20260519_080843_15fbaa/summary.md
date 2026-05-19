# Eval Run: 20260519_080843_15fbaa
Prompt: v7 | Model: claude-sonnet-4-6 | Cases: 10

## Overall
Pass rate: 2/10 (20%)  |  Mean score: 0.85

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 5/10 | 0.78 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 7/10 | 0.91 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 8/10 | 0.90 | 0.7 |
| query_entity_adherence | 10 | 9/10 | 0.93 | 0.7 |
| factual_accuracy | 10 | 10/10 | 0.97 | 0.7 |
| groundedness | 8 | 3/8 | 0.55 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | tool_use_appropriateness (0.50) |
| Q003 | groundedness (0.70) |
| Q004 | groundedness (0.00) |
| Q005 | groundedness (0.70) |
| Q006 | query_entity_adherence (0.50) |
| Q007 | groundedness (0.00) |
| Q008 | groundedness (0.00) |
| Q010 | tool_use_appropriateness (0.50) |
