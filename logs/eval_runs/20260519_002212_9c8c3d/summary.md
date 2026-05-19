# Eval Run: 20260519_002212_9c8c3d
Prompt: v4 | Model: claude-sonnet-4-6 | Cases: 10

## Overall
Pass rate: 1/10 (10%)  |  Mean score: 0.88

## By Category (per case)
| Category | Rubrics | Cases Passed | Mean Score |
|---|---|---|---|
| accuracy | factual_accuracy, groundedness | 2/10 | 0.81 |
| retrieval | query_entity_adherence, tool_use_appropriateness | 8/10 | 0.95 |

## By Rubric
| Rubric | Cases Evaluated | Pass Rate | Mean Score | Threshold |
|---|---|---|---|---|
| tool_use_appropriateness | 10 | 10/10 | 0.97 | 0.7 |
| query_entity_adherence | 10 | 8/10 | 0.92 | 0.7 |
| factual_accuracy | 10 | 10/10 | 1.00 | 0.7 |
| groundedness | 10 | 2/10 | 0.61 | 0.8 |

## Failed Cases
| ID | Failing Rubrics |
|---|---|
| Q001 | groundedness (0.50) |
| Q002 | groundedness (0.30) |
| Q004 | groundedness (0.00) |
| Q005 | groundedness (0.70) |
| Q006 | query_entity_adherence (0.67), groundedness (0.70) |
| Q007 | groundedness (0.70) |
| Q008 | groundedness (0.70) |
| Q009 | query_entity_adherence (0.50) |
| Q010 | groundedness (0.50) |
