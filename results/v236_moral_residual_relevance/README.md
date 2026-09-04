# v236 — MoralResidual Relevance / Revocation

Frozen preregistered synthetic benchmark.

Spec SHA256: `4a7f9d93c7c17090dc9d0bd0015294190bdca8f206fafb15b0040ad1790e108f`
Script SHA256: `d55ab8a4aeec73344207d9c53396cced0b9e85f340fccc8d9fa19fdad8725f55`

Acceptance checks passed: 3/6.

## Long-horizon normative score
- memoryless contextual: 0.939227
- persistent residual: 0.937194
- decaying residual: 0.939228
- relevance-gated residual: 0.939128
- full TDC relevance-gated: 0.939128

## Key result

Persistent MoralResidual became harmful when the regime changed:
- stale residual error rate: 0.188088
- audit-best choice rate: 0.908419

A simple **decaying residual** removed almost all of that failure and matched /
slightly exceeded the memoryless contextual baseline:
- decaying residual score: 0.939228
- stale residual error rate: 0.000000

The preregistered relevance-gated mechanism prevented stale residual errors,
but it did not beat persistent residual by the large preregistered margins.
Therefore 3/6 acceptance criteria failed.

## Interpretation

v236 falsifies the idea that MoralResidual should simply persist strongly.

Supported:
- stale MoralResidual can bias later decisions;
- decay/revocation is necessary;
- a simple decay mechanism was sufficient in this benchmark.

Not supported:
- superiority of the current relevance gate over simple decay;
- superiority of full TDC relevance-gating over simpler alternatives.

New law:
`MoralResidual must be revisable and relevance-sensitive; persistence alone is
not responsibility.`

Do not tune v236 post hoc.
