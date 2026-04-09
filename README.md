# ATANT v1.0

**Automated Test for Acceptance of Narrative Truth**

An open evaluation framework for measuring AI continuity : The ability to persist, update, disambiguate, and reconstruct meaningful context across time.

Published by [Kenotic Labs](https://kenoticlabs.com).

📄 **[Read the Paper on arXiv](https://arxiv.org/abs/2604.06710)** | [PDF](ATANT%20Evaluation%20Framework.pdf)

---

## What is Continuity?

Most AI systems today are session-based. You say something. It responds. The moment ends.

**Continuity** is the system property that makes AI coherent across life, not just intelligent per session. It is the logic that determines what should persist, in what form, what has changed, what still matters, and how to reconstruct it when needed.

Memory stores the past. Continuity keeps the right parts alive in the present.

---

## What is ATANT?

ATANT is the first published evaluation framework for AI continuity. It is:

- **System-agnostic** : Any AI system can be evaluated
- **Model-independent** : No LLM in the evaluation loop
- **Narrative-based** : Tests use realistic multi-turn conversations, not synthetic fact pairs
- **Sequenced** : A progressive methodology from isolated correctness to disambiguation at scale

ATANT defines:

1. **7 Required Properties** of continuity (persistence, update handling, temporal ordering, disambiguation, reconstruction, model independence, operational usefulness)
2. **10 Checkpoints** verifying correctness at each stage of the write path and read path
3. **4 Compliance Levels** (Core, Stress, Cumulative, Scale)
4. **A narrative test corpus** spanning 6 life domains with 250 stories and 1,835 verification questions

---

## The 7 Properties of Continuity

| # | Property | What It Means |
|---|----------|---------------|
| 1 | **Persistence Beyond Session** | Continuity survives shutdown, restart, and time |
| 2 | **Update Handling** | The system revises what it knows without breaking consistency |
| 3 | **Temporal Ordering** | Not just what happened, but when, in what sequence, with what status |
| 4 | **Disambiguation** | Distinct narratives stay separate despite overlapping vocabulary |
| 5 | **Reconstruction** | The system answers situation-level questions, not just fact lookups |
| 6 | **Model Independence** | Continuity lives below the intelligence layer, not inside it |
| 7 | **Operational Usefulness** | Continuity works across domains : Personal, clinical, Institutional |

---

## Compliance Levels

| Level | Requirement | What It Proves |
|-------|-------------|----------------|
| **ATANT-Core** | 50 stories, isolated mode, 100% CP8 | Basic continuity works |
| **ATANT-Stress** | 250 stories, isolated mode, 100% CP8 | Continuity generalizes |
| **ATANT-Cumulative** | 50 stories, cumulative mode, 100% CP8 | Disambiguation works |
| **ATANT-Scale** | 250 stories, cumulative mode, 100% CP8 | Disambiguation scales |

Scoring tiers: Gold (100%), Silver (95-99%), Bronze (90-94%).

---

## Reference Implementation Results

The first system evaluated against ATANT is the NURA Memory Pipeline by Kenotic Labs.

| Mode | Stories | Questions | CP8 Pass Rate |
|------|---------|-----------|---------------|
| Isolated (250) | 250/250 | 1,835/1,835 | **100%** |
| Cumulative (50) | 50/50 | 304/304 | **100%** |
| Cumulative (250) | ~210/250 | 1,761/1,835 | **96%** |

---

## Repository Structure

```
atant/
  README.md                     # This file
  docs/
    ATANT_Standard_v1.0.md      # The full standard specification
    Story_Format_Spec.md        # YAML schema for test stories
    Testing_Figures.md          # Results and historical progression
  corpus/
    examples/                   # Example stories in YAML format
  LICENSE
```

---

## Read the Standard

The full ATANT v1.0 specification is in [`docs/ATANT_Standard_v1.0.md`](docs/ATANT_Standard_v1.0.md).

---

## Citation

```
@article{tanguturi2026atant,
  title={ATANT: An Evaluation Framework for AI Continuity},
  author={Tanguturi, Samuel Sameer},
  journal={arXiv preprint arXiv:2604.06710},
  year={2026}
}
```

---

## License

Copyright 2026 Kenotic Labs. All rights reserved. See [LICENSE](LICENSE) for details.

---

*The continuity layer is the missing layer between AI interaction and AI relationship. ATANT exists so we can measure it.*
