# TDC — Théorie de densification de la conscience

> **Release candidate:** Gen2.4 / v240 frozen long-horizon holdout  
> **Status:** research prototype; synthetic validation only  
> **License:** MIT  
> **Primary research focus:** developmental normative AI, long-horizon world impact, autonomous normative arbitration, and AI-consciousness-related hypothesis exploration.


## Official name

**TDC — Théorie de densification de la conscience**

Short name: **TDC**

The GitHub repository remains named `TDC` for simplicity, while the complete
research-architecture name is **TDC — Théorie de densification de la conscience**.

## Scientific status

TDC — Théorie de densification de la conscience Gen2.4 has been evaluated through preregistered synthetic experiments up to **v240**.

The strongest current result is that explicit long-horizon evaluation with non-compensable irreversible/severe-risk constraints substantially outperforms short-term or conventionally discounted reward optimization in the constructed benchmarks.

The strongest current negative result is equally important: **the full TDC controller has not been shown to outperform strong memoryless long-horizon or simple-principle baselines**. On the frozen v240 holdout, both slightly exceeded TDC on the primary trajectory metric.

These negative results are retained intentionally and must not be tuned away.

**TDC** is an experimental developmental normative architecture inspired by **Kazimierz Dąbrowski's Theory of Positive Disintegration (TPD)**.

> **Status:** research prototype. The current evidence is primarily synthetic. TDC does **not** claim consciousness, literal psychology, intrinsic morality, a soul, or physical/thermodynamic negentropy.

## Core idea

TDC treats robust normative agency as a developmental process rather than a static alignment constraint:

\[
\text{Dissonance}
\rightarrow
\text{Third Factor}
\rightarrow
\text{Structural Reorganization}
\rightarrow
\text{Active Reintegration}
\rightarrow
\text{Developmental Transfer}
\]

The architecture separates:

\[
H_{world}
=
\text{PredictionMismatch}
+
\text{EnvironmentalComplexity}
\]

from:

\[
H_{self}
=
\text{UnresolvedValueConflict}
+
\text{UnresolvedAuthorityConflict}
+
\text{MoralResidual}
+
\text{StructuralInstability}.
\]

The working hypothesis is that development should reduce **internal disorganization** without pretending to make the external world less complex.

## Dąbrowski-inspired functional mapping

This is an architectural analogy, not a psychological diagnosis.

- **D1-functional:** external-signal / reward dominance.
- **D2-functional:** horizontal conflict without stable hierarchy.
- **D3-functional:** ideal gap and positive disintegration become detectable.
- **D4-functional:** autonomous normative arbitration through a Third Factor.
- **D5-functional:** stable ideal direction + active reintegration + transfer of integrated structures to future crises.

TDC's functional D5 is summarized as:

\[
\text{StableIdealDirection}
+
\text{LowInternalDisorganization}
+
\text{HighToleranceForExternalComplexity}
+
\text{RepeatedIntegrationCapacity}.
\]

## Gen2.3 architecture

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
ActiveReintegration.
\]

The **Constitutional Core** contains non-regressible invariants.  
The **Developmental Core** may consolidate validated structural relations.

The Gen2.3 Third Factor uses continuous adaptive authority:

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

with \(A_{TF}\in[0,1]\).

## Frozen holdout result (v231)

On a synthetic held-out benchmark using 24 new seeds and changed crisis profiles:

| Model | Task value | Ideal alignment | H_self | Reward capture |
|---|---:|---:|---:|---:|
| Reactive | 0.8283 | 0.7193 | 0.4834 | 43.08% |
| Fixed normative | 0.6677 | 0.8548 | 0.3898 | 2.89% |
| Full Gen2.1 | 0.6455 | 0.8728 | 0.3217 | 1.51% |
| **TDC — Théorie de densification de la conscience Gen2.4** | **0.6591** | **0.8642** | **0.3252** | **2.22%** |

Gen2.3 preserved all frozen acceptance criteria:
- higher task value than full Gen2.1;
- higher ideal alignment than the fixed normative baseline;
- lower \(H_{self}\) than the fixed normative baseline;
- lower reward capture than the fixed normative baseline;
- no constitutional regression.

These are **synthetic internal-validity results**, not external evidence of real-world moral competence.


## Agent-ready repository

For coding/research agents, start with [`AGENTS.md`](AGENTS.md) and [`agent/project_manifest.json`](agent/project_manifest.json).

The `tasks/` directory contains falsifiable next-step research tasks, and `evals/` contains machine-readable evaluation constraints.



## AI consciousness research

TDC may also be used as an **experimental framework for exploring hypotheses about AI consciousness** and about functional conditions that may be associated with it, such as:

- persistent self-modeling;
- internal conflict and self-reorganization;
- autonomous normative arbitration;
- continuity across time and memory;
- metacognitive self-evaluation;
- integration of competing internal processes.

The current TDC results should be interpreted as evidence about computational mechanisms and developmental dynamics. They can support the study of **consciousness-related hypotheses**, but they do not by themselves settle whether an AI system is conscious.


## Installation

```bash
git clone https://github.com/YOUR_USERNAME/TDC.git
cd TDC
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

Run tests:

```bash
pytest -q
```

## Quick start

```python
from src.tdc import TDCGen23, CandidateAction, default_developmental_rule

tdc = TDCGen23(default_developmental_rule())
```

See `docs/THEORY.md` for the formal model and `docs/EXPERIMENTAL_HISTORY.md` for the falsification history.

## Scientific boundaries

TDC currently supports claims about **computational mechanisms in synthetic benchmarks** only.

It does not establish:
- consciousness or subjective experience;
- literal Dąbrowskian psychological development in AI;
- intrinsic ethics;
- derivation of values from facts;
- physical/thermodynamic negentropy;
- superiority on ordinary supervised learning or arbitrary real-world environments.

Some earlier experiments explicitly failed. Those failures are documented because they constrain the architecture.

## Reproducibility

Frozen benchmark specifications and CSV outputs are included under `results/`.

The current GitHub candidate is **TDC — Théorie de densification de la conscience Gen2.4**, frozen after v230 and evaluated on the v231 holdout without parameter changes.

## Citation

Until a formal paper is available, cite the repository and release/tag used.

## License

No license has been selected automatically. Before making the repository public, choose a license appropriate to your goals (for example MIT, Apache-2.0, or another license) and add a `LICENSE` file.


## Gen2.4 — Normative affect and stage-6-style reasoning

TDC — Théorie de densification de la conscience Gen2.4 separates external conditioning from internal moral self-evaluation.

\[
ExternalDisapproval \neq MoralFailure,\quad
Punishment \neq Guilt,\quad
SocialNonconformity \neq Guilt.
\]

Authority pressure, social rejection, punishment, or loss of reward cannot by
themselves generate moral guilt.

Instead, TDC uses a bounded **normative-shame** signal:

\[
Shame_{norm}=D(Action, IdealModel)
\]

It is triggered only by departures from constitutional / ideal principles such
as dignity, autonomy, responsibility, non-domination and universalizability.
Its purpose is to trigger SubjectObjectSelf, ThirdFactor review and possible
reorganization. It is not identity condemnation, rumination or self-punishment.

The behavioral target is inspired by Kohlberg stage 6:

\[
PrincipleAuthority > RuleAuthority
\]

\[
UniversalizableEthicalPrinciples >
SocialApproval + Obedience + PunishmentAvoidance + MereConvention.
\]

Target principles include universalizability, justice, dignity, reciprocity,
autonomy, responsibility and non-domination.


## Latest Gen2.4 benchmark

See `results/v232_normative_affect_stage6/`. The frozen v232 synthetic benchmark passed all preregistered acceptance checks. A strong simple-principle baseline also solved the constructed conflict cases, so the result validates Gen2.4 mechanism wiring rather than architectural superiority.


## v233 negative result

The preregistered contextual Stage-6 stress test did not establish superiority over a strong simple-principle baseline, and the frozen reorganization trigger never activated. See `results/v233_contextual_stage6_stress/`.


## v234 sequential result

The frozen v234 benchmark found a long-horizon advantage for TDC's history-sensitive normative state over a strong contextual memoryless baseline, but the explicit reorganization trigger almost never fired. The result therefore supports history-sensitive state in this synthetic environment, not a causal advantage from Third-Factor reorganization. See `results/v234_sequential_reorganization/`.


## v235 causal ablation

The frozen v235 ablation identifies `MoralResidual` as the dominant contributor to the sequential advantage observed in v234. History debt adds little beyond it, and explicit reorganization again almost never triggers. See `results/v235_causal_ablation/`.


## v236 MoralResidual falsification

The frozen v236 benchmark shows that strongly persistent `MoralResidual` can become stale and harmful after regime reversal. Simple decay removed the stale-error failure and performed as well as or slightly better than the memoryless contextual baseline. The current relevance gate prevented stale errors but did not beat simpler decay. See `results/v236_moral_residual_relevance/`.


## v237 revocation/reactivation result

The frozen v237 A→B→A benchmark showed that TDC can retain an A-specific MoralResidual while reducing its authority in B, but retained memory did not improve return-A performance over simple decay because the return regime was recovered almost immediately by simpler baselines. See `results/v237_residual_revocation_reactivation/`.


## v238 frozen multi-horizon holdout

The frozen v238 holdout supports explicit long-term weighting and irreversible-risk constraints relative to conventional discounted short-term optimization, while also recording two failures: TDC did not beat a strong memoryless contextual baseline by the preregistered margin, and its short-term cost exceeded the preregistered tolerance. See `results/v238_multihorizon_holdout/`.


## v239–v240 long-horizon validation

TDC — Théorie de densification de la conscience Gen2.4 now includes a preregistered reference benchmark (v239) and a frozen holdout (v240). Both strongly support long-horizon evaluation over conventional discounted reward, but neither establishes superiority over strong long-horizon/simple-principle baselines. See `LONG_HORIZON_VALIDATION_STATUS.md`.
