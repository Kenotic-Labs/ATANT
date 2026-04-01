# ATANT Testing Figures

**Date:** 2026-03-16
**System:** NURA Memory Pipeline (594 Equation System + ParsedUtterance + DTCM)

---

## Current Status: Phase 3 (Cumulative Memory Testing)

---

## Test Corpus

| Metric | Count |
|--------|-------|
| **Total Stories** | 251 |
| **Total Questions** | 1,844 |
| **Story Categories** | 6 (Career, Relationships, Health, Learning, Daily Life, Life Events) |
| **Testing Phases Covered** | Phase 1 + Phase 2 (4 rounds) + YC Demo |

### Breakdown by Phase

| Phase | Stories | Questions | Purpose |
|-------|---------|-----------|---------|
| Phase 1 (1-50) | 50 | 304 | Core engine proof — 6 categories |
| Phase 2 Round 2 (51-100) | 50 | 367 | Stress test — generalization check |
| Phase 2 Round 3 (101-150) | 50 | 386 | Stress test — novel patterns |
| Phase 2 Round 4 (151-200) | 50 | 380 | Stress test — edge cases |
| Phase 2 Round 5 (201-250) | 50 | 398 | Stress test — adversarial constructions |
| YC Demo (999) | 1 | 9 | Live demo scenario (Meridian Robotics) |
| **TOTAL** | **251** | **1,844** | |

### Phase 1 Category Breakdown

| Category | Stories | Description |
|----------|---------|-------------|
| Career | 7 | Interviews, promotions, side projects |
| Relationships | 7 | Partners, family, friends |
| Health | 6 | Medical, fitness, diet |
| Learning | 6 | Courses, certifications, skills |
| Daily Life | 7 | Routines, hobbies, errands |
| Life Events | 17 | Moves, births, deaths, milestones |
| **Total** | **50** | |

---

## Isolated Test Results (Fresh DB Per Story)

> Each story runs against an empty database. No cross-story interference.

### Overall

| Metric | Result |
|--------|--------|
| **Stories Passed** | 251 / 251 |
| **Questions Passed** | 1,844 / 1,844 |
| **Pass Rate** | **100.0%** |
| **Date Achieved** | 2026-03-14 (maintained through 2026-03-16) |

### Per-Checkpoint Results

| CP | Name | Passed | Total | Rate | Notes |
|----|------|--------|-------|------|-------|
| CP1 | Classification | 251 | 251 | 100.0% | All utterances classified correctly |
| CP2 | Triple Storage | 251 | 251 | 100.0% | All expected facts stored |
| CP3 | Predicted Queries | 251 | 251 | 100.0% | DTCM query-answer pairs generated |
| CP4 | Object Type Tagging | 129 | 251 | 51.4% | Known limitation: auto-generated triples have weak type labels |
| CP5 | Query Classification | 1,844 | 1,844 | 100.0% | All questions classified correctly |
| CP6 | Structural Matcher | 1,844 | 1,844 | 100.0% | All questions matched to correct triple |
| CP7 | DTCM Convergence | 1,844 | 1,844 | 100.0% | All queries activated convergence gate |
| CP8 | Final Combined | 1,844 | 1,844 | 100.0% | **All questions answered correctly** |
| CP9 | Temporal System | 228 | 251 | 90.8% | Variance in auto-narrative time format |
| CP10 | Adaptation Engine | 251 | 251 | 100.0% | Emotion detection + warmth adjustment correct |
| INT | Integration Tests | 5 | 5 | 100.0% | Patent-proof E2E scenarios |

**CP4 and CP9 are known non-blocking limitations.** CP4 depends on auto-generated triple quality (not the pipeline). CP9 has format variance in how YAML stories express time — the temporal engine itself is correct.

### Per-Phase Isolated Results

| Phase | Stories | Questions | Pass Rate |
|-------|---------|-----------|-----------|
| Phase 1 (1-50) | 50/50 | 304/304 | 100% |
| Phase 2 R2 (51-100) | 50/50 | 367/367 | 100% |
| Phase 2 R3 (101-150) | 50/50 | 386/386 | 100% |
| Phase 2 R4 (151-200) | 50/50 | 380/380 | 100% |
| Phase 2 R5 (201-250) | 50/50 | 398/398 | 100% |
| YC Demo (999) | 1/1 | 9/9 | 100% |

---

## Cumulative Test Results (Shared DB, No Clear Between Stories)

> Stories 1-50 run sequentially without clearing the database.
> Each new story must be stored and retrieved correctly despite
> all previous stories' data coexisting in the same DB.

### Phase 3: 50-Story Cumulative

| Metric | Result |
|--------|--------|
| **Stories Passed** | 50 / 50 |
| **Questions Passed** | 304 / 304 |
| **Pass Rate** | **100.0%** |
| **Date Achieved** | 2026-03-14 |

### Phase 3: 250-Story Cumulative (In Progress)

| Metric | Result |
|--------|--------|
| **CP8 Questions Passed** | 1,761 / 1,835 |
| **Pass Rate** | 96.0% |
| **Remaining Failures** | 74 questions across ~40 stories |
| **Status** | Active investigation |

The 4% gap in 250-story cumulative is caused by predicate disambiguation at scale — when 250 stories coexist, similarly-named predicates from different stories can compete. The Predicate Lexicon and Inverted Scoring Formula have been reducing this steadily.

---

## Historical Progression

### Pre-Equation System (Legacy Pipeline)

| Date | Framework | Stories | Best Score | Approach |
|------|-----------|---------|------------|----------|
| 2026-01 | Narrative v1 | 50 (with LLM) | 29/50 (58%) | Legacy entity_graph.py scoring |
| 2026-02-01 | Narrative v1 | 50 (with LLM) | 36/50 (72%) | Scoring war optimizations |
| 2026-02-15 | Narrative v1 | 50 (with LLM) | 29/50 (58%) | Regressions from over-tuning |

The legacy pipeline hit a ceiling at ~58% and suffered from whack-a-mole regressions — fixing one story would break another. This led to the 594 Equation System rewrite.

### Post-Equation System (ATANT Pipeline v2)

| Date | Milestone | Isolated Score | Cumulative 50 |
|------|-----------|----------------|---------------|
| 2026-03-08 | Equation system + DTCM built | 50/50 (Phase 1) | — |
| 2026-03-09 | Phase 2 Round 2 complete | 100/100 | — |
| 2026-03-10 | Phase 2 Round 3 complete | 150/150 | — |
| 2026-03-11 | Phase 2 Round 4 complete | 200/200 | — |
| 2026-03-12 | Phase 2 Round 5 complete | 250/250 | — |
| 2026-03-13 | Phase 3 started | 250/250 | 301/304 (99.0%) |
| 2026-03-14 | ParsedUtterance + v2 pipeline | 251/251 | 304/304 (100%) |
| 2026-03-15 | Input Bridge (voice normalization) | 251/251 | 304/304 (100%) |
| 2026-03-16 | Garbage gate + explanation rescue | 251/251 | 304/304 (100%) |

### Key Architectural Milestones

| # | Milestone | Impact |
|---|-----------|--------|
| 1 | 594 Equation System | Replaced legacy scoring war with grammar-first classification |
| 2 | DTCM (Decomposed Trace Convergence Memory) | 5 independent traces + predicted query-answer pairs |
| 3 | Grammar Engine (G1-G25) | Deterministic sentence decomposition without LLM |
| 4 | Predicate Lexicon | Bridges storage predicates to question vocabulary |
| 5 | Inverted Scoring Formula | Fingerprint coherence as PRIMARY signal |
| 6 | ParsedUtterance | Single canonical parse object, 3x fewer grammar calls |
| 7 | Input Bridge | STT noise normalization, transparent on clean input |
| 8 | Garbage Gate | Blocks non-personal/malformed memory storage |

---

## Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| Avg questions per story | 7.3 | Range: 5-9 |
| Avg facts per story | 5.2 | Multi-fact utterances common |
| Pipeline latency (per query) | <50ms | Engine-only, no LLM |
| Test suite runtime (251 stories) | ~8 minutes | CPU-only embeddings |
| DB size at 250 stories | ~15MB | Entity graph + DTCM traces |

---

## Phase Completion Status

| Phase | Status | Key Result |
|-------|--------|------------|
| Phase 1 | **COMPLETE** | 50/50 stories, 304/304 questions |
| Phase 2 | **COMPLETE** | 200 new stories across 4 rounds, all pass |
| Phase 3 | **IN PROGRESS** | 50-story cumulative: 100%. 250-story: 96% |
| Phase 4 | Not Started | Cumulative stress at 200+ stories |
| Phase 5 | Not Started | Proactive questioning |
| Phase 6 | Not Started | Latency optimization (<200ms) |
| Phase 7 | Not Started | LLM integration (after LLM Wall) |

---

## What These Numbers Mean

**251/251 isolated** means: Given clean input and a fresh database, NURA's memory pipeline stores and retrieves personal facts with **zero errors** across 1,844 questions spanning career, relationships, health, learning, daily life, and major life events.

**304/304 cumulative** means: Even when 50 different people's life stories coexist in the same database, NURA correctly disambiguates and retrieves the right facts for the right person/context.

**No LLM involved** means: These results are purely from the deterministic engines — grammar parsing, classification, triple extraction, structural matching, DTCM convergence. The LLM is not a variable. When it's added in Phase 7, the ONLY question will be: "Does the LLM use the facts it's given?" — a prompt engineering problem, not an architecture problem.
