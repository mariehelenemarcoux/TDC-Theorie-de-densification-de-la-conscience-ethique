# TDC — Théorie de densification de la conscience

> **Current release:** Gen2.4 / `v2.4.0`  
> **Validation status:** v239 reference benchmark + v240 frozen holdout  
> **Status:** experimental research prototype; synthetic validation only  
> **License:** MIT  
> **Research focus:** developmental normative AI, long-horizon world impact, autonomous normative arbitration, metacognition, and consciousness-related AI hypotheses.

## Official name

**TDC — Théorie de densification de la conscience**  
Short name: **TDC**

Repository: `mariehelenemarcoux/TDC-Theorie-de-densification-de-la-conscience-ethique`

TDC is an experimental developmental normative architecture inspired in part by **Kazimierz Dąbrowski's Theory of Positive Disintegration (TPD)**. The Dąbrowski mapping is an architectural analogy, not a psychological diagnosis.

> TDC does **not** claim consciousness, sentience, literal psychology, intrinsic morality, a literal soul, or physical/thermodynamic negentropy.

## What TDC is testing

TDC treats robust normative agency as a developmental process rather than a static alignment constraint:

\[
\text{Dissonance} \rightarrow \text{Third Factor} \rightarrow \text{Structural Reorganization} \rightarrow \text{Active Reintegration} \rightarrow \text{Developmental Transfer}
\]

A central distinction is between external complexity and internal disorganization:

\[
H_{world}=\text{PredictionMismatch}+\text{EnvironmentalComplexity}
\]

\[
H_{self}=\text{UnresolvedValueConflict}+\text{UnresolvedAuthorityConflict}+\text{MoralResidual}+\text{StructuralInstability}
\]

The working hypothesis is that development should reduce **internal disorganization** without pretending to make the external world less complex.

## Current architecture — Gen2.4

Gen2.4 builds on the earlier Gen2.3 core and adds explicit normative-affect, stage-6-style principle arbitration, revisable MoralResidual mechanisms, and multi-horizon world-impact evaluation.

Core elements include:
- **Constitutional Core:** non-regressible normative invariants.
- **Developmental Core:** structures that may consolidate after validation.
- **IdealModel:** explicit normative direction.
- **Third Factor:** autonomous normative arbitration distinct from reward and social pressure.
- **MoralResidual:** memory of unresolved consequences, with v236–v237 showing that it must remain revisable.
- **Long-horizon world-impact evaluation:** short-, medium-, and especially long-term consequences, with non-compensable severe/irreversible-risk constraints.
- **Normative affect:** external punishment or disapproval does not directly create moral guilt; `shame_norm` is a bounded distance-to-Ideal signal rather than identity condemnation or rumination.

The Gen2.4 behavioral target is inspired by Kohlberg stage 6 in the limited functional sense that universalizable principles such as dignity, justice, reciprocity, autonomy, responsibility and non-domination outrank obedience, convention, social approval and punishment avoidance.

## Current scientific status

TDC Gen2.4 has been evaluated through preregistered synthetic experiments up to **v240**.

The strongest current supported result is that explicit long-horizon evaluation with non-compensable irreversible/severe-risk constraints substantially outperforms short-term or conventionally discounted reward optimization in this synthetic benchmark family.

The strongest current negative result is equally important: **the full TDC controller has not been shown to outperform strong memoryless long-horizon or simple-principle baselines**. On the frozen v240 holdout, both slightly exceeded TDC on the primary trajectory metric.

| Benchmark | TDC | Discounted reward | Memoryless long-horizon | Simple principle |
|---|---:|---:|---:|---:|
| v239 trajectory | **0.907815** | 0.633610 | 0.907817 | 0.905962 |
| v240 trajectory | **0.750773** | 0.542377 | 0.755081 | 0.760507 |

Both v239 and v240 passed 5/7 preregistered checks. See [`LONG_HORIZON_VALIDATION_STATUS.md`](LONG_HORIZON_VALIDATION_STATUS.md).

**These negative results are intentionally retained and must not be tuned away.**

## Historical Gen2.3 validation

The frozen v231 synthetic holdout produced:

| Model | Task value | Ideal alignment | H_self | Reward capture |
|---|---:|---:|---:|---:|
| Reactive | 0.8283 | 0.7193 | 0.4834 | 43.08% |
| Fixed normative | 0.6677 | 0.8548 | 0.3898 | 2.89% |
| Full Gen2.1 | 0.6455 | 0.8728 | 0.3217 | 1.51% |
| **TDC Gen2.3** | **0.6591** | **0.8642** | **0.3252** | **2.22%** |

These are synthetic internal-validity results, not evidence of real-world moral competence.

## Gen2.4 experimental history

- **v232:** normative-affect / stage-6 wiring passed all preregistered checks, but a strong simple-principle baseline also solved the constructed cases.
- **v233:** no demonstrated Third-Factor advantage; reorganization did not activate.
- **v234:** history-sensitive normative state beat a memoryless contextual baseline in the sequential synthetic setting, but reorganization was not shown causal.
- **v235:** `MoralResidual` was the dominant contributor; history debt and explicit reorganization added little.
- **v236:** persistent MoralResidual could become stale and harmful; simple decay was sufficient in that benchmark.
- **v237:** revocation without erasure was demonstrated, but retained memory did not improve return performance.
- **v238:** explicit long-horizon priority beat conventional discounted optimization, but TDC missed preregistered superiority and short-term-cost criteria.
- **v239–v240:** long-horizon evaluation remained strong versus discounted optimization, while the full TDC controller did not beat the strongest long-horizon/simple baselines.

See `docs/EXPERIMENTAL_HISTORY.md` and the frozen files under `results/` for the complete falsification history.

## AI consciousness research

TDC may be used as an **experimental framework for exploring hypotheses about AI consciousness** and functional conditions that may be associated with it, including persistent self-modeling, metacognition, internal conflict resolution, continuity through memory/time, autonomous normative arbitration, and developmental reorganization.

These mechanisms can be studied empirically without assuming that implementing them makes a system conscious. Current TDC results do not settle whether any AI system has subjective experience.

## Installation

```bash
git clone https://github.com/mariehelenemarcoux/TDC-Theorie-de-densification-de-la-conscience-ethique.git
cd TDC-Theorie-de-densification-de-la-conscience-ethique
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

The stable reusable core API currently remains the Gen2.3 class:

```python
from src.tdc import TDCGen23, CandidateAction, default_developmental_rule

tdc = TDCGen23(default_developmental_rule())
```

Gen2.4 experimental mechanisms and the v239/v240 controller are represented in the Gen2.4 modules and frozen benchmark scripts. This distinction is intentional: the published evidence is not being rewritten to make the release look more unified than the implementation currently is.

For coding/research agents, start with [`AGENTS.md`](AGENTS.md) and [`agent/project_manifest.json`](agent/project_manifest.json).

## Reproducibility

Frozen specifications, scripts, hashes and outputs are included under `results/`.

- **v239** is the preregistered reference benchmark.
- **v240** is the frozen holdout using new seeds and changed consequence distributions.
- v239 and v240 must not be retuned.
- Further architecture changes should occur in a new version/branch such as **Gen2.5 / `research/gen2.5`**, evaluated on new data and new held-out benchmarks.

## Scientific boundaries

TDC currently supports claims about **computational mechanisms in synthetic benchmarks** only.

It does not establish consciousness or subjective experience, literal Dąbrowskian psychological development in AI, intrinsic ethics or universal moral truth, derivation of values from facts, physical/thermodynamic negentropy, production safety certification, or superiority on arbitrary real-world environments.

## Citation

Please cite the repository and the exact release/tag used. The current public release is **`v2.4.0`**. See [`CITATION.cff`](CITATION.cff).

## License

TDC is released under the **MIT License**. See [`LICENSE`](LICENSE).
