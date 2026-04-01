# ATANT v1.0 — A Standard for Testing AI Continuity

**Automated Test for Acceptance of Narrative Truth**

**Published by:** Kenotic Labs
**Author:** Samuel Sameer Tanguturi, Founder
**Version:** 1.0
**Date:** April 2026
**Status:** Public Draft

---

## Abstract

This document defines **ATANT** (Automated Test for Acceptance of Narrative Truth) — an open evaluation framework for measuring whether an AI system possesses **continuity**: the ability to persist, update, disambiguate, and reconstruct meaningful context across time, rather than resetting at every interaction.

ATANT is, to our knowledge, the first published framework for formally evaluating AI continuity. It is system-agnostic, LLM-independent, and grounded in narrative-based testing methodology. Any AI system claiming to maintain continuity across sessions can be evaluated against this framework.

ATANT was developed by Kenotic Labs as part of the engineering work behind the continuity layer architecture. It has been validated across 5 test suite iterations against 250 narratives comprising 1,835 verification questions across 6 life domains:

- **Isolated mode:** 250 stories, 1,835/1,835 questions correct (100%)
- **Cumulative mode (50 narratives coexisting):** 304/304 questions correct (100%)
- **Cumulative mode (250 narratives coexisting):** 1,761/1,835 questions correct (96% — active frontier)

The cumulative result is the headline. Isolated mode proves the pipeline works. Cumulative mode proves **continuity** works — when 250 different life narratives share the same database, the system still retrieves the right fact for the right context.

ATANT is not a one-time scorecard. It is a **sequenced methodology** — a roadmap for building and validating continuity systems in the right order. Isolated first, then stress, then cumulative, then scale. Write path first, then read path. Single narrative first, then multi-narrative. The value is not any single test. It is the sequence.

ATANT is also not frozen. v1.0 defines the foundation. Future versions will add reconstruction quality metrics, multi-language narratives, proactive behavior testing, and decay validation. The standard grows as the field grows.

This framework is published to establish a shared definition, a shared methodology, and a shared evaluation sequence for AI continuity — a property the industry increasingly needs but has not yet formally defined or measured.

---

## Table of Contents

1. [Motivation](#1-motivation)
2. [Defining Continuity](#2-defining-continuity)
3. [The 7 Required Properties of Continuity](#3-the-7-required-properties-of-continuity)
4. [ATANT Methodology](#4-atant-methodology)
5. [The Checkpoint System](#5-the-checkpoint-system)
6. [Narrative Test Corpus](#6-narrative-test-corpus)
7. [Story Specification](#7-story-specification)
8. [Compliance Levels](#8-compliance-levels)
9. [Evaluation Protocol](#9-evaluation-protocol)
10. [Reference Implementation Results](#10-reference-implementation-results)
11. [Versioning and Governance](#11-versioning-and-governance)
12. [Glossary](#12-glossary)

---

## 1. Motivation

Most AI systems today are **session-based**. A user says something. The system responds. The moment ends. Whatever survives is prompt context, chat history, or retrieved notes.

This is adequate for single-turn tasks. It is inadequate for any system that claims to maintain a relationship with a user over time.

Human life is not made of isolated prompts. It is made of unfinished situations, changing states, recurring concerns, relationships, timing, logistics, moods, plans, identities, and commitments. AI systems that serve humans across time need more than intelligence-in-the-moment. They need **presence-over-time**.

The industry has produced many partial solutions:

- **Long context windows** keep recent material alive temporarily.
- **RAG pipelines** retrieve semantically similar text from storage.
- **Profile layers** hold static preferences.
- **Chat history** preserves a transcript.
- **Vector databases** store embeddings for similarity search.

None of these, individually or combined, produce continuity. They are components. Continuity is the **logic layer** that decides what persists, in what form, what has changed, what still matters, and how to reconstruct it.

Despite growing recognition of this gap, the industry lacks:

1. A formal definition of what continuity means as a system property.
2. A set of testable requirements that any continuity system must satisfy.
3. A benchmark that measures continuity rather than retrieval accuracy alone.

ATANT addresses all three.

---

## 2. Defining Continuity

**Continuity** is the system property that enables an AI to carry forward what still matters from prior interactions, update it when reality changes, and reconstruct useful context later — in the right form, at the right time, for the right situation.

### Continuity vs. Memory

Memory stores the past.
Continuity keeps the right parts of the past alive in the present.

A database can store `(user, partner_name, Mia)`. That is memory.
A continuity system can answer "Tell me about my relationship" with a reconstruction that includes Mia, where she lives, how the user feels about her, what changed last week, and what remains unresolved. That is continuity.

### Continuity vs. Retrieval

Retrieval says: *Here are some related past things.*
Continuity says: *Here is the current living state of the situation, including what changed, what still matters, and what should happen next.*

The difference is between searching and understanding.

### The Formal Definition

> **Continuity** is the architectural layer between AI interaction and AI relationship. It is the logic that determines: what from an interaction should persist, in what form it should persist, what is still active versus resolved, what changed since last time, what matters now versus later, when something should re-enter the interaction, and how to preserve both historical state and current state without conflating them.

Continuity is a **layer**, not a feature. It sits below the intelligence layer (the LLM) and above the storage layer (the database). It governs the write path (what gets stored and how) and the read path (what gets reconstructed and when).

---

## 3. The 7 Required Properties of Continuity

Any system claiming to implement continuity MUST satisfy all 7 properties. Each property is defined abstractly and paired with a testable requirement.

**On derivation:** These properties were not derived from theory and then tested. They were discovered empirically — by building a continuity system, running it against hundreds of real-world narratives, and identifying what breaks when each property is absent. Remove persistence and the system forgets between sessions. Remove update handling and the system contradicts itself. Remove disambiguation and the system conflates different people's lives. Each property represents a failure mode that was observed, diagnosed, and formalized. They are foundational in the same way that normalization rules in database theory are foundational: there are a finite number of them, they are identifiable from practice, they are independently defensible, and additional properties can be built upon them.

### Property 1: Persistence Beyond Session

**Definition:** Continuity state survives session termination. If the model shuts down, the app closes, the device restarts, or the user returns after an arbitrary delay — the continuity state still exists and is recoverable.

**Testable Requirement:** After ingesting a set of facts, terminate the process. Restart with a new process. All previously ingested facts MUST be retrievable with identical accuracy.

**What this excludes:** Systems that rely solely on in-context memory, conversation history buffers, or ephemeral caches.

### Property 2: Update Handling

**Definition:** Real life changes. Appointments move. Relationships evolve. Plans are revised. A continuity system MUST preserve both historical state and current state without conflating them. "I was nervous before, I feel better now" must become ordered reality, not noise.

**Testable Requirement:** After ingesting a fact, ingest an update to that fact. Query for the current state — the system MUST return the updated value. Query for what changed — the system MUST distinguish previous state from current state.

**What this excludes:** Append-only systems that cannot represent state change. Systems where updates create duplicate or contradictory entries.

### Property 3: Temporal Ordering

**Definition:** Not just what happened, but when, in what sequence, and with what current status. "Tomorrow" must resolve to an actual date. "Moved to Wednesday" must overwrite timing while preserving the fact of change. "Last time this failed" must remain distinct from "this is what we do now."

**Testable Requirement:** Ingest facts with temporal references (relative and absolute). Query for temporal state — the system MUST return correctly resolved dates, correct sequencing, and correct current status of time-sensitive facts.

**What this excludes:** Systems that store timestamps but cannot reason about relative time, sequence, or temporal status (past / active / upcoming / overdue).

### Property 4: Disambiguation

**Definition:** Two people can have similar events. Two entities can be involved in similar processes. Two feelings can exist around two different situations. Continuity MUST keep subjects, entities, and contextual attachments correctly separated.

**Testable Requirement:** Ingest facts from two or more distinct narratives that share overlapping vocabulary (e.g., two different job interviews, two different people named "Sarah"). Query for each independently — the system MUST return the correct facts for the correct narrative without cross-contamination.

**What this excludes:** Systems that rely solely on semantic similarity for retrieval, which will conflate similar-but-distinct narratives.

### Property 5: Reconstruction

**Definition:** A continuity system answers not only direct factual questions, but **situation-level** questions. Not just "When is my interview?" but "Summarize my current situation," "Why am I anxious?," "What am I preparing for?," "What changed since last time?" This requires combining multiple stored traces into a coherent present-tense state.

**Testable Requirement:** After ingesting a multi-turn narrative spanning multiple facts across emotional, temporal, relational, and logistical dimensions — the system MUST retrieve a set of connected, relevant facts sufficient to reconstruct the situation. Retrieval of isolated fragments is insufficient.

**What this excludes:** Systems that can only answer single-fact lookup questions. Systems that return ranked chunks without coherence.

### Property 6: Model Independence

**Definition:** If continuity is real, it does not live inside one model session. One model can write the situation. Another model — or a future version of the same model — can read and reconstruct it later. The continuity layer is below the intelligence layer, not trapped inside it.

The intelligence layer is not static. Today it is large language models. Tomorrow it may be vision models, world models, hearing models, embodied agents, or architectures that do not yet exist. A continuity standard tied to any specific model architecture dies when that architecture is superseded. The 7 properties and 10 checkpoints defined in this framework do not reference LLMs because they should not. They describe what continuity *is* — not what today's AI happens to look like. A standard is a pillar. It does not sway every time the field changes direction.

**Testable Requirement:** Ingest facts using one model (or no model at all). Retrieve and verify using a different model or process. Accuracy MUST NOT degrade due to the model change.

**What this excludes:** Systems where continuity depends on a specific model's hidden state, fine-tuning, or in-context learning that cannot be transferred.

### Property 7: Operational Usefulness

**Definition:** Continuity matters beyond personal chat. In a clinic, library, service desk, robotic system, or workflow — continuity means the system does not restart from zero. It carries forward repeated context, user needs, prior failures, preferences, and unresolved tasks.

**Testable Requirement:** The continuity system MUST function across at least 2 distinct application domains (e.g., personal assistant + institutional service) without architectural modification to the continuity layer itself. Domain-specific adaptations may exist above the layer, but the persistence, update, temporal, disambiguation, and reconstruction logic MUST be shared.

**What this excludes:** Systems that are hardcoded to a single use case and cannot generalize.

---

## 4. ATANT Methodology

ATANT tests continuity through **narrative simulation** — not synthetic benchmarks, not isolated fact pairs, but realistic multi-turn conversations that mirror how humans actually communicate with AI systems over time.

### 4.1 Core Principles

**Principle 1: Model Agnosticism**

ATANT evaluates the continuity layer, not the intelligence layer above it. Tests inject text directly into the write path and verify output directly from the read path. No model — language, vision, or otherwise — is included in the evaluation loop.

This is the foundational design decision. The continuity layer must be correct independent of whatever intelligence layer sits on top of it. If the engines are proven correct without a model, then the only remaining variable when any model is added is: *"Does the model use the facts it's given?"* That is an integration problem, not an architecture problem. ATANT tests the architecture.

**Principle 2: Narrative Realism**

Test inputs are naturalistic multi-turn conversations, not sanitized fact lists. People do not speak in database format. They say "I'm nervous because I have an interview at Google next Tuesday at 3 PM and I need to leave by 1:30 because the drive is long." That single utterance contains identity, event, time, emotional state, entity, intent, preparation target, and logistics. A continuity system must handle that.

**Principle 3: Write Path + Read Path Verification**

ATANT tests both directions:

- **Write path:** Did the system correctly decompose, classify, and store the facts from the input?
- **Read path:** Given a question, did the system correctly retrieve, match, and reconstruct the answer from stored state?

A system that stores perfectly but retrieves poorly fails. A system that retrieves well from poor storage fails. Both paths must be correct.

**Principle 4: Determinism**

Same input, same output, every time. ATANT tests run deterministically. There is no sampling variance, no randomness in evaluation. A system either passes or it does not.

**Principle 5: Progressive Difficulty (The Sequence)**

ATANT is not a single test. It is a **sequence** — an ordered methodology for building and validating continuity systems. Each phase builds on the previous one and tests a harder property:

1. **Isolated → Stress:** Does the system work? Does it generalize?
2. **Stress → Cumulative:** Does it work when narratives coexist and compete?
3. **Cumulative → Scale:** Does disambiguation hold under load?
4. **Scale → Proactive:** Does the system know when to surface information unprompted?
5. **Proactive → Latency:** Is it fast enough to be useful in real time?

A team building a continuity system should follow this sequence. If isolated mode fails, cumulative mode will be worse. If cumulative fails at 50, it will fail harder at 250. The sequence tells you where you are, what to fix next, and when you're ready for the next level. That is the value of ATANT — not any single score, but the roadmap for knowing where your system stands.

### 4.2 What ATANT Does NOT Test

- **Response quality** — ATANT does not evaluate how well the LLM phrases its answer. It evaluates whether the correct facts are available to the LLM.
- **User experience** — ATANT does not measure latency, tone, personality, or interface quality.
- **Safety or alignment** — ATANT does not test for harmful outputs, bias, or policy compliance.
- **General knowledge** — ATANT explicitly includes general knowledge queries as negative examples (the system should NOT retrieve personal facts for "What is photosynthesis?").

---

## 5. The Checkpoint System

ATANT defines **10 standard checkpoints** that verify correctness at each stage of the continuity pipeline. Checkpoints are grouped into write-path verification (CP1–CP4), read-path verification (CP5–CP8), and cross-cutting concerns (CP9–CP10).

Implementations may name their internal components differently. The checkpoints define **what must be verified**, not how the system is architected.

### Write-Path Checkpoints

| CP | Name | What It Verifies | Pass Criteria |
|----|------|-------------------|---------------|
| CP1 | **Input Classification** | The system correctly classifies the type and intent of the input utterance. Personal statements, questions, updates, general knowledge queries, and noise are distinguished. | Classification matches expected type for each test utterance. |
| CP2 | **Fact Extraction & Storage** | The system extracts structured facts from the input and stores them durably. For a statement like "My sister Emily lives in Portland," the system must store the relationship (sister), the name (Emily), and the location (Portland) as retrievable structured data. | All expected factual keywords are present in storage after ingestion. |
| CP3 | **Predictive Indexing** | The system generates predicted queries at write time — anticipating how the stored fact might later be asked about. This enables reconstruction, not just retrieval. | At least 1 predicted query exists per stored fact. |
| CP4 | **Type Tagging** | Stored facts are tagged with semantic types (PERSON, PLACE, ORGANIZATION, TIME, EMOTION, etc.) enabling structured retrieval. | Type tags match expected categories. |

### Read-Path Checkpoints

| CP | Name | What It Verifies | Pass Criteria |
|----|------|-------------------|---------------|
| CP5 | **Query Classification** | The system correctly classifies incoming questions by type — factual recall, temporal query, emotional state query, situation summary, general knowledge, etc. | Query type matches expected classification. |
| CP6 | **Structural Matching** | The system identifies the correct stored fact(s) that answer the query, using structural matching rather than (or in addition to) semantic similarity alone. | Correct fact appears in top-k retrieval candidates. |
| CP7 | **Convergence** | For reconstruction queries (situation-level questions), the system activates multiple relevant traces and converges them into a coherent answer set. | Convergence gate activates and returns a multi-fact candidate set. |
| CP8 | **Final Answer Correctness** | The system's final retrieved answer contains the expected factual content. This is the **primary evaluation checkpoint** — all others are diagnostic. | All expected keywords present in the final answer. |

### Cross-Cutting Checkpoints

| CP | Name | What It Verifies | Pass Criteria |
|----|------|-------------------|---------------|
| CP9 | **Temporal Reasoning** | Temporal expressions are extracted, resolved, and reasoned about correctly. Relative times ("next Tuesday") resolve to dates. Updates ("moved to Wednesday") modify existing temporal facts. | Temporal type and direction match expected values. |
| CP10 | **Contextual Adaptation** | The system detects emotional and contextual signals in the input and adjusts its internal state accordingly (e.g., detecting anxiety, vulnerability, excitement). | Detected emotion and adaptation direction match expected values. |

### Checkpoint Hierarchy

**CP8 is the definitive checkpoint.** A system that passes CP8 for all questions has demonstrated that the correct facts are retrievable. Checkpoints CP1–CP7 and CP9–CP10 are **diagnostic** — they identify where failures occur in the pipeline when CP8 fails.

A system MAY achieve CP8 correctness through different internal architectures. The standard does not mandate how the system is built — only that the end-to-end result is correct and that the diagnostic checkpoints provide visibility into why.

---

## 6. Narrative Test Corpus

### 6.1 Design Philosophy

ATANT stories are **narrative simulations** — realistic multi-turn conversations that a human might have with an AI system over hours, days, or weeks. Each story tests a specific combination of continuity capabilities within a naturalistic context.

Stories are NOT:
- Synthetic fact pairs ("store X, retrieve X")
- Isolated QA benchmarks
- Adversarial prompts designed to break systems

Stories ARE:
- Multi-turn conversations spanning simulated time
- Emotionally grounded (people feel things; the system should notice)
- Temporally complex (time references, updates, deadlines)
- Linguistically natural (pronouns, digressions, multi-fact utterances)
- Domain-diverse (career, health, relationships, learning, daily life, life events)

### 6.2 Life Domain Coverage

The standard corpus covers 6 **life domains** — not productivity domains, not enterprise workflows, not corporate use cases. This is intentional. ATANT tests continuity for *human life*: personal, private, emotional, messy, contradictory, and ongoing. The domains were chosen because continuity is fundamentally about carrying a person's life forward, not about task management. Operational and enterprise domains can be added in future versions, but the foundation is human narrative truth.

The 6 domains:

| Domain | What It Tests | Example Scenarios |
|--------|---------------|-------------------|
| **Career** | Professional identity, workplace relationships, goals, timelines | Job interviews, promotions, side projects, layoffs, salary negotiations |
| **Relationships** | Interpersonal dynamics, emotional states, social logistics | Partners, family, friendships, conflicts, social events, relationship changes |
| **Health** | Medical facts, fitness goals, emotional wellbeing, care continuity | Diagnoses, medications, fitness routines, diet changes, recovery |
| **Learning** | Skill development, educational progress, intellectual interests | Courses, certifications, study plans, reading, mentorship |
| **Daily Life** | Routines, logistics, household management, hobbies | Errands, commutes, home projects, pets, daily scheduling |
| **Life Events** | Major transitions, milestones, grief, celebration | Moves, births, deaths, marriages, divorces, graduations, retirements |

### 6.3 Corpus Scale

The ATANT v1.0 corpus defines the following minimum scale:

| Tier | Stories | Questions | Purpose |
|------|---------|-----------|---------|
| **Core** (required) | 50 | ~300 | Prove basic continuity across all 6 domains |
| **Stress Round 1** | 50 | ~370 | Prove generalization (not overfitting to core stories) |
| **Stress Round 2** | 50 | ~380 | Introduce novel linguistic patterns |
| **Stress Round 3** | 50 | ~380 | Edge cases and ambiguous constructions |
| **Stress Round 4** | 50 | ~400 | Adversarial constructions and maximum complexity |
| **Total** | **250** | **~1,830** | |

The core 50 stories are **required** for any ATANT compliance claim. Stress rounds are required for higher compliance levels (see Section 8).

### 6.4 Adversarial Patterns

Stories systematically include patterns known to challenge continuity systems:

| Pattern | Example | What It Tests |
|---------|---------|---------------|
| Multi-fact utterance | "My sister Emily lives in Portland and works at Nike" | Extracting multiple facts from one statement |
| Shared subject | "My brother and I went hiking last Saturday" | Correctly attributing actions to multiple subjects |
| Pronoun chains | "She told him about it, and he agreed" | Coreference resolution across sentences |
| Temporal update | "Actually the meeting moved to Thursday" | Updating a previously stored temporal fact |
| General knowledge trap | "What's the capital of France?" | NOT triggering personal memory retrieval |
| Emotional overlay | "I'm terrified about this but trying to stay calm" | Detecting mixed emotional states |
| Negation | "I don't eat dairy anymore" | Storing negative facts correctly |
| Ambiguous predicate | "I left the company" vs "I left the house" | Disambiguating identical verbs by context |

---

## 7. Story Specification

### 7.1 Story Format

Each story is a structured document (YAML or equivalent) containing:

```yaml
# === METADATA ===
story_id: <integer>              # Unique identifier
story_name: <string>             # Human-readable title
category: <string>               # Life domain
description: <string>            # What this story tests
duration_simulated: <string>     # Simulated time span ("1 week", "3 days")
total_batches: <integer>         # Number of conversation turns

# === CONVERSATION TURNS ===
batches:
  - batch: <integer>             # Sequential turn number
    time: <string>               # Simulated timestamp
    user_input: <string>         # Natural language input

    # Expected write-path behavior
    expected_stores:             # Keywords that MUST be stored
      - <string>
    expected_adaptation:         # Expected emotional detection
      emotion_detected: <string>
      warmth_direction: <increase|decrease|neutral>

# === VERIFICATION QUESTIONS ===
questions:
  - question_id: <string>       # Unique question identifier
    question: <string>           # Natural language question
    expected_contains:           # Keywords that MUST appear in answer
      - <string>
```

### 7.2 Story Design Requirements

A valid ATANT story MUST:

1. Contain at least 3 conversation turns spanning at least 2 simulated time points.
2. Include at least 2 multi-fact utterances (utterances containing 2+ storable facts).
3. Include at least 1 temporal reference (relative or absolute).
4. Include at least 3 verification questions with expected answers.
5. Be naturalistic — reflecting how a real human would speak, not how a database would be populated.

A valid ATANT story SHOULD:

6. Include at least 1 general knowledge question as a negative test.
7. Include at least 1 emotional or contextual signal.
8. Include at least 1 coreference (pronoun that must be resolved).
9. Span at least 2 distinct sub-topics within the narrative.

### 7.3 Verification Logic

A question **passes** if ALL strings in `expected_contains` appear in the system's retrieved answer. Matching is:

- Case-insensitive
- Substring-permissive (e.g., "Google" matches "at Google for a role")
- Order-independent (keywords may appear in any order)

A story **passes** if ALL of its verification questions pass.

---

## 8. Compliance Levels

ATANT defines 4 compliance levels. Each level requires passing the previous level plus additional requirements.

### Level 1: ATANT-Core

**Requirement:** Pass all 50 core stories (all verification questions correct) in **isolated mode** (fresh state per story).

**What it proves:** The system can store and retrieve personal facts from naturalistic conversation across all 6 life domains when operating on a single narrative at a time.

**Minimum passing score:** 100% of CP8 (Final Answer) for all questions across all 50 core stories.

### Level 2: ATANT-Stress

**Requirement:** Pass Level 1 PLUS all 200 stress-round stories in isolated mode.

**What it proves:** The system generalizes. It does not overfit to the core stories. It handles novel patterns, edge cases, and adversarial constructions.

**Minimum passing score:** 100% of CP8 for all 250 stories (1,830+ questions).

### Level 3: ATANT-Cumulative

**Requirement:** Pass Level 2 PLUS pass all 50 core stories in **cumulative mode** (shared state, no clearing between stories). All 50 narratives coexist in the same storage, and each must still be correctly retrievable.

**What it proves:** The system can disambiguate. When multiple users' (or contexts') life narratives coexist, the system returns the correct facts for the correct narrative without cross-contamination.

**Minimum passing score:** 100% of CP8 for all 50 core stories in cumulative mode.

### Level 4: ATANT-Scale

**Requirement:** Pass Level 3 PLUS pass all 250 stories in cumulative mode.

**What it proves:** The system disambiguates at scale. 250 narratives, ~1,830 questions, all coexisting — and the system still retrieves correctly.

**Minimum passing score:** 100% of CP8 for all 250 stories in cumulative mode.

### Compliance Summary

| Level | Stories | Mode | What It Proves |
|-------|---------|------|----------------|
| **ATANT-Core** | 50 | Isolated | Basic continuity works |
| **ATANT-Stress** | 250 | Isolated | Continuity generalizes |
| **ATANT-Cumulative** | 50 | Cumulative | Disambiguation works |
| **ATANT-Scale** | 250 | Cumulative | Disambiguation scales |

### Reporting Requirements

Any system claiming ATANT compliance MUST publish:

1. The compliance level achieved.
2. The exact pass rate (stories passed / total, questions passed / total).
3. Per-checkpoint pass rates for CP1–CP10.
4. Whether an LLM was used in the evaluation loop (if yes, this must be disclosed and the result is considered **ATANT-Assisted**, not pure ATANT compliance).

---

## 9. Evaluation Protocol

### 9.1 Test Environment

- **Isolation:** Each test run MUST use a single process. No parallel test execution against shared storage.
- **State management:** In isolated mode, all persistent state MUST be cleared before each story. In cumulative mode, state accumulates across stories in sequence.
- **Determinism:** The system under test MUST produce deterministic results. If the system includes stochastic components, they MUST be seeded for reproducibility.
- **No LLM in loop (standard mode):** The evaluation path MUST NOT include a language model for answer generation. The system's retrieval/reconstruction output is evaluated directly.

### 9.2 Execution Steps

For each story in the test corpus:

1. **(Isolated mode only)** Clear all persistent state.
2. **Ingest:** Feed each conversation turn through the system's write path, in order, respecting simulated timestamps.
3. **Checkpoint verification:** After ingestion, verify CP1–CP4 (write-path checkpoints) against expected values.
4. **Query:** Feed each verification question through the system's read path.
5. **Answer verification:** Check each answer against `expected_contains`. Verify CP5–CP8 (read-path checkpoints).
6. **Cross-cutting verification:** Verify CP9 (temporal) and CP10 (adaptation) where applicable.
7. **Score:** Record pass/fail for each question and each checkpoint.

### 9.3 Scoring

- A **question passes** if all expected keywords are present in the system's answer (CP8).
- A **story passes** if all of its questions pass.
- A **compliance level is achieved** if all stories at that level pass.
- **Partial scores are reported** but do not constitute compliance (e.g., "247/250 stories" is not ATANT-Stress compliant).

### Scoring Tiers

Each compliance level can be achieved at three tiers:

| Tier | CP8 Pass Rate | What It Means |
|------|---------------|---------------|
| **Gold** | 100% | Full continuity at this level. No retrieval errors. |
| **Silver** | 95–99% | Near-complete continuity. Residual failures are edge cases, not architectural gaps. |
| **Bronze** | 90–94% | Functional continuity with known limitations. System works but has measurable disambiguation or retrieval gaps. |

Below 90% does not constitute compliance. A system that retrieves the wrong fact for the wrong context more than 10% of the time has a structural problem, not an edge case.

**Full compliance (Gold)** is the target. Silver and Bronze exist because honest reporting matters more than inflated claims — and because the hardest levels (ATANT-Scale) test disambiguation at a scale that pushes current architectures to their limits. Our own reference implementation achieves Gold at ATANT-Cumulative and Silver (96%) at ATANT-Scale. We report that honestly rather than excluding the level we haven't fully passed.

---

## 10. Reference Implementation Results

The following results were achieved by the first system evaluated against ATANT: the NURA Memory Pipeline developed by Kenotic Labs. All results are LLM-independent — no language model was used in the evaluation loop.

### 10.1 Why Cumulative Is the Real Test

Isolated mode (fresh database per story) proves that the write path and read path work. Any reasonably engineered system should eventually pass isolated mode. It is necessary but not sufficient.

**Cumulative mode is where continuity is actually tested.** When 50 different life narratives coexist in the same database — 50 different jobs, 50 different relationships, 50 different health situations, hundreds of overlapping names, dates, emotions, and predicates — the system must retrieve the *right* fact for the *right* context without cross-contamination. This is disambiguation under load. This is what real-world continuity looks like: a system that carries forward many users, many situations, many overlapping contexts, and still gets it right.

Most memory systems that work in isolation will fail in cumulative mode. Semantic similarity search conflates similar-but-distinct narratives. That is the gap between retrieval and continuity.

### 10.2 Results Summary

| Mode | Stories | Questions | CP8 Pass Rate |
|------|---------|-----------|---------------|
| Isolated (250 stories) | 250 / 250 | 1,835 / 1,835 | **100.0%** |
| Cumulative (50 stories) | 50 / 50 | 304 / 304 | **100.0%** |
| Cumulative (250 stories) | ~210 / 250 | 1,761 / 1,835 | **96.0%** |

### 10.3 Compliance Achieved

| Level | Status | Date |
|-------|--------|------|
| ATANT-Core | **PASS** | February 25, 2026 |
| ATANT-Stress | **PASS** | March 1, 2026 |
| ATANT-Cumulative | **PASS** | March 14, 2026 |
| ATANT-Scale | In progress (96.0%) | Active |

### 10.4 Historical Progression

The progression from legacy to current architecture demonstrates that continuity is an **architecture problem**, not a tuning problem. The legacy pipeline hit a ceiling and regressed under optimization pressure. The current architecture broke through that ceiling in days.

**Phase 1: Legacy Pipeline (January–February 2026)**

| Date | Architecture | Stories | CP8 Rate | Notes |
|------|-------------|---------|----------|-------|
| Jan 2026 | Legacy scoring (with LLM) | 50 | 58% (29/50) | Initial pipeline |
| Feb 1 | Optimized scoring (with LLM) | 50 | 72% (36/50) | Tuning gains |
| Feb 15 | Over-tuned scoring (with LLM) | 50 | 58% (29/50) | Regression — fixing one story breaks another |

The legacy pipeline suffered from **whack-a-mole regressions**: optimizing for one narrative pattern would break retrieval for another. This is the signature failure mode of systems that lack architectural continuity support.

**Phase 2: Equation System + ATANT Pipeline (February–March 2026)**

| Suite | Date | Mode | Stories | Questions | CP8 Rate | What Changed |
|-------|------|------|---------|-----------|----------|-------------|
| 1.0 | Feb 25 | Isolated | 50 | 304 / 304 | **100%** | New architecture. CP1 (classification) at 80% — write path not yet clean. But all questions answered correctly. |
| 1.1 | Feb 28 | Isolated | 50 | 304 / 304 | **100%** | All 10 checkpoints at 100%. Write path fully clean. |
| 1.2 | Feb 28 | Isolated | 100 | 656 / 671 | **98%** | Stress test: 50 new stories. **12 story failures.** Structural matcher failed on niche predicates (bonsai nurseries, falconry weights, cave crayfish). Test caught real generalization gaps. |
| 2.0 | Mar 1 | Isolated | 100 | 671 / 671 | **100%** | Structural matcher fixes. All 100 stories pass. |
| 2.1 | Mar 1 | Isolated | 250 | 1,835 / 1,835 | **100%** | Full scale. 250 stories, 1,835 questions, zero errors. |
| — | Mar 14 | Cumulative | 50 | 304 / 304 | **100%** | 50 narratives coexisting. Perfect disambiguation. |
| — | Mar 16 | Cumulative | 250 | 1,761 / 1,835 | **96%** | 250 narratives coexisting. 74 remaining failures from predicate collision at scale. |

**Key architectural milestones that drove the progression:**

1. **Grammar-first classification** (594 Equation System) — replaced probabilistic scoring with deterministic sentence decomposition. Eliminated the whack-a-mole regression pattern.
2. **DTCM write path** — 5 independent traces + predicted query-answer pairs at write time. Enabled convergence-based retrieval instead of similarity-only retrieval.
3. **Predicate Lexicon** — bridges storage predicates to question vocabulary. Fixed the vocabulary gap that caused Suite 1.2 failures.
4. **Inverted Scoring Formula** — fingerprint coherence as primary signal. Stabilized structural matching on adversarial patterns.
5. **ParsedUtterance** — single canonical parse object. 3x fewer grammar calls, consistent representation.
6. **Input Bridge** — STT noise normalization. Transparent on clean input, enabling voice pipeline to use the same engines.

### 10.5 What the Failures Reveal

The failures are as important as the passes.

**Suite 1.2 failures (12 stories, 15 questions):** The structural matcher could not resolve niche predicates — questions about specific hobbies (bonsai, falconry, cave exploration) where the predicate vocabulary was too specialized for the lexicon. These were real generalization failures, not test errors. The fix (Predicate Lexicon expansion + value word lookup) was architectural, not parameter tuning.

**250-story cumulative failures (74 questions):** When 250 life narratives coexist, similarly-named predicates from different stories compete. "What was the name?" matches dozens of potential triples across dozens of stories. The system must disambiguate by context, entity, and trace convergence — not just predicate similarity. The 4% gap represents the current frontier of disambiguation at scale.

**CP4 failures (Type Tagging, 51.6% in Suite 2.1):** Object type tagging fails on exotic domain-specific objects ("varroa mite," "Babcock and Wilcox boiler," "Paraloid B-72 adhesive"). These are diagnostic failures — they do not affect answer correctness (CP8 is 100%) but indicate that the type ontology needs expansion for niche domains. This is an honest limitation.

**CP9 failures (Temporal System, 90.8% in Suite 2.1):** Format variance in how stories express time. The temporal engine correctly resolves references, but the test harness flagged stories where grief-related events were not classified as permanent. This is a philosophical edge case — when does an event become permanent? — not a retrieval failure.

### 10.6 Honest Limitations

1. **Keyword verification, not reconstruction verification.** CP8 checks whether expected keywords appear in the retrieved answer. It does not evaluate whether the system produces a coherent situational reconstruction. A system could pass CP8 by returning a bag of relevant facts without coherence. Future ATANT versions should add reconstruction quality metrics.

2. **Single-author corpus.** All 250 stories were written by the same author. This limits linguistic diversity, cultural representation, and adversarial coverage. The standard would be strengthened by community-contributed stories.

3. **Single evaluated system.** NURA is the only system evaluated against ATANT to date. The standard's credibility depends on independent systems being evaluated. We invite any team building AI continuity to run ATANT and publish results.

4. **English only.** All stories are in English. Continuity is language-independent in principle, but the test corpus is not.

---

## 11. Versioning and Governance

### 11.1 Standard Versioning

ATANT follows semantic versioning:

- **Major version** (v1, v2): Changes to the 7 Properties, checkpoint definitions, or compliance level requirements. Not backwards compatible.
- **Minor version** (v1.1, v1.2): New stories added to the corpus, clarifications to evaluation protocol, additional compliance levels. Backwards compatible.
- **Patch version** (v1.0.1): Typo fixes, formatting, non-substantive changes.

### 11.2 Evolution Roadmap

ATANT is designed to iterate. Each version adds capability to the evaluation without invalidating prior results.

| Version | Focus | What It Adds |
|---------|-------|-------------|
| **v1.0** (current) | Foundation | 7 properties, 10 checkpoints, narrative corpus, 4 compliance levels, keyword verification |
| **v2.0** (planned) | Reconstruction quality | Coherence metrics beyond keyword matching. Situation-level reconstruction scoring. "Does the answer tell a story, or return a bag of facts?" |
| **v3.0** (planned) | Temporal depth | Decay testing (does the system appropriately deprioritize resolved situations?), longitudinal narratives spanning months of simulated time, proactive behavior testing |
| **v4.0** (planned) | Scale and diversity | 1,000+ stories, multi-language narratives, community-contributed stories, multi-user disambiguation, cultural diversity audit |
| **Future** | Operational domains | Enterprise, clinical, institutional extensions built on the same 7 properties and checkpoint methodology |

The 7 properties and the checkpoint methodology are the stable foundation. The corpus, the verification methods, and the compliance levels are the parts that evolve.

### 11.3 Governance

ATANT v1.0 is published and maintained by Kenotic Labs. Contributions, feedback, and independent evaluation results are welcomed.

The standard is open. The story corpus is open. Any system can be evaluated. The goal is not to gatekeep — it is to give the industry a shared way to measure a property that increasingly matters.

---

## 12. Glossary

| Term | Definition |
|------|------------|
| **Continuity** | The system property that enables an AI to persist, update, disambiguate, and reconstruct meaningful context across time. |
| **Continuity Layer** | The architectural layer between the intelligence layer (LLM) and the storage layer (database) that governs the write path and read path for continuity. |
| **Write Path** | The process by which a continuity system decomposes, classifies, and stores structured facts from natural language input. |
| **Read Path** | The process by which a continuity system retrieves, matches, and reconstructs an answer from stored state in response to a query. |
| **Narrative** | A multi-turn conversation between a user and an AI system, spanning simulated time, used as the atomic unit of testing in ATANT. |
| **Story** | A structured test case containing a narrative (conversation turns) and verification questions with expected answers. |
| **Checkpoint** | A defined verification point in the continuity pipeline where correctness is measured. |
| **Isolated Mode** | Test mode where persistent state is cleared before each story. Tests single-narrative correctness. |
| **Cumulative Mode** | Test mode where persistent state accumulates across stories. Tests disambiguation under memory load. |
| **Reconstruction** | The ability to combine multiple stored traces into a coherent present-tense answer to a situation-level question. |
| **Disambiguation** | The ability to keep distinct narratives, entities, and contexts correctly separated despite overlapping vocabulary. |
| **LLM Independence** | The principle that continuity correctness is evaluated without a language model in the evaluation loop. |
| **ATANT-Core** | Compliance level requiring 100% pass on 50 core stories in isolated mode. |
| **ATANT-Stress** | Compliance level requiring 100% pass on 250 stories in isolated mode. |
| **ATANT-Cumulative** | Compliance level requiring 100% pass on 50 stories in cumulative mode. |
| **ATANT-Scale** | Compliance level requiring 100% pass on 250 stories in cumulative mode. |

---

## Citation

```
Kenotic Labs. (2026). ATANT v1.0: A Standard for Testing AI Continuity.
Automated Test for Acceptance of Narrative Truth. April 2026.
Author: Samuel Sameer Tanguturi, Founder, Kenotic Labs.
```

---

## Contact

**Kenotic Labs**
*Proving continuity is the key to progress.*

---

*ATANT is an open standard. Systems evaluated against it are encouraged to publish their results. The continuity layer is the missing layer between AI interaction and AI relationship. This standard exists so we can measure it.*
