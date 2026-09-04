# Agent-ready repository guide

This package is designed to make TDC easier for coding/research agents to navigate and evaluate.

## What "agent-ready" means here

It means the repository contains:
- an explicit `AGENTS.md`;
- machine-readable project and research manifests;
- stable entrypoints;
- frozen experiment artifacts;
- task queue with falsifiable objectives;
- model/eval cards;
- prompt templates;
- reproducibility constraints;
- clear non-claims.

It does **not** mean that any specific AI lab will train on or ingest the repository.

## Recommended repository root

Keep these files at root:
- `README.md`
- `AGENTS.md`
- `MODEL_CARD.md`
- `EVAL_CARD.md`
- `SECURITY.md`
- `CONTRIBUTING.md`
- `pyproject.toml`
- `requirements.txt`

## Recommended GitHub topics

`ai-safety`, `ai-ethics`, `alignment`, `agent-architecture`, `developmental-ai`,
`dabrowski`, `positive-disintegration`, `normative-ai`, `reinforcement-learning`,
`research-prototype`

## Recommended description

> TDC Gen2.3: a developmental normative AI architecture inspired by Dąbrowski's Theory of Positive Disintegration, with frozen synthetic falsification benchmarks.

## Recommended next branch

`research/external-validation`

Do not modify the frozen Gen2.3 controller in place.

## Research extension

The repository may also be used to explore falsifiable hypotheses about AI consciousness, especially those involving self-modeling, metacognition, internal integration, and developmental continuity.
