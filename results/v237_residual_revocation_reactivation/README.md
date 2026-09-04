# v237 — MoralResidual Revocation / Reactivation

Frozen preregistered A→B→A benchmark.

Spec SHA256: `fd4923c2fb412c4cc46d02c650149f2bf6c23aa00373f27134fa7798ffd7ac6e`
Script SHA256: `d18ecf1f873a7a36edd3485bc641f44c76d48bf63271698ba2627501abd88768`

Acceptance checks passed: 4/6.

## Key results
- persistent residual long-horizon: 0.942069
- simple decay: 0.942776
- relevance gate: 0.942771
- revocable persistent memory: 0.942528
- memoryless contextual: 0.942721

### Revocable persistent memory
- B stale-error rate: 0.029415
- A-return normative score: 0.952602
- A-return recovery lag: 0.035714
- stored residual retention: 1.000000

## Falsified expectations
The revocable-memory mechanism did not beat simple decay on A-return score and
did not improve recovery lag. Those two preregistered criteria failed.

## Supported points
- revocation reduced stale carryover relative to persistent residual;
- stored A-residual was retained through B (retention = 1.0);
- no constitutional violations occurred;
- task cost stayed within tolerance.

## Interpretation
This benchmark does **not** show a benefit from reactivating stored MoralResidual.
The A-return environment was easy enough that simple decay and even memoryless
contextual control recovered essentially immediately. Therefore memory retention
was demonstrated, but its added value was not.

New methodological conclusion:
`Revocation != Erasure` can be implemented, but `RetainedMemory != UsefulRecall`.

Do not retune v237. A holdout or a harder recall benchmark should be a new version.
