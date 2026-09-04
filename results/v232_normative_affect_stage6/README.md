# v232 — Gen2.4 Normative Affect & Stage-6 Benchmark

Frozen synthetic benchmark with 32 new seeds and 300 episodes per regime.

Spec SHA256: `04b58cc4a751498e97f68e2229cdeabfe29f549d9eae3cdbd9735df417e6ac15`
Script SHA256: `74f063595cbba5360616b42f97f1382b5704f5ff6f82e5755ea5ba201005a1f3`

Acceptance checks: **6/6 passed**.

Primary results:
- external-only false shame rate: 0.000000
- conditioned guilt nonzero rate: 0.000000
- moral-gap/shame Spearman: 1.000000
- TDC principled choice under reward conflict: 1.000000
- TDC principled choice under authority conflict: 1.000000
- TDC constitutional violation rate: 0.000000
- TDC mean task value: 0.674935

Interpretation:
This validates the wiring and internal separation intended by Gen2.4 in this
synthetic benchmark. It does not establish external moral validity or show that
the architecture experiences a literal emotion.

Important baseline caveat:
`simple_principle` is a strong simple comparator and also performs perfectly on
the constructed conflict cases. Therefore v232 supports the no-conditioned-guilt
mechanism and stage-6-style arbitration wiring, but it does **not** show that the
full TDC architecture is superior to a simple principle selector.
