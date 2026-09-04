# Benchmarks

The frozen CSV/spec outputs for v230 and v231 are included under `results/`.

The original exploratory notebook-style experiment scripts were executed interactively during development. For scientific publication, treat `results/v231_frozen_holdout/spec.json` and its SHA as the frozen evaluation record.

Recommended next step: extract the holdout generator/evaluator into a standalone deterministic script before submitting a paper or asking third parties to reproduce the exact benchmark.
