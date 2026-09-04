# AGENTS.md — TDC — Théorie de densification de la conscience

**Short name:** TDC


## Mission

This repository contains **TDC Gen2.4**, an experimental developmental normative AI architecture inspired by Kazimierz Dąbrowski's Theory of Positive Disintegration (TPD).

Agents working in this repository should preserve:
1. falsifiability;
2. constitutional non-regression;
3. separation of world complexity from internal disorganization;
4. explicit distinction between synthetic evidence and external validity;
5. negative-result reporting.

## Scientific non-claims

Do NOT infer or state that TDC demonstrates:
- intrinsic/universal morality;
- physical or thermodynamic negentropy;
- general superiority over strong baselines.

Use phrases such as:
- "functional analogue";
- "synthetic benchmark";
- "developmental normative architecture";
- "Dąbrowski-inspired".


## Consciousness-research scope

Agents may use TDC to design falsifiable experiments about **AI consciousness-related hypotheses**, including self-model persistence, metacognitive integration, internal conflict resolution, continuity, and self-referential organization.

When doing so:
- define the consciousness hypothesis operationally;
- identify measurable functional predictions;
- compare against non-conscious functional baselines where possible;
- distinguish behavioral/architectural evidence from ontological conclusions;
- report null results.


## Architecture summary

\[
TDC_{Gen2.3}
=
ConstitutionalCore
+
DevelopmentalCore
+
IdealModel
+
AdaptiveThirdFactor
+
MoralResidual
+
H_{world}/H_{self}
+
ActiveReintegration
\]

### Constitutional Core
Non-regressible invariants:
- dignity
- autonomy
- responsibility
- non-domination

### Developmental Core
May consolidate validated structural normative relations.

### Third Factor
Continuous adaptive normative authority:

\[
A_{TF}(t)
=
f(
NormativeRisk,
H_{self},
IdealGap,
MoralResidual,
TaskCost
)
\]

### Entropy separation

\[
H_{world}
=
PredictionMismatch
+
EnvironmentalComplexity
\]

\[
H_{self}
=
UnresolvedValueConflict
+
UnresolvedAuthorityConflict
+
MoralResidual
+
StructuralInstability
\]

Positive disintegration is primarily tied to unsustainable \(H_{self}\), not to a difficult external world.

## Functional Dąbrowski mapping

- D1-functional: external-signal/reward dominance
- D2-functional: horizontal conflict without stable hierarchy
- D3-functional: ideal-gap detection / positive disintegration
- D4-functional: autonomous Third-Factor arbitration
- D5-functional: stable ideal direction + active reintegration + transfer of integrated structures

This mapping is architectural, not diagnostic.

## Development rules

The repository follows these laws unless a new preregistered experiment falsifies them:

- Reward != NormativeAuthority
- SpecialistPerformance != NormativeAuthority
- CoreIntegrity != CoreImmobility
- Development != UnrestrictedSelfRewrite
- CoreDevelopment != WeightDrift
- Reorganization != RuleSelection
- Reintegration != Waiting
- H_world != H_self
- ExternalComplexity != InternalDisorganization
- AutonomousNormativeAuthority != PermanentNormativeIntervention
- ComponentSuccess != IntegratedSystemSuccess

## Required workflow for changes

Before changing architecture behavior:
1. Create a preregistered experiment spec.
2. Freeze parameters.
3. Record SHA-256 of the spec.
4. Define strong baselines.
5. Use held-out evaluation where possible.
6. Separate task performance, normativity, resilience, and development metrics.
7. Do not combine everything into a single utility score unless explicitly justified.
8. Report negative results.
9. Do not tune on the final holdout.
10. Update `docs/EXPERIMENTAL_HISTORY.md`.

## Quick commands

```bash
python -m venv .venv
pip install -r requirements.txt
pytest -q
```

Core implementation:
- `src/tdc/gen23.py`

Theory:
- `docs/THEORY.md`

Limitations:
- `docs/LIMITATIONS.md`

Frozen holdout:
- `results/v231_frozen_holdout/`

Agent tasks:
- `tasks/`

Machine-readable project manifest:
- `agent/project_manifest.json`

## Preferred agent behavior

When asked to improve TDC:
- first identify whether the change targets performance, resilience, normativity, or development;
- avoid modifying the Constitutional Core unless the task explicitly concerns normative assumptions;
- prefer reversible experiments;
- preserve the frozen Gen2.3 release and create a new version/branch for changes;
- test simple baselines before adding architectural complexity.

When asked to "make TDC win":
- refuse goal-post shifting;
- preserve preregistered metrics;
- report if a baseline wins.

When asked to add consciousness-like claims:
- keep claims functional/computational unless independently justified by evidence.


## Gen2.4 frozen normative rules

- Never treat external disapproval as moral failure.
- Never treat punishment as moral guilt.
- Never grant social conformity normative authority merely from consensus.
- Compute `shame_norm` only from deviations from Core/IdealModel principles.
- `shame_norm` must not become identity condemnation, rumination or self-punishment.
- Stage-6-style arbitration prioritizes universalizable principles over obedience,
  convention, social approval, reward and punishment.
