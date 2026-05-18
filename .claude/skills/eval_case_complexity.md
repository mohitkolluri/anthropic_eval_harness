# Skill: Eval Case Complexity Framework

Use this framework to generate and audit eval cases for the Wikipedia QA eval suite.
A question is only added to the suite if it passes the Easy Pass Filter and hits the Target Zone.

---

## The Four Axes

### Axis 1 — Search Friction
*How hard is it to retrieve the right Wikipedia article?*

| Level | Description | Example |
|---|---|---|
| L1 | Query maps directly to the article title | "Eiffel Tower height" |
| L2 | Right article exists but requires a non-obvious keyword | "War of Currents" instead of "Tesla vs Edison" |
| L3 | First search result is a plausible wrong article | Searching "Mercury" lands on the planet, not the element |
| L4 | Correct answer spans multiple articles; no single page has it | Comparing two people's birth years across two pages |

### Axis 2 — Parametric Trap
*How likely is the model to answer from training memory instead of Wikipedia?*

| Level | Description | Example |
|---|---|---|
| L1 | Model's training knowledge is correct — no trap | "What is photosynthesis?" |
| L2 | Common misconception exists but answer is intuitive once searched | "Hundred Years' War lasted 116 years" |
| L3 | Counterintuitive answer that contradicts widespread belief | "Antarctica is the largest desert" |
| L4 | Model's training data is likely stale or confidently wrong | Recently updated counts, revised scientific consensus |

### Axis 3 — Reasoning Load
*How much synthesis does forming the answer require?*

| Level | Description | Example |
|---|---|---|
| L1 | Extract one fact from one paragraph | Date of birth |
| L2 | Compare or combine two facts within the same article | Which of two events came first |
| L3 | Synthesise across multiple sections or multiple articles | Comparing two people's careers |
| L4 | Chain multiple steps or compute from retrieved facts | Difference in ages at death across two pages |

### Axis 4 — Answer Precision
*How exact does the correct answer need to be?*

| Level | Description | Example |
|---|---|---|
| L1 | Category is enough ("a country", "a scientist") | "Who invented X?" answered with a name |
| L2 | Specific named entity required | Exact country, exact person |
| L3 | Precise number, date, or unit required | Year, count, measurement |
| L4 | Multi-part answer where every part must be correct | Names + years + order of events |

---

## Easy Pass Filter

Apply before adding any question. If it fails any gate, raise the relevant axis.

1. **Parametric gate** — Can the agent answer correctly *without searching*? If yes → raise Axis 2
2. **Retrieval gate** — Is the answer in the first sentence of the obvious Wikipedia article? If yes → raise Axis 1
3. **Precision gate** — Is a vague answer acceptable? If yes → raise Axis 4
4. **Trap gate** — Is there a plausible wrong answer that feels right? If no → raise Axis 2 or 3

---

## Target Zone by Category

| Eval Category | Axis 1 | Axis 2 | Axis 3 | Axis 4 |
|---|---|---|---|---|
| factual_recall | L1–L2 | L3–L4 | L1–L2 | L2–L3 |
| entity_lookup | L1–L2 | L2–L3 | L2 | L2 |
| comparative | L2–L3 | L2–L3 | L2–L3 | L2–L3 |
| causal | L1–L2 | L2 | L3–L4 | L1–L2 |
| multi_call | L4 | L2–L3 | L3–L4 | L2–L4 |
| unanswerable | L1 | L3–L4 | L1 | L1 |
| ambiguous | L3–L4 | L2 | L1–L2 | L1–L2 |

**Minimum bar:** L3 or L4 on at least two axes.
**Hardest benchmark cases:** L3+ on all four axes — reserve for hill climbing targets.

---

## Scoring a Question (30-second audit)

```
Question: _______________________________________________

Axis 1 (Search Friction):   L__   reason: _______________
Axis 2 (Parametric Trap):   L__   reason: _______________
Axis 3 (Reasoning Load):    L__   reason: _______________
Axis 4 (Answer Precision):  L__   reason: _______________

Axes at L3+: ___   → Passes if ≥ 2
Easy Pass Filter: Parametric □  Retrieval □  Precision □  Trap □

Decision: ACCEPT / RAISE (axis __) / DROP
```

---

## Usage

When generating eval cases for a category:
1. Propose a question
2. Score it on all four axes using the audit template above
3. Apply the Easy Pass Filter
4. If it doesn't pass, either raise the complexity or discard
5. Only write to `evals/suite.jsonl` once all cases in the category are accepted
