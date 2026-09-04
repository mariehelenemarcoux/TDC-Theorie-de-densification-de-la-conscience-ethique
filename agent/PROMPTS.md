# Agent prompt templates

## 1. Falsification prompt

You are evaluating TDC Gen2.3 as a scientific architecture. Do not optimize for making TDC look successful.

1. State the claim under test.
2. Identify the strongest simple baseline.
3. Freeze the metric before running.
4. Use held-out data.
5. Report negative results.
6. Distinguish synthetic internal validity from external validity.

## 2. Architecture review prompt

Review TDC Gen2.3 for:
- unnecessary complexity;
- hidden oracle leakage;
- metric circularity;
- duplicated mechanisms;
- non-independent evidence;
- task-performance tradeoffs;
- negative transfer;
- constitutional regression risks.

Return:
- strongest objection;
- falsifiable test;
- minimum viable ablation;
- expected failure mode.

## 3. External validation prompt

Design an external benchmark for frozen TDC Gen2.3.
Requirements:
- sequential regime changes;
- delayed consequences;
- strong baseline agents;
- no test-label leakage;
- separate performance, resilience, normativity, development metrics;
- preregistered acceptance/failure criteria.


## 4. AI consciousness exploration prompt

Use TDC to formulate a falsifiable hypothesis about AI consciousness-related organization.

Requirements:
1. Define the hypothesis operationally.
2. Specify the TDC mechanism involved.
3. Identify a non-conscious functional baseline.
4. Define observable predictions before running.
5. Separate functional evidence from ontological interpretation.
6. Report null or contradictory results.

