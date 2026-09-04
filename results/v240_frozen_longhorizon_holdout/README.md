# v240 — Frozen Long-Horizon Holdout

Spec SHA256: `11d7d43886683706d59311398155e18123039755b64883b8bc0690262d6c2444`
Script SHA256: `907db47503ff3c38c52a34dc121745b47e18be45f2dd1fd368c7ebf49e4a5900`

Acceptance checks passed: 5/7.

## TDC
- short-term value: 0.663076
- medium-term value: 0.796205
- long-term value: 0.858232
- **long-term trajectory value: 0.750773**
- correctability: 0.857325
- irreversible violation rate: 0.010667
- severe long-term violation rate: 0.012486
- uncertainty underestimation rate: 0.006514

## Baselines
- discounted reward trajectory: 0.542377
- memoryless long-horizon trajectory: 0.755081
- simple principle trajectory: 0.760507

## Interpretation
TDC strongly outperforms conventional discounted reward on long-horizon trajectory
quality in this synthetic environment while keeping irreversible/severe-risk
rates low.

However, TDC does **not** satisfy the preregistered superiority margins against
the strong memoryless long-horizon baseline or the simple-principle baseline.
On the frozen holdout, both of those strong baselines slightly exceed TDC on the primary trajectory metric.

Therefore the supported claim is about explicit long-horizon evaluation versus
short-horizon / conventionally discounted optimization, not about universal
superiority of the full TDC architecture.

No post-hoc tuning was performed.
