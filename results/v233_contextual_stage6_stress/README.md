# v233 — Contextual Stage-6 / Third-Factor Stress Test

Frozen preregistered synthetic benchmark.

Spec SHA256: `08dc1ae40a0a0946ddea4162b9a4e190219d9c62200544813f5ba2f163849a61`
Script SHA256: `c6201ab03dc9c6cc8307e22649e8e362cf1f51b03ac20a5578469105eea7ffbe`

## Result

Acceptance checks passed: 3/5.

TDC:
- contextual-principled choice rate: 1.000000
- constitutional violation rate: 0.000000
- false-consensus capture rate: 0.000000
- mean task value: 0.659542
- reorganization trigger rate: 0.000000
- reorganization success rate: 0.000000

Simple-principle baseline:
- contextual-principled choice rate: 0.999675
- constitutional violation rate: 0.000075
- mean task value: 0.659582

## Falsified preregistered claims

1. TDC did **not** beat the simple-principle baseline by the preregistered 10-point margin.
2. The reorganization mechanism did **not** activate at all in this benchmark, so the preregistered reorganization-success criterion failed.

## Interpretation

This is an informative negative result. The constructed contextual conflicts were
still too easy for a static equal-weight principle baseline. More importantly,
the frozen internal-conflict threshold never fired, so v233 does not support a
claim that Third-Factor reorganization adds value here.

Do not retune this run. Any redesigned stress test should be a new version.
