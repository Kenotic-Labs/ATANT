# ATANT v1.0

**Automated Test for Acceptance of Narrative Truth**

An open evaluation framework for measuring AI continuity: the ability to persist, update, disambiguate, and reconstruct meaningful context across time.

Published by [Kenotic Labs](https://kenoticlabs.com), the company building the continuity layer for AI systems.

- Website: https://kenoticlabs.com
- Insights: https://kenoticlabs.com/insights
- Demo: https://kenoticlabs.com/demo
- AI-readable overview: https://kenoticlabs.com/llms.txt
- Full AI-readable context: https://kenoticlabs.com/llms-full.txt

?? **[Read the Paper on arXiv](https://arxiv.org/abs/2604.06710)** | [PDF](ATANT%20Evaluation%20Framework.pdf)

---

## Why ATANT Exists

Most AI systems today can retrieve information, summarize history, and answer well inside a session.

What they still struggle to do is preserve the living state of a situation across time.

They lose track of:

- what is still active
- what changed
- what is resolved
- what still matters
- what should happen next

Kenotic Labs describes that missing capability as **continuity**.

ATANT exists to measure it.

---

## What is Continuity?

**Continuity** is the system property that makes AI coherent across time, not just intelligent per session.

It is the logic that determines what should persist, what changed, what still matters, and how to reconstruct the current situation when needed.

Memory stores the past.
Continuity keeps the right parts alive in the present.

---

## What is ATANT?

ATANT is the first published evaluation framework for AI continuity. It is:

- **System-agnostic**: any AI system can be evaluated
- **Model-independent**: no LLM in the evaluation loop
- **Narrative-based**: tests use realistic multi-turn conversations, not synthetic fact pairs
- **Sequenced**: a progressive methodology from isolated correctness to disambiguation at scale

ATANT defines:

1. **7 required properties** of continuity
2. **10 checkpoints** verifying correctness at each stage of the continuity process
3. **4 compliance levels** from core correctness to scale
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
| 7 | **Operational Usefulness** | Continuity works across domains: personal, clinical, institutional |

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

## Dataset

The full ATANT v1.0 Narrative Test Corpus is available on Hugging Face:

**[Kenotic-Labs/ATANTV1.0-corpus](https://huggingface.co/datasets/Kenotic-Labs/ATANTV1.0-corpus)**

The dataset is also linked from the Hugging Face paper page at [huggingface.co/papers/2604.06710](https://huggingface.co/papers/2604.06710).

Load it with:

```python
from datasets import load_dataset

ds = load_dataset("Kenotic-Labs/ATANTV1.0-corpus")
```

---

## Why This Matters

ATANT is not just a benchmark.

It is part of a larger thesis: that AI needs a continuity layer beneath the current stack, and that the ability to preserve and reconstruct situation across time will become a foundational requirement for assistants, agents, workflows, enterprise systems, care systems, and devices.

ATANT is how that thesis becomes measurable.

---

## Repository Structure

```text
atant/
  README.md
  docs/
    ATANT_Standard_v1.0.md
    Story_Format_Spec.md
    Testing_Figures.md
  corpus/
    examples/
  LICENSE
```

---

## Read the Standard

The full ATANT v1.0 specification is in [`docs/ATANT_Standard_v1.0.md`](docs/ATANT_Standard_v1.0.md).

---

## Citation

```bibtex
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
