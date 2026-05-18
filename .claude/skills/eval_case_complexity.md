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

### Axis 2 — Extraction Depth
*Once the right Wikipedia article is retrieved, how hard is it to locate the answer within it?*

| Level | Description | Example |
|---|---|---|
| L1 | Answer is in the opening paragraph or infobox | Birth year, population of a capital city |
| L2 | Answer requires reading a specific named section | Finding a record in the "Career" or "Legacy" section |
| L3 | Answer is in a table, footnote, or requires cross-referencing within the article | Specific stat in a data table; figure mentioned only in a footnote |
| L4 | Answer requires synthesising across multiple sections or is not explicitly stated — must be inferred or computed from scattered data points | Trend derived from multiple tables; fact implied but never directly written |

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

1. **Search gate** — Does one obvious keyword find the right article immediately? If yes → raise Axis 1
2. **Extraction gate** — Is the answer in the opening paragraph or infobox of the article? If yes → raise Axis 2
3. **Reasoning gate** — Can the answer be copied verbatim from one sentence? If yes → raise Axis 3
4. **Precision gate** — Is a vague or partial answer acceptable? If yes → raise Axis 4

---

## Target Zone by Category

| Eval Category | Axis 1 | Axis 2 | Axis 3 | Axis 4 |
|---|---|---|---|---|
| factual_recall | L1–L4 | L3–L4 | L3–L4 | L3–L4 |
| entity_lookup | L2–L3 | L2–L3 | L2–L3 | L2–L3 |
| comparative | L2–L3 | L2–L3 | L2–L3 | L2–L3 |
| causal | L1–L2 | L2–L3 | L3–L4 | L2–L3 |
| multi_call | — | — | — | — | (retired — covered implicitly by comparative, causal, factual_recall) |
| unanswerable | L1 | L1 | L1 | L1 |
| ambiguous | L3–L4 | L2–L3 | L2–L3 | L2–L3 |

**Minimum bar:** L3 or L4 on at least two axes.
**Hardest benchmark cases:** L3+ on all four axes — reserve for hill climbing targets.

### entity_lookup definition

The question **does not name the entity** — the agent must infer what to search for from a description, then retrieve the entity name plus attributes. Axis 1 is L2–L3 because the search term must be derived, not read directly from the question.

| Question form | Entity named? | Category |
|---|---|---|
| "What is the Magna Carta?" | ✅ yes | NOT entity_lookup — use factual_recall |
| "What is the name of the 1215 royal charter that limited the English king's power?" | ❌ no | entity_lookup ✅ |

---

### factual_recall vs multi_call

`factual_recall` always produces **one answer**, even if multiple entity articles are needed to derive it.
`multi_call` asks for **multiple independent answers** in a single question.

| Question | Pattern | Category |
|---|---|---|
| "How many years apart were Darwin and Lincoln born?" | 2 entities → 1 computed answer | `factual_recall` (Axis 1: L4) |
| "What are the capitals of Japan and Brazil?" | 2 entities → 2 independent answers | `multi_call` |
| "Which was invented first — the telephone or the radio, and by how many years?" | 2 entities → 1 ordered answer + computed delta | `factual_recall` (Axis 1: L4) |

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
