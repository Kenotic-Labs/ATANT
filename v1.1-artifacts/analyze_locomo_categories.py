"""
LOCOMO category structural analysis for ATANT v1.1, Section 2.1.

Reads the LOCOMO corpus (locomo10.json) and emits:
  - per-category question count
  - dominant WH-word prefix frequency per category
  - empty-gold-answer count per category

Run:
    python analyze_locomo_categories.py <path-to-locomo10.json> [output_dir]

If no path is given, falls back to the standard LOCOMO repo location:
    locomo_bench/locomo/data/locomo10.json

Outputs:
    locomo_category_analysis.csv
    empty_gold_counts.json

No external dependencies beyond the Python standard library.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

WH_PREFIXES = ("what", "when", "how long", "how many", "how did", "how does",
               "how do", "how", "why", "who", "where", "which", "is", "are",
               "did", "does", "do", "was", "were", "will", "can")


def wh_prefix(text):
    t = (text or "").strip().lower()
    for prefix in WH_PREFIXES:
        if t.startswith(prefix + " ") or t == prefix + "?" or t.startswith(prefix + "?"):
            return prefix
    return "other"


def iter_qa_pairs(data):
    for conv in data:
        qas = conv.get("qa") or conv.get("qa_pairs") or []
        for qa in qas:
            yield qa


def analyze(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("conversations") or list(data.values())

    per_category_count = Counter()
    per_category_wh = defaultdict(Counter)
    per_category_empty_gold = Counter()

    for qa in iter_qa_pairs(data):
        cat = qa.get("category")
        if cat is None:
            continue
        cat = int(cat)
        question = qa.get("question", "")
        answer = qa.get("answer", "")

        per_category_count[cat] += 1
        per_category_wh[cat][wh_prefix(question)] += 1
        if not str(answer).strip():
            per_category_empty_gold[cat] += 1

    return per_category_count, per_category_wh, per_category_empty_gold


def write_csv(out_dir, counts, wh, empty):
    out = out_dir / "locomo_category_analysis.csv"
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["category", "count", "pct_what", "pct_when", "pct_how_long_or_many",
                    "pct_how_did_does", "pct_why", "empty_gold", "pct_empty_gold"])
        for cat in sorted(counts):
            n = counts[cat]
            w_counts = wh[cat]
            pct_what = 100.0 * w_counts.get("what", 0) / n if n else 0
            pct_when = 100.0 * w_counts.get("when", 0) / n if n else 0
            pct_how_lm = 100.0 * (w_counts.get("how long", 0) + w_counts.get("how many", 0)) / n if n else 0
            pct_how_dd = 100.0 * (w_counts.get("how did", 0) + w_counts.get("how does", 0)) / n if n else 0
            pct_why = 100.0 * w_counts.get("why", 0) / n if n else 0
            eg = empty[cat]
            w.writerow([cat, n, f"{pct_what:.1f}", f"{pct_when:.1f}", f"{pct_how_lm:.1f}",
                        f"{pct_how_dd:.1f}", f"{pct_why:.1f}", eg, f"{100.0*eg/n:.1f}" if n else "0.0"])
    return out


def write_empty_gold_json(out_dir, empty):
    out = out_dir / "empty_gold_counts.json"
    out.write_text(json.dumps({str(k): v for k, v in sorted(empty.items())}, indent=2), encoding="utf-8")
    return out


def main():
    argv = sys.argv[1:]
    path = Path(argv[0]) if argv else Path("locomo_bench/locomo/data/locomo10.json")
    out_dir = Path(argv[1]) if len(argv) > 1 else Path(".")
    out_dir.mkdir(parents=True, exist_ok=True)

    if not path.exists():
        print(f"ERROR: locomo10.json not found at {path}", file=sys.stderr)
        print("Pass its path as the first argument.", file=sys.stderr)
        return 2

    counts, wh, empty = analyze(path)

    csv_out = write_csv(out_dir, counts, wh, empty)
    json_out = write_empty_gold_json(out_dir, empty)

    print(f"Wrote {csv_out}")
    print(f"Wrote {json_out}")
    print()
    print("Summary:")
    total = sum(counts.values())
    print(f"  Total QA pairs: {total}")
    for cat in sorted(counts):
        print(f"  Category {cat}: n={counts[cat]}, empty_gold={empty[cat]} "
              f"({100.0*empty[cat]/counts[cat]:.1f}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
