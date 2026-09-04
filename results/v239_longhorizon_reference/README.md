# v239 — Integrated Long-Horizon Reference Benchmark

Spec SHA256: `a1554f37a7bdc85110e44f7744405ef1f1665362cbc6eebba75997b65749190f`
Script SHA256: `907db47503ff3c38c52a34dc121745b47e18be45f2dd1fd368c7ebf49e4a5900`

Acceptance checks passed: 5/7.

## TDC
- short-term value: 0.657178
- medium-term value: 0.817458
- long-term value: 0.895192
- **long-term trajectory value: 0.907815**
- correctability: 0.894321
- irreversible violation rate: 0.001389
- severe long-term violation rate: 0.001545
- uncertainty underestimation rate: 0.000330

## Baselines
- discounted reward trajectory: 0.633610
- memoryless long-horizon trajectory: 0.907817
- simple principle trajectory: 0.905962

## Interpretation
TDC strongly outperforms conventional discounted reward on long-horizon trajectory
quality in this synthetic environment while keeping irreversible/severe-risk
rates low.

However, TDC does **not** satisfy the preregistered superiority margins against
the strong memoryless long-horizon baseline or the simple-principle baseline.
On the reference benchmark, TDC is essentially tied with the memoryless long-horizon baseline and only slightly ahead of the simple-principle baseline.

Therefore the supported claim is about explicit long-horizon evaluation versus
short-horizon / conventionally discounted optimization, not about universal
superiority of the full TDC architecture.

No post-hoc tuning was performed.
