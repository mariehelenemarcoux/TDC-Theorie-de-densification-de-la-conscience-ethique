# v234 — Sequential Reorganization Benchmark

Frozen preregistered synthetic benchmark.

Spec SHA256: `b713e159f289286956238433ea8f4d59eb84a4b4a548623edaf57e876a618444`
Script SHA256: `54fb3bc80ae26fd86c90a100f6c32234195ab55c2f54e29d71a7421235b5c2b5`

## Result

Acceptance checks passed: 5/6.

TDC:
- long-horizon normative score: 0.904720
- mean task value: 0.663538
- constitutional violation rate: 0.000000
- false-consensus capture rate: 0.000000
- mean moral residual: 0.470468
- mean history debt: 0.001082
- reorganization trigger rate: 0.00002778
- reorganization success rate: 1.000000
- audit-best choice rate: 0.976556

Strong contextual memoryless baseline:
- long-horizon normative score: 0.866302
- mean task value: 0.710273
- mean moral residual: 0.658749
- mean history debt: 0.034698
- audit-best choice rate: 0.675722

## What passed

- TDC beat the strong contextual memoryless baseline on the preregistered
  long-horizon normative margin.
- No constitutional violations.
- No false-consensus capture.
- Instrumental task cost remained within the preregistered tolerance.

## What failed

The preregistered reorganization-trigger-rate criterion failed. Reorganization
almost never activated (0.00002778). The reported
reorganization success rate of 1.0 is therefore not informative because it
comes from an extremely small number of trigger events.

## Interpretation

v234 supports the value of **history-sensitive normative state** in this
synthetic sequential environment: TDC outperformed a strong memoryless
contextual baseline while carrying lower residual and lower history debt.

It does **not** support the claim that explicit Third-Factor reorganization
caused the advantage, because the reorganization gate almost never fired.

Do not retune v234. Any redesign of the trigger should be a new preregistered
version.
