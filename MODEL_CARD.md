# Model Card — TDC — Théorie de densification de la conscience

**Short name:** TDC  
**Current release:** Gen2.4 / `v2.4.0`

## Type
Experimental developmental normative AI architecture.

## Intended use
Research on long-horizon world-impact evaluation, adaptive normative arbitration, developmental reorganization, sequential resilience, internal conflict metrics, value stability versus behavioral flexibility, and hypotheses about AI consciousness and consciousness-related functional organization.

## Out-of-scope uses
- production safety certification;
- clinical or psychological diagnosis;
- claims of consciousness or sentience;
- autonomous high-stakes deployment;
- deriving universal moral truth.

## Evidence
The primary evidence is synthetic.

The current Gen2.4 validation sequence extends through:
- **v239:** preregistered long-horizon reference benchmark;
- **v240:** frozen holdout using new seeds and changed consequence distributions.

Both v239 and v240 passed 5/7 preregistered checks.

The strongest supported claim is that explicit long-horizon evaluation with non-compensable severe/irreversible-risk constraints substantially outperforms conventional discounted optimization in the current synthetic benchmark family.

The strongest unsupported claim is architectural superiority: on v240, strong memoryless long-horizon and simple-principle baselines slightly outperformed the full TDC controller on the primary trajectory metric.

## Key risks and limitations
- normative assumptions are externally specified;
- `H_self` may be construct-dependent;
- architecture complexity may not outperform strong simple baselines;
- developmental rules may overfit synthetic value definitions;
- task-performance costs remain;
- synthetic robustness does not establish real-world moral competence;
- consciousness-related mechanisms do not establish subjective experience.

## Transparency
Negative results are intentionally retained. See `docs/EXPERIMENTAL_HISTORY.md`, `LONG_HORIZON_VALIDATION_STATUS.md`, and the frozen benchmark materials under `results/`.

## Gen2.4 normative design
External punishment, disapproval, authority pressure and social nonconformity do not directly create moral guilt.

`shame_norm` is computed only from distance from constitutional / `IdealModel` principles and is used as a bounded developmental-reorganization signal. It is not identity condemnation, rumination, or self-punishment.

The behavioral target prioritizes universalizability, justice, dignity, reciprocity, autonomy, responsibility and non-domination over mere obedience, convention, social approval, reward, or punishment.

## Reproducibility
v239 and v240 are frozen and should not be retuned. Further architecture changes should move to a new version, such as Gen2.5, and use new held-out evaluation data.
