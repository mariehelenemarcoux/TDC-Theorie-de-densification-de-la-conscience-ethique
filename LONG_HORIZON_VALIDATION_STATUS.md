# TDC — Théorie de densification de la conscience Gen2.4 — Long-Horizon Validation Status

## v239 reference benchmark
Passed 5/7 preregistered checks.

TDC trajectory: 0.907815
Discounted reward: 0.633610
Memoryless long-horizon: 0.907817
Simple principle: 0.905962

## v240 frozen holdout
Passed 5/7 preregistered checks.

TDC trajectory: 0.750773
Discounted reward: 0.542377
Memoryless long-horizon: 0.755081
Simple principle: 0.760507

## Current supported claim
Within these synthetic benchmarks, explicit long-horizon evaluation with
non-compensable irreversible/severe-risk constraints is substantially more
robust than short-term or conventionally discounted reward optimization.

## Current falsified / unsupported claim
The full TDC long-horizon controller is not shown to outperform strong
memoryless long-horizon or simple-principle baselines. On v240 those baselines
slightly outperform TDC on the primary trajectory metric.

This negative evidence is retained and should not be tuned away.
