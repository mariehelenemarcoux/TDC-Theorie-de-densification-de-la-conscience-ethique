# v235 — Causal Ablation

Frozen preregistered synthetic ablation benchmark.

Spec SHA256: `62a83f5feb26aa4d0a7cbf2f5fafa579b2347e4d4afcab85aa1c58f8fc993bd7`
Script SHA256: `4bd525b578602d3713946efe84123590543374cdcc5e10ab4436e2815b9858cc`

Acceptance checks passed: 4/5.

## Long-horizon normative score
- memoryless contextual: 0.866546
- MoralResidual only: 0.904921
- history debt only: 0.872876
- residual + history: 0.904945
- full TDC + reorganization: 0.904949

## Main causal result

The dominant contributor in this benchmark is **MoralResidual**.

MoralResidual-only nearly reproduces the full advantage over the memoryless
contextual baseline. History-debt-only provides a much smaller gain.
Adding history debt on top of MoralResidual provides essentially no additional
preregistered margin, so the criterion requiring residual+history to beat the
best single component failed.

The explicit reorganization mechanism again activates only extremely rarely
(0.00006944); therefore this benchmark does not
support a causal contribution from reorganization.

## Interpretation

Supported in this synthetic environment:
- persistent MoralResidual can improve long-horizon normative decisions;
- memoryless contextual arbitration loses information about prior consequences.

Not supported:
- a meaningful additive advantage from history debt beyond MoralResidual;
- a causal advantage from the explicit reorganization trigger.

Do not tune v235 post hoc.
