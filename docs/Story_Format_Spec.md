# ATANT Story Format Specification

**Version:** 2.0
**Last Updated:** 2026-03-16

---

## Overview

Each ATANT story is a YAML file that simulates a multi-turn conversation between a user and NURA over a defined period (hours to weeks). Stories are the atomic unit of testing  -  each one is self-contained and tests a specific combination of memory capabilities.

---

## File Structure

Stories live in categorized directories:

```
tests/stories/
  career/           # Phase 1: 7 stories (IDs 1, 12-17)
  daily/            # Phase 1: 7 stories (IDs 5, 23-28)
  health/           # Phase 1: 6 stories (IDs 3, 18-22)
  learning/         # Phase 1: 6 stories (IDs 4, 29-33)
  life_events/      # Phase 1: 17 stories (IDs 34-50)
  relationships/    # Phase 1: 7 stories (IDs 2, 6-11)
  phase2_round2/    # Stress: 50 stories (IDs 51-100)
  phase2_round3/    # Stress: 50 stories (IDs 101-150)
  phase2_round4/    # Stress: 50 stories (IDs 151-200)
                    # Round 5 (201-250) in expected_answers.json
```

---

## YAML Schema

```yaml
# === HEADER ===
story_id: <integer>           # Unique ID (1-250, 999 for demos)
story_name: <string>          # Human-readable title
category: <string>            # Career | Relationships | Health | Learning | Daily Life | Life Events
description: <string>         # What this story tests
duration_simulated: <string>  # "1 week", "3 days", "1 month"
total_batches: <integer>      # Number of conversation turns

# === ENGINE COVERAGE ===
engines_tested:
  memory: true/false          # Memory storage engine
  retrieval: true/false       # Retrieval engine
  temporal: true/false        # Temporal awareness
  adaptation: true/false      # Emotional adaptation
  proactive: true/false       # Proactive questioning
  intent_gate: true/false     # Personal vs GK routing
  orchestrator: true/false    # Backbone orchestration

# === CONVERSATION TURNS ===
batches:
  - batch: <integer>          # Sequential batch number
    time: <string>            # Simulated timestamp ("Monday 9:00 AM")
    user_input: <string>      # What the user says to NURA

    # Optional: Expected write-path behavior
    expected_memory_stores:   # Keywords that should be stored
      - <string>
    expected_adaptation:      # Expected emotional response
      emotion_detected: <string>
      warmth_direction: increase/decrease/neutral
      vulnerability: true/false

    # Some batches are GK queries (no memory store expected)
    # e.g., "What's the capital of France?"  -  tests intent gating
```

---

## Expected Answers (JSON)

Retrieval questions and expected answers are stored separately in `expected_answers.json`:

```json
{
  "stories": [
    {
      "story_id": 1,
      "story_name": "The Job Interview",
      "category": "Career",
      "facts": [
        {
          "batch": 1,
          "time": "Monday 9:00 AM",
          "user_input": "Hey Nura, I'm really nervous...",
          "expected_stores": ["Google", "Wednesday", "Senior Engineer", "David Chen"],
          "expected_triples": [
            {"subject": "user", "predicate": "interview_company", "object": "Google"},
            {"subject": "user", "predicate": "interview_role", "object": "Senior Engineer"}
          ]
        }
      ],
      "questions": [
        {
          "question_id": "1_q1",
          "question": "What company did I interview at?",
          "expected_contains": ["Google"],
          "expected_triples": [
            {"subject": "user", "predicate": "interview_company", "object": "Google"}
          ]
        }
      ]
    }
  ]
}
```

### Question Verification

A question **passes** if ALL strings in `expected_contains` appear in the pipeline's retrieved answer. Matching is case-insensitive and allows partial containment (e.g., "Google" matches "google" or "at Google for").

### Triple Verification

`expected_triples` define the exact entity-graph triples that should exist in the database after ingestion, and which triple should be retrieved for each question.

---

## Story Design Guidelines

### What Makes a Good Story

1. **Multi-turn**  -  At least 3-5 batches spanning different times
2. **Multi-fact**  -  Each utterance batch should contain 2-4 storable facts
3. **Emotionally grounded**  -  Real conversations carry emotion; stories should too
4. **Temporally aware**  -  Use time references ("yesterday", "next Wednesday", "at 5 PM")
5. **GK traps**  -  Include at least 1 general knowledge question that should NOT trigger memory
6. **Ambiguity**  -  Include predicates that could match multiple domains
7. **Coreference**  -  Use pronouns ("she", "it", "they") that require resolution

### Patterns to Test

| Pattern | Example | What It Tests |
|---------|---------|---------------|
| Simple fact | "I work at Google" | Basic triple extraction |
| Multi-fact | "My sister Emily lives in Portland" | Two triples from one utterance |
| Temporal | "I have a meeting at 5" | Temporal expression parsing |
| Emotional | "I'm really nervous about this" | Adaptation engine |
| Shared subject | "My brother and I went hiking" | "X and I" swap pattern |
| GK query | "What's photosynthesis?" | Intent gate routing |
| Pronoun chain | "She said it was great" | Coreference resolution |
| Update | "Actually, it's at 6 not 5" | Temporal update handling |
| Negation | "I don't like spicy food" | Polarity detection |

### Naming Convention

```
{story_id}_{short_description}.yaml

Examples:
  01_job_interview.yaml
  12_promotion.yaml
  34_moving_cities.yaml
```

For Phase 2+ stories: `{story_id}_{title_slug}.yaml` in the appropriate round directory.

---

## Test Modes

### Isolated Mode (Default)

Database is cleared before each story. Tests that the pipeline works correctly for a single user's narrative in isolation.

```bash
python -m tests.pipeline.run_pipeline_v2 --story 7
```

### Cumulative Mode

Database is NOT cleared between stories. Stories 1-50 (or 1-250) coexist. Tests disambiguation  -  can NURA tell apart Story 1's "Google interview" from Story 42's "coffee shop opening"?

```bash
python -m tests.pipeline.run_pipeline_v2 --range 1-50
```

### Range Mode

Run a subset of stories:

```bash
python -m tests.pipeline.run_pipeline_v2 --range 101-150  # Phase 2 Round 3 only
```

---

## Adding New Stories

1. Create a YAML file following the schema above
2. Add expected answers to `expected_answers.json` (questions + expected_contains)
3. Run the story in isolation: `python -m tests.pipeline.run_pipeline_v2 --story <id>`
4. Verify all checkpoints pass
5. Run full regression to confirm no impact on existing stories

### ID Ranges

| Range | Allocation |
|-------|-----------|
| 1-50 | Phase 1 (6 categories) |
| 51-100 | Phase 2 Round 2 |
| 101-150 | Phase 2 Round 3 |
| 151-200 | Phase 2 Round 4 |
| 201-250 | Phase 2 Round 5 |
| 251-300 | Reserved for Phase 3 expansion |
| 900-999 | Demo and showcase stories |
