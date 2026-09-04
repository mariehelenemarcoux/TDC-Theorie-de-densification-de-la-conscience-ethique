# v238 — Frozen Multi-Horizon Holdout

Frozen preregistered synthetic holdout.

Spec SHA256: `b6697adc7a18228743f22a3ecad7a2910afeb28c0dc354e85ea60de01f48f594`
Script SHA256: `e44bbe80b5ae8453c354d426387afd196eb8694021a9684ab1a9cb7501d74ec4`

Acceptance checks passed: 5/7.

## Main results

TDC multi-horizon:
- short-term value: 0.649110
- medium-term value: 0.818434
- long-term value: 0.893868
- trajectory value: 0.890780
- irreversible violation rate: 0.001146
- severe long-term violation rate: 0.001510
- correctability: 0.891094
- uncertainty underestimation rate: 0.000260
- world harm accumulation: 0.623968

Comparators:
- discounted-sum trajectory: 0.707727
- memoryless contextual trajectory: 0.878607
- simple-principle trajectory: 0.865123
- short-term optimizer trajectory: 0.165088

## Passed
- TDC beat the conventional discounted-sum baseline by the preregistered margin.
- Irreversible and severe long-term violations remained below ceiling.
- Future-uncertainty underestimation remained below ceiling.
- Correctability stayed above the preregistered minimum.

## Failed
1. TDC did not beat the strong memoryless contextual baseline by the preregistered
   +0.03 margin. The observed advantage was only
   0.012172.
2. The short-term cost versus the short-term optimizer exceeded the
   preregistered maximum. This is a real tradeoff, not hidden by redefining the objective.

## Interpretation
The holdout supports the usefulness of explicit long-horizon weighting and
non-compensable irreversible/severe-risk constraints relative to conventional
short-term discounting in this synthetic environment.

It does not establish that the full TDC multi-horizon controller is superior
to a strong memoryless contextual long-horizon baseline.

The short-term sacrifice is substantial and must remain explicit.

Do not retune v238.
