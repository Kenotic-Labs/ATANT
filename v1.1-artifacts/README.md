# ATANT v1.1 Artifacts

Companion artifacts for ATANT v1.1, Section 2.1 (LOCOMO structural analysis).

## Files

| File | What it is |
|------|------------|
| `analyze_locomo_categories.py` | Python script that reads `locomo10.json` and reproduces the per-category counts, WH-word frequencies, and empty-gold counts cited in v1.1 §2.1. Standard-library only. |
| `locomo_category_analysis.csv` | Output of the script on the full LOCOMO corpus (10 conversations, 1,986 QA pairs). One row per category, with counts and WH-prefix percentages. |
| `empty_gold_counts.json` | Per-category empty-gold answer counts. Confirms the 444/446 (99.6%) figure for Category 5 cited in v1.1 §2.1. |

## Reproducing the analysis

```
python analyze_locomo_categories.py <path-to-locomo10.json>
```

`locomo10.json` is distributed as part of the LOCOMO benchmark. Pass its path as the first argument.

## Numbers cited in v1.1 §2.1

Running the script on the full corpus produces:

| Category | n | %what | %when | %how-long/many | %how-did/does | %why | empty-gold |
|---------:|--:|------:|------:|---------------:|--------------:|-----:|-----------:|
| 1 | 282 | 64.9 | 1.4 | 8.9 | 1.8 | 0.7 | 0 |
| 2 | 321 | 4.7 | 76.6 | 6.5 | 0.0 | 0.0 | 0 |
| 3 |  96 | 34.4 | 0.0 | 1.0 | 0.0 | 2.1 | 0 |
| 4 | 841 | 70.6 | 0.8 | 1.9 | 9.5 | 4.5 | 0 |
| 5 | 446 | 68.8 | 1.1 | 0.9 | 9.0 | 5.2 | 444 (99.6%) |

Total: 1,986 QA pairs across 10 conversations.

## What this supports

The v1.1 paper (arXiv:TBD) argues that LOCOMO's published category labels do not match the question shapes they contain, and that 444 of 446 Category-5 items are unscorable by construction under the Mem0 reference runner's `answer_matches` function. The numbers in the table above are the structural evidence for both claims.
