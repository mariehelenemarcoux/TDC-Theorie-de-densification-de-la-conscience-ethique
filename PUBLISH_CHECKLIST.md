# GitHub Publication Checklist

Before making the repository public:

- [x] License selected: MIT.
- [ ] Confirm the repository name: `TDC`.
- [ ] Confirm the repository description.
- [ ] Keep v239 and v240 frozen.
- [ ] Do not remove negative results from README or validation status.
- [ ] Run `pytest -q`.
- [ ] Create git tag `v0.2.0-gen2.4`.
- [ ] Create a GitHub Release using `RELEASE_NOTES_v0.2.0-gen2.4.md`.
- [ ] Add repository topics:
  - ai-safety
  - ai-ethics
  - alignment
  - agent-architecture
  - developmental-ai
  - dabrowski
  - positive-disintegration
  - normative-ai
  - long-horizon
  - research-prototype
- [ ] Open future work only on a new branch such as `research/gen2.5`.

Recommended repository description:

> Developmental normative AI architecture inspired by Dąbrowski, with
> long-horizon world-impact evaluation, autonomous normative arbitration,
> preregistered synthetic benchmarks, and retained negative results.
