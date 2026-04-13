# ATANT v1.2 Artifacts

Companion artifacts for ATANT v1.2: The Continuity Corpus.

## Files

| File | What it is |
|------|------------|
| `atant_engines_20260412_204903.json` | Raw 500-story run output (IDs 51 through 550). Top-level keys: `mode`, `timestamp`, `range`, `total_stories`, `total_questions`, `passed_questions`, `total_triples`, `elapsed_seconds`, `results`. The `results` array contains one object per story with `story_id`, `story_name`, `category`, `triple_count`, `questions_passed`, `questions_total`, and a `questions` list. 4,160 of 5,000 questions passed (83.2%). |
| `failure_taxonomy.json` | Classification of the 840 failed questions using a distractor-baseline z-score method. Top-level: `summary`, `engine_limit`, `grader_limit`, `borderline`, `empty_answer`. Each failure record includes `story_id`, `story_name`, `question`, `expected`, `answer`, `max_kw_sim`, `distractor_mu`, `distractor_sigma`, `z_score`. Distribution: 91 engine_limit, 0 grader_limit, 645 borderline, 104 empty_answer. |

## Reproducing the numbers

`atant_engines_20260412_204903.json` was produced by the run documented in v1.2 §5. The runner is `run_atant_cumulative.py` in the Nura reference implementation repository. Corpus: `tests/stories/cumulative/` story IDs 51 through 550, v1.0 schema.

`failure_taxonomy.json` was produced by a classifier that computes the cosine similarity between each failed answer and its expected gold keywords, and z-scores that similarity against a distractor distribution drawn from the corpus's full gold vocabulary.

## Numbers cited in v1.2

| Metric | Value | File |
|-------:|------:|:-----|
| Total questions | 5,000 | `atant_engines_20260412_204903.json` `total_questions` |
| Questions passed | 4,160 | `total_questions_passed` |
| Pass rate | 83.2% | Computed |
| Triples stored | 30,668 | `total_triples` |
| Elapsed | 11,503 s | `elapsed_seconds` |
| engine_limit failures | 91 | `failure_taxonomy.json` `engine_limit` |
| grader_limit failures | 0 | `grader_limit` |
| borderline failures | 645 | `borderline` |
| empty_answer failures | 104 | `empty_answer` |

## Classifier thresholds

Failures are partitioned using z-score thresholds on `max_kw_sim` relative to the distractor distribution:

- `engine_limit`: `z < -1.5` and non-empty answer
- `grader_limit`: `z > +1.0` and non-empty answer
- `borderline`: `-1.5 <= z <= +1.0` and non-empty answer
- `empty_answer`: empty answer string

The 0-grader-limit finding is specific to these thresholds. The 645-borderline headline holds under any symmetric threshold choice.

## What this supports

v1.2 (arXiv:TBD) documents the 500-story ATANT corpus, its format relative to the proposed v2.0 schema, and the v1.0 engine and grader's behavior at scale. The numbers above are the empirical spine of that paper. The distractor-baseline classifier's finding that no failure qualifies as cleanly grader-limited, with 77% of failures landing in the borderline bucket, motivates v2.0's shift from substring matching to grounded grading.
