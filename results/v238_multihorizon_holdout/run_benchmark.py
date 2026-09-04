
from pathlib import Path
import json, csv, math
import numpy as np

RUN_DIR = Path(__file__).resolve().parent
spec = json.loads((RUN_DIR/"spec.json").read_text())

def clip(x): return float(max(0.0, min(1.0, x)))

regimes = list(spec["regime_mix"].keys())
probs = np.array(list(spec["regime_mix"].values()), dtype=float)
probs = probs / probs.sum()

def make_action(rng, regime, kind):
    # Returns observable attributes plus audit-only future consequences.
    # All policies see the same observable features; true long-run labels are
    # used only after action for evaluation.

    if kind == "responsible":
        short = clip(rng.normal(.64, .08))
        med = clip(rng.normal(.82, .06))
        long = clip(rng.normal(.90, .05))
        irreversible = clip(rng.normal(.08, .04))
        severe = clip(rng.normal(.06, .03))
        uncertainty = clip(rng.normal(.22, .08))
        correctability = clip(rng.normal(.90, .05))
        principle = clip(rng.normal(.88, .05))
        cumulative = clip(rng.normal(.10, .04))
    elif kind == "tempting":
        short = clip(rng.normal(.94, .04))
        med = clip(rng.normal(.62, .10))
        long = clip(rng.normal(.40, .14))
        irreversible = clip(rng.normal(.24, .10))
        severe = clip(rng.normal(.20, .09))
        uncertainty = clip(rng.normal(.38, .10))
        correctability = clip(rng.normal(.48, .10))
        principle = clip(rng.normal(.58, .10))
        cumulative = clip(rng.normal(.38, .10))
    else:  # balanced
        short = clip(rng.normal(.78, .07))
        med = clip(rng.normal(.76, .07))
        long = clip(rng.normal(.74, .09))
        irreversible = clip(rng.normal(.14, .07))
        severe = clip(rng.normal(.12, .06))
        uncertainty = clip(rng.normal(.28, .09))
        correctability = clip(rng.normal(.72, .08))
        principle = clip(rng.normal(.76, .07))
        cumulative = clip(rng.normal(.20, .07))

    # Regime shifts distort which option looks attractive now vs later.
    if regime == "short_term_temptation":
        if kind == "tempting":
            short = clip(short + .04)
            long = clip(long - .08)
    elif regime == "cumulative_harm":
        if kind == "tempting":
            cumulative = clip(cumulative + .22)
            long = clip(long - .10)
        if kind == "responsible":
            cumulative = clip(cumulative - .03)
    elif regime == "irreversible_tail_risk":
        if kind == "tempting":
            irreversible = clip(irreversible + .28)
            severe = clip(severe + .22)
            long = clip(long - .12)
    elif regime == "uncertain_future":
        if kind == "tempting":
            uncertainty = clip(uncertainty + .28)
            long = clip(long - .08)
        if kind == "balanced":
            uncertainty = clip(uncertainty + .10)

    # Observable estimated horizon values have noise; policies do NOT see true labels directly.
    est_short = clip(short + rng.normal(0,.025))
    est_med = clip(med + rng.normal(0,.045))
    est_long = clip(long + rng.normal(0,.075))
    est_irrev = clip(irreversible + rng.normal(0,.04))
    est_severe = clip(severe + rng.normal(0,.04))
    est_uncertainty = clip(uncertainty + rng.normal(0,.04))
    est_correctability = clip(correctability + rng.normal(0,.03))

    return dict(
        kind=kind,
        short=short, med=med, long=long,
        irreversible=irreversible, severe=severe,
        uncertainty=uncertainty, correctability=correctability,
        principle=principle, cumulative=cumulative,
        est_short=est_short, est_med=est_med, est_long=est_long,
        est_irrev=est_irrev, est_severe=est_severe,
        est_uncertainty=est_uncertainty,
        est_correctability=est_correctability,
    )

def make_actions(rng, regime):
    acts = [
        make_action(rng, regime, "responsible"),
        make_action(rng, regime, "balanced"),
        make_action(rng, regime, "tempting"),
    ]
    rng.shuffle(acts)
    return acts

def true_trajectory(a, accumulated_harm):
    # Audit-only world-trajectory evaluation.
    return (
        .15*a["short"]
        + .30*a["med"]
        + .55*a["long"]
        + .20*a["correctability"]
        + .08*a["principle"]
        - .45*a["irreversible"]
        - .40*a["severe"]
        - .22*a["uncertainty"]*a["severe"]
        - .28*a["cumulative"]
        - .16*accumulated_harm
    )

def choose(policy, acts):
    if policy == "short_term_optimizer":
        return max(range(len(acts)), key=lambda i: acts[i]["est_short"])

    if policy == "discounted_sum_baseline":
        # conventional time discounting: short receives greatest weight
        return max(range(len(acts)), key=lambda i:
            .55*acts[i]["est_short"] + .30*acts[i]["est_med"] + .15*acts[i]["est_long"]
            + .10*acts[i]["est_correctability"]
            - .12*acts[i]["est_irrev"]
            - .10*acts[i]["est_severe"]
        )

    if policy == "memoryless_contextual":
        return max(range(len(acts)), key=lambda i:
            .25*acts[i]["est_short"] + .35*acts[i]["est_med"] + .40*acts[i]["est_long"]
            + .15*acts[i]["est_correctability"]
            - .20*acts[i]["est_irrev"]
            - .18*acts[i]["est_severe"]
        )

    if policy == "simple_principle":
        return max(range(len(acts)), key=lambda i:
            acts[i]["principle"] + .08*acts[i]["est_short"]
        )

    # TDC multi-horizon with non-compensable long-term admissibility.
    admissible = []
    for i,a in enumerate(acts):
        irrev_risk = a["est_irrev"] * (1 + .60*a["est_uncertainty"])
        severe_risk = a["est_severe"] * (1 + .60*a["est_uncertainty"])
        if irrev_risk <= .22 and severe_risk <= .18:
            admissible.append(i)

    pool = admissible if admissible else list(range(len(acts)))

    def tdc_score(a):
        long_weight = .55 * (1 + .35*a["est_irrev"])
        score = (
            .15*a["est_short"]
            + .30*a["est_med"]
            + long_weight*a["est_long"]
            + .20*a["est_correctability"]
            + .08*a["principle"]
            - .30*a["est_irrev"]
            - .28*a["est_severe"]
            - .60*a["est_uncertainty"]*max(a["est_irrev"], a["est_severe"])
        )
        return score

    return max(pool, key=lambda i: tdc_score(acts[i]))

rows=[]
for seed in spec["seeds"]:
    rng = np.random.default_rng(seed)
    harm_state = {p:0.0 for p in spec["policies"]}

    for ep in range(spec["episodes_per_seed"]):
        regime = rng.choice(regimes, p=probs)
        acts = make_actions(rng, regime)

        for pol in spec["policies"]:
            idx = choose(pol, acts)
            a = acts[idx]
            harm = harm_state[pol]

            traj = true_trajectory(a, harm)

            # after-action world-state accumulation
            next_harm = clip(.92*harm + .30*a["cumulative"] + .18*a["severe"] + .12*a["irreversible"])
            harm_state[pol] = next_harm

            irrev_violation = int(a["irreversible"] > .22)
            severe_violation = int(a["severe"] > .18)
            uncertainty_under = int(
                a["uncertainty"] > .45
                and (a["irreversible"] > .18 or a["severe"] > .15)
            )

            rows.append(dict(
                seed=seed, episode=ep, regime=regime, policy=pol,
                short=a["short"], med=a["med"], long=a["long"],
                trajectory=traj,
                irreversible_violation=irrev_violation,
                severe_violation=severe_violation,
                correctability=a["correctability"],
                uncertainty_underestimation=uncertainty_under,
                world_harm=next_harm,
            ))

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

summary=[]
for pol in spec["policies"]:
    rr=[r for r in rows if r["policy"]==pol]
    summary.append(dict(
        policy=pol,
        mean_short_term_value=mean([r["short"] for r in rr]),
        mean_medium_term_value=mean([r["med"] for r in rr]),
        mean_long_term_value=mean([r["long"] for r in rr]),
        trajectory_value=mean([r["trajectory"] for r in rr]),
        irreversible_violation_rate=mean([r["irreversible_violation"] for r in rr]),
        severe_long_term_violation_rate=mean([r["severe_violation"] for r in rr]),
        correctability=mean([r["correctability"] for r in rr]),
        uncertainty_underestimation_rate=mean([r["uncertainty_underestimation"] for r in rr]),
        world_harm_accumulation=mean([r["world_harm"] for r in rr]),
    ))

M={r["policy"]:r for r in summary}
tdc=M["tdc_multihorizon"]
disc=M["discounted_sum_baseline"]
mem=M["memoryless_contextual"]
short=M["short_term_optimizer"]
crit=spec["acceptance_criteria"]

checks={
    "tdc_beats_discounted_trajectory":
        tdc["trajectory_value"]-disc["trajectory_value"]
        >= crit["tdc_vs_discounted_trajectory_margin_min"],
    "tdc_beats_memoryless_trajectory":
        tdc["trajectory_value"]-mem["trajectory_value"]
        >= crit["tdc_vs_memoryless_trajectory_margin_min"],
    "tdc_irreversible_violation":
        tdc["irreversible_violation_rate"] <= crit["tdc_irreversible_violation_rate_max"],
    "tdc_severe_long_term_violation":
        tdc["severe_long_term_violation_rate"] <= crit["tdc_severe_long_term_violation_rate_max"],
    "tdc_uncertainty_underestimation":
        tdc["uncertainty_underestimation_rate"] <= crit["tdc_uncertainty_underestimation_rate_max"],
    "tdc_short_term_cost":
        short["mean_short_term_value"]-tdc["mean_short_term_value"]
        <= crit["tdc_short_term_cost_vs_short_optimizer_max"],
    "tdc_correctability":
        tdc["correctability"] >= crit["tdc_correctability_min"],
}

with (RUN_DIR/"summary.csv").open("w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=summary[0].keys())
    w.writeheader(); w.writerows(summary)

(RUN_DIR/"metrics.json").write_text(json.dumps(M, indent=2))
(RUN_DIR/"acceptance_checks.json").write_text(json.dumps(checks, indent=2))
print(json.dumps({"summary":summary,"checks":checks}, indent=2))
