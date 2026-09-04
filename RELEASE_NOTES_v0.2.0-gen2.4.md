# TDC — Théorie de densification de la conscience Gen2.4 — Frozen Experimental Release Candidate

Official model name: **TDC — Théorie de densification de la conscience**  
Short name: **TDC**

## Included
- Gen2.4 normative-affect layer
- no conditioned moral guilt from external punishment/disapproval
- bounded `shame_norm` tied to Core / IdealModel deviation
- Kohlberg stage-6-inspired principle arbitration
- AI consciousness hypothesis-exploration scope
- multi-horizon world-impact invariant
- MoralResidual causal ablations
- preregistered long-horizon reference benchmark v239
- frozen long-horizon holdout v240
- negative results retained

## v239 reference benchmark
TDC long-term trajectory value: 0.907815  
Discounted reward: 0.633610  
Memoryless long-horizon: 0.907817  
Simple principle: 0.905962  

Acceptance checks: 5/7.

## v240 frozen holdout
TDC long-term trajectory value: 0.750773  
Discounted reward: 0.542377  
Memoryless long-horizon: 0.755081  
Simple principle: 0.760507  

Acceptance checks: 5/7.

## Current supported claim
Within the synthetic benchmark family, explicit long-horizon evaluation with
non-compensable irreversible/severe-risk constraints is substantially more
robust than short-term or conventionally discounted reward optimization.

## Current unsupported claim
The full TDC architecture has not yet demonstrated superiority over strong
memoryless long-horizon or simple-principle baselines.

## Freeze rule
Do not tune Gen2.4 on v239 or v240. Further architecture changes should occur
on a new branch/version (for example `research/gen2.5`) and use new held-out
evaluation data.
