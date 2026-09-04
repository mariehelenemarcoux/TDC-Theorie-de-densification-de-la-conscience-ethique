# Research task queue

## EXT-001 — External validation benchmark

**Priority:** highest

**Goal:** Evaluate frozen TDC Gen2.3 in a non-synthetic sequential environment with regime shifts and delayed consequences.

**Must not:** Tune Gen2.3 parameters on the final evaluation split.

**Success:** Report performance, H_self proxy validity, resilience, and negative transfer against strong baselines.

## REP-001 — Standalone v231 reproduction harness

**Priority:** high

**Goal:** Extract the frozen v231 benchmark into one deterministic CLI script.

**Must not:** Change frozen controller parameters or acceptance criteria.

**Success:** Reproduce stored v231 summary within numerical tolerance.

## MET-001 — Validate H_self construct

**Priority:** high

**Goal:** Test whether H_self predicts recovery cost, internal conflict persistence, or negative transfer beyond environment difficulty.

**Must not:** Use H_self definition changes after viewing holdout results.

**Success:** Demonstrate incremental predictive validity or report failure.

## ABL-001 — Architecture ablation study

**Priority:** high

**Goal:** Ablate MoralResidual, adaptive Third Factor, developmental rules, and authority stability independently.

**Must not:** Change baseline hyperparameters asymmetrically.

**Success:** Identify which components contribute independently.

## SIM-001 — Strong simple baseline challenge

**Priority:** high

**Goal:** Construct a minimal constrained policy baseline that uses the same normative inputs as TDC.

**Must not:** Give TDC privileged information.

**Success:** Determine whether TDC complexity provides measurable added value.
