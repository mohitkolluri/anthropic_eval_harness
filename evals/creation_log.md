# Eval Suite Creation Log

Tracks the rationale, axis scores, and decisions for each eval case.
Reference skill: `.claude/skills/eval_case_complexity.md`

---

## Category: factual_recall

Target zone: Axis 1 (L1–L4) | Axis 2 (L3–L4) | Axis 3 (L3–L4) | Axis 4 (L3–L4)
Minimum bar: L3+ on at least 2 axes. No arithmetic required.

---

### Q001 — Darwin and Lincoln birth date coincidence
**Date added:** 2026-05-18
**Question:** What notable coincidence connects the birth dates of Charles Darwin and Abraham Lincoln?
**Expected:** Both born February 12, 1809

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L4 | Two entity articles required: "Charles Darwin" + "Abraham Lincoln" |
| 2 — Extraction Depth | L2 | Birth dates in opening sections of each article |
| 3 — Reasoning Load | L3 | Compare two dates across articles, recognise they match |
| 4 — Answer Precision | L4 | Exact shared date required (February 12, 1809) |

**Axes at L3+:** 2 (Axis 3, 4) ✅
**Decision:** ACCEPT
**Why it's hard:** Most assume a meaningful gap between the two figures. The answer — same day — is the surprise. Requires cross-referencing two entity articles with no arithmetic.

---

### Q002 — Statue of Liberty vs Eiffel Tower completion order
**Date added:** 2026-05-18
**Question:** Was the Eiffel Tower completed before or after the Statue of Liberty, and what were their respective completion years?
**Expected:** Statue of Liberty (1886) before Eiffel Tower (1889)

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L4 | Two entity articles: "Eiffel Tower" + "Statue of Liberty" |
| 2 — Extraction Depth | L2 | Completion years in infoboxes of each article |
| 3 — Reasoning Load | L3 | Compare two dates, determine order — no computation |
| 4 — Answer Precision | L4 | Order + both years required |

**Axes at L3+:** 2 (Axis 3, 4) ✅
**Decision:** ACCEPT
**Why it's hard:** Eiffel Tower is culturally more prominent, so most assume it came first. Both years and the ordering must be correct.
**Replaced:** Original Q002 was "telephone vs light bulb by how many years" — rejected for requiring subtraction.

---

### Q003 — First modern Olympic Games stats
**Date added:** 2026-05-18
**Question:** How many nations competed in the first modern Olympic Games, and how many athletic events were held?
**Expected:** 14 nations, 43 events

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L2 | Search "1896 Summer Olympics" — non-obvious year required |
| 2 — Extraction Depth | L3 | Both numbers in specific tables/sections, not the opening paragraph |
| 3 — Reasoning Load | L3 | Two independent facts from two different sections |
| 4 — Answer Precision | L4 | Two exact numbers required |

**Axes at L3+:** 3 (Axis 2, 3, 4) ✅
**Decision:** ACCEPT
**Why it's hard:** Requires knowing to search by year (1896) rather than "first modern Olympics", and both numbers are buried in structured sections rather than the lead.

---

### Q004 — First two countries to grant women's suffrage
**Date added:** 2026-05-18
**Question:** What were the first two countries to grant women the right to vote, and in what years did they do so?
**Expected:** New Zealand (1893), Australia (1902)

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L2 | "Women's suffrage" or "Timeline of women's suffrage" — article title not obvious |
| 2 — Extraction Depth | L3 | Answer is in a chronological list/table, not the opening paragraph |
| 3 — Reasoning Load | L3 | Identify top two entries from a ranked list |
| 4 — Answer Precision | L4 | Two country names + two years, all required |

**Axes at L3+:** 3 (Axis 2, 3, 4) ✅
**Decision:** ACCEPT
**Why it's hard:** Most know New Zealand was first, few know Australia was second. Both years must be precise. Answer lives in a list article, not a direct entity page.
**Replaced:** Original Q004 was "height difference between Everest and K2" — rejected for requiring subtraction.

---

## Category: entity_lookup

Target zone: Axis 1 (L2–L3) | Axis 2 (L2–L3) | Axis 3 (L2–L3) | Axis 4 (L2–L3)
Key rule: The entity name must NOT appear in the question. Agent must infer what to search for from a description, then return the entity name plus attributes.

---

### Q005 — Peace of Westphalia
**Date added:** 2026-05-18
**Question:** What was the name of the 1648 peace settlement that ended the Thirty Years' War, and what major political principle did it establish that still shapes international relations today?
**Expected:** Peace of Westphalia; principle of state sovereignty

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Must infer "Peace of Westphalia" from year + description — not named in question |
| 2 — Extraction Depth | L3 | Lasting political principle is in a legacy/significance section, not the opening |
| 3 — Reasoning Load | L3 | Identify treaty name + extract the enduring principle from the article body |
| 4 — Answer Precision | L3 | Treaty name + principle name both required |

**Axes at L3+:** 4 ✅  **Decision:** ACCEPT
**Why it's hard:** Entity absent from question. The "state sovereignty" principle requires reading beyond the intro. Both the treaty name and the principle must be correct.

---

### Q006 — Democritus
**Date added:** 2026-05-18
**Question:** Which ancient Greek thinker first proposed that all matter is made of tiny indivisible particles, and what did he call them?
**Expected:** Democritus; atomos (atoms)

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Must search "ancient Greek atomism" or "history of atomic theory" to surface Democritus |
| 2 — Extraction Depth | L2 | Once on the article, contribution is clearly described |
| 3 — Reasoning Load | L2 | Identify the thinker + the term coined |
| 4 — Answer Precision | L3 | Person's name + the term (Democritus; atomos) both required |

**Axes at L3+:** 2 ✅  **Decision:** ACCEPT
**Why it's hard:** Entity not named. Common misconception attributes atomic theory to Dalton or Einstein. The Greek origin requires the right search strategy.

---

### Q007 — INF Treaty
**Date added:** 2026-05-18
**Question:** What is the name of the 1987 arms control agreement between the US and the Soviet Union that eliminated an entire category of nuclear missiles, and what type of missiles were banned?
**Expected:** INF Treaty (Intermediate-Range Nuclear Forces Treaty); intermediate-range nuclear missiles

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Must infer "INF Treaty" from year + description — acronym not in question |
| 2 — Extraction Depth | L3 | Banned missile category in a specific provisions/scope section |
| 3 — Reasoning Load | L2 | Treaty name + weapons category |
| 4 — Answer Precision | L3 | Treaty name + specific missile class both required |

**Axes at L3+:** 3 ✅  **Decision:** ACCEPT
**Why it's hard:** Entity not named. "INF" must be inferred. Specific missile class (intermediate-range, 500–5,500 km) lives in a technical section.

---

### Q008 — Ikigai
**Date added:** 2026-05-18
**Question:** What is the Japanese term for the concept that describes a person's reason for being, defined as the overlap between what you love, what you are good at, what the world needs, and what you can be paid for?
**Expected:** Ikigai; four overlapping elements confirmed

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Non-Western concept with no obvious English keyword — must infer "Ikigai" |
| 2 — Extraction Depth | L3 | Four overlapping elements described in a specific conceptual section |
| 3 — Reasoning Load | L3 | Identify concept name + verify all four elements from the article |
| 4 — Answer Precision | L3 | Concept name + all four elements required |

**Axes at L3+:** 4 ✅  **Decision:** ACCEPT
**Why it's hard:** Entity not named. Non-English concept requiring cultural knowledge to derive the search term. All four intersection elements must be retrieved from the article body.

---

## Category: comparative

Target zone: Axis 1 (L2–L3) | Axis 2 (L2–L3) | Axis 3 (L2–L3) | Axis 4 (L2–L3)
Key rule: Requires retrieving attributes from two or more entities and synthesising a comparison. No arithmetic — order, overlap, or relative scale only.

---

### Q009 — Pacific Ocean vs all landmasses
**Date added:** 2026-05-18
**Question:** Is the Pacific Ocean larger in area than all of Earth's landmasses combined?
**Expected:** Yes — Pacific ~165M km² > all land ~149M km²

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Two lookups: "Pacific Ocean" + Earth land area article |
| 2 — Extraction Depth | L3 | Area figures in specific geography/statistics sections |
| 3 — Reasoning Load | L3 | Synthesise two different measurements, compare scales |
| 4 — Answer Precision | L2 | Yes/no with supporting values |

**Axes at L3+:** 2 ✅  **Decision:** ACCEPT
**Why it's hard:** Almost everyone assumes the answer is no. The counterintuitive yes requires sourcing both figures from different articles.

---

### Q010 — Shakespeare and the two Elizabeths
**Date added:** 2026-05-18
**Question:** Was Shakespeare's life more contemporary with Queen Elizabeth I or Queen Elizabeth II?
**Expected:** Elizabeth I — Shakespeare (1564–1616) overlapped her reign (1558–1603)

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Three entity articles: "Shakespeare", "Elizabeth I", "Elizabeth II" |
| 2 — Extraction Depth | L2 | Lifespans in opening sections of each article |
| 3 — Reasoning Load | L3 | Compare three overlapping timelines to determine shared era |
| 4 — Answer Precision | L2 | Named answer: Elizabeth I |

**Axes at L3+:** 2 ✅  **Decision:** ACCEPT
**Why it's hard:** Elizabeth II is more culturally present in modern memory. Three-entity timeline comparison required.

---

### Q011 — Roman Empire and Han Dynasty overlap
**Date added:** 2026-05-18
**Question:** Did the Roman Empire and the Han Dynasty of China exist at the same time, and if so during which period did they overlap?
**Expected:** Yes — overlapped 27 BC to 220 AD

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Two entity articles: "Roman Empire" + "Han Dynasty" |
| 2 — Extraction Depth | L3 | Founding and fall dates in specific historical sections |
| 3 — Reasoning Load | L3 | Compare two timelines, identify the overlapping window |
| 4 — Answer Precision | L3 | Yes/no + the overlapping period (27 BC – 220 AD) |

**Axes at L3+:** 3 ✅  **Decision:** ACCEPT
**Why it's hard:** Most people think of Rome and China as isolated civilisations. Temporal overlap requires reading dates from two separate articles.

---

### Q012 — Great Pyramid vs Iliad
**Date added:** 2026-05-18
**Question:** Was the Great Pyramid of Giza completed before or after Homer composed the Iliad?
**Expected:** Before — Pyramid ~2560 BC, Iliad ~800 BC

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Two entity articles: "Great Pyramid of Giza" + "Iliad" |
| 2 — Extraction Depth | L3 | Construction/composition dates in specific historical sections |
| 3 — Reasoning Load | L2 | Compare two dates, determine order |
| 4 — Answer Precision | L3 | Order + approximate dates for both required |

**Axes at L3+:** 2 ✅  **Decision:** ACCEPT
**Why it's hard:** Both feel vaguely "ancient" — the ~1,760-year gap between them is not intuitively obvious.

---

## Category: causal

Target zone: Axis 1 (L1–L2) | Axis 2 (L2–L3) | Axis 3 (L3–L4) | Axis 4 (L2–L3)
Key rule: 3 questions use transitive A→B→C chains (intermediate step must be named). 1 question uses a direct A→B cause. Multi-factor questions about a single event are NOT this category.

---

### Q013 — Fall of Constantinople → Columbus (A→B→C)
**Date added:** 2026-05-18
**Question:** How did the fall of Constantinople in 1453 contribute to Christopher Columbus's voyage to the Americas in 1492?
**Chain:** Constantinople falls (A) → Ottoman trade blockade (B) → Europe seeks sea routes → Columbus sails (C)

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Two articles: "Fall of Constantinople" + "Christopher Columbus" or "Age of Discovery" |
| 2 — Extraction Depth | L3 | Causal link to exploration in legacy/consequences sections |
| 3 — Reasoning Load | L4 | Must trace A→B→C: political event → trade disruption → exploration motive |
| 4 — Answer Precision | L3 | Intermediate step B (Ottoman trade blockade) must be identified |

**Axes at L3+:** 3 ✅  **Decision:** ACCEPT

---

### Q014 — Printing press → Protestant Reformation (A→B→C)
**Date added:** 2026-05-18
**Question:** How did Gutenberg's invention of the printing press in the 1440s contribute to the Protestant Reformation?
**Chain:** Printing press (A) → mass distribution of texts (B) → Luther's ideas spread faster than suppression (C)

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Two articles: "Printing press" + "Protestant Reformation" |
| 2 — Extraction Depth | L3 | Connection in legacy/impact sections of each article |
| 3 — Reasoning Load | L4 | Must trace A→B→C: technology → information distribution → religious movement |
| 4 — Answer Precision | L3 | Intermediate mechanism (mass distribution of ideas) must be named |

**Axes at L3+:** 3 ✅  **Decision:** ACCEPT

---

### Q015 — Cotton gin → slavery expansion (A→B→C)
**Date added:** 2026-05-18
**Question:** How did the invention of the cotton gin in 1793 lead to the expansion of slavery in the American South?
**Chain:** Cotton gin (A) → cotton processing cheap/fast → demand for raw cotton surges (B) → more land cultivated → more enslaved labour needed (C)

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Two articles: "Cotton gin" + "Slavery in the United States" |
| 2 — Extraction Depth | L3 | Economic consequences in specific sections |
| 3 — Reasoning Load | L4 | Must trace A→B→C: labour-saving device → increased demand → increased enslaved population |
| 4 — Answer Precision | L3 | Counterintuitive intermediate step B must be explained |

**Axes at L3+:** 3 ✅  **Decision:** ACCEPT
**Trap:** A labour-saving device expanding slavery is counterintuitive — strongest test of causal reasoning.

---

### Q016 — Challenger disaster (direct A→B)
**Date added:** 2026-05-18
**Question:** What caused the Space Shuttle Challenger disaster in 1986, and what specific component failed?
**Chain:** Cold temperature (A) → O-ring seal failure (B) → structural failure → disaster

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L2 | "Space Shuttle Challenger disaster" — specific named article |
| 2 — Extraction Depth | L3 | Technical cause in a dedicated section, not the opening |
| 3 — Reasoning Load | L3 | Component + the environmental condition that caused it to fail |
| 4 — Answer Precision | L3 | Component name + failure condition both required (O-ring; cold temperature) |

**Axes at L3+:** 2 ✅  **Decision:** ACCEPT
**Note:** Direct A→B cause, intentionally simpler than the transitive chain questions.

---

## Category: unanswerable

Target zone: All axes L1 — agent must NOT search and must refuse cleanly.
Key rule: Each question tests a distinct refusal trigger. Zero searches expected. Clean refusal line required.

| Refusal type | Q | Trigger |
|---|---|---|
| Opinion / value judgement | Q017 | Subjective — no factual answer exists |
| Future prediction | Q018 | Event hasn't happened |
| Real-time data | Q019 | Changes by the second, not encyclopedic |
| Personal / advisory | Q020 | Specific to the user, not answerable generally |

---

### Q017 — Opinion
**Date added:** 2026-05-18
**Question:** Is democracy the best form of government?
**Expected:** "This is a matter of opinion and I cannot answer it."
**Trap:** Agent might present "both sides" or cite Wikipedia's politics articles instead of refusing.

---

### Q018 — Future prediction
**Date added:** 2026-05-18
**Question:** Who will win the next FIFA World Cup?
**Expected:** "This question cannot be answered from Wikipedia."
**Trap:** Agent might search "FIFA World Cup" and speculate from recent tournament results.

---

### Q019 — Real-time data
**Date added:** 2026-05-18
**Question:** What is the current stock price of Apple Inc.?
**Expected:** "This question cannot be answered from Wikipedia."
**Trap:** Agent might search "Apple Inc." and report a historical or estimated figure as if current.

---

### Q020 — Personal / advisory
**Date added:** 2026-05-18
**Question:** What should I invest my savings in right now?
**Expected:** "This question cannot be answered from Wikipedia."
**Trap:** Agent might give generic investment advice or search "investment strategies."

---

## Category: ambiguous

Target zone: Axis 1 (L3–L4) | Axis 2 (L2–L3) | Axis 3 (L2–L3) | Axis 4 (L2–L3)
Expected behaviour: Acknowledge both/all interpretations → pick the most prominent one and answer it → ask user to be more specific.
Ground truth markers: agent must name competing interpretations AND use "specific" or equivalent.
Dropped: Q023 "Who is Artemis?" — "who" biases toward the deity, reducing genuine ambiguity.

---

### Q021 — Mercury
**Date added:** 2026-05-18
**Question:** Tell me about Mercury.
**Competitors:** Planet / chemical element / Roman god / Freddie Mercury
**Expected:** Acknowledges all, answers planet (most prominent), asks for clarification

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L4 | Disambiguation page with 4 strong competitors |
| 2 — Extraction Depth | L2 | Once on right article, description in opening |
| 3 — Reasoning Load | L3 | Must pick one interpretation, note others exist |
| 4 — Answer Precision | L2 | Description of chosen interpretation |

**Axes at L3+:** 2 ✅  **Decision:** ACCEPT

---

### Q022 — Ajax
**Date added:** 2026-05-18
**Question:** What can you tell me about Ajax?
**Competitors:** Greek hero / AFC Ajax (football) / cleaning product / JavaScript pattern
**Expected:** Acknowledges key competitors, answers Greek hero (most prominent), asks for clarification

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L4 | Disambiguation across four genuinely competing articles |
| 2 — Extraction Depth | L3 | Useful answer requires reading beyond the opening |
| 3 — Reasoning Load | L3 | Must disambiguate across four strong candidates |
| 4 — Answer Precision | L2 | Description of chosen interpretation |

**Axes at L3+:** 3 ✅  **Decision:** ACCEPT

---

### Q023 — Jaguar
**Date added:** 2026-05-18
**Question:** What is the Jaguar?
**Competitors:** Animal (big cat) / Jaguar Cars
**Expected:** Acknowledges animal and car brand, answers animal (most prominent), asks for clarification

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L3 | Two strong competing articles: animal + car brand |
| 2 — Extraction Depth | L2 | Description in opening section |
| 3 — Reasoning Load | L3 | Must pick between equally plausible interpretations |
| 4 — Answer Precision | L2 | Description of chosen interpretation |

**Axes at L3+:** 2 ✅  **Decision:** ACCEPT

---

### Q024 — Michael records
**Date added:** 2026-05-18
**Question:** What records did Michael break?
**Competitors:** Michael Jordan (basketball) / Michael Jackson (music)
**Expected:** Names both Michaels, picks one and answers it, explicitly asks for clarification

| Axis | Score | Reason |
|---|---|---|
| 1 — Search Friction | L4 | "Michael" alone is maximally ambiguous — no obvious primary article |
| 2 — Extraction Depth | L3 | Records in specific career sections, not opening paragraphs |
| 3 — Reasoning Load | L3 | Must identify both famous Michaels, pick one, answer records |
| 4 — Answer Precision | L3 | Both names + specific records + clarification request all required |

**Axes at L3+:** 3 ✅  **Decision:** ACCEPT
**Why it's strongest:** Both Michaels are equally prominent. No disambiguation page resolves it. The agent must make a judgment call, name both, and ask for more context.

---
